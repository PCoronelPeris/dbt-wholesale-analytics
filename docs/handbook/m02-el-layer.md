# M02 — The EL layer

| Field | Value |
|---|---|
| Status | Done · 2026-11-06 |
| Hours | 1.5 estimated · 2.5 actual |
| Branch | `m02-el-layer` |
| Exam sections | Prepares 03 Managing data pipelines (source freshness, M03), 01 Developing models (incremental and microbatch, M08–M09) and snapshots with `hard_deletes` (M13); no exam topic is closed here |

## In one paragraph
The warehouse is no longer empty. A Python script, `el/load_raw.py`, generates the TPC-H dataset (a wholesale supplier: regions, nations, parts, suppliers, customers, orders and line items) and writes it into the schema `raw` of `data/warehouse.duckdb`. Every row carries `_loaded_at` and `_batch_id`, the way an extract-load tool stamps what it copies. Orders arrive in date waves (`make load THROUGH_DATE=...`), and `make load MUTATE=1` changes and deletes reference rows on purpose. The first wave loaded every order up to 1996-12-31: 1,138,594 orders and 4,556,169 line items at scale factor 1.

## 1. The problem this solves
dbt only transforms data that is already inside the warehouse; it never extracts anything. After M01 the warehouse file existed but held no tables, so there was nothing for dbt to read. In a company, a separate tool (Fivetran, Airbyte, or a team's own Python job) copies data from the source systems into a `raw` schema before dbt runs. This milestone builds that step.

A one-time copy would not be enough. Three later milestones need data that grows and changes: source freshness needs a load timestamp (M03), incremental and microbatch models need new orders arriving in waves (M08, M09), and snapshots need rows that change and rows that disappear (M13). The loader provides all three.

## 2. Where it sits
```text
dbt-wholesale-analytics/
├── .gitignore                 CHANGED  (+ __pycache__/)
├── Makefile                   CHANGED  (+ load target, load in .PHONY)
├── el/                        NEW      (extract-load, outside the dbt project)
│   ├── README.md              NEW
│   └── load_raw.py            NEW
├── data/
│   └── warehouse.duckdb       CHANGED  (local only: schema raw with 8 tables)
└── docs/
    ├── PROJECT_LOG.md         CHANGED
    └── handbook/
        ├── README.md          CHANGED  (generated)
        └── m02-el-layer.md    NEW      (this chapter)
```

Outside the repository, DuckDB downloaded its `tpch` extension once into `~/.duckdb/extensions/<duckdb version>/linux_amd64/`, a hidden folder in the home directory shared by every project of the same user.

Position in the pipeline:
```text
tpch extension → el/load_raw.py → data/warehouse.duckdb, schema raw → dbt sources (M03) → staging → intermediate → marts
```

## 3. How it was built
### Step 1 — Create the milestone branch
```bash
make start M=02
```
The command switched to an up-to-date `main` and created the branch `m02-el-layer`. It printed `Ready: M02 — The EL layer` and `Branch: m02-el-layer`.

### Step 2 — Move the two downloaded files into the repository
```bash
make fetch F="el/load_raw.py el/README.md"
```
`scripts/milestone.py` found the newest `load_raw*.py` and `README*.md` in the Windows Downloads folder, copied them to `el/`, created the folder, and deleted the downloads. It reported 8035 and 2056 bytes. `git status --short --branch` then showed `## m02-el-layer` and `?? el/`.

### Step 3 — Read the loader
`el/load_raw.py` has 167 lines in seven blocks:
1. **Arguments.** `--scale-factor` (default 1, or the variable `TPCH_SCALE_FACTOR`), `--through-date`, `--mutate`, `--full-reset` and `--db-path` (default `data/warehouse.duckdb`, or the variable `DUCKDB_PATH`).
2. **Generation.** The script opens the warehouse, installs and loads the `tpch` extension, attaches a temporary file `data/_tpch_source.duckdb` as the database `src`, and runs `call dbgen(sf=..., catalog='src')`, which writes the eight TPC-H tables there.
3. **Transaction and guard.** Everything from here to the end runs inside one transaction (`begin` … `commit`), so a failure leaves `raw` as it was. If `raw.part` exists with a different row count than the generated one, the data came from another scale factor; the script rolls back and stops.
4. **Reference tables** (`region`, `nation`, `part`, `supplier`, `partsupp`, `customer`). The first run creates them with three extra columns: `_loaded_at`, `_batch_id` and `_updated_at`. Later runs keep the rows and only write a new `_loaded_at` and `_batch_id`. `_updated_at` changes only when `--mutate` changes the row. The first run also adds five synthetic suppliers with no parts.
5. **Event tables** (`orders`, `lineitem`). Each run inserts the orders with `o_orderdate` on or before `--through-date` that are not in `raw.orders` yet, and all their line items.
6. **Mutation** (only with `--mutate`). About 1% of customers move to the next market segment, about 2% of real suppliers gain 100.00 in `s_acctbal`, and the five synthetic suppliers are deleted. Both changes set `_updated_at`.
7. **Report.** One line per table with its row count and what happened to it.

### Step 4 — Add the `load` target to the Makefile and ignore `__pycache__/`
```bash
sed -i 's/^\.PHONY: \(.*\) fetch$/.PHONY: \1 fetch load/' Makefile
printf '\nload:\n\t$(PYTHON) el/load_raw.py $(if $(SF),--scale-factor $(SF)) $(if $(THROUGH_DATE),--through-date $(THROUGH_DATE)) $(if $(MUTATE),--mutate) $(if $(RESET),--full-reset)\n' >> Makefile
printf '__pycache__/\n' >> .gitignore
```
`sed -i` edits the file in place: it adds ` load` to the end of the `.PHONY` line. `printf` writes text with `\n` as a line break and `\t` as a TAB, and `>>` appends that text to the end of the file. The recipe line must start with a TAB, which is why it was not pasted into an editor (D-M02-2). Each `$(if $(X),...)` adds a flag only when the variable `X` was given on the command line.

### Step 5 — Load the first wave
```bash
make load THROUGH_DATE=1996-12-31
```
Output:
```text
/home/pedro/projects/dbt-wholesale-analytics/.venv/bin/python el/load_raw.py  --through-date 1996-12-31
Batch e7bd99be-06e8-4fd8-80e1-7453e031869e loaded at 2026-11-06 17:38:51 UTC
Database /home/pedro/projects/dbt-wholesale-analytics/data/warehouse.duckdb · scale factor 1.0 · through 1996-12-31
  raw.region             5 rows  (created)
  raw.nation            25 rows  (created)
  raw.part         200,000 rows  (created)
  raw.supplier      10,005 rows  (created)
  raw.partsupp     800,000 rows  (created)
  raw.customer     150,000 rows  (created)
  raw.orders     1,138,594 rows  (+1,138,594 rows)
  raw.lineitem   4,556,169 rows  (+ their line items)
```
`supplier` holds 10,000 TPC-H suppliers plus the five synthetic ones. TPC-H at scale factor 1 has 1,500,000 orders in total; the other 361,406 are dated after 1996-12-31 and arrive in later waves.

### Step 6 — Verify the load
The block is pasted whole; nothing in it may be indented (E-M02-1, E-M02-2).
```bash
.venv/bin/python - <<'EOF'
import duckdb
con = duckdb.connect("data/warehouse.duckdb", read_only=True)
print("tables in raw:", con.execute("select count(*) from information_schema.tables where table_schema = 'raw'").fetchone()[0])
print("max order date:", con.execute("select max(o_orderdate) from raw.orders").fetchone()[0])
print("line items without order:", con.execute("select count(*) from raw.lineitem l left join raw.orders o on l.l_orderkey = o.o_orderkey where o.o_orderkey is null").fetchone()[0])
for t in ["region", "nation", "part", "supplier", "partsupp", "customer", "orders", "lineitem"]:
    rows, loaded, batch = con.execute(f"select count(*), count(_loaded_at), count(_batch_id) from raw.{t}").fetchone()
    print(f"raw.{t:<9} rows={rows:>7,} loaded_at={loaded:>7,} batch_id={batch:>7,}")
EOF
```
`.venv/bin/python -` reads the program from standard input, and `<<'EOF'` … `EOF` is a heredoc that sends it the lines in between. The quotes around `'EOF'` stop bash from changing anything inside. The database opens with `read_only=True`, so the check cannot change it.

The four SQL checks:
- `information_schema.tables` is the standard view that lists every table in the database; counting its rows where `table_schema = 'raw'` counts the tables in `raw`.
- `max(o_orderdate)` returns the latest order date.
- The `left join` keeps every line item and fills the order columns with null when no order matches; `where o.o_orderkey is null` keeps only line items without an order.
- `count(*)` counts rows and `count(column)` counts non-null values, so equal numbers mean no row lacks its load metadata.

## 4. How to verify it
| Command | Expected result |
|---|---|
| the Step 6 block | `tables in raw: 8`, `max order date: 1996-12-31`, `line items without order: 0`, and `rows` = `loaded_at` = `batch_id` in all eight tables |
| `make load THROUGH_DATE=1996-12-31` run a second time | every reference table `(re-stamped)`, `raw.orders ... (+0 rows)` |
| `ls -lh data/` | `warehouse.duckdb`, about 216 MB at scale factor 1; no `_tpch_source.duckdb` left behind |
| `make -n load SF=0.01` | one line: `.../.venv/bin/python el/load_raw.py --scale-factor 0.01` |
| `make handbook` | `Handbook index: 3 chapters, ...` |

## 5. What went wrong
| ID | Symptom | Cause | Fix |
|---|---|---|---|
| E-M02-1 | The prompt kept printing `>` after the verification block was pasted | Every line of the block started with two spaces, so bash never saw a line equal to `EOF` and kept waiting for the end of the heredoc | Ctrl+C, then the block was pasted again without indentation |
| E-M02-2 | `IndentationError: unexpected indent` | On the second try `EOF` was typed by hand, which closed the heredoc, but Python received lines that began with spaces | The block was delivered again with every line starting at the first column |

## 6. Decisions
### D-M02-1 — The loader lives in `el/`, outside the dbt project
**Context.** dbt only transforms; extraction belongs to a separate tool. **Decision.** Put the loader in `el/` at the repository root, next to `transform/`. **Consequences.** The folder layout matches the pipeline: `el/` writes `raw`, `transform/` reads it. dbt never imports or runs the loader.

### D-M02-2 — The Makefile is edited with `sed` and `printf`, not pasted
**Context.** A Makefile recipe line must start with a TAB, and a TAB pasted into the terminal triggers autocompletion. **Decision.** Append the target with `printf '...\t...' >> Makefile` and edit `.PHONY` with `sed -i`. **Consequences.** The TAB is exact and the edit is reproducible from the commands. The same method is used for later one-line Makefile changes.

### D-M02-3 — The load is checked with a read-only Python query, not with dbt
**Context.** dbt has no sources until M03, so it cannot test `raw` yet. **Decision.** Check the exit criteria with one read-only query run by the project's Python. **Consequences.** The check cannot modify the warehouse. From M03 on, dbt tests and source freshness replace it.

### D-M02-4 — A load and a dbt run never overlap
**Context.** A DuckDB file accepts one process that writes, or several processes that only read. **Decision.** Never run `make load` while dbt is running, or the reverse. **Consequences.** A lock error is avoided. On BigQuery (M12) this restriction does not exist, because the engine is a server.

### D-M02-5 — Build-side files move to one folder at the final revision
**Context.** The plan documents, the handbook and the milestone tooling sit next to the product folders (`el/`, `transform/`). **Decision.** Group them in one folder at the final revision, not now. **Consequences.** The plan for M03–M18 keeps its current paths until the end. The move is one commit, tested once from a clean clone.

## 7. Exam map
| Outline bullet | Where in this chapter | Question |
|---|---|---|
| Source freshness and `loaded_at_field` | Step 3 (block 4), Step 5 | Q1, Q2 |
| Snapshots, `timestamp` strategy and `updated_at` | Step 3 (blocks 4 and 6) | Q3 |

## 8. New terms
| Term | Meaning |
|---|---|
| EL / ELT | Extract and load: copying data from source systems into the warehouse; ELT means the transformation (T, done by dbt) happens after loading, inside the warehouse |
| `raw` schema | The schema that holds data exactly as it was loaded, before any transformation |
| Schema | A named group of tables inside a database; the full name of a table is `database.schema.table` |
| TPC-H | A standard benchmark dataset of a wholesale supplier, published by the TPC council, generated at any size by a scale factor |
| Scale factor | The size multiplier of TPC-H; scale factor 1 has 1,500,000 orders |
| DuckDB extension | An optional module that DuckDB downloads once into `~/.duckdb/extensions/` and loads on request, such as `tpch` |
| Load metadata | Columns a loader adds to every row, such as `_loaded_at` (when it was loaded) and `_batch_id` (which run loaded it) |
| Date wave | One run of the loader that adds the orders up to a later date |
| Idempotent | Running the same operation twice leaves the same result as running it once |
| Transaction | A group of statements that is applied completely or not at all |
| Synthetic supplier | A supplier added by the loader with no parts, so that deleting it breaks no reference |
| Single writer | DuckDB's rule that only one process may write to a database file at a time |
| `information_schema` | Standard views inside a database that describe its schemas, tables and columns |
| Orphan row | A row whose foreign key points to no row in the referenced table, found with `left join ... where key is null` |

## 9. Check yourself
<details><summary>Q1. A source table declares `loaded_at_field: _loaded_at` with `warn_after: {count: 12, period: hour}` and `error_after: {count: 24, period: hour}`. The last load ran 20 hours ago. What status does `dbt source freshness` report?</summary>

`warn`. dbt takes the maximum value of `_loaded_at`, compares it with the current time, and reports the most severe threshold that was passed: 20 hours passes 12 but not 24. The tempting answer is `error`, which would require more than 24 hours.

</details>

<details><summary>Q2. Why does freshness use `_loaded_at` and not `o_orderdate`?</summary>

Freshness asks when data last arrived, not when the business event happened. `o_orderdate` holds dates from the 1990s, so a freshness check on it would always fail, even right after a load. `_loaded_at` is written by the loader at load time. The tempting answer is that any date column works; it has to be a column that changes when new data lands.

</details>

<details><summary>Q3. A `timestamp` snapshot of `raw.customer` uses `updated_at: _loaded_at` instead of `_updated_at`. What does it record after each load?</summary>

A new version of every customer, every time. The loader writes a new `_loaded_at` on every row of every reference table, so the snapshot sees all rows as changed. With `updated_at: _updated_at`, only the rows that `--mutate` really changed get a new version. The tempting answer is that nothing changes because the data is the same; the `timestamp` strategy looks only at the timestamp column, not at the other values.

</details>
