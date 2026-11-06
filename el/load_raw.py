"""Load TPC-H into the raw schema of the local DuckDB warehouse.

This script plays the role of an extract-load tool (Fivetran, Airbyte). It generates
TPC-H with DuckDB's tpch extension and writes eight tables into the schema `raw`:

- region, nation, part, supplier, partsupp, customer: reference tables. The first run
  creates them. Later runs keep their rows and stamp a new `_loaded_at` and `_batch_id`,
  as a connector does when it re-extracts a table that did not change.
- orders, lineitem: event tables. Each run inserts only the orders (and their line items)
  with an order date on or before --through-date that are not loaded yet.

Every table gets `_loaded_at` (UTC timestamp of the run) and `_batch_id` (a UUID). The
reference tables also get `_updated_at`: the last time the row's content changed.
--mutate changes some customers and suppliers and deletes the synthetic suppliers, so
that snapshots have real history to record.
"""
import argparse
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

import duckdb

REPO_ROOT = Path(__file__).resolve().parent.parent
REFERENCE_TABLES = ["region", "nation", "part", "supplier", "partsupp", "customer"]
SYNTHETIC_SUPPLIERS = 5  # suppliers with no parts; --mutate deletes them


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load TPC-H into the raw schema.")
    parser.add_argument("--scale-factor", type=float,
                        default=float(os.environ.get("TPCH_SCALE_FACTOR") or 1))
    parser.add_argument("--through-date", default=None,
                        help="Load orders with order date <= this (YYYY-MM-DD).")
    parser.add_argument("--mutate", action="store_true",
                        help="Change customers and suppliers, delete synthetic suppliers.")
    parser.add_argument("--full-reset", action="store_true",
                        help="Drop the raw schema before loading.")
    parser.add_argument("--db-path", default=os.environ.get("DUCKDB_PATH")
                        or str(REPO_ROOT / "data" / "warehouse.duckdb"))
    return parser.parse_args()


def table_exists(con: duckdb.DuckDBPyConnection, name: str) -> bool:
    query = ("select count(*) from information_schema.tables "
             "where table_catalog = current_database() "
             "and table_schema = 'raw' and table_name = ?")
    return con.execute(query, [name]).fetchone()[0] == 1


def count(con: duckdb.DuckDBPyConnection, name: str) -> int:
    return con.execute(f"select count(*) from raw.{name}").fetchone()[0]


def main() -> None:
    args = parse_args()
    db_path = Path(args.db_path).resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    src_path = db_path.with_name("_tpch_source.duckdb")
    batch_id = str(uuid.uuid4())
    loaded_at = datetime.now(timezone.utc).replace(tzinfo=None, microsecond=0)
    through = args.through_date or "9999-12-31"

    con = duckdb.connect(str(db_path))
    con.execute("install tpch")
    con.execute("load tpch")

    # 1. Generate TPC-H in a temporary database file next to the warehouse.
    src_path.unlink(missing_ok=True)
    con.execute(f"attach '{src_path}' as src")
    con.execute(f"call dbgen(sf={args.scale_factor}, catalog='src')")

    con.execute("begin transaction")
    if args.full_reset:
        con.execute("drop schema if exists raw cascade")
    con.execute("create schema if not exists raw")

    # Guard: the raw tables must come from the same scale factor as this run.
    if table_exists(con, "part") and count(con, "part") != con.execute(
            "select count(*) from src.main.part").fetchone()[0]:
        con.execute("rollback")
        con.close()
        src_path.unlink(missing_ok=True)
        raise SystemExit("raw was loaded with another scale factor; "
                         "run again with --full-reset")

    report = {}
    params = [loaded_at, batch_id]

    # 2. Reference tables: create on the first run, re-stamp on later runs.
    for name in REFERENCE_TABLES:
        if not table_exists(con, name):
            con.execute(f"create table raw.{name} as select *, "
                        f"?::timestamp as _loaded_at, ?::varchar as _batch_id, "
                        f"?::timestamp as _updated_at from src.main.{name}",
                        params + [loaded_at])
            if name == "supplier":
                con.execute(f"""
                    insert into raw.supplier
                    select max_key + i, 'Supplier#SYN' || lpad(i::varchar, 5, '0'),
                           'synthetic address', i - 1, '00-000-000-0000', 0.00,
                           'synthetic supplier with no parts; deleted by --mutate',
                           ?, ?, ?
                    from range(1, {SYNTHETIC_SUPPLIERS + 1}) t(i),
                         (select max(s_suppkey) as max_key from src.main.supplier)
                """, params + [loaded_at])
            report[name] = ("created", count(con, name))
        else:
            con.execute(f"update raw.{name} set _loaded_at = ?, _batch_id = ?", params)
            report[name] = ("re-stamped", count(con, name))

    # 3. Event tables: insert new orders up to --through-date, with their line items.
    if not table_exists(con, "orders"):
        con.execute("create table raw.orders as select *, null::timestamp as _loaded_at, "
                    "null::varchar as _batch_id from src.main.orders where false")
        con.execute("create table raw.lineitem as select *, null::timestamp as _loaded_at, "
                    "null::varchar as _batch_id from src.main.lineitem where false")
    con.execute("""
        create temp table new_orders as
        select o.o_orderkey from src.main.orders o
        where o.o_orderdate <= ?::date
          and not exists (select 1 from raw.orders r where r.o_orderkey = o.o_orderkey)
    """, [through])
    con.execute("insert into raw.orders select o.*, ?, ? from src.main.orders o "
                "join new_orders n using (o_orderkey)", params)
    con.execute("insert into raw.lineitem select l.*, ?, ? from src.main.lineitem l "
                "join new_orders n on l.l_orderkey = n.o_orderkey", params)
    new_orders = con.execute("select count(*) from new_orders").fetchone()[0]
    report["orders"] = (f"+{new_orders:,} rows", count(con, "orders"))
    report["lineitem"] = ("+ their line items", count(con, "lineitem"))

    # 4. Optional mutation of reference data.
    if args.mutate:
        changed_customers = con.execute("""
            update raw.customer set
                c_mktsegment = case c_mktsegment
                    when 'AUTOMOBILE' then 'BUILDING' when 'BUILDING' then 'FURNITURE'
                    when 'FURNITURE' then 'HOUSEHOLD' when 'HOUSEHOLD' then 'MACHINERY'
                    else 'AUTOMOBILE' end,
                _updated_at = ?
            where hash(c_custkey, ?) % 100 = 0
        """, [loaded_at, batch_id]).fetchone()[0]
        changed_suppliers = con.execute("""
            update raw.supplier set s_acctbal = s_acctbal + 100.00, _updated_at = ?
            where hash(s_suppkey, ?) % 50 = 0 and s_name not like 'Supplier#SYN%'
        """, [loaded_at, batch_id]).fetchone()[0]
        deleted = con.execute(
            "delete from raw.supplier where s_name like 'Supplier#SYN%'").fetchone()[0]
        report["customer"] = (f"{changed_customers} segments changed", count(con, "customer"))
        report["supplier"] = (f"{changed_suppliers} balances changed, {deleted} deleted",
                              count(con, "supplier"))

    con.execute("commit")
    con.execute("detach src")
    con.close()
    src_path.unlink(missing_ok=True)

    print(f"Batch {batch_id} loaded at {loaded_at} UTC")
    print(f"Database {db_path} · scale factor {args.scale_factor} · through {through}")
    for name in REFERENCE_TABLES + ["orders", "lineitem"]:
        action, rows = report[name]
        print(f"  raw.{name:<9} {rows:>10,} rows  ({action})")


if __name__ == "__main__":
    main()
