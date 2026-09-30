# PROJECT CHARTER — `dbt-wholesale-analytics`

`Version v3 · 2026-09-29 · hard cap 40 h end-to-end (30.5 h planned + 30% buffer = 39.65 h), exam on 2026-10-30, PostgreSQL replaced by BigQuery for grants, Data Studio dashboard, project handbook`

> **What this document is.** The stable contract for the whole project. If something
> here conflicts with a milestone, this document wins and the milestone is wrong. If
> something here conflicts with `PROJECT_LOG.md` about what *exists*, the log wins.
>
> **How it is used.** It lives in the Project knowledge of the claude.ai Project, so every
> chat reads it. From M00 on it is also committed to the repo at `docs/PROJECT_CHARTER.md`.

---

## 1. Purpose

Three outputs, in this priority order.

| # | Output | Test for "done" |
|---|--------|-----------------|
| 1 | **Every bullet of the official dbt Analytics Engineering Certification outline (dbt Core 1.11) executed at least once, by hand, against real data** — before the exam on **2026-10-30**. | Section 9 coverage matrix has no empty cell. |
| 2 | **A project handbook that explains how the project was built and why**, one chapter per milestone, in which any error or decision can be traced to its cause. | `docs/handbook/` has one chapter per merged milestone and a generated index. |
| 3 | **A public GitHub repository a US hiring manager reads as production-grade analytics engineering**, with a cloud warehouse (BigQuery) and a BI dashboard (Data Studio). | A stranger clones it, runs three commands, gets a working warehouse with passing tests; the docs site and the dashboard open from the README. |

When outputs conflict, the lower number wins.

---

## 2. Hard constraints (non-negotiable)

| Constraint | Value |
|---|---|
| Total cost | **US$0**, forever: no trials, no credit card, no billing account |
| Total effort | **≤ 40 h end-to-end**, installs and friction included: 30.0 h of milestones + 0.5 h of audits + 9.15 h buffer = 39.65 h (§2.2) |
| Exam | dbt Analytics Engineering Certification, dbt Core **1.11**, on **2026-10-30** |
| Target dbt version | **dbt Core 1.11** (1.12 exists; the exam tests 1.11 — do not upgrade) |
| Core path runs locally | DuckDB on the laptop; BigQuery is a second target, not a dependency |
| Reproducible by a stranger | `make setup && make load && make build` from a clean clone |
| Data acquisition risk | **Zero** — nothing downloaded, no login or API key for the core path |
| Git | One milestone = one branch, one PR, squash merge; CI required from M15 |
| Documentation | One handbook chapter per milestone, written at the close of that milestone |
| Exposure | **Tier A — public repository, no licence, all rights reserved** (§2.1) |

**Out of scope, deliberately.** Orchestration (Airflow, Dagster), a paid BI tool, Looker
(the enterprise product), Tableau, Kubernetes, Terraform, a semantic layer, dbt Mesh,
streaming, a managed EL connector, an AI agent layer. They add hours and add nothing to the
exam.

### 2.1 Exposure policy — tier A

| Item | Decision |
|---|---|
| Repository visibility | Public |
| Licence | **None selected** at creation. Default copyright applies: all rights reserved *(GitHub Docs, "Licensing a repository")* |
| Notice | README §9 states the copyright and allows cloning and running locally only to evaluate the project |
| What GitHub's terms still allow | Others may view and fork a public repo on GitHub. Accepted: the value is the author's ability to build and defend the work, which a copy does not transfer |
| Why not private | On GitHub Free a private repo loses GitHub Pages (the docs site) and branch protection (M15), and hides the evidence reviewers read |
| Never committed | `AI_OPERATING_BRIEF.md`, `SESSION_PROTOCOL.md`, `WALKTHROUGH.md`, `PROJECT_INSTRUCTIONS.txt`, `.env`, `data/*.duckdb`, any credential |
| Guard | The pre-publish check (`AI_OPERATING_BRIEF.md` §3.13) runs before every commit |

### 2.2 Effort and calendar (computed in code, 2026-09-29)

| Item | Hours |
|---|---|
| 19 milestones, M00–M18 | 30.0 |
| 2 phase audits (after M06 and M16) | 0.5 |
| Planned work | 30.5 |
| Buffer, 30% of planned work | 9.15 |
| **Cap** | **39.65 ≤ 40** |

| Weekly capacity | Weeks for 39.65 h | Build ends around | Fits before the exam-week plan (starts 2026-10-25)? |
|---|---|---|---|
| 12 h (4 × 3 h) — **recommended** | 3.3 | 2026-10-22 | Yes, 2 days of slack |
| 10 h (4 × 2.5 h) | 4.0 | 2026-10-27 | No — M18 moves to after the exam |

The exam-week study plan (MILESTONES Appendix B, about 8 h) is study, not project work,
and sits outside the 40 h.

**Why the plan shrank from v2 (55.5 h) to v3 (30.5 h planned).** Milestones that
exercised the same exam bullet were merged (staging + seeds + packages; tests + unit tests;
contracts + versions + access; snapshots + Python), PostgreSQL and Docker were removed
(grants move to BigQuery, which is also the portfolio's cloud target), and three items with
no exam weight were cut (`dbt_project_evaluator`, the AI triage agent, `dim_date`). Exam
coverage is unchanged: §9 still has no empty cell.

---

## 3. Verified stack

| Layer | Tool | Why | Cost |
|---|---|---|---|
| Transformation | **dbt Core 1.11** | The exam target | Free (Apache 2.0) |
| Primary warehouse | **DuckDB** via `dbt-duckdb` 1.11 | Local file; supports Python models, microbatch, and **engine-enforced** constraints | Free |
| Cloud warehouse | **BigQuery sandbox** via `dbt-bigquery` 1.11 | Grants (IAM) for the exam; a cloud warehouse for the portfolio | Free, no card |
| BI | **Data Studio** (Looker Studio 2022–2026) | Dashboard on the BigQuery marts; makes the exposure real | Free |
| Extract/Load | **Python 3.11+** (`el/`) | Occupies the EL slot of a managed connector (Fivetran, Airbyte). Local by necessity: managed connectors write to cloud destinations only | Free |
| Version control, CI, docs hosting | **GitHub**, **GitHub Actions**, **GitHub Pages** | Portfolio surface, Slim CI, docs site | Free on public repos |

### 3.1 Version pinning (verified by installing, 2026-09-29)

```
dbt-core==1.11.*
dbt-duckdb==1.11.*
dbt-bigquery==1.11.*
pandas
```

`pandas` is already installed as a dependency of `dbt-bigquery` (verified); it is listed
because the Python models (M13) use it directly.

Installed together on Python 3.11 they resolve to core 1.11.15, duckdb 1.11.0, bigquery
1.11.3. The same run also verified, on a small DuckDB project: microbatch, an enforced
contract with constraints, YAML snapshots with `hard_deletes`, a Python model, a unit test,
`--empty`, `--sample`, `dbt clone`, `dbt retry` and `state:modified`.

### 3.2 Why DuckDB stays primary and BigQuery is second

The BigQuery **sandbox** — the only no-card way to use BigQuery — does not support DML
statements *(Google Cloud docs, "Try BigQuery using the sandbox", checked 2026-09-29)*.
Incremental runs after the first, microbatch and snapshots are DML, so they must run on
DuckDB. What the sandbox does support is everything built with `create table as select`
or views, plus load jobs, which is enough for the staging, intermediate and marts layers
(with `--full-refresh`) and for grants.

The sandbox also has three limits the plan respects: a **lifetime** storage limit of
10 GiB that deletions do not refund (so BigQuery gets TPC-H at scale factor 0.1), tables
that expire after 60 days (so the dashboard needs `make bq-build` every 60 days, and a
screenshot is committed), and 1 TiB of queries per month.

### 3.3 Why BigQuery for grants instead of PostgreSQL

DuckDB has no roles. `dbt-duckdb` 1.11 ignores a `grants` config with the debug message
"Grants for relations are not supported by DuckDB" (verified 2026-09-29). BigQuery applies
it as IAM `GRANT` statements to real principals — here two service accounts with no keys,
`dbt-reporter` and `dbt-finance`. This removes Docker from the project. The one assumption
not found in Google's documentation — that the sandbox accepts `GRANT` — is tested in M00
before anything depends on it (R2).

---

## 4. Business context

The project models a **global B2B wholesale parts distributor**: it buys parts from
suppliers and sells them to business customers across 25 nations in 5 regions. Orders have
line items with quantity, price, discount, tax, a committed date and a receipt date. Some
lines are returned.

The data is the TPC-H schema — the Transaction Processing Performance Council's standard
model of this business, shipped as sample data by Snowflake and Databricks — generated
deterministically by DuckDB's `tpch` extension.

### 4.1 Business questions the marts answer

1. **Revenue** — net revenue by region, nation, market segment and month, against target.
2. **Delivery reliability** — share of line items received after the committed date, by
   supplier, region and ship mode.
3. **Supplier risk** — revenue that depends on suppliers above the late-delivery threshold.
4. **Customer concentration** — ABC (Pareto) classification of customers (Python).
5. **Revenue anomalies** — daily revenue points far from a rolling baseline (Python).

### 4.2 Data volume

| TPC-H table | Rows at SF 1 (DuckDB) | Rows at SF 0.1 (BigQuery) |
|---|---|---|
| `lineitem` | ~6,001,215 | ~600,572 |
| `orders` | 1,500,000 | 150,000 |
| `partsupp` | 800,000 | 80,000 |
| `part` | 200,000 | 20,000 |
| `customer` | 150,000 | 15,000 |
| `supplier` | 10,000 | 1,000 |
| `nation` / `region` | 25 / 5 | 25 / 5 |

The `.duckdb` file is git-ignored; the repo ships the generator, not the data.

### 4.3 What the EL layer adds to raw TPC-H

| Behaviour | Implementation | Exam topic it enables |
|---|---|---|
| Load metadata | `_loaded_at`, `_batch_id` on every raw table | source freshness |
| Incremental arrival | orders and line items load in date waves (`--through-date`) | incremental, microbatch |
| Mutating dimensions | `--mutate` changes segments and balances, deletes suppliers | snapshots, `hard_deletes` |

---

## 5. Target architecture

```
  el/load_raw.py  ──►  data/warehouse.duckdb (SF 1)            el/load_bigquery.py ──► BigQuery sandbox (SF 0.1)
                         raw                                                            raw
                          │ dbt sources                                                  │
                          ▼                                                              ▼
                        {env}_staging     stg_*   views                                bq_staging
                          ▼                                                              ▼
                        {env}_intermediate int_*  ephemeral/table                      bq_intermediate
                          ▼                                                              ▼
                        {env}_marts       dim_* fct_* agg_*                            bq_marts ──► grants (IAM)
                                          + snapshots, microbatch,                        │
                                            Python models (DuckDB only)                   └──► Data Studio dashboard
                          │
                          └──► docs site (GitHub Pages) · exposures
```

`{env}` is `dev` or `prod`, produced by a custom `generate_schema_name` macro keyed on
`target.name`. One DuckDB file, two schema namespaces — the pattern Snowflake teams use —
which lets `--defer` and `dbt clone` work without a second catalog.

### 5.1 Targets

| Target | Engine | Schemas / datasets | Used for |
|---|---|---|---|
| `dev` | DuckDB | `dev_staging`, `dev_marts`, … | Daily development |
| `prod` | DuckDB | `prod_staging`, `prod_marts`, … | Source of deferred state and clone |
| `bq` | BigQuery sandbox | `bq_staging`, `bq_intermediate`, `bq_marts` | Grants; portfolio; dashboard |

### 5.2 Naming conventions

| Object | Pattern | Example |
|---|---|---|
| Source | `{system}` / table as-is | `source('tpch_raw', 'orders')` |
| Staging model | `stg_{system}__{entity}` | `stg_tpch__orders` |
| Intermediate | `int_{entity}_{verb}` | `int_order_lines_enriched` |
| Dimension · Fact · Aggregate | `dim_` · `fct_` · `agg_` | `dim_customers`, `fct_order_lines`, `agg_monthly_revenue` |
| Property YAML | `_{folder}__models.yml`, `_{system}__sources.yml` | `_staging__models.yml` |
| Seed | `ref_{subject}` | `ref_region_targets` |
| Snapshot | `{entity}_snapshot` | `customers_snapshot` |
| Singular test | `assert_{expectation}` | `assert_no_negative_revenue` |
| Handbook chapter | `mNN-{branch-slug}.md` | `m08-incremental.md` |

### 5.3 Repository layout

```
dbt-wholesale-analytics/
├── README.md                       ← portfolio surface; v0 now, final at M18
├── Makefile
├── requirements.txt
├── .env.example                    ← every key, no values
├── .gitignore
├── .github/workflows/
│   ├── ci.yml                      ← M15
│   └── docs.yml                    ← M17
├── docs/
│   ├── PROJECT_CHARTER.md          ← this file
│   ├── MILESTONES.md
│   ├── PROJECT_LOG.md              ← plan versus reality, hours
│   ├── handbook/                   ← how it was built and why
│   │   ├── README.md               ← generated index: chapters, errors, decisions, glossary
│   │   └── mNN-slug.md             ← one chapter per milestone
│   └── assets/                     ← dashboard screenshot (M18)
├── scripts/
│   └── build_handbook_index.py     ← M01
├── el/
│   ├── load_raw.py                 ← M02
│   ├── load_bigquery.py            ← M12
│   └── README.md
├── prod-artifacts/manifest.json    ← M14
├── data/warehouse.duckdb           ← git-ignored
└── transform/                      ← the dbt project root
    ├── dbt_project.yml
    ├── packages.yml · package-lock.yml
    ├── profiles.yml                ← committed; every secret via env_var
    ├── models/{staging/tpch, intermediate, marts/core, marts/finance}/
    ├── seeds/ snapshots/ macros/ tests/ analyses/
    └── target/                     ← git-ignored
```

`profiles.yml` lives inside the dbt project, not in `~/.dbt/`: it holds no secrets (every
value comes from `env_var()`), and dbt Core looks in the current directory before
`~/.dbt/`. Recorded as `D-M01-1`.

---

## 6. Git workflow

One milestone → one branch → one PR → (CI from M15) → squash merge. No commits to `main`,
except the initial commit of M00 (a new repo has no base branch for a PR).
Conventional Commits: `feat`, `fix`, `test`, `docs`, `refactor`, `chore`, `ci`; scope is
the layer (`el`, `staging`, `intermediate`, `marts`, `governance`, `ci`, `docs`).

---

## 7. Documentation system

Four layers, each with one job:

| Layer | File(s) | Answers | Written |
|---|---|---|---|
| Portfolio front door | `README.md` | What is this and how do I run it? | v0 now, final at M18 |
| Build log | `docs/PROJECT_LOG.md` | What exists now, what took how long, what deviated? | At every close |
| **Handbook** | `docs/handbook/mNN-slug.md` + generated `README.md` | How was it built, why, what broke and how was it fixed, what does the exam ask? | One chapter at every close |
| Reference | dbt docs site (`dbt docs generate`) | What does each model and column mean, and what feeds it? | From YAML descriptions, published at M17 |

The chapter template is in `AI_OPERATING_BRIEF.md` §3.14. The index is generated by
`make handbook`, never edited by hand. Chapters are written in plain English: short
sentences, every term defined the first time it appears, the real command before the
explanation of it.

---

## 8. Risks and pre-decided fallbacks

| # | Risk | Probability | Fallback, decided now |
|---|---|---|---|
| R1 | Version incompatibility in the pinned stack | **Retired** (installed together on 2026-09-29) | — |
| R2 | The BigQuery sandbox rejects `GRANT` | Low (not documented either way) | Tested in M00. If rejected: grants run on PostgreSQL in Docker in M12 (+0.5 h from the buffer). |
| R3 | SF 1 too slow on the laptop | Low | `TPCH_SCALE_FACTOR=0.1`. Nothing else changes. |
| R4 | GitHub Pages unavailable | Low | Link the generated docs from a `docs-site` branch. |
| R5 | The 40 h cap is at risk | Medium | Stop any milestone at 1.5× its budget (brief §2.3). If cumulative drift exceeds 30%, M18 moves to after the exam. M00–M17 are never cut. |
| R6 | Sandbox tables expire (60 days) and break the dashboard | Certain, after 60 days | `make bq-build` recreates them; the committed screenshot stays valid. |
| R7 | A private file or secret is pushed | Low | Pre-publish check before every commit; `.gitignore` from M00. |

---

## 9. Exam coverage matrix

Every bullet is copied from the official dbt Labs study guide for exam version 1.11.
`M##` refers to `MILESTONES.md`. **No bullet may be left without a milestone.**

### 01 — Developing and optimizing dbt models

| Bullet | Milestone | How it is exercised |
|---|---|---|
| Identifying and verifying raw object dependencies | M03 | Sources with `identifier` override; a raw table renamed by hand and diagnosed |
| Understanding core dbt materializations | M05, M07 | Ephemeral inlining; view/table/ephemeral on the same model, DDL read in `target/run/` |
| Modularity and DRY principles | M05 | `int_` models and the `net_revenue` macro |
| Commands: `build`, `run`, `test`, `docs`, `show`, `snapshot`, `seed` | M04–M17 | Each introduced where first needed |
| Logical model flow and clean DAGs | M04–M06 | staging → intermediate → marts, no staging-on-staging |
| Configurations in `dbt_project.yml` | M01, M07 | Written by hand; precedence tested |
| Using dbt Packages | M04 | `dbt_utils`, `codegen`; a package config overridden from `dbt_project.yml` |
| Creating Python Models | M13 | ABC classification, revenue anomalies |
| `grants` config | M12 | Project, folder (`+`) and model level on BigQuery, verified in `OBJECT_PRIVILEGES` |
| Creating snapshots in YAML | M13 | `check` and `timestamp`, `hard_deletes` |
| Selecting the optimal incremental strategy | M08 | `append` / `delete+insert` / `merge` timed on the same model |
| `--empty` dry runs | M15 | CI job; the zero-row `unique` pass of official sample Q7 |
| `--sample` mode | M15 | CI job with `--sample` |
| Advanced materializations: microbatch | M09 | `event_time`, `batch_size`, `lookback`, `begin`, explicit backfill |

### 02 — Managing dbt models governance

| Bullet | Milestone | How it is exercised |
|---|---|---|
| Contracts to ensure model shape | M11 | Enforced on marts; failure read and fixed |
| Model versions and deprecating old ones | M11 | `dim_customers` v1 → v2, `deprecation_date` |
| Constraints in YAML at platform level | M11 | DuckDB rejects a violating `insert` |

### 03 — Debugging data modeling errors

| Bullet | Milestone | How it is exercised |
|---|---|---|
| Understanding logged error messages | M16 (+ every chapter's errors table) | Deliberate breakage lab |
| Troubleshooting using compiled code | M05, M16 | Ephemeral inlining; empty Jinja loop found in `target/compiled/` |
| Troubleshooting `.yml` compilation errors | M16 | "did not find matching node for patch", "mapping values are not allowed" |
| Developing and testing a fix before merging | M15 | Slim CI on a PR |
| Managing dbt behavior with flags | M16 | `flags:`, `--warn-error`, `--warn-error-options`, `--fail-fast` |

### 04 — Troubleshooting and optimizing dbt pipelines

| Bullet | Milestone | How it is exercised |
|---|---|---|
| Failure points in the DAG | M10, M16 | `SKIP` propagation; `--fail-fast` |
| Using `dbt clone` | M14 | Clone of `prod_marts`, contrasted with `--defer` |

### 05 — Implementing dbt tests

| Bullet | Milestone | How it is exercised |
|---|---|---|
| Generic, singular, custom, custom generic, and unit tests | M10 | One of each |
| Testing assumptions for models and sources | M03, M10 | Source tests; `relationships`, `accepted_values` |
| Testing steps in the workflow | M10, M15 | `where`, `severity`, `warn_if`/`error_if`, `store_failures`, `--indirect-selection`, CI |

### 06 — External dependencies

| Bullet | Milestone | How it is exercised |
|---|---|---|
| Implementing dbt exposures | M17 | `dashboard` and `analysis` exposures |
| Implementing source freshness | M03 | `loaded_at_field`, `warn_after`/`error_after`, override, `freshness: null` |

### 07 — Leveraging the dbt state

| Bullet | Milestone | How it is exercised |
|---|---|---|
| Understanding state and state selection | M14, M15 | `state:modified`, `state:new`, `source_status:fresher+`, `--defer`, CI |
| Using `dbt retry` | M14 | Partial failure resumed |

### Cross-cutting topics from the sample and practice questions

| Topic | Milestone |
|---|---|
| Hooks: `on-run-start`, `on-run-end`, `pre-hook`, `post-hook` | M07 |
| Model `groups` and `access` | M11 |
| `require-dbt-version` | M01 |
| Git branching and PRs | M15, and every milestone |
| `dbt show`, `compile`, `parse`, `ls` | M04, M16 |
| Artifacts: `manifest.json`, `run_results.json`, `catalog.json` | M14, M17 |

---

## 10. Clock

| Item | Date | Status |
|---|---|---|
| Build starts | 2026-09-29 | — |
| Build ends (latest) | 2026-10-24 | at 12 h/week, around 2026-10-22 |
| Exam-week plan | 2026-10-25 → 2026-10-29 | outside the 40 h |
| **Exam** | **2026-10-30** | confirmed by the user on 2026-09-29 |

---

## 11. Working agreements

1. **Nothing is written that has not been run.**
2. **Every session ends green**: `main` always works.
3. **Every session ends documented**: log updated and handbook chapter committed with the
   code it explains.
4. **One decision → one `D-MNN-n` entry** in that milestone's chapter.
5. **Every error met is recorded** as `E-MNN-n` with its verbatim message, cause and fix.
6. **Terminal first** for git: `git switch -c`, `git add`, `git commit`, `gh pr create`.
7. **Numbers are computed, never estimated in the head.**
