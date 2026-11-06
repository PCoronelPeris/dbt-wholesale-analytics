# el/ — extract and load

`load_raw.py` fills the schema `raw` of the local DuckDB warehouse
(`data/warehouse.duckdb`) with TPC-H data. It stands in for a managed extract-load tool
such as Fivetran or Airbyte, which cannot write to a local file.

**Why it simulates a source system.** Raw TPC-H is static: generated once, it never
changes. dbt features that react to change would have nothing to show. The loader adds
the three behaviours a real source has:

| Behaviour | How the loader does it | dbt feature it makes visible |
|---|---|---|
| Load metadata | `_loaded_at` (UTC) and `_batch_id` on every table; `_updated_at` on the six reference tables | source freshness, snapshots with the `timestamp` strategy |
| Data arriving over time | `--through-date` loads orders and their line items in waves; each run adds only orders not loaded yet | incremental models, microbatch |
| Data that changes | `--mutate` changes ~1% of customer segments and ~2% of supplier balances, and deletes the five synthetic suppliers | snapshots, `hard_deletes` |

**Reference tables** (`region`, `nation`, `part`, `supplier`, `partsupp`, `customer`) are
created on the first run. Later runs keep their rows and give them a new `_loaded_at` and
`_batch_id`, as a connector does when it re-extracts an unchanged table. `supplier` has
five extra synthetic suppliers with no parts, so that deleting them breaks no
relationship between tables.

**Event tables** (`orders`, `lineitem`) only grow: each run inserts the orders with an
order date on or before `--through-date` that are not loaded yet, with all their line
items.

**Usage** (from the repository root):

```bash
make load THROUGH_DATE=1996-12-31   # first wave
make load THROUGH_DATE=1997-06-30   # second wave: only the new orders
make load MUTATE=1                  # load everything left and mutate reference data
make load RESET=1 THROUGH_DATE=1996-12-31   # start again from an empty raw schema
```

`SF=0.1` changes the scale factor; a different scale factor than the one already loaded
requires `RESET=1`.
