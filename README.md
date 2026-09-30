# Wholesale Analytics — a production-shaped dbt project

[![CI](https://github.com/PLACEHOLDER_USER/dbt-wholesale-analytics/actions/workflows/ci.yml/badge.svg)](https://github.com/PLACEHOLDER_USER/dbt-wholesale-analytics/actions)

> **Status: v0.3 — living document.** Written at project start so the repo is
> self-describing from day one; rewritten in full at milestone M18 once every claim below
> is backed by code. Anything marked `PLACEHOLDER_*` is a literal placeholder to be
> replaced, not a real value.

An analytics warehouse for a global B2B wholesale parts distributor, built with
**dbt Core 1.11**. It runs locally on **DuckDB**, builds the same models on **Google
BigQuery** with IAM grants applied by dbt, and feeds a **Data Studio** dashboard.
Everything costs nothing and reproduces from a clean clone in three commands.

**Read next:** [the handbook](docs/handbook/README.md) explains how every part was built
and why, one chapter per milestone.

---

## 1. The business

The company buys manufactured parts from ~10,000 suppliers and sells them to ~150,000
business customers across 25 nations in 5 regions. Each order carries line items with a
quantity, unit price, discount, tax, a **committed** delivery date and an **actual**
receipt date. Some lines are returned.

| # | Question | Where it is answered |
|---|---|---|
| 1 | What is net revenue by region, nation, market segment and month, against target? | `agg_monthly_revenue` |
| 2 | What share of line items arrived after the committed date, by supplier, region and ship mode? | `int_delivery_performance`, `fct_order_lines` |
| 3 | How much revenue depends on suppliers above the agreed late-delivery threshold? | `fct_order_lines` × `ref_sla_thresholds` |
| 4 | Which customers make up the first 80% of revenue? | `cust_abc_classification` (Python) |
| 5 | Which daily revenue points deviate from the rolling baseline? | `revenue_anomalies` (Python) |

---

## 2. Data

The source data is **TPC-H**, generated deterministically by DuckDB's `tpch` extension —
scale factor 1 locally (~6M line items), 0.1 on BigQuery. TPC-H is the Transaction
Processing Performance Council's standard model of exactly this business, shipped as
sample data by Snowflake and Databricks.

**Nothing is downloaded.** The repository ships the generator, not the data, so there is
no dead link, no expired bucket, and every result is byte-identical for anyone who clones it.

### 2.1 Simulated source-system behaviour

The `el/` layer is the **extract-load stage** — the slot a managed connector like
Fivetran or Airbyte occupies in a real stack. It is a Python script here because the
local warehouse is a DuckDB file, and managed connectors write to cloud destinations
only. Raw TPC-H is static, so the loader simulates what a real source does:

| Behaviour | Mechanism |
|---|---|
| Load metadata | Every raw table carries `_loaded_at` and `_batch_id` |
| Incremental arrival | `--through-date` loads orders and line items in date-ordered waves |
| Mutating dimensions | `--mutate` changes customer segments and supplier balances, and deletes suppliers |

This is the difference between a snapshot that tracks history and one that has never
produced a second row.

---

## 3. Architecture

```
  el/load_raw.py ──► DuckDB (local)                 el/load_bigquery.py ──► BigQuery
                      raw                                                     raw
                       ▼  dbt sources                                          ▼
                      {env}_staging       stg_*   views                      bq_staging
                       ▼                                                       ▼
                      {env}_intermediate  int_*   joins + logic              bq_intermediate
                       ▼                                                       ▼
                      {env}_marts         dim_* fct_* agg_*                  bq_marts ──► IAM grants
                                          contracted, versioned                 │
                                                                                └──► Data Studio dashboard
        docs site (GitHub Pages) · exposures · Slim CI on every pull request
```

`{env}` is `dev` or `prod`, produced by a custom `generate_schema_name` macro keyed on
`target.name`: one DuckDB file, two schema namespaces — the pattern Snowflake teams use,
and what lets `--defer` and `dbt clone` work without a second catalog.

### 3.1 Why two engines

DuckDB is the development warehouse: local, columnar, free, and it supports Python models,
microbatch and **engine-enforced** constraints. BigQuery is the cloud target: the same
dbt project builds its staging, intermediate and marts layers there, and dbt applies
table-level IAM grants to service accounts. What does not run on the BigQuery sandbox —
anything that needs DML, such as microbatch and snapshots — is documented rather than
hidden, because knowing where a project stops being adapter-agnostic is the point of
running it on two engines.

---

## 4. Quickstart

Requirements: Python 3.11+, Git. (Linux, macOS, or WSL2 on Windows.)

```bash
git clone https://github.com/PLACEHOLDER_USER/dbt-wholesale-analytics.git
cd dbt-wholesale-analytics

make setup          # venv, pinned deps, dbt debug
make load           # generate TPC-H and load the raw schema
make build          # dbt deps && dbt seed && dbt snapshot && dbt build
```

Documentation site: `PLACEHOLDER_DOCS_URL` · Dashboard: `PLACEHOLDER_DASHBOARD_URL`

---

## 5. Repository layout

```
.
├── docs/
│   ├── handbook/                 how it was built and why — start here
│   ├── PROJECT_CHARTER.md        scope, stack, architecture, exam coverage matrix
│   ├── MILESTONES.md             how the work was decomposed, and why
│   └── PROJECT_LOG.md            plan versus reality, session by session
├── el/                           extract + load (DuckDB and BigQuery)
├── scripts/                      handbook index generator
├── transform/                    the dbt project
│   ├── dbt_project.yml
│   ├── profiles.yml              committed; every secret via env_var
│   └── models/{staging/tpch, intermediate, marts/core, marts/finance}/
├── prod-artifacts/               production manifest, for state comparison
└── Makefile
```

---

## 6. Engineering practices demonstrated

> Rows are checked as the corresponding milestone merges. An unchecked row means not
> built yet.

| Practice | Where to look | Done |
|---|---|---|
| Layered DAG: sources → staging → intermediate → marts | `transform/models/` | ☐ |
| Source freshness policies, with a documented exemption | `_tpch__sources.yml` | ☐ |
| Core materializations chosen with measured reasons | handbook M07 | ☐ |
| Incremental model with a justified strategy | `fct_order_lines.sql`, handbook M08 | ☐ |
| Microbatch incremental with event-time backfill | `fct_shipments.sql` | ☐ |
| Generic, singular, custom generic and unit tests | `transform/tests/`, `_marts__models.yml` | ☐ |
| Test severity thresholds and `store_failures` | `_marts__models.yml` | ☐ |
| Enforced model contracts and database constraints | `_marts__models.yml` | ☐ |
| Model versioning with a managed deprecation date | `dim_customers` v1/v2 | ☐ |
| Model groups and `access` levels | `_marts__models.yml` | ☐ |
| BigQuery target with IAM grants applied by dbt | `dbt_project.yml`, handbook M12 | ☐ |
| SCD Type 2 snapshots with demonstrable history | `transform/snapshots/` | ☐ |
| Python models for logic SQL handles poorly | `marts/finance/*.py` | ☐ |
| Slim CI: state comparison, deferral, `--empty`, `--sample` | `.github/workflows/ci.yml` | ☐ |
| `dbt clone` and `dbt retry` in the workflow | handbook M14 | ☐ |
| Catalogued debugging scenarios | handbook M16 and the error index | ☐ |
| Exposures tied to a real dashboard | `_marts__exposures.yml` | ☐ |
| Data Studio dashboard on the BigQuery marts | `PLACEHOLDER_DASHBOARD_URL` | ☐ |

---

## 7. How this project was built

The work was split into 19 milestones, each sized to one working session and each closable
by a command rather than an opinion. Every milestone has one ID that names its branch, its
pull request, its log entry and its handbook chapter, so any line of code, error or
decision can be traced back to the session that produced it.

- [`docs/handbook/`](docs/handbook/README.md) — one chapter per milestone: the problem,
  how it was built, how to verify it, what went wrong and how it was fixed, decisions.
- [`docs/MILESTONES.md`](docs/MILESTONES.md) — the plan and its decomposition criterion.
- [`docs/PROJECT_LOG.md`](docs/PROJECT_LOG.md) — what actually happened, against the estimate.

---

## 8. What I would do differently at production scale

> Written at M18, once there is something to be honest about.

---

## 9. Copyright

Copyright © 2026 Pedro Coronel. All rights reserved.

This repository is public so that it can be read and evaluated. Permission is granted to
clone it and run it locally for the sole purpose of evaluating it. No other licence is
granted: the code may not be copied, modified, redistributed or reused in other work
without written permission.

TPC-H is a trademark of the Transaction Processing Performance Council; the data here is
generated by DuckDB's `tpch` extension for non-benchmark, educational use.
