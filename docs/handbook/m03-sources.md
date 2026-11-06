# M03 — Sources, freshness, and dependency verification

| Field | Value |
|---|---|
| Status | Done · 2026-11-06 |
| Hours | 1.5 estimated · 1.9 actual |
| Branch | `m03-sources` |
| Exam sections | 06 External dependencies (implementing source freshness), 05 Implementing dbt tests (testing assumptions for models and sources), 01 Developing and optimizing dbt models (identifying and verifying raw object dependencies) |

## In one paragraph
dbt now knows the eight tables of the schema `raw`. One file, `_tpch__sources.yml`, declares them as the source `tpch_raw`, with a description for every table, a freshness policy based on `_loaded_at`, one table exempt from freshness, one table with its own thresholds, one table whose dbt name differs from its physical name, and 18 tests. `make freshness` reports how old each table is, and `dbt test` checks the key columns. A deliberate break (renaming `raw.part` by hand) showed how a missing table is reported and how one line of YAML repairs it.

## 1. The problem this solves
After M02 the tables existed in the warehouse, but dbt did not know about them. A model that reads a raw table by typing `raw.orders` in its SQL works, but dbt cannot draw that table in the dependency graph, cannot test it, and cannot tell how old its data is.

A source declaration fixes all three. Models read raw data with `source('tpch_raw', 'orders')`, so dbt records the dependency. The same declaration holds the tests that check the raw data and the freshness policy that says how late a load may be. If the physical table is renamed later, only the declaration changes, not every model.

## 2. Where it sits
```text
dbt-wholesale-analytics/
├── Makefile                                   CHANGED  (+ freshness target, freshness in .PHONY)
├── transform/
│   ├── models/
│   │   └── staging/
│   │       └── tpch/
│   │           └── _tpch__sources.yml         NEW      (109 lines)
│   └── target/
│       └── sources.json                       local only, git-ignored, rewritten by every make freshness
└── docs/
    ├── PROJECT_LOG.md                         CHANGED
    └── handbook/
        ├── README.md                          CHANGED  (generated)
        └── m03-sources.md                     NEW      (this chapter)
```

Position in the pipeline:
```text
el/load_raw.py → data/warehouse.duckdb, schema raw → [dbt sources tpch_raw] → staging (M04) → intermediate → marts
```

## 3. How it was built
### Step 1 — Create the milestone branch
```bash
make start M=03
```
The command switched to an up-to-date `main` and created the branch `m03-sources`. It printed `Ready: M03 — Sources, freshness, and dependency verification` and `Branch: m03-sources`.

### Step 2 — Place the first sources file and the Makefile
```bash
make fetch F="transform/models/staging/tpch/_tpch__sources.yml Makefile"
```
`scripts/milestone.py` looks for the newest file with that name in the Windows Downloads folder, moves it to the path given, and reports its size. The first attempt stopped because the file had not been downloaded yet (E-M03-2). After the download it moved both files.

### Step 3 — Read the sources file
The first version had 47 lines and no tests. Its structure, from the outside in:
1. `sources:` is the list of sources; this file declares one, named `tpch_raw`.
2. `schema: raw` tells dbt where the tables physically are. The source `name` is only the label models use in `source('tpch_raw', ...)`.
3. `loaded_at_field: _loaded_at` names the column that freshness reads. `freshness:` at this level sets the default policy for every table: warn after 12 hours, error after 24 hours.
4. `tables:` lists the eight tables, each with a `name` and a `description`.
5. Three tables differ from the default:
   - `region` has `freshness: null`. This switches freshness off for that table, because its five rows never change.
   - `orders` has its own `freshness:` block with warn after 6 hours and error after 12 hours. A table-level block replaces the source-level block for that table; the two are not merged.
   - `line_items` has `identifier: lineitem`. The name models use is `line_items`, and the physical table is `raw.lineitem`.

```yaml
      - name: line_items
        identifier: lineitem
```
The rule behind this: `source('tpch_raw', 'line_items')` always uses the table `name`. The `identifier` is read only when dbt writes the SQL, where it replaces the name with the physical one.

### Step 4 — Run freshness for the first time
```bash
make freshness
```
`make` runs `cd transform && dbt source freshness`. For each table that has a `loaded_at_field`, dbt runs a query of the form `select max(_loaded_at) ... from raw.<table>`, subtracts that moment from the current time, and compares the age with the thresholds. The result is `pass`, `warn` or `error`, and dbt writes all results to `transform/target/sources.json`.

Output: dbt reported 8 sources, then `1 of 7` to `7 of 7` lines, each `PASS`, and `Finished running 7 sources`. The table `region` does not appear because it is exempt. A `warn` exits with code 0; an `error` exits with code 1, which `make` shows as `Error 1`.

To read the ages, a short Python line prints the file:
```bash
.venv/bin/python -c 'import json; [print(r["unique_id"].split(".")[-1].ljust(11), r["status"].ljust(6), r["max_loaded_at"][:19], str(round(r["max_loaded_at_time_ago_in_s"] / 3600, 2)).rjust(6), "h") for r in sorted(json.load(open("transform/target/sources.json"))["results"], key=lambda r: r["unique_id"])]'
```
It opens `sources.json`, takes the list `results`, and prints for each table its name, status, last load moment (in UTC) and age in hours. All seven rows showed `2026-11-06T17:38:51` and about 1.6 hours, because M02 loaded everything in one run.

### Step 5 — Replace the sources file with the version that has tests
```bash
make fetch F="transform/models/staging/tpch/_tpch__sources.yml"
```
The second version has 109 lines (3,739 bytes). Each table gained a `columns:` list, and the key columns gained `data_tests:`:
- `unique` and `not_null` on the primary key of `region`, `nation`, `part`, `supplier`, `customer`; `orders` has them on `o_orderkey`.
- `not_null` only on `ps_partkey` and `ps_suppkey` of `partsupp`, and on `l_orderkey` and `l_linenumber` of `line_items`. These keys have two columns, and `unique` on one column of a two-column key would fail. The check on the pair waits for `dbt_utils` in M04 (D-M03-3).
- `o_custkey` of `orders` has `not_null` and a `relationships` test: every value must exist in `c_custkey` of the source table `customer`.

```yaml
          - name: o_custkey
            data_tests:
              - not_null
              - relationships:
                  arguments:
                    to: source('tpch_raw', 'customer')
                    field: c_custkey
```
A generic test is a query that selects the rows that break the rule. The test passes when the query returns zero rows. In dbt 1.11 the settings of a test sit under `arguments:`.

### Step 6 — Run the tests
```bash
make test
```
Output ended with `Done. PASS=18 WARN=0 ERROR=0 SKIP=0 NO-OP=0 TOTAL=18`. dbt had found `18 data tests, 8 sources`. There are still 0 models, so every test in the project is a source test.

### Step 7 — Load the same window again and compare freshness
```bash
make load THROUGH_DATE=1996-12-31
make freshness
```
The loader re-stamped the six reference tables (new `_loaded_at` and `_batch_id`, same rows), and inserted `+0 rows` into `orders`. The Python line then printed:
```text
customer    pass   2026-11-06T19:26:32    0.0 h
line_items  pass   2026-11-06T17:38:51    1.8 h
nation      pass   2026-11-06T19:26:32    0.0 h
orders      pass   2026-11-06T17:38:51    1.8 h
part        pass   2026-11-06T19:26:32    0.0 h
partsupp    pass   2026-11-06T19:26:32    0.0 h
supplier    pass   2026-11-06T19:26:32    0.0 h
```
Five reference tables moved to the new moment; `orders` and `line_items` stayed at the old one, because additive tables change only when new rows arrive. `region` was re-stamped too, but freshness skips it. The times are UTC; local time in Asunción is three hours earlier.

### Step 8 — Break the dependency by hand
```bash
.venv/bin/python -c "import duckdb; duckdb.connect('data/warehouse.duckdb').execute('alter table raw.part rename to part_renamed')"
(cd transform && ../.venv/bin/dbt build --select "source:tpch_raw+")
```
The first line opens the warehouse and renames the table `raw.part`; no data moves. The second line runs the tests of the source and everything that depends on it: `source:tpch_raw` selects the source, and the `+` at the end adds its descendants, which here are the 18 tests.

dbt printed `Found 18 data tests, 8 sources` normally, because reading the YAML does not touch the warehouse. Then two tests ended in `ERROR`, the `not_null` and the `unique` of `p_partkey` of `part`, and the summary read `PASS=16 WARN=0 ERROR=2`. The message is in E-M03-1. dbt also names the file that holds the SQL it sent: `target/compiled/wholesale_analytics/models/staging/tpch/_tpch__sources.yml/source_not_null_tpch_raw_part_p_partkey.sql`.

### Step 9 — Repair it in the YAML only
```bash
sed -i '/^      - name: part$/a\        identifier: part_renamed' transform/models/staging/tpch/_tpch__sources.yml
(cd transform && ../.venv/bin/dbt build --select "source:tpch_raw+")
```
`sed` inserted one line after `- name: part`, so the table now reads:
```yaml
      - name: part
        identifier: part_renamed
```
The build ended with `PASS=18`. dbt now wrote `raw.part_renamed` in the SQL of the `part` tests. No model and no test changed.

### Step 10 — Undo both changes
```bash
.venv/bin/python -c "import duckdb; duckdb.connect('data/warehouse.duckdb').execute('alter table raw.part_renamed rename to part')"
sed -i '/identifier: part_renamed/d' transform/models/staging/tpch/_tpch__sources.yml
(cd transform && ../.venv/bin/dbt build --select "source:tpch_raw+")
md5sum transform/models/staging/tpch/_tpch__sources.yml
```
The table got its real name back, the `identifier` line was deleted, and the build ended with `PASS=18`. The hash printed was `03f5977f64876113cba88b27243fd595`, the same as before the drill, so the file is identical byte by byte. Later milestones read `raw.part` under its real name.

## 4. How to verify it
| Command | Expected result |
|---|---|
| `make freshness` | `Found 18 data tests, 8 sources`; seven lines `PASS`; `Finished running 7 sources`; `region` is not listed |
| `make test` | `Found 18 data tests, 8 sources` and `Done. PASS=18 WARN=0 ERROR=0 SKIP=0 NO-OP=0 TOTAL=18` |
| `cd transform && ../.venv/bin/dbt test --select source:tpch_raw` | the same 18 tests, because all tests in the project are source tests |
| the Python line of Step 4 | one row per table; `region` absent; `orders` and `line_items` older than the reference tables after a reload |
| `md5sum transform/models/staging/tpch/_tpch__sources.yml` | `03f5977f64876113cba88b27243fd595` |
| `make handbook` | `Handbook index: 4 chapters, ...` |

## 5. What went wrong
| ID | Symptom | Cause | Fix |
|---|---|---|---|
| E-M03-1 | Runtime Error in test source_not_null_tpch_raw_part_p_partkey: Catalog Error: Table with name part does not exist! Did you mean "partsupp"? LINE 18: from "warehouse"."raw"."part" | Deliberate: the physical table was renamed by hand, and the SQL of each test still named raw.part. DuckDB found no table with that name when the tests ran | Added identifier: part_renamed to the table part in the YAML, then undid both the rename and the line |
| E-M03-2 | STOPPED: _tpch__sources.yml is not in your Downloads folder; download it from the chat, then make: *** [Makefile:37: fetch] Error 1 | Most likely the command ran before the browser had saved the file; the second attempt worked from the same folder with no change | Downloaded the file, checked it was in Downloads, ran the same command again |

## 6. Decisions
### D-M03-1 — `lineitem` is exposed to dbt as `line_items`
**Context.** The milestone asks for one table whose dbt name differs from its physical name. The frozen staging model is `stg_tpch__line_items`. **Decision.** Declare the table with `name: line_items` and `identifier: lineitem`, and keep the other seven tables with their physical names. **Consequences.** Models call `source('tpch_raw', 'line_items')`, and the physical table stays `raw.lineitem`. This is the one exception to the rule that a source table keeps its physical name. M09 puts `event_time` on the source `line_items`.

### D-M03-2 — `region` is exempt from freshness and `orders` has stricter thresholds
**Context.** The milestone asks to override freshness on one table and exempt one table. **Decision.** `region` gets `freshness: null` because its five rows never change. `orders` gets warn after 6 hours and error after 12 hours because it is the table that grows with every load. **Consequences.** `dbt source freshness` reports seven tables. The other six use the default of 12 and 24 hours.

### D-M03-3 — Uniqueness of two-column keys waits for `dbt_utils`
**Context.** `partsupp` is keyed by the pair (`ps_partkey`, `ps_suppkey`) and `lineitem` by (`l_orderkey`, `l_linenumber`). A `unique` test on one column of a pair fails. **Decision.** Test only `not_null` on each column of those two tables now. **Consequences.** M04 installs `dbt_utils` and adds `unique_combination_of_columns` for both pairs.

### D-M03-4 — `duckdb` stays unpinned in `requirements.txt`
**Context.** M02 left open whether to pin it. `duckdb` arrives as a dependency of `dbt-duckdb`. DuckDB keeps its extensions in a folder named after its version, so another version downloads the `tpch` extension again. **Decision.** Do not pin it now. **Consequences.** The installed version is whatever `dbt-duckdb` brings. M15 revisits the decision when CI needs the same versions as the laptop.

## 7. Exam map
| Outline bullet | Where in this chapter | Question |
|---|---|---|
| Identifying and verifying raw object dependencies | Steps 8 to 10, D-M03-1 | Q1; MILESTONES lists practice Q09 and official sample Q10 (numbers not checked in this chat) |
| Implementing source freshness | Steps 3, 4 and 7, D-M03-2 | Q2; MILESTONES lists practice Q16 and Q18 (numbers not checked in this chat) |
| Testing assumptions for models and sources | Steps 5 and 6, D-M03-3 | Q3 |

## 8. New terms
| Term | Meaning |
|---|---|
| Source | A table that dbt did not create, declared in YAML so models can read it with `source()` and dbt can test it and check its freshness |
| `source()` | The function a model calls to read a declared source table; its two arguments are the source name and the table name |
| `schema` (in a source) | The physical schema where the source tables live; it can differ from the source name |
| `identifier` | A table property that sets the physical table name when it differs from the table `name` |
| Freshness | The age of the newest row of a table, measured as the current time minus the maximum of `loaded_at_field` |
| `loaded_at_field` | The column that freshness reads to find the newest load |
| `warn_after` and `error_after` | The two age thresholds of a freshness policy; passing the first gives `warn`, passing the second gives `error` |
| `freshness: null` | The setting that removes the freshness check from one table |
| `sources.json` | The file `dbt source freshness` writes in `target/`, with one result per table |
| Data test | A query that selects the rows that break a rule; it passes when it returns zero rows |
| `relationships` test | A test that fails when a value in one column has no match in a column of another table |
| `arguments` (in a test) | The key that holds the settings of a generic test in dbt 1.11, such as `to` and `field` |
| Composite key | A key made of two or more columns, such as (`ps_partkey`, `ps_suppkey`) |
| `source:` selector | A node selection that picks a source; with `+` at the end it also picks everything that depends on it |
| Runtime error | A failure that appears when dbt runs SQL in the warehouse, not when it reads the YAML |
| `ERROR` and `FAIL` | A test is `ERROR` when its SQL could not run, and `FAIL n` when it ran and returned n rows; the final summary counts both under `ERROR` |
| Catalog Error | The DuckDB error returned when a statement names a table or schema that does not exist |

## 9. Check yourself
<details><summary>Q1. A source table is declared with `name: line_items` and `identifier: lineitem`. A model calls `{{ source('tpch_raw', 'lineitem') }}`. What happens, and what is the correct call?</summary>

dbt stops with a compilation error, because no table of the source `tpch_raw` has the name `lineitem`; `source()` looks up the table `name`, never the `identifier`. The correct call is `{{ source('tpch_raw', 'line_items') }}`. When dbt writes the SQL, it replaces `line_items` with the physical table `lineitem`. The tempting answer is that dbt accepts either word; it accepts only the `name`.

</details>

<details><summary>Q2. The source sets warn after 12 hours and error after 24 hours. `orders` sets warn after 6 hours and error after 12 hours. `region` has `freshness: null`. The last load was 8 hours ago. What does `dbt source freshness` report for `orders`, for `customer` and for `region`?</summary>

`orders` reports `warn`, because 8 hours passes 6 but not 12. `customer` reports `pass`, because it uses the source-level policy and 8 hours is below 12. `region` is not reported, because the check is switched off for it. The tempting answer for `orders` is `pass`, which would merge the two policies; the table-level block replaces the source-level block.

</details>

<details><summary>Q3. After the physical table `raw.part` is renamed, the test `source_unique_tpch_raw_part_p_partkey` ends in `[ERROR in 0.03s]`. Were duplicate part keys found?</summary>

No. `ERROR` means the SQL of the test could not run, here because of the Catalog Error. A test that runs and finds duplicates ends in `FAIL n`, where n is the number of rows the query returned. The final summary line counts both under `ERROR`, so the line of each test is the place to tell them apart. The tempting answer is to inspect the data; the first thing to inspect is the name of the physical table.

</details>
