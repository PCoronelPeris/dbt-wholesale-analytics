# MILESTONES — `dbt-wholesale-analytics`

`Version v4 · 2026-10-18 · recalibrated after M00 and M01 took 4.0 h each: the same 19 milestones, every remaining one budgeted at 1.5–2 h of real time; files pre-built and tested before they reach the terminal; one-command start and close; no calendar dates; loader semantics fixed so snapshots and relationship tests cannot break`

> **Companion to `PROJECT_CHARTER.md`.** The charter is stable; this document is the
> sequence.
>
> **How it is used.** One chat per milestone. You open a **new** chat in the Project and
> write `START MNN.` (for example `START M02.`); the chat reads this milestone, the
> charter, the brief and the log from Project knowledge and checks `main` on GitHub.

---

## 0. How this document is built

### 0.1 The decomposition criterion

A milestone is the **smallest unit of work that satisfies all five** of these:

1. **Closable** — it ends in a state you can *verify with a command*, not with an
   opinion. "Staging layer designed" is not a milestone. "`dbt build --select
   staging` returns PASS=8 ERROR=0" is.
2. **Committable** — it produces one Git commit whose message makes sense read alone,
   six months later, by someone else.
3. **Reversible** — if it goes wrong, you revert *it* and nothing else breaks.
4. **No open dependencies** — it leaves nothing half-built for the next milestone to
   finish.
5. **Fits one session of 1.5–2 h of real time** — including reading, mistakes, the
   chapter and the merge.

### 0.2 One ID everywhere — the traceability rule

Every milestone has one ID, and that ID names everything it produces:

| Thing | Name | Example |
|---|---|---|
| Milestone | `MNN` | `M08` |
| Git branch | `mNN-slug` | `m08-incremental` |
| Pull request title | `MNN — Title` | `M08 — Incremental models` |
| Log entry | `## MNN — Title` in `docs/PROJECT_LOG.md` | |
| Handbook chapter | `docs/handbook/mNN-slug.md` | `docs/handbook/m08-incremental.md` |
| Error met while building | `E-MNN-n` | `E-M08-2` |
| Decision taken | `D-MNN-n` | `D-M08-1` |

To trace anything: find its ID, open the chapter with the same number.

`scripts/milestone.py` reads the `## MNN — Title` heading and the `**Commit.**` line of
each milestone to name the branch, the commit and the pull request. Both lines keep
exactly this format.

### 0.3 The budget, in real hours (recalibrated 2026-10-18)

M00 and M01 were each estimated at 1.5 h and each took 4.0 h. The causes, measured in the
M01 chat: the milestone was restarted once after the explanation format failed; it was
delivered as 74 numbered steps (57 to build, 17 to close), each a separate action with its
own paste-back; files were typed in fragments (four heredocs for one 40-line file);
shell mechanics were explained at length while the milestone-level "what are we building
and why" was missing; and the close needed 17 manual steps. The method in the brief, Part
1, now removes each of these. The budgets below are **real time at the user's pace**,
not an expert's estimate.

| Milestone | Budget (h) | | Milestone | Budget (h) |
|---|---|---|---|---|
| M00 (done) | 4.0 actual | | M10 | 2.0 |
| M01 (done) | 4.0 actual | | M11 | 2.0 |
| M02 | 1.5 | | M12 | 2.0 |
| M03 | 1.5 | | M13 | 2.0 |
| M04 | 2.0 | | M14 | 2.0 |
| M05 | 1.5 | | M15 | 2.0 |
| M06 | 1.5 | | M16 | 1.5 |
| M07 | 1.5 | | M17 | 1.5 |
| M08 | 2.0 | | M18 | 1.5 |
| M09 | 1.5 | | Audits A and B | 0.5 |

**Total:** 8.0 h spent + 29.5 h for M02–M18 + 0.5 h of audits = **38.0 h**, under the
40 h cap. The cap now has 2.0 h of slack instead of a 30% buffer, so the stop rule
matters: a milestone that reaches **1.5× its budget** stops (brief section 2.3).

**What makes 1.5–2 h possible** (brief Part 1 has the rules):
- Every file is written and **run in Claude's sandbox before it is sent**. The terminal
  receives finished, tested files, not fragments to debug.
- A file longer than about 60 lines is downloaded from the chat and placed with
  `make fetch`; shorter files are one paste each. Never in fragments.
- Each response opens with the map of the milestone: what it builds, where it sits in the
  project, which exam bullets it serves, the parts and their minutes.
- Every line of every file and every command is explained, every time, in a compact
  annotated form: what it does, its role in this project, its link to dbt and the exam.
- A milestone is 3 parts: build, verify, close. Each part ends with **one** command whose
  output you paste.
- `make start M=NN` and `make close M=NN` replace the git sequence; the close is two
  downloads and one command.

### 0.4 Milestone template

| Field | Meaning |
|---|---|
| **Objective** | One sentence. What exists at the end that did not exist at the start. |
| **Preconditions** | What must already be true. If one is false, stop. |
| **Work** | The concrete steps, in order. |
| **Exam topics** | Which study-guide bullets this exercises. |
| **Exit criteria** | The command(s) that prove it is done. |
| **Parts** | The three parts of the session and their minutes. |
| **Commit** | Branch name and commit message, in the exact format `scripts/milestone.py` reads. |
| **Chapter** | The handbook file written at `CLOSE SESSION.` |
| **Budget · Model** | Real hours · model, Effort and Thinking to select before the first message. |

**Question references.** "Official sample Q#" = the 10 sample questions in the dbt Labs
study guide for 1.11. "Practice Q#" = the 65-question third-party practice set, whose
answer keys are **not** authoritative (Appendix B).

### 0.5 Phase map

| Phase | Milestones | Hours | Theme |
|---|---|---|---|
| 0 — Viability gate | M00 | 4.0 (actual) | Prove the local stack and the BigQuery sandbox |
| 1 — Foundations | M01–M03 | 4.0 actual + 3.0 | Project skeleton, handbook tooling, EL layer, sources |
| 2 — Core modelling | M04–M06 | 5.0 | Staging, seeds, packages → intermediate → marts |
| | *Audit A* | *0.25* | *after M06* |
| 3 — Materializations | M07–M09 | 5.0 | view/table/ephemeral, hooks, incremental, microbatch |
| 4 — Testing | M10 | 2.0 | Every test type, including unit tests |
| 5 — Governance and cloud | M11–M12 | 4.0 | Contracts, versions, access; BigQuery target and grants |
| 6 — History and Python | M13 | 2.0 | Snapshots, Python models |
| 7 — State, CI, debugging | M14–M16 | 5.5 | The high-yield exam phase |
| | *Audit B* | *0.25* | *after M16* |
| 8 — Publish | M17–M18 | 3.0 | Exposures and docs site; dashboard and final README |
| | **Total** | **38.0** | **cap 40** |

**Cut order if time runs short:** M18 moves to after the exam. Nothing else is cut:
M00–M17 cover 100% of the exam outline (charter section 9).

---


# PHASE 0 — VIABILITY GATE

## M00 — Prove the stack before building on it

**Status.** Done · 2026-09-30 · 4.0 h actual.

**Objective.** Every technical assumption in the charter is verified on your machine and
in the BigQuery sandbox, and the public repo exists with its first commit.

**Preconditions.** A GitHub account and a Google account. The plan files downloaded to
your computer, in one folder: `AI_OPERATING_BRIEF.md`, `PROJECT_CHARTER.md`,
`MILESTONES.md`, `PROJECT_LOG.md`, `README.md`, `SESSION_PROTOCOL.md`, `WALKTHROUGH.md`,
`PROJECT_INSTRUCTIONS.txt`. WSL2, Python, Git and GitHub CLI are installed inside this
milestone if missing. **No Docker is needed anywhere in this project.**

**Work.** The order matters: the repo folder exists before anything is written into it,
and `.gitignore` exists before any secret or data file does.

1. **Tooling.** On Windows: install WSL2 with Ubuntu (`wsl --install` in PowerShell run
   as administrator, then reboot) and from here on work only in the Ubuntu terminal.
   Inside Ubuntu, install whatever is missing among Python 3.11+ with `venv`, Git and
   GitHub CLI (`gh`). Expected: `python3 --version`, `git --version` and `gh --version`
   each print a version.
2. **GitHub login.** `gh auth login` (GitHub.com → HTTPS → login with a web browser).
   Expected: `gh auth status` says you are logged in.
3. **Private folder.** `mkdir -p ~/projects/_contexto-dbt` and copy the plan files into
   it. On Windows the Downloads folder is visible from Ubuntu at
   `/mnt/c/Users/<your-windows-user>/Downloads/`.
4. **Create the repo.** `cd ~/projects && gh repo create dbt-wholesale-analytics
   --public --clone`, then `cd dbt-wholesale-analytics`. No `--license` flag, so no
   licence file is created (exposure tier A, charter section 2.1). Expected: an empty folder
   containing only `.git/`.
5. **`.gitignore` first.** Create it with these lines: `.venv/`, `.env`,
   `data/*.duckdb`, `data/*.duckdb.wal`, `AI_OPERATING_BRIEF.md`, `SESSION_PROTOCOL.md`,
   `WALKTHROUGH.md`, `PROJECT_INSTRUCTIONS.txt`.
6. **Python environment.** `python3 -m venv .venv`, `source .venv/bin/activate`, write
   `requirements.txt` with the pins in charter section 3.1, `pip install -r requirements.txt`.
7. **dbt check.** `dbt --version` must show core `1.11.x` with plugins `duckdb 1.11.x` and
   `bigquery 1.11.x`. It will also say "Update available" for 1.12: **do not upgrade** —
   the exam tests 1.11. (This exact install was verified on 2026-09-29: core 1.11.15,
   duckdb 1.11.0, bigquery 1.11.3.)
8. **TPC-H probe.** `mkdir -p data`, then in a Python REPL:
   ```python
   import duckdb
   con = duckdb.connect("data/probe.duckdb")
   con.sql("INSTALL tpch; LOAD tpch; CALL dbgen(sf=1);")
   print(con.sql("select count(*) from lineitem").fetchone())
   ```
   Confirm ~6,001,215. Note the wall-clock time and the file size. Then
   `rm data/probe.duckdb`.
9. **BigQuery sandbox probe — web console only, no install.** This retires the one
   unverified assumption of the plan: that the sandbox accepts `GRANT` statements.
   1. Open `https://console.cloud.google.com/bigquery` with your Google account. Create a
      project when asked. **Do not enable billing, do not enter a card.** Confirm the
      page shows a "sandbox" notice. Write down the project ID.
   2. In **IAM & Admin → Service Accounts**, create two service accounts with no roles
      and **no keys**: `dbt-reporter` and `dbt-finance`. If the console asks to enable the
      IAM API, enable it (it is free and needs no billing).
   3. In the BigQuery query editor, run (replace `PROJECT_ID`):
      ```sql
      create schema probe options (location = 'US');
      create table probe.t as select 1 as x;
      grant `roles/bigquery.dataViewer` on table probe.t
        to "serviceAccount:dbt-reporter@PROJECT_ID.iam.gserviceaccount.com";
      drop schema probe cascade;
      ```
   4. If the `grant` succeeds: grants run on BigQuery in M12 (the plan as written). If it
      fails: copy the error; M12 then runs grants on PostgreSQL in Docker instead (charter
      R2, about +0.5 h from the buffer). Either way, record it as `D-M00-1`.
10. **Environment file.** `.env` with `GCP_PROJECT_ID=<your project ID>`; `.env.example`
    with the same key and no value.
11. **Plan documents into the repo.** `mkdir -p docs/handbook`, copy `PROJECT_CHARTER.md`,
    `MILESTONES.md` and `PROJECT_LOG.md` from `~/projects/_contexto-dbt/` into `docs/`,
    and `README.md` into the repo root. From here on the repo copies are the master copies.
12. **Stage and check, do not commit yet.** `git add -A`, `git status`, then the
    pre-publish check (`AI_OPERATING_BRIEF.md` section 3.13). The commit happens at
    `CLOSE SESSION.`, so that it includes the updated log and the first chapter.

**Exam topics.** None directly. This milestone retires risks R1 and R2.

**Exit criteria.**
- `dbt --version` lists core 1.11.x + plugins duckdb 1.11.x and bigquery 1.11.x
- the probe printed ~6,001,215 and the value is noted
- the BigQuery `grant` result (success or the exact error) is noted
- `gh repo view dbt-wholesale-analytics --json visibility,licenseInfo` shows
  `"visibility":"PUBLIC"` and `"licenseInfo":null`
- `git status` lists as staged `.gitignore`, `.env.example`, `requirements.txt`,
  `README.md` and the three files in `docs/` — and not `.env`, `.venv/` or any `.duckdb`
- the pre-publish check prints two `OK` lines

**Commit.** Straight to `main` — the one exception in the brief section 3.10, because an empty
repo has no base branch for a PR. At `CLOSE SESSION.`: update `docs/PROJECT_LOG.md`,
create `docs/handbook/m00-stack-verification.md` → `git add -A` → pre-publish check →
`git commit -m "chore: pin toolchain and verify local and cloud stack"` →
`git branch -M main` → `git push -u origin main`. Then re-upload `docs/PROJECT_LOG.md`
to Project knowledge.

**Chapter.** `docs/handbook/m00-stack-verification.md`

**Budget.** 1.5h. **Model.** Claude Opus 5 · Effort High · Thinking on (fixed).

---

# PHASE 1 — FOUNDATIONS

## M01 — Project skeleton, `dbt_project.yml`, handbook tooling

**Status.** Done · 2026-10-09 · 4.0 h actual. At its close (2026-10-18) the replan added `make start`, `make close` and `make fetch` (`scripts/milestone.py`).

**Objective.** A dbt project that connects to `dev` and `prod` and passes `dbt debug`, a
`dbt_project.yml` written by hand, a Makefile, and the handbook index generator.

**Preconditions.** M00 committed and pushed to `main`.

**Work.**

1. `cd ~/projects/dbt-wholesale-analytics`, `source .venv/bin/activate`, then
   `dbt init wholesale_analytics --skip-profile-setup` and `mv wholesale_analytics
   transform`. **Delete `transform/models/example/`** immediately.
2. Rewrite `transform/dbt_project.yml` from scratch: `name`, `version`,
   `config-version`, `require-dbt-version: ">=1.11.0,<1.12.0"`, `profile`, all six
   `*-paths`, `clean-targets`, a `models:` tree with per-folder `+materialized` and
   `+schema`, `vars:`, and an empty `flags:` block (filled in M16).
3. Write `transform/profiles.yml` with two outputs, `dev` and `prod` (DuckDB, same file
   `{{ env_var('DUCKDB_PATH', '../data/warehouse.duckdb') }}` — relative to `transform/`,
   where dbt runs; brief section 3.4). The `bq` output is added in M12.
4. Write `transform/macros/generate_schema_name.sql` so schemas render as
   `{target.name}_{custom_schema_name}` — e.g. `dev_marts`, `prod_marts`.
5. Append to `.gitignore`: `target/`, `dbt_packages/`, `logs/`.
6. Create `scripts/build_handbook_index.py` with exactly this content (tested on
   2026-09-29; it reads every chapter and writes `docs/handbook/README.md`):

   ```python
   """Build docs/handbook/README.md from the chapter files.

   Each chapter is docs/handbook/mNN-slug.md and follows the chapter template.
   This script reads every chapter and writes one index with four tables:
   chapters, errors, decisions and glossary. Never edit README.md by hand.
   """
   import re
   from pathlib import Path

   HANDBOOK = Path(__file__).resolve().parent.parent / "docs" / "handbook"
   HEADER = """# Project Handbook

   How this project was built, one chapter per milestone. Every milestone has the same ID
   everywhere: branch `mNN-...`, pull request `MNN — ...`, log entry `## MNN`, and chapter
   `mNN-....md`. Errors are `E-MNN-n`, decisions are `D-MNN-n`.

   **How to read it.** Start with the chapters in order. Every chapter has the same nine
   sections: the problem, where it sits, how it was built, how to verify it, what went
   wrong, decisions, exam map, new terms, and check-yourself questions.

   **This file is generated** by `make handbook` (`scripts/build_handbook_index.py`).
   Do not edit it by hand.
   """


   def section(text: str, number: int) -> str:
       """Return the body of '## {number}. ...' up to the next '## ' heading."""
       match = re.search(rf"^## {number}\. .*?$(.*?)(?=^## |\Z)", text, re.M | re.S)
       return match.group(1) if match else ""


   def table_rows(block: str) -> list[list[str]]:
       """Return the data rows of the first Markdown table in a block."""
       rows = [line for line in block.splitlines() if line.strip().startswith("|")]
       cells = [[c.strip() for c in row.strip().strip("|").split("|")] for row in rows]
       return [r for r in cells[2:] if any(r)]


   def meta(text: str, field: str) -> str:
       match = re.search(rf"^\|\s*{field}\s*\|\s*(.*?)\s*\|\s*$", text, re.M)
       return match.group(1) if match else ""


   def main() -> None:
       chapters, errors, decisions, terms = [], [], [], {}
       for path in sorted(HANDBOOK.glob("m[0-9][0-9]-*.md")):
           text = path.read_text(encoding="utf-8")
           title = re.search(r"^# (.+)$", text, re.M).group(1).strip()
           link = f"[{title}]({path.name})"
           chapters.append(f"| {link} | {meta(text, 'Status')} | {meta(text, 'Hours')} |")
           for row in table_rows(section(text, 5)):
               if re.match(r"E-M\d\d-\d+", row[0]):
                   errors.append(f"| {row[0]} | {row[1]} | {row[3] if len(row) > 3 else ''} | {link} |")
           for d_id, d_title in re.findall(r"^### (D-M\d\d-\d+) — (.+)$", section(text, 6), re.M):
               decisions.append(f"| {d_id} | {d_title.strip()} | {link} |")
           for row in table_rows(section(text, 8)):
               if len(row) >= 2 and row[0]:
                   terms.setdefault(row[0], (row[1], path.name))

       out = [HEADER, "## Chapters", "", "| Chapter | Status | Hours |", "|---|---|---|", *chapters]
       out += ["", "## Errors — every failure met while building", "",
               "| ID | Symptom | Fix | Chapter |", "|---|---|---|---|", *errors]
       out += ["", "## Decisions", "", "| ID | Decision | Chapter |", "|---|---|---|", *decisions]
       out += ["", "## Glossary", "", "| Term | Meaning | First used in |", "|---|---|---|"]
       out += [f"| {t} | {m} | [{f[:3].upper()}]({f}) |" for t, (m, f) in sorted(terms.items(), key=lambda kv: kv[0].lower())]
       (HANDBOOK / "README.md").write_text("\n".join(out) + "\n", encoding="utf-8")
       print(f"Handbook index: {len(chapters)} chapters, {len(errors)} errors, "
             f"{len(decisions)} decisions, {len(terms)} terms")


   if __name__ == "__main__":
       main()
   ```

   The lines inside `HEADER` start at column 0 in the real file (the indentation above
   comes only from this list).
7. Write the `Makefile` with the targets that exist now: `setup` (it runs
   `mkdir -p data` first, because DuckDB cannot create a file inside a missing folder),
   `build`, `test`, `handbook` (`python scripts/build_handbook_index.py`), `clean`. Start
   the Makefile with `-include .env` and `export`, so every target sees `GCP_PROJECT_ID`.
   Every other target in the brief section 3.6 is added by the milestone that first needs it.
8. `cd transform && dbt debug --target dev && dbt debug --target prod && dbt parse`.
9. `make handbook`. Expected: `Handbook index: 1 chapters, …` (the M00 chapter).

**Exam topics.** `dbt_project.yml` configurations; `require-dbt-version`; custom
schemas; targets and environments.

**Exit criteria.** `dbt debug` passes on `dev` and `prod`; `dbt parse` succeeds with zero
models; `make handbook` writes `docs/handbook/README.md` listing M00.

**Commit.** `m01-project-skeleton` → `feat: scaffold dbt project, makefile and handbook index`

**Chapter.** `docs/handbook/m01-project-skeleton.md`

**Budget.** 1.5h. **Model.** Claude Sonnet 5 · Effort Medium · Thinking on.

---

## M02 — The EL layer

**Objective.** A Python script that loads raw TPC-H into the `raw` schema with load
metadata, loads orders in date waves, and can mutate reference data on demand.

**Preconditions.** M01 merged (`git log --oneline -1` on `main` shows the M01 squash
commit).

**What it is for in the project.** dbt never extracts data: it transforms what is already
in the warehouse. This script is the "EL" in ELT. It writes the eight tables that M03
declares as dbt **sources**, and it adds the three behaviours that later milestones need
to see: `_loaded_at` for source freshness (M03), date waves for incremental and microbatch
models (M08, M09), and mutations plus deletions for snapshots with `hard_deletes` (M13).

**Pre-built and tested (2026-10-18, DuckDB 1.5.5, dbt-core 1.11.15, dbt-duckdb 1.11.0).**
`el/load_raw.py` (delivered below), `el/README.md` and the `make load` target. Verified:
first wave through 1996-12-31; second wave through 1997-06-30 inserts only the new orders;
re-running the same window inserts 0 rows; `--mutate` changes segments and balances and
deletes the 5 synthetic suppliers; a different scale factor without `--full-reset` stops
with a message; `dbt source freshness` passes on `_loaded_at`; `check` and `timestamp`
snapshots with `hard_deletes: new_record` record the mutations.

**Work.**

1. `make start M=02`.
2. `make fetch F="el/load_raw.py el/README.md"` — the two files are downloaded from the
   chat (they are too long to paste safely). The chat shows `load_raw.py` section by
   section with what each section does, its role in the project and the dbt feature it
   feeds.
3. Add the `load` target to the Makefile (exact text below) and `__pycache__/` to
   `.gitignore`.
4. Run the **first wave**: `make load THROUGH_DATE=1996-12-31`. At SF 1 it takes about
   20 seconds and prints one line per table.
5. Verify with one query (the chat gives it): 8 tables in `raw`; `max(o_orderdate)` =
   1996-12-31; `count(_loaded_at)` equals `count(*)` in every table.

`make load` target (appended at the end of the Makefile, and `load` added to `.PHONY`):

```make
load:
	$(PYTHON) el/load_raw.py $(if $(SF),--scale-factor $(SF)) $(if $(THROUGH_DATE),--through-date $(THROUGH_DATE)) $(if $(MUTATE),--mutate) $(if $(RESET),--full-reset)
```

Load semantics (brief section 3.5):
- `region`, `nation`, `part`, `supplier`, `partsupp`, `customer` are created on the first
  run; later runs keep their rows and set a new `_loaded_at` and `_batch_id`. They also
  carry `_updated_at`, which changes only when `--mutate` changes the row.
- `supplier` gets 5 synthetic suppliers (`Supplier#SYN00001` to `Supplier#SYN00005`) with
  no parts. `--mutate` deletes them. Deleting real suppliers would leave line items
  pointing at suppliers that no longer exist and break the `relationships` tests of M06
  and M10.
- `orders` and `lineitem` only grow: each run inserts the orders with order date on or
  before `--through-date` that are not loaded yet, with all their line items.

**Files.** The complete `el/load_raw.py`, as tested:

```python
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
```

The complete `el/README.md`:

````markdown
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
````

**Exam topics.** None directly. It is the substrate that makes freshness, incremental,
microbatch and snapshots demonstrable. The chat names, for each behaviour, the exam bullet
it will serve.

**Exit criteria.** `raw` has 8 tables; `orders` contains only rows through 1996-12-31;
every table has a non-null `_loaded_at`.

**Parts.** 1 — map, start, fetch and read the loader (35 min). 2 — Makefile target, first
wave, verification query (30 min). 3 — close (15 min).

**Commit.** `m02-el-layer` → `feat(el): add TPC-H loader with load metadata and date waves`

**Chapter.** `docs/handbook/m02-el-layer.md`

**Budget.** 1.5h. **Model.** Claude Sonnet 5.5 · Effort High · Thinking on.

---

## M03 — Sources, freshness, and dependency verification

**Objective.** All 8 raw tables declared as dbt sources with descriptions, freshness
policies, and one deliberate `identifier` override.

**Preconditions.** M02 merged; raw schema populated.

**Work.**

1. `models/staging/tpch/_tpch__sources.yml`: one source `tpch_raw` with `schema: raw` and
   8 tables. Rename one table at the source level with `identifier:` so the dbt-facing name
   differs from the physical name — practice Q09 tests exactly this (the `source()` call
   uses the source name and the table `name`, never the `identifier`).
2. Source-level `freshness` with `warn_after: {count: 12, period: hour}` and
   `error_after: {count: 24, period: hour}`, `loaded_at_field: _loaded_at`.
3. Override freshness on one table; **exempt one table with `freshness: null`**
   (practice Q16 and Q18).
4. Source tests: `not_null` and `unique` on primary keys, `relationships` between
   `orders` and `customer`.
5. Add `make freshness` to the Makefile. `make freshness`; then
   `make load THROUGH_DATE=1996-12-31` (same window: the six replaced tables get a new
   `_loaded_at`, the two additive ones do not change) and run it again; read the
   difference.
6. **Dependency drill** (official sample Q10): rename the physical `raw.part` table by
   hand, run `dbt build --select source:tpch_raw+`, read the failure, fix it with
   `identifier:` — not by editing model SQL. **Then undo both** (rename the table back,
   remove that `identifier:`), so later milestones read the table under its real name.

**Exam topics.** Identifying and verifying raw object dependencies; source freshness;
`freshness: null`; testing assumptions for sources; `source:` selector.

**Exit criteria.** `dbt source freshness` reports 7 tables and skips the exempted one.
`dbt test --select source:tpch_raw` passes.

**Parts.** 1 — map, `_tpch__sources.yml` and the first `make freshness` (35 min). 2 — source tests, a second load and freshness compared (25 min). 3 — dependency drill and close (30 min).

**Commit.** `m03-sources` → `feat(staging): declare tpch sources with freshness policies`

**Chapter.** `docs/handbook/m03-sources.md`

**Budget.** 1.5h. **Model.** Claude Sonnet 5.5 · Effort High · Thinking on.

---

# PHASE 2 — CORE MODELLING

## M04 — Staging layer, seeds and packages

**Objective.** Eight `stg_tpch__*` views, two reference seeds, and `dbt_utils` + `codegen`
installed and used.

**Preconditions.** M03 merged.

**Work.**

1. `packages.yml`: `dbt_utils`, `codegen`. `dbt deps`. Commit `package-lock.yml`.
2. Scaffold with `dbt run-operation generate_base_model` (codegen), then hand-edit. Each
   staging model: one `source` CTE, one `renamed` CTE, `select * from renamed`. Rename
   TPC-H prefixes (`o_orderkey` → `order_id`, `l_extendedprice` → `extended_price_usd`).
   Cast types explicitly. No joins, no business logic.
3. `_staging__models.yml`: description per model and per column, generic tests on keys.
   Folder configured `+materialized: view`.
4. Two hand-written seeds: `ref_region_targets.csv` (annual revenue target per region)
   and `ref_sla_thresholds.csv` (acceptable late-delivery rate by ship mode). Seed
   configs: `+schema`, `+quote_columns`, explicit `+column_types` on one seed.
   `_seeds__properties.yml` with descriptions and tests.
5. **Override a package config from your own `dbt_project.yml`** under the package's
   namespace — practice Q08 and Q50.
6. Inspect without building: `dbt show --select stg_tpch__orders --limit 5`,
   `dbt ls --select staging`, `dbt compile --select stg_tpch__orders` and open
   `target/compiled/`.

**Exam topics.** Clean DAGs; `dbt seed`; seed configs; packages and overriding package
configs; `dbt show`/`compile`/`ls`/`build`; generic tests; `ref`/`source` dependency
inference (practice Q31, Q36, Q51; official sample Q4).

**Exit criteria.** `dbt build --select staging resource_type:seed` → 8 views, 2 seeds and
all tests PASS.

**Parts.** 1 — map, packages and the eight staging models, built (50 min). 2 — seeds, seed configs and the package config override (35 min). 3 — `dbt show`, `compile`, `ls`, then close (35 min).

**Commit.** `m04-staging-seeds-packages` → `feat(staging): add staging models, reference seeds and packages`

**Chapter.** `docs/handbook/m04-staging-seeds-packages.md`

**Budget.** 2h. **Model.** Claude Sonnet 5.5 · Effort High · Thinking on.

---

## M05 — Intermediate layer and dimensions

**Objective.** Two `int_` models holding the reusable business logic, and three conformed
dimensions with surrogate keys.

**Preconditions.** M04 merged.

**Work.**

1. `macros/net_revenue.sql`: `extended_price * (1 - discount) * (1 + tax)` — the revenue
   formula exists in exactly one place.
2. `int_order_lines_enriched` — line items joined to orders, customers, nations,
   regions, parts, suppliers; calls the macro.
3. `int_delivery_performance` — per line item: `days_late = receipt_date - commit_date`,
   `is_late`, bucketed lateness.
4. Materialize the intermediate folder `ephemeral`; build a model that uses it; open
   `target/compiled/` and see the CTE inlined. Switch one model to `table` and compare.
   Decision `D-M05-1`: when ephemeral is and is not right.
5. `dim_customers`, `dim_suppliers`, `dim_parts` in `marts/core/`, `+materialized: table`,
   surrogate keys via `dbt_utils.generate_surrogate_key`, `unique` + `not_null` on each key.
6. Doc blocks: `models/marts/_marts__docs.md` with `{% docs %}` for `net_revenue` and
   `market_segment`, referenced with `{{ doc('...') }}`.

**Exam topics.** Modularity and DRY (practice Q40, Q57); ephemeral; macros; clean DAGs;
documentation; packages.

**Exit criteria.** `dbt build --select intermediate+ marts.core` passes; the compiled SQL of
a downstream model visibly inlines the ephemeral CTE.

**Parts.** 1 — map, macro, the two `int_` models and the inlined ephemeral CTE (45 min). 2 — three dimensions and doc blocks (30 min). 3 — close (15 min).

**Commit.** `m05-intermediate-dimensions` → `feat(marts): add intermediate logic and conformed dimensions`

**Chapter.** `docs/handbook/m05-intermediate-dimensions.md`

**Budget.** 1.5h. **Model.** Claude Sonnet 5.5 · Effort High · Thinking on.

---

## M06 — Fact models

**Objective.** Two facts and one aggregate at explicit, documented, tested grains.

**Preconditions.** M05 merged.

**Work.**

1. `fct_order_lines` — grain: one row per order line (`table` for now; incremental in M08).
2. `fct_orders` — grain: one row per order.
3. `agg_monthly_revenue` in `marts/finance/` — grain: month × region × market segment;
   joins the `ref_region_targets` seed for attainment vs target.
4. The grain is the **first line** of each description. Singular test
   `tests/assert_fct_order_lines_grain.sql` returns rows if a key appears twice.
5. `relationships` tests from facts to every dimension.

**Exam topics.** Clean DAGs; singular tests; `relationships`; seeds in the DAG;
`dbt build`.

**Exit criteria.** `dbt build` (whole project) passes. `fct_order_lines` row count equals
the `lineitem` source count for the loaded window.

**Parts.** 1 — map, two facts and the aggregate (45 min). 2 — grain test, `relationships` tests, full build (30 min). 3 — close (15 min).

**Commit.** `m06-facts` → `feat(marts): add fct_order_lines, fct_orders and monthly revenue`

**Chapter.** `docs/handbook/m06-facts.md`

**Budget.** 1.5h. **Model.** Claude Sonnet 5.5 · Effort High · Thinking on.

> **Audit A** — after closing M06, in a separate chat (0.25 h): `PHASE AUDIT.` for M00–M06.
> Output defined in the brief section 2.4.

---

# PHASE 3 — MATERIALIZATIONS

## M07 — Materializations, config precedence, and hooks

**Objective.** Measured understanding of view/table/ephemeral and of which config wins
when three places disagree; run hooks writing an audit table.

**Preconditions.** M06 merged.

**Work.**

1. Build `agg_monthly_revenue` as `view`, then `table`, then `ephemeral`; after each, read
   `target/run/` for the DDL dbt emitted and note build time. Practice Q17.
2. **Precedence lab.** Set `materialized` in `dbt_project.yml`, in the model's YAML
   `config:` and in the model's `{{ config() }}` with three different values. Predict,
   run, record the order as `D-M07-1`. Practice Q64.
3. Reproduce the "unused configuration paths" warning with a hyphen in a folder key, read
   it, fix it. Practice Q25.
4. Hooks: `on-run-start` and `on-run-end` writing to an audit table, and one model
   `post-hook`. Wrap every hook that writes rows in `{% if target.type == 'duckdb' %}` —
   an `insert` is DML, and the BigQuery sandbox (M12) rejects DML. Practice Q19.

**Exam topics.** Core materializations; `dbt_project.yml` configurations; config
precedence; hooks; YAML config warnings.

**Exit criteria.** The precedence order is written in the chapter and matches what ran.
The audit table has one row per run.

**Parts.** 1 — map and the view/table/ephemeral comparison (30 min). 2 — precedence lab: predict, then run (25 min). 3 — hooks, the warning reproduced, close (35 min).

**Commit.** `m07-materializations` → `feat: add run hooks and document materialization tradeoffs`

**Chapter.** `docs/handbook/m07-materializations.md`

**Budget.** 1.5h. **Model.** Claude Sonnet 5.5 · Effort High · Thinking on.

---

## M08 — Incremental models

**Objective.** `fct_order_lines` incremental, with `append`, `delete+insert` and `merge`
tried and one chosen for a written reason.

**Preconditions.** M07 merged.

**Work.**

1. `materialized: 'incremental'`, `unique_key`, and the `{% if is_incremental() %}`
   filter against `max(order_date)` in `{{ this }}`.
2. Second EL wave: `make load THROUGH_DATE=1997-06-30`. Build. Only new rows are
   processed. Read `target/run/` for the emitted statements.
3. Try `append`, `delete+insert`, `merge`; time each; decide — `D-M08-1` (official
   sample Q2).
4. Add a column and exercise `on_schema_change`: `fail`, `append_new_columns`,
   `sync_all_columns`.
5. `dbt run --select fct_order_lines --full-refresh`; observe `is_incremental()` false
   (practice Q49).

**Exam topics.** Selecting the optimal incremental strategy; `is_incremental()`;
`unique_key`; `on_schema_change`; `--full-refresh`; `{{ this }}`.

**Exit criteria.** The second wave processes strictly fewer rows than the first, and the
row count equals a full refresh exactly.

**Parts.** 1 — map, incremental model and the second load wave (45 min). 2 — the three strategies timed (35 min). 3 — `on_schema_change`, `--full-refresh`, close (40 min).

**Commit.** `m08-incremental` → `feat(marts): make fct_order_lines incremental`

**Chapter.** `docs/handbook/m08-incremental.md`

**Budget.** 2h. **Model.** Claude Opus 5.5 · Effort High · Thinking on.

---

## M09 — Microbatch

**Objective.** `fct_shipments` built with the `microbatch` strategy and backfilled by an
explicit time window.

**Preconditions.** M08 merged.

**Work.**

1. Declare `event_time` on the inputs (the source table and `stg_tpch__line_items`) —
   microbatch filters its inputs by `event_time`, not only the model.
2. `fct_shipments`: `incremental_strategy: 'microbatch'`, `event_time: ship_date`,
   `batch_size: month`, `lookback: 1`, `begin: '1992-01-01'`.
3. First build: one query per month from `begin`. Read the log.
4. **The trap, verified on 2026-09-29:** a later plain `dbt run` processes only the
   batches around **today** (current batch + `lookback`), and TPC-H dates end in 1998, so
   it processes nothing useful. Historical windows are rebuilt explicitly:
   `dbt run --select fct_shipments --event-time-start 1995-01-01 --event-time-end 1995-04-01`.
5. Force one batch to fail and see the others succeed. `D-M09-1`: microbatch versus the
   `is_incremental()` pattern.

**Exam topics.** Advanced materializations — microbatch; `event_time`; `batch_size`;
`lookback`; `begin`; `--event-time-start/--event-time-end`.

**Exit criteria.** The log shows one batch per month; the targeted backfill rewrites
exactly three months.

**Parts.** 1 — map, `event_time` and the first microbatch build (40 min). 2 — explicit backfill window and a failing batch (30 min). 3 — close (20 min).

**Commit.** `m09-microbatch` → `feat(marts): add fct_shipments using microbatch`

**Chapter.** `docs/handbook/m09-microbatch.md`

**Budget.** 1.5h. **Model.** Claude Opus 5.5 · Effort High · Thinking on.

---

# PHASE 4 — TESTING

## M10 — Every test type

**Objective.** Generic, package, singular, custom generic and unit tests in place, with
severity, filtering and selection exercised.

**Preconditions.** M09 merged.

**Work.**

1. **Generic:** complete `unique`, `not_null`, `accepted_values`, `relationships`
   (practice Q23, Q58). **From a package:** `dbt_utils.expression_is_true`,
   `dbt_utils.accepted_range`.
2. **Singular:** `assert_no_negative_revenue.sql`, `assert_order_totals_reconcile.sql`.
   A singular test fails when its query returns rows (practice Q13).
3. **Custom generic:** `tests/generic/not_negative.sql` as a
   `{% test not_negative(model, column_name) %}` block (practice Q39; practice Q42's key
   says `{% macro %}` — the docs say `{% test %}`).
4. **Configs:** `where:` (official sample Q1); `severity: warn`; `warn_if`/`error_if`
   (official sample Q9); `store_failures: true` on one test, then query the failures table.
5. **Selection:** `test_type:singular`, `test_type:generic`, `test_type:unit` (practice
   Q07/Q45); `--indirect-selection` `eager`/`cautious`/`buildable`/`empty` (practice Q38)
   and compare node counts.
6. **Unit tests** on `int_delivery_performance` (on-time / late / early boundaries) and
   on the net revenue logic (zero discount, max discount, null tax). Break the logic on
   purpose and watch the unit test catch it before any data is touched. `D-M10-1`: data
   test versus unit test.
7. Break a model and watch `dbt build` skip its children.

**Exam topics.** All of section 05; severity; `where`; `store_failures`;
`--indirect-selection`; `test_type:` selectors; unit tests; failure propagation.

**Exit criteria.** `dbt test` runs 30+ tests; the `--indirect-selection` variants give
different node counts; a failures table exists; `dbt test --select test_type:unit`
passes and caught the deliberate break.

**Parts.** 1 — map, generic, package, singular and custom generic tests (45 min). 2 — `where`, `severity`, `store_failures`, selectors (40 min). 3 — unit tests, failure propagation, close (35 min).

**Commit.** `m10-testing` → `test: add full test taxonomy, severity thresholds and unit tests`

**Chapter.** `docs/handbook/m10-testing.md`

**Budget.** 2h. **Model.** Claude Sonnet 5.5 · Effort High · Thinking on.

---

# PHASE 5 — GOVERNANCE AND CLOUD

## M11 — Contracts, constraints, versions, groups and access

**Objective.** Enforced contracts on the marts, a versioned `dim_customers` with a
deprecation date, and model access enforced by groups.

**Preconditions.** M10 merged.

**Work.**

1. `contract: {enforced: true}` on all `dim_*` and `fct_*` (except the microbatch
   `fct_shipments`), `data_type` on every column, explicit casts in SQL (a contract compares
   types literally).
2. `constraints:` — `primary_key`, `not_null` and a `check` (`net_revenue >= 0`). Then
   add one `foreign_key` from `fct_orders` to `dim_customers`, run `dbt build` **twice**,
   and read the second run's failure: `Dependency Error: Cannot alter entry
   "dim_customers" because there are entries that depend on it` (verified 2026-09-29 —
   DuckDB enforces the key, so the dimension can no longer be replaced). Remove the
   foreign key; the `relationships` tests keep checking it. Record as `E-M11-1` and
   `D-M11-1`.
3. Break it on purpose: rename a column in SQL only → read the `missing in definition` /
   `missing in contract` table (practice Q62). Add a `check` to a column without
   `data_type` → parsing error (official sample Q8).
4. `insert` a violating row in DuckDB and see the engine reject it (verified on
   2026-09-29: `Constraint Error: NOT NULL constraint failed`).
5. Contracts do not apply to ephemeral models, Python models, snapshots or seeds
   (practice Q33).
6. **Versions:** `dim_customers` v2 (two columns added, one renamed), `latest_version: 2`,
   `ref('dim_customers', v=1)` pinned in one place and unpinned in another,
   `deprecation_date` on v1 → read the warning (practice Q24).
7. **Groups and access:** `groups:` `core` and `finance` with owners. Staging and
   intermediate belong to group `core` and are `private` (a private model must belong to a
   group); dimensions `protected`; `fct_order_lines`, `fct_orders` and
   `agg_monthly_revenue` `public`. Rule that follows: `finance` models may `ref()` only
   `public` or `protected` models. `ref()` a private staging model from a `finance` model →
   read the error, revert (practice Q03, Q29).

**Exam topics.** Contracts; constraints at platform level; model versions and
deprecation; groups and access.

**Exit criteria.** `dbt build --select marts` passes with contracts on; the manual
violating `insert` fails; `dbt build` warns for v1; the cross-group `ref()` fails to
compile.

**Parts.** 1 — map, contracts, constraints and the foreign-key lesson (45 min). 2 — model versions and deprecation (30 min). 3 — groups and access, close (45 min).

**Commit.** `m11-governance` → `feat(governance): enforce contracts, version dim_customers, add access`

**Chapter.** `docs/handbook/m11-governance.md`

**Budget.** 2h. **Model.** Claude Sonnet 5.5 · Effort High · Thinking on.

---

## M12 — BigQuery target and grants

**Objective.** The same project builds on BigQuery, and dbt applies real IAM grants there
through the `grants` config.

**Preconditions.** M11 merged. `D-M00-1` says the sandbox accepted `grant`. (If it did
not: this milestone runs the grants part on PostgreSQL in Docker — charter R2.)

**Work.**

1. Install the Google Cloud CLI in Ubuntu and run `gcloud auth application-default login`
   (browser login; OAuth, no key file).
2. Add the `bq` output to `transform/profiles.yml`:
   ```yaml
   bq:
     type: bigquery
     method: oauth
     database: "{{ env_var('GCP_PROJECT_ID', 'no-gcp-project') }}"
     schema: bq
     location: US
     threads: 4
   ```
   `dbt debug --target bq`.
3. `el/load_bigquery.py`: generates TPC-H at **SF 0.1** in an in-memory DuckDB, adds
   `_loaded_at`/`_batch_id`, and uploads each table to the `raw` dataset with BigQuery
   **load jobs** (free, and not DML). Add `make bq-load`. SF 0.1 because the sandbox's
   10 GiB of storage is a lifetime limit that deletions do not refund.
4. Grants in `dbt_project.yml`:
   - project level: `+grants: {roles/bigquery.dataViewer: ["serviceAccount:dbt-reporter@{{ env_var('GCP_PROJECT_ID', 'no-gcp-project') }}.iam.gserviceaccount.com"]}` — the default matters: `dbt_project.yml` is rendered on every parse, so without it CI and a fresh clone would fail where `GCP_PROJECT_ID` is not set
   - `marts/finance` folder: `+grants: {+roles/bigquery.dataViewer: ["serviceAccount:dbt-finance@..."]}` — the `+` inside the key **adds** to the inherited grantees
   - one model without the inner `+` — it **replaces** them.
   On DuckDB the same config is ignored with the debug message "Grants for relations are
   not supported by DuckDB" (verified 2026-09-29), so it lives in the project once.
5. Add `make bq-build` to the Makefile and run it: `dbt build --target bq --full-refresh --exclude fct_shipments dim_customers_history resource_type:snapshot config.language:python`.
   `--full-refresh` makes every incremental model a `create table as select` (DDL, allowed).
   Excluded: `fct_shipments` (microbatch writes batches with DML), snapshots and
   `dim_customers_history` (DML), and Python models (on BigQuery they need Dataproc, which
   is not free). The last three do not exist yet — they arrive in M13 — so today the
   exclusion matches nothing and dbt may say so; it is written now so the command never
   changes. Hooks that write already skip non-DuckDB targets.
6. Verify the grants landed:
   ```sql
   select object_name, privilege_type, grantee
   from `region-us`.INFORMATION_SCHEMA.OBJECT_PRIVILEGES
   where object_schema = 'bq_marts' order by 1, 3;
   ```
   Predict the matrix before running it (practice Q12, Q28).
7. `D-M12-1`: what ports to BigQuery and what does not, and why (DML in the sandbox;
   60-day table expiry; lifetime storage).

**Exam topics.** `grants` config; inheritance with `+`; multi-target projects.

**Exit criteria.** `make bq-build` ends with 0 errors; the `OBJECT_PRIVILEGES` query shows
exactly the grantees the YAML declares, including the `+` addition and the one override.

**Parts.** 1 — map, Google Cloud CLI login and the `bq` target (40 min). 2 — BigQuery load and build (40 min). 3 — grants verified, close (40 min).

**Commit.** `m12-bigquery-grants` → `feat(governance): add BigQuery target and IAM grants`

**Chapter.** `docs/handbook/m12-bigquery-grants.md`

**Budget.** 2h. **Model.** Claude Opus 5.5 · Effort High · Thinking on.

---

# PHASE 6 — HISTORY AND PYTHON

## M13 — Snapshots and Python models

**Objective.** Two YAML snapshots with visible history produced by real source mutation,
and two Python models doing work that is awkward in SQL.

**Preconditions.** M12 merged.

**Work.**

1. `snapshots/_snapshots.yml` in the 1.9+ YAML format: `customers_snapshot` (`check`,
   `check_cols: [c_mktsegment]`) and `suppliers_snapshot` (`timestamp`, `updated_at: _updated_at`,
   `hard_deletes: new_record`). `_updated_at` changes only when `--mutate` changes a row
   (M02), so the `timestamp` strategy records real changes and nothing else.
2. `dbt snapshot`; inspect `dbt_valid_from`, `dbt_valid_to`, `dbt_scd_id`.
3. `make load MUTATE=1`, `dbt snapshot` again → two rows for a changed customer; a
   deleted synthetic supplier recorded by `hard_deletes`
   (a row with `dbt_is_deleted = True`; verified on 2026-10-18). Build `dim_customers_history` on top.
4. `marts/finance/cust_abc_classification.py` (Pareto classes at 80/95/100% of revenue)
   and `marts/finance/revenue_anomalies.py` (rolling 28-day mean and standard deviation,
   flag beyond 2.5σ). Contract: `def model(dbt, session)`, `dbt.config(...)`,
   `dbt.ref()` returns a DuckDB relation, return a DataFrame.
5. Python models cannot be `ephemeral` (practice Q46) and cannot carry contracts. Add a
   data test on each Python output.

**Exam topics.** Creating snapshots in YAML; `check` versus `timestamp`; `hard_deletes`;
`dbt snapshot`; creating Python models.

**Exit criteria.** One customer has 2+ snapshot rows with exactly one where
`dbt_valid_to is null`; `dbt build --select config.language:python` builds both models;
ABC classes cover 100% of customers.

**Parts.** 1 — map, two snapshots, a mutation and the recorded history (50 min). 2 — the two Python models (45 min). 3 — close (25 min).

**Commit.** `m13-snapshots-python` → `feat: add SCD2 snapshots and python models`

**Chapter.** `docs/handbook/m13-snapshots-python.md`

**Budget.** 2h. **Model.** Claude Sonnet 5.5 · Effort High · Thinking on.

---

# PHASE 7 — STATE, CI, DEBUGGING

> The highest-yield phase for the exam relative to its size. Do not compress it.

## M14 — State, defer, clone, retry

**Objective.** A production manifest on disk and fluency in the four state-based
operations.

**Preconditions.** M13 merged.

**Work.**

1. From `transform/`: `dbt build --target prod`, then `dbt source freshness --target
   prod`, then copy `target/manifest.json` **and** `target/sources.json` to
   `../prod-artifacts/` (the folder is at the repo root; dbt runs from `transform/`, so
   every `--state` below is `../prod-artifacts`).
2. **State selection:** modify one model; `dbt ls --select state:modified --state
   ../prod-artifacts`; then `state:new`, `state:modified.body`, `state:modified.configs`,
   `state:modified+`, `+state:modified`, `@state:modified`, and a union with a config
   selector (practice Q27).
3. **Defer:** `dbt build --select state:modified --defer --state ../prod-artifacts` on
   `dev`; the compiled SQL points unmodified refs at `prod_*` (practice Q15, Q63).
4. **Clone:** `dbt clone --select marts --state ../prod-artifacts --target dev`. `D-M14-1`:
   clone creates objects, defer only redirects refs (practice Q06, Q35, Q48).
5. **Retry:** break one model, `dbt build` (see `SKIP`), fix, `dbt retry` — it resumes
   from `run_results.json` without rebuilding successes (practice Q61; practice Q47's key
   says `manifest.json` — the docs say `run_results.json`).
6. `make load` (new rows arrive), `dbt source freshness`, then
   `dbt build --select "source_status:fresher+" --state ../prod-artifacts` — it compares
   the new `target/sources.json` with the one saved in step 1 (practice Q02: a freshness
   block **and** a prior freshness run).

**Exam topics.** All of section 07; `dbt clone`; `--defer`; `dbt retry`; state
selectors; `source_status:`; artifacts.

**Exit criteria.** A deferred build of one modified model compiles refs pointing at
`prod_*`. `dbt retry` resumes without rebuilding successful nodes.

**Parts.** 1 — map, production artifacts and state selectors (40 min). 2 — `--defer` and `dbt clone` (40 min). 3 — `dbt retry`, `source_status:fresher+`, close (40 min).

**Commit.** `m14-state-operations` → `feat(ci): add prod artifacts and state workflows`

**Chapter.** `docs/handbook/m14-state-operations.md`

**Budget.** 2h. **Model.** Claude Opus 5.5 · Effort High · Thinking on.

---

## M15 — Slim CI with `--empty` and `--sample`

**Objective.** A GitHub Actions workflow that builds only what changed on every PR.

**Preconditions.** M14 merged.

**Work.**

1. `.github/workflows/ci.yml`, on pull request. The runner starts empty, so it builds its
   own "production" first — this is standard Slim CI:
   1. check out the PR, and check out `main` into a second folder;
   2. install; generate TPC-H at SF 0.01 (`python el/load_raw.py --scale-factor 0.01`);
   3. in the `main` copy: `dbt build --target prod` → its `target/manifest.json` is the
      state to compare against, and the `prod_*` schemas exist for deferral;
   4. in the PR copy: `dbt build --select state:modified+ --defer --state <main copy>/transform/target`.
   Both copies point `DUCKDB_PATH` at the same absolute file.
2. A fast job with `dbt build --empty`: structure validated with zero rows. Observe
   official sample Q7: a `unique` test passes on an empty table even with duplicates in
   the source — expected behaviour.
3. A job with `--sample` over an explicit window:
   `dbt build --sample="{'start': '1998-07-01', 'end': '1998-08-01'}"`. A relative window
   such as `"30 days"` counts back from today, and TPC-H ends in 1998, so it would select
   nothing (verified 2026-09-29: the explicit window compiles to
   `where order_date >= '1998-07-01' and order_date < '1998-08-01'` on every input with
   `event_time`).
4. Open a PR with a deliberate break; CI fails; fix; CI passes.
5. Branch protection on `main` requiring CI (free on a public repo).
6. Add the CI status badge to the top of the README:
   `[![CI](https://github.com/PCoronelPeris/dbt-wholesale-analytics/actions/workflows/ci.yml/badge.svg)](https://github.com/PCoronelPeris/dbt-wholesale-analytics/actions)`.

**Exam topics.** `--empty`; `--sample`; state selection in CI; developing and testing a
fix before merging; git branching and PRs (official sample Q3; practice Q01, Q22, Q26,
Q30).

**Exit criteria.** A PR touching one model builds only that model and its children. The
`--empty` job finishes in under a minute.

**Parts.** 1 — map, the workflow file and the first PR (50 min). 2 — a deliberate break, the fix, branch protection (40 min). 3 — close (30 min).

**Commit.** `m15-slim-ci` → `ci: add slim CI with state deferral, --empty and --sample`

**Chapter.** `docs/handbook/m15-slim-ci.md`

**Budget.** 2h. **Model.** Claude Opus 5.5 · Effort High · Thinking on.

---

## M16 — The debugging lab and flags

**Objective.** Seven deliberate breakages, each recorded with its verbatim error, cause
and fix as `E-M16-1` … `E-M16-7`.

**Preconditions.** M15 merged.

**Work.** On a throwaway branch, break, read, fix, record:

1. `ref` to a non-existent model → `depends on a node named 'X' which was not found`
   (practice Q56).
2. YAML indentation → `mapping values are not allowed in this context` (practice Q05).
3. Test config nested one level too deep → `Did not find matching node for patch`
   (practice Q14).
4. Nested Jinja braces `{{ source({{ env_var('input') }}, 'table') }}` →
   `expected token ':', got '}'` (practice Q65).
5. Jinja loop over an undefined variable → silently empty SQL, found in
   `target/compiled/` (practice Q59).
6. `--fail-fast` with 2 threads: predict which models complete (practice Q10, Q54).
7. **Flags:** fill the `flags:` block; `--warn-error` and `--warn-error-options` turn a
   warning into an error. Use them on the command line; do not leave `warn_error: true`
   in the permanent `flags:` block — other targets emit harmless warnings (for example, a
   `check` constraint that BigQuery does not enforce) that would then fail the build. The debugging order of practice Q20: log → error → isolate one
   model → run it with its children.

**Exam topics.** All of sections 03 and 04; flags; compiled code; `.yml` errors; DAG
failure points.

**Exit criteria.** The chapter's "What went wrong" table has seven `E-M16-n` rows, each
with the verbatim error, the cause in one sentence, and the fix; `make handbook` lists them.

**Parts.** 1 — map and breakages 1 to 4 (40 min). 2 — breakages 5 to 7 and flags (30 min). 3 — close (20 min).

**Commit.** `m16-debugging-lab` → `docs: catalogue deliberate failures and fixes`

**Chapter.** `docs/handbook/m16-debugging-lab.md`

**Budget.** 1.5h. **Model.** Claude Sonnet 5.5 · Effort High · Thinking on.

> **Audit B** — after closing M16, in a separate chat (0.25 h): `PHASE AUDIT.` for
> M07–M16, including a check that every row of the charter section 9 matrix has been run.
> Output defined in the brief section 2.4.

---

# PHASE 8 — PUBLISH

## M17 — Exposures and the docs site

**Objective.** Two exposures in the DAG and the dbt documentation site published.

**Preconditions.** M16 merged.

**Work.**

1. Complete descriptions on every model and non-obvious column (practice Q34 orders the
   YAML keys).
2. `models/marts/_marts__exposures.yml`: `revenue_dashboard` (type `dashboard`, the Data
   Studio report built in M18 — URL placeholder until then) and `anomaly_review` (type
   `analysis`), each with `owner`, `maturity`, `url`, `depends_on`.
3. `dbt ls --select +exposure:revenue_dashboard` (practice Q43).
4. `dbt docs generate`; read `catalog.json` versus `manifest.json` — which facts come from
   the warehouse, which from YAML, which from SQL (practice Q11).
5. Add `make docs` to the Makefile. `.github/workflows/docs.yml` publishes the site to
   GitHub Pages on merge to `main`.

**Exam topics.** Exposures; `dbt docs`; documentation sources; `exposure:` selector.

**Exit criteria.** The docs site is live at a public URL; both exposures appear in the
lineage graph with correct upstream nodes.

**Parts.** 1 — map, descriptions and the two exposures (40 min). 2 — `dbt docs generate` and the Pages workflow (30 min). 3 — close (20 min).

**Commit.** `m17-exposures-docs` → `docs: add exposures and publish the docs site`

**Chapter.** `docs/handbook/m17-exposures-docs.md`

**Budget.** 1.5h. **Model.** Claude Sonnet 5.5 · Effort High · Thinking on.

---

## M18 — Data Studio dashboard and final README

**Objective.** A public, view-only dashboard on the BigQuery marts, and a README a
stranger reads in five minutes. **Cut to after the exam if behind schedule.**

**Preconditions.** M17 merged; `make bq-build` run within the last 60 days (sandbox
tables expire after 60 days).

**Work.**

1. In **Data Studio** (Google's free BI tool, called Looker Studio from 2022 to April 2026;
   `lookerstudio.google.com`), connect the BigQuery tables `bq_marts.agg_monthly_revenue`
   and `bq_marts.fct_order_lines`.
   Three charts: revenue by month, revenue vs target by region, late-delivery rate by ship
   mode. Share as "anyone with the link can view".
2. Put the report URL in the `revenue_dashboard` exposure; save a screenshot to
   `docs/assets/dashboard.png` (the live report stops working when sandbox tables expire;
   the screenshot does not).
3. Rewrite the README: problem → architecture → how to run → what is in each layer →
   practices table, each row linking to the proving file and checked only if merged →
   links to docs site, dashboard and handbook → "what I would do differently at production
   scale" → copyright.
4. Add `make verify` (clean rebuild from scratch: `make clean && make load && make build`)
   and time it. Paste section 10 of the private `~/projects/_contexto-dbt/WALKTHROUGH.md` into
   the chat (the chat cannot read that file); run each command it lists and replace every
   `{{FILL:…}}` in that file with the real value.
5. Pre-publish check on the whole repo.

**Exam topics.** None. Portfolio only.

**Exit criteria.** The dashboard opens in a private browser window without login; the
README links all resolve;
`grep -cE "\{\{FILL:[A-Z0-9_]+\}\}" ~/projects/_contexto-dbt/WALKTHROUGH.md` prints `0`;
the pre-publish check prints two `OK` lines.

**Parts.** 1 — map and the dashboard (40 min). 2 — README rewrite and `make verify` (35 min). 3 — close (15 min).

**Commit.** `m18-dashboard-readme` → `docs: add Data Studio dashboard and final README`

**Chapter.** `docs/handbook/m18-dashboard-readme.md`

**Budget.** 1.5h. **Model.** Claude Sonnet 5.5 · Effort High · Thinking on.

---

## Appendix A — Session ledger

Budgets in real hours (section 0.3). Actual hours live in one place: each
`PROJECT_LOG.md` entry ("Hours used so far"). The phase audits fill the third column.

| Milestone | Budget | Actual |
|---|---|---|
| M00 | 1.5 (old estimate) | 4.0 |
| M01 | 1.5 (old estimate) | 4.0 |
| M02 | 1.5 |  |
| M03 | 1.5 |  |
| M04 | 2.0 |  |
| M05 | 1.5 |  |
| M06 | 1.5 |  |
| Audit A | 0.25 |  |
| M07 | 1.5 |  |
| M08 | 2.0 |  |
| M09 | 1.5 |  |
| M10 | 2.0 |  |
| M11 | 2.0 |  |
| M12 | 2.0 |  |
| M13 | 2.0 |  |
| M14 | 2.0 |  |
| M15 | 2.0 |  |
| M16 | 1.5 |  |
| Audit B | 0.25 |  |
| M17 | 1.5 |  |
| M18 | 1.5 |  |
| **Total** | **38.0** (8.0 spent + 30.0) | **cap: 40** |

## Appendix B — Exam-week plan (the five days before the exam, outside the 40 h)

| Day | Activity |
|---|---|
| 1 | Re-read the official study guide outline. For every bullet, say which chapter covered it; open that chapter's "Check yourself". A bullet you cannot answer is a gap. |
| 2 | The 10 official sample questions + the 65-question practice set, untimed, writing why each distractor is wrong. |
| 3 | Reference pages: node selection syntax, `dbt_project.yml`, incremental strategies, test configs. Then the handbook's error index. |
| 4 | One full timed simulation: 65 questions in 120 minutes. |
| 5 | Review only what you got wrong. Rest before the exam. |

**About the practice set.** A third-party dump, not dbt Labs material. Several answer keys
contradict the dbt documentation — at least Q28 (a `public` role that is never granted),
Q42 (generic tests are `{% test %}` blocks, not `{% macro %}`), Q47 (`dbt retry` reads
`run_results.json`, not `manifest.json`) and Q53 (a `target-path` setting does not decide
materialization). Use it to practise reasoning; verify every key against the docs.

**About the exam format** (official study guide, 1.11): multiple choice, fill-in-the-blank,
matching, hotspot, build list, and DOMC (options appear one at a time; answer yes/no to
each). Some questions are unscored. 65 questions, 2 hours, 65% to pass. Reschedule or
cancel on Talview without penalty up to 24 hours before the exam.
