# PROJECT LOG — `dbt-wholesale-analytics`

> **The truth about what currently exists.** `PROJECT_CHARTER.md` and `MILESTONES.md`
> are the plan; this file is reality. When they disagree, this file wins.
> The explanation of *how* and *why* lives in the handbook (`docs/handbook/`); this file
> keeps only facts: state, hours, deviations.
>
> Lives in Project knowledge and, from M00 on, in the repo at `docs/PROJECT_LOG.md`.
> The "Current state" block is **replaced** at every close. Entries are **appended** at
> the end, oldest first. After editing, re-upload it to Project knowledge.

---

## Current state — replace this block every session

| Field | Value |
|---|---|
| Last milestone completed | **M03 — Sources, freshness, and dependency verification** (2026-11-06) |
| Next milestone | **M04 — Staging layer, seeds and packages** |
| Hours used | 12.4 of 40 (cap) · budgeted ahead: 26.5 h for M04–M18 + 0.5 h of audits · planned total 39.4 h · slack 0.6 h |
| Schedule status | same 19 milestones, M04–M18 at 1.5–2 h each; stop rule at 1.5× each budget; a final-revision milestone (proposed M19, 1.5 h) would bring the plan to 40.9 h, over the cap, and is decided at Audit A |
| Repo exists on GitHub | yes · `PCoronelPeris/dbt-wholesale-analytics` · public · no licence · 4 commits on `main` (initial commit, M01, M02 and M03 squash merges) |
| DuckDB file exists | yes · `data/warehouse.duckdb` · schema `raw` with 8 tables · local only, git-ignored |
| BigQuery sandbox project | created · sandbox, no billing · ID in local `.env` only (variable `GCP_PROJECT_ID`) · service accounts `dbt-reporter`, `dbt-finance` (no keys, no roles) |
| Grants engine | **BigQuery** — the sandbox accepted `GRANT` (D-M00-1); R2 retired |
| Raw schema loaded through date | **1996-12-31** · scale factor 1 · 1,138,594 orders, 4,556,169 line items · loaded again with the same window in M03 (the six reference tables re-stamped at 2026-11-06 19:26:32 UTC; `orders` and `lineitem` still at 17:38:51 UTC) |
| dbt project | `transform/` · dbt-core 1.11.15 · python 3.12.3 · `dbt debug` passes on `dev` and `prod` · 0 models · 1 source (`tpch_raw`, 8 tables) · 18 data tests · schemas render as `{target.name}_{custom}` |
| Handbook chapters | 4 (M00, M01, M02, M03) |
| Plan documents | charter v4, milestones v4, brief v4 (2026-10-18) |
| Decisions | D1 exam date kept out of the plan documents (2026-10-18) · D2 every milestone 1.5–2 h of real time · D3 exposure tier A (default) · D4 build-side files grouped in one folder at the final revision (2026-11-05) · D5 explanations start from the whole map, in plain language, with the step count of each part (2026-11-05) · D-M03-1 to D-M03-4 in the M03 chapter |
| Open blockers | none |

**Commands to restore working state at the start of the next session:**

```bash
# Open Ubuntu from the Windows Start menu (or run `wsl ~` in PowerShell), then:
cd ~/projects/dbt-wholesale-analytics
source .venv/bin/activate
make start M=04   # expect: "Ready: M04 — Staging layer, seeds and packages" and "Branch: m04-staging-seeds-packages"
```

---

## Entry template

Copy this block for each new entry and append it at the end of the file. Details,
errors and reasoning go in the handbook chapter, not here.

````markdown
## M{NN} — {title}
**Date:** YYYY-MM-DD · **Estimated:** Xh · **Actual:** Xh · **Hours used so far:** X of 40
**Chapter:** `docs/handbook/m{NN}-{slug}.md`

**Now exists that did not before**
- files:
- schemas / tables:
- dbt resources:

**Deviations from the milestone as written**
- (none) | what changed and why → D-M{NN}-n

**Binding for later milestones**
- (none) | decision → which milestones it affects

**Registry changes**
- (none) | what changed in AI_OPERATING_BRIEF.md Part 3

**Left open**
- (nothing) | item → owner (me / M{NN})

**Commit**
`m{NN}-{slug}` → `type(scope): summary`
````

---

## Entries

## DOCS-REVISION — 2026-09-21

**Why.** Audit of the v1 documents before M00, while writing the generic execution method.

**Found and fixed**
- `MILESTONES.md` claimed 43 h for M00–M24; the budgets sum to 51.5 h. Re-computed in
  code: spine M00–M22 = 46.5 h, M23 = 2 h, M24 = 3 h, M25–M26 = 4 h.
- Question references checked against the official study guide and the practice PDF:
  M03 cited "sample question 09" (it is practice Q09 and official sample Q10); M16 cited
  "exam sample question 12" (it is practice Q12). Fixed. Practice answer keys that
  contradict the docs listed in `MILESTONES.md` Appendix B (Q28, Q42, Q47, Q53).
- Documents still said "paste these files"; the workflow is now a claude.ai Project.
- The BigQuery (charter section 3.2, M25) and Fivetran wording decisions of 2026-09-18 were
  not yet in the Project documents. Applied.

**Added**
- Exposure policy, tier A (charter section 2.1); licence changed from MIT to all rights reserved
  (README section 9); repo created with no licence (M00).
- Capacity table and exam-date risk R7 (charter section 2.2, section 8, section 10).
- Model line per milestone; exact model names and settings (brief Part 4).
- M26 — walkthrough finalization; `WALKTHROUGH.md` v0 (private).
- `SESSION_PROTOCOL.md` v2 (private) and a Project instructions block.

**Files and versions**
- `PROJECT_CHARTER.md` v2 · `MILESTONES.md` v2 · `AI_OPERATING_BRIEF.md` v2 ·
  `README.md` v0.2 · `PROJECT_LOG.md` (this entry)

## DOCS-REVISION — 2026-09-23

**Why.** End-to-end dry run of M00 as written, before starting it.

**Found and fixed**
- The pre-publish check lived only in `SESSION_PROTOCOL.md`, which no chat can read.
  Copied verbatim into `AI_OPERATING_BRIEF.md` section 3.13; every reference now points there.
- M00 created the virtual environment and `requirements.txt` before the repo folder
  existed, and ran `gh auth login` after creating the repo. Reordered: tooling → login →
  repo → `.gitignore` → everything else.
- M00's first commit contradicted "no commits to `main`": a new repo has no base branch
  for a PR. Exception written into brief section 3.10 and charter section 6; the commit runs at close,
  with `git branch -M main` before the push.
- M00 used a host `psql` that may not be installed; now uses the container's `psql`.
- Actual hours were to be written in two places (log and `MILESTONES.md` Appendix A).
  The log is now the only place; the phase audit fills Appendix A.

**Files and versions**
- `AI_OPERATING_BRIEF.md` v2.1 · `PROJECT_CHARTER.md` v2.1 · `MILESTONES.md` v2.1 ·
  `PROJECT_LOG.md` (this entry) · `SESSION_PROTOCOL.md` v2.1 (private)

## DOCS-REVISION — 2026-09-29

**Why.** New requirements from the user: a hard cap of 40 h end-to-end including all
friction; exam confirmed on 2026-10-30; a project handbook for understanding and
traceability; BigQuery and a BI tool for the portfolio.

**Changed**
- Replanned from 27 milestones (55.5 h, no buffer) to 19 milestones: 30.0 h + 0.5 h of
  audits + 9.15 h buffer (30%) = 39.65 h. Computed in code.
- Merged: staging + seeds + packages (M04); intermediate + dimensions (M05); all tests +
  unit tests (M10); contracts + versions + access (M11); snapshots + Python (M13).
- Cut (no exam weight): `dbt_project_evaluator`, the AI triage agent and dbt MCP,
  `dim_date`, `int_customer_order_history`, two seeds, the walkthrough rehearsal milestone.
- PostgreSQL and Docker removed. Grants move to the BigQuery sandbox with two keyless
  service accounts (M12); a `GRANT` probe in M00 decides it before anything depends on it.
- Data Studio (the name of Looker Studio since April 2026) dashboard added (M18),
  cuttable to after the exam.
- Handbook: one chapter per milestone, template frozen in the brief section 3.14, index
  generated by `scripts/build_handbook_index.py` (tested). The chapter is closing
  deliverable 2; ADR files are replaced by `D-MNN-n` sections inside chapters.
- Stop rule tightened from 2× to 1.5× the milestone budget. Phase audits reduced to two.

**Verified by running (2026-09-29)**
- `dbt-core==1.11.*`, `dbt-duckdb==1.11.*` and `dbt-bigquery==1.11.*` install together
  (1.11.15 / 1.11.0 / 1.11.3). Risk R1 retired.
- On dbt-duckdb 1.11: microbatch, enforced contract + constraints (a violating insert is
  rejected), YAML snapshot with `hard_deletes`, Python model, unit test, `--empty`,
  `--sample`, `dbt clone`, `dbt retry`, `state:modified`.
- `dbt-duckdb` ignores `grants` with a debug message; the v2 claim that it raised a parse
  error was wrong.
- A plain microbatch run after the first processes only batches around today; TPC-H
  history must be backfilled with `--event-time-start/--event-time-end` (written into M09).
- An enforced `foreign_key` in DuckDB makes the second build of the referenced dimension
  fail (`Cannot alter entry … because there are entries that depend on it`). M11 now shows
  it once and removes it.
- `--sample` with an explicit window (`{'start': …, 'end': …}`) filters every input that
  declares `event_time`; a relative window counts back from today (written into M15).

**Found by an independent review of v3 and fixed**
- `--state` paths are `../prod-artifacts` (dbt runs from `transform/`); `sources.json` is
  saved with the manifest for `source_status:fresher+` (M14).
- CI builds its own production state from `main` before deferring (M15).
- `env_var('GCP_PROJECT_ID', 'no-gcp-project')` everywhere; Makefile loads `.env`;
  `make setup` creates `data/` (M01, M12).
- Loader semantics fixed: `orders`/`lineitem` additive, other tables replaced; `--mutate`
  deletes suppliers physically so `hard_deletes` can see it (M02, M13).
- Private models belong to group `core`; the M03 identifier drill is undone afterwards;
  WIP closing and audit outputs defined (brief section 2.2, section 2.4); chapter metadata no longer
  asks for a PR number the chat cannot know.

**Files and versions**
- `PROJECT_CHARTER.md` v3 · `MILESTONES.md` v3 · `AI_OPERATING_BRIEF.md` v3 ·
  `README.md` v0.3 · `PROJECT_LOG.md` (this entry) · private: `SESSION_PROTOCOL.md` v3,
  `WALKTHROUGH.md` v0.1

## DOCS-REVISION — 2026-09-29 (b)

**Why.** During M00 each step could be run but not explained: responses gave the purpose
of a command, not what runs where, and described file edits instead of showing them.

**Changed**
- `AI_OPERATING_BRIEF.md` v3.1: section 1.2 item 10 (analogies only when asked in that message,
  never as a fallback); new section 1.12 mechanism disclosure (eight points for every new tool,
  file, setting or connection); new section 1.13 command anatomy (token by token, one command
  per line, say whether a block is pasted or typed).
- Project instructions block names section 1.12, section 1.13 and BEFORE/AFTER edits.
- Hours are counted inside M00's 4.0 h (not split).

**Files and versions**
- `AI_OPERATING_BRIEF.md` v3.1 (private) · Project instructions · `PROJECT_LOG.md`
  (this entry)

## M00 — Prove the stack before building on it
**Date:** 2026-09-30 (started 2026-09-29) · **Estimated:** 1.5h · **Actual:** 4.0h · **Hours used so far:** 4.0 of 39.65
**Chapter:** `docs/handbook/m00-stack-verification.md`

**Now exists that did not before**
- files: `.gitignore`, `.env.example`, `requirements.txt`, `README.md`,
  `docs/PROJECT_CHARTER.md`, `docs/MILESTONES.md`, `docs/PROJECT_LOG.md`,
  `docs/handbook/m00-stack-verification.md` (committed); `.env`, `.venv/`, empty `data/`
  (local only); `~/.gitconfig`, `~/.config/gh/hosts.yml`, `~/projects/_contexto-dbt/`
  with the 8 plan files (outside the repo)
- tools: WSL2 + Ubuntu; Git; GitHub CLI logged in as `PCoronelPeris` (scopes `gist`,
  `read:org`, `repo`, `workflow`); dbt-core 1.11.15, dbt-duckdb 1.11.0, dbt-bigquery 1.11.3
- cloud: public GitHub repo; BigQuery sandbox project; service accounts `dbt-reporter`
  and `dbt-finance`
- probe results: `lineitem` 6,001,215 rows at SF 1; 8.9 s (second run, extension
  cached); 252.0 MB file
- schemas / tables: none (the BigQuery `probe` dataset and `data/probe.duckdb` were
  created and deleted)
- dbt resources: none

**Deviations from the milestone as written**
- Git identity step added (name, GitHub noreply email, `init.defaultBranch main`); the
  first commit needs it → D-M00-7
- TPC-H probe run as a measured script instead of a REPL → D-M00-6
- `.env.example` lists the optional keys commented out → D-M00-3
- The `GRANT` probe script starts with `drop schema if exists probe cascade;` so it can
  be re-run after a partial failure
- 4.0 h against 1.5 h: past the 1.5× stop rule; M00 could not close as WIP because M01
  requires it committed

**Binding for later milestones**
- Grants run on BigQuery → M12 as written (D-M00-1)
- Work only under `~/projects`; open Ubuntu from the Start menu or `wsl ~` → all (D-M00-2)
- Multi-line blocks are pasted, not typed; one command per line → all (D-M00-5)
- M18 moves to after the exam (MILESTONES Appendix A, drift above 30%) → M18, Audit A
  re-checks (D-M00-8)
- The `workflow` token scope already exists → M15 needs no `gh auth refresh`

**Registry changes**
- (none)

**Left open**
- Editor for files inside WSL is not chosen; proposal: VS Code with the WSL extension → M01
- `python3 --version` was not recorded → M01 chapter
- Audit A decides whether D-M00-8 stands once M00–M06 hours exist → Audit A

**Commit**
`main` (initial commit, no branch) → `chore: pin toolchain and verify local and cloud stack`

## M01 — Project skeleton, `dbt_project.yml`, handbook tooling
**Date:** 2026-10-09 (started 2026-10-08) · **Estimated:** 1.5h · **Actual:** 4.0h · **Hours used so far:** 8.0 of 40
**Chapter:** `docs/handbook/m01-project-skeleton.md`

**Now exists that did not before**
- files (committed): `transform/dbt_project.yml` (40 lines), `transform/profiles.yml`
  (15 lines), `transform/macros/generate_schema_name.sql` (8 lines), `.gitkeep` in
  `transform/analyses`, `macros`, `models`, `seeds`, `snapshots` and `tests`,
  `Makefile` (28 lines), `scripts/build_handbook_index.py` (72 lines),
  `docs/handbook/README.md` (generated), `docs/handbook/m01-project-skeleton.md`,
  `scripts/milestone.py` (added at the close, by the replan of 2026-10-18);
  `.gitignore` gained `target/`, `dbt_packages/`, `logs/`, `.user.yml`;
  `docs/PROJECT_LOG.md`, `docs/PROJECT_CHARTER.md` (v4), `docs/MILESTONES.md` (v4) and
  `README.md` (v0.4) updated
- files (local only, git-ignored): `data/warehouse.duckdb` (empty), `logs/`,
  `transform/logs/`, `transform/target/`, `transform/.user.yml`
- tools: python 3.12.3 (closes the open item of M00); GNU Make 4.3
- schemas / tables: none (a throwaway model proved `dev_staging` and `prod_staging`, then
  was deleted)
- dbt resources: 0 models; one macro, `generate_schema_name`, which overrides the built-in

**Deviations from the milestone as written**
- `.user.yml` also ignored → D-M01-8
- `make clean` also removes `data/*.duckdb.wal`; `make setup` does not upgrade pip → D-M01-9
- `transform/models/.gitkeep` added so the folder survives a clone → D-M01-11
- Files created with terminal heredocs, not an editor → D-M01-7
- 4.0 h against 1.5 h: past the 1.5× stop rule. The exit criteria were met, so M01
  closes as Done, not WIP. Main causes: the explanation format of the first responses had
  to be rewritten and the milestone restarted from zero; the rest went into per-step
  explanations and fixing four small errors (E-M01-1 to E-M01-4)

**Binding for later milestones**
- `profiles.yml` lives in `transform/` and is committed; every dbt command runs from
  `transform/` → all (D-M01-1)
- Schemas render as `{target.name}_{custom_schema_name}`; the `bq` target added in M12
  must have a name that works as a BigQuery dataset prefix → M04–M06, M12 (D-M01-4)
- Intermediate models are `ephemeral` by default → M05 overrides it if it needs a table
  (D-M01-3)
- `make` calls `.venv/bin/*` by absolute path, so it works without activating the
  environment → all (D-M01-5)
- The script that builds the handbook index is run, not imported; add `__pycache__/` to
  `.gitignore` before any script imports another → M02 (D-M01-10)
- After writing each chapter, run `make handbook` and compare the counts it prints with
  the chapter's own tables → all
- The warning about 3 unused configuration paths disappears when models exist → M04 to M06
  (E-M01-3)

**Registry changes**
- Brief section 3.6, `make clean`: now also removes `data/*.duckdb.wal` (brief v3.4)
- Brief section 3.6: `make start`, `make close`, `make fetch` added (brief v4)

**Left open**
- Dates and pace: resolved by the DOCS-REVISION of 2026-10-18 (next entry)
- Editor for files inside WSL is still not chosen; not needed: files arrive whole, by
  paste or by `make fetch` → closed
- Audit A decides whether D-M00-8 stands → superseded: M18 is back in the 38.0 h plan and
  is the first thing to move if the cap is at risk

**Commit**
`m01-project-skeleton` → `feat: scaffold dbt project, makefile and handbook index`

## DOCS-REVISION — 2026-10-18

**Why.** M00 and M01 were estimated at 1.5 h each and took 4.0 h each. The user asked for
the same 19 milestones, each of the remaining ones at 1.5–2 h of real time, complete
explanations of every line every time, no calendar dates, and a full review so that
nothing breaks later.

**Diagnosis of M01 (counted in the M01 chat)**
- Restarted once from zero after the first responses explained too little; the brief was
  rewritten in the middle of the milestone.
- Delivered as 74 numbered steps: 57 to build and 17 to close, each a separate action with
  its own paste-back.
- Files typed in fragments: `dbt_project.yml` in four heredocs and the index script in
  four, each followed by a size check.
- Explanations went deep into shell mechanics (`cd`, `ls`, heredocs) while the
  milestone-level picture (what is built, why, what the exam asks) came late, so the user
  had to stop and work out the purpose of steps.
- The close was 17 manual steps: download, copy, branch, add, check, commit, push, PR,
  merge, pull.

**Changed**
- Brief v4: every line of every command and file is annotated every time, in a four-column
  table (what it does, role in the project, link to dbt and the exam) (1.13); steps are
  actions, files are never fragmented, long files arrive by `make fetch` (1.14); a new step
  shape (1.15); a milestone map opens every milestone (1.17); the chat checks `main` on
  GitHub at opening (2.1); one-command close (2.2); minutes tracked with the time tool
  (2.3); a pre-testing recipe so every file is run before it is sent (2.5); current model
  names (Part 4).
- `scripts/milestone.py` with `make start M=NN`, `make close M=NN` and `make fetch F=...`,
  tested against a local bare remote with a simulated `gh`: closes M01 from `main` with
  uncommitted work, from an existing branch, and closes M02 after a fetch; stops with a
  message when a download is missing.
- `MILESTONES.md` v4: budgets in real hours (M02–M18 = 29.5 h; total 38.0 h), a Parts line
  per milestone, no dates, M02 rewritten with the tested loader embedded, M15 adds the CI
  badge. `PROJECT_CHARTER.md` v4: section 2.2 and section 10 without dates. README v0.4:
  the clone URL points at the real repository; the CI badge waits for M15.
- Loader design fixed before it is written. The v3 design replaced the six reference
  tables on every load and let `--mutate` delete real suppliers. Two later failures
  followed from it: line items would point at deleted suppliers and break the
  `relationships` tests (M06, M10), and every reload would revert earlier mutations and
  re-stamp every row, so a `timestamp` snapshot would record noise. Now reference tables
  are created once and re-stamped, they carry `_updated_at`, and `--mutate` deletes five
  synthetic suppliers with no parts.
- D-M00-8 superseded: M18 is back in the plan.

**Verified by running (2026-10-18, DuckDB 1.5.5, dbt-core 1.11.15, dbt-duckdb 1.11.0, SF 0.01)**
- First wave through 1996-12-31: 8 tables, 11,367 orders, 45,730 line items, every
  `_loaded_at` non-null, no line item without its order.
- Second wave through 1997-06-30 inserts only the 1,153 new orders; the same window again
  inserts 0.
- `--mutate` changed 11 customer segments and 2 supplier balances and deleted the 5
  synthetic suppliers; a second `--mutate` deleted 0.
- A different scale factor without `--full-reset` stops with a message; `--full-reset`
  starts over.
- `dbt source freshness` on `_loaded_at` passes; `check` and `timestamp` snapshots with
  `hard_deletes: new_record` record the changed rows and the 5 deletions.
- `make load` passes `SF`, `THROUGH_DATE`, `MUTATE` and `RESET` through to the script.

**Hours.** Not counted in milestone hours (work done by the assistant).

**Files and versions**
- `AI_OPERATING_BRIEF.md` v4 (private) · `PROJECT_CHARTER.md` v4 · `MILESTONES.md` v4 ·
  `README.md` v0.4 · `PROJECT_LOG.md` (this entry) · `scripts/milestone.py` · Makefile
  (`start`, `close`, `fetch`)

## DOCS-REVISION — 2026-11-05

**Why.** Requirements stated by the user during M02, before and after part 1.

**Recorded**
- At the end of the project every file is reviewed and corrected where needed (README,
  handbook, plan documents), and the project is proven to work from a clean clone:
  `make setup && make load && make build` with 0 errors, CI green on `main`, every link in
  README and docs resolves, the pre-publish check prints two `OK` lines.
- A private walkthrough (15–20 minutes, git-ignored) is written from the finished
  repository, not from the plan.
- The milestone tooling stays in the repository. Build-side files (plan documents,
  handbook, `scripts/`, the `start`/`close`/`fetch` targets) move to one dedicated folder
  at the final revision (D-M02-5).
- Explanations start from the whole map (what exists, what is missing, what this
  milestone adds), use plain language, and replace the per-token tables with a short
  explanation of each command and of everything it triggers underneath. Every milestone
  map states how many steps each part has.
- A final-revision milestone (proposed M19, 1.5 h) would bring the plan to 40.5 h, over
  the cap. Audit A decides it with real hours; M18 is the first to move.

**Found and left for the final revision**
- 40 lines in committed documents name private files or a private local folder that a
  reader of the repository cannot open.
- This log said M01 was published on 2026-10-30; the M01 squash commit on `main` is dated
  2026-11-05. Fixed in the Current state block.

**Hours.** Not counted in milestone hours.

## M02 — The EL layer
**Date:** 2026-11-06 (started 2026-11-05) · **Estimated:** 1.5h · **Actual:** 2.5h (estimated from session timestamps) · **Hours used so far:** 10.5 of 40
**Chapter:** `docs/handbook/m02-el-layer.md`

**Now exists that did not before**
- files (committed): `el/load_raw.py` (167 lines, 8,035 bytes), `el/README.md`
  (37 lines, 2,056 bytes); `Makefile` gained the `load` target and `load` in `.PHONY`;
  `.gitignore` gained `__pycache__/`
- files (local only): `data/warehouse.duckdb` with schema `raw`;
  `~/.duckdb/extensions/<duckdb version>/linux_amd64/tpch.duckdb_extension` (outside the
  repo, downloaded by DuckDB on the first load)
- schemas / tables: `raw.region` 5 · `raw.nation` 25 · `raw.part` 200,000 ·
  `raw.supplier` 10,005 (5 synthetic) · `raw.partsupp` 800,000 · `raw.customer` 150,000 ·
  `raw.orders` 1,138,594 · `raw.lineitem` 4,556,169; orders through 1996-12-31; every
  row has `_loaded_at` and `_batch_id`; reference tables also have `_updated_at`
- dbt resources: none

**Deviations from the milestone as written**
- The Makefile and `.gitignore` were changed with `sed` and `printf` → D-M02-2
- The verification block failed twice because it was delivered indented (E-M02-1,
  E-M02-2)
- 2.5 h against 1.5 h: past the 1.5× stop rule. The exit criteria were met, so M02 closes
  as Done. Main causes: the explanation method was rewritten in the middle of the
  milestone (DOCS-REVISION 2026-11-05) and conceptual questions about the environment
  (DuckDB, `.venv`, make, git) were answered before part 2

**Binding for later milestones**
- M03 declares the 8 tables of `raw` as sources; freshness uses `_loaded_at` → M03
- Later waves use `make load THROUGH_DATE=<later date>`; the scale factor stays 1 →
  M08, M09
- `make load MUTATE=1` produces the changes and deletions for snapshots; snapshots use
  `_updated_at`, never `_loaded_at` → M13
- A load and a dbt run never overlap on the DuckDB file → all (D-M02-4)
- Code blocks meant to be pasted are never indented → all (E-M02-1)

**Registry changes**
- (none) — `make load` and the loader flags match the milestone as written

**Left open**
- `duckdb` is not pinned in `requirements.txt`; it arrives as a dependency of
  `dbt-duckdb` → M03 decides whether to pin it
- Moving build-side files to one folder → final revision (D-M02-5)
- Proposed final-revision milestone → Audit A

**Commit**
`m02-el-layer` → `feat(el): add TPC-H loader with load metadata and date waves`

## M03 — Sources, freshness, and dependency verification
**Date:** 2026-11-06 (started 2026-11-06, 15:05 local) · **Estimated:** 1.5h · **Actual:** 1.9h (estimated from session timestamps) · **Hours used so far:** 12.4 of 40
**Chapter:** `docs/handbook/m03-sources.md`

**Now exists that did not before**
- files (committed): `transform/models/staging/tpch/_tpch__sources.yml` (109 lines,
  3,739 bytes); `Makefile` gained the `freshness` target and `freshness` in `.PHONY`
- files (local only): `transform/target/sources.json`, rewritten by every
  `make freshness`
- schemas / tables: no new tables. The loader ran again with the same window: the six
  reference tables were re-stamped, `orders` and `lineitem` were not changed. During the
  drill `raw.part` was renamed and renamed back; the net change is none
- dbt resources: 1 source `tpch_raw` (`schema: raw`, 8 tables, `loaded_at_field:
  _loaded_at`, freshness warn 12 h / error 24 h); `region` exempt (`freshness: null`);
  `orders` override warn 6 h / error 12 h; `line_items` with `identifier: lineitem`;
  18 data tests; 0 models

**Deviations from the milestone as written**
- 1.9 h against 1.5 h: over the budget, under the stop rule (2.25 h). The exit criteria
  were met, so M03 closes as Done. Main causes: a stop in part 1 (a file not yet
  downloaded when `make fetch` ran, E-M03-2) and a request in the middle of part 1 to
  explain what the milestone is, answered before part 2
- Composite keys of `partsupp` and `line_items` get `not_null` only; the uniqueness of
  the pairs waits for `dbt_utils` → D-M03-3
- The exit criterion `dbt test --select source:tpch_raw` was met through `make test`
  (all 18 tests of the project are source tests); the literal selector was run only in
  the sandbox
- `_tpch__sources.yml` was delivered twice by design: without tests in part 1, with
  tests in part 2

**Binding for later milestones**
- The source table is named `line_items`; the physical table is `raw.lineitem`. Models
  call `source('tpch_raw', 'line_items')` → M04, M09 (D-M03-1). M09 puts `event_time` on
  the source `line_items`
- The source table `region` has no freshness check; `orders` has its own thresholds →
  M14 (`source_status:fresher+`) (D-M03-2)
- Tests on sources use `data_tests:` and, for `relationships`, `arguments:` → M04, M10
- Uniqueness of (`ps_partkey`, `ps_suppkey`) and (`l_orderkey`, `l_linenumber`) →
  M04 with `dbt_utils` (D-M03-3)
- `make freshness` exists; `--select "source:tpch_raw+"` selects the source and its
  descendants → all
- Download a file before running `make fetch` for it; small files can also be pasted →
  all (E-M03-2)
- `raw.part` and `_tpch__sources.yml` are back to their original state; the hash of the
  file is `03f5977f64876113cba88b27243fd595`

**Registry changes**
- (none) — `make freshness` and the file name `_tpch__sources.yml` match brief 3.6 and
  3.8. Separately, brief 1.13 still describes the per-token tables that the
  DOCS-REVISION of 2026-11-05 replaced; the brief has not been edited → final revision

**Left open**
- `dbt deps` was not tested in the sandbox because `hub.getdbt.com` answered 403; M04
  pre-tests the packages from GitHub, and the user's machine runs the real command → M04
- `duckdb` stays unpinned (D-M03-4) → M15 revisits it for CI
- Brief 1.13 text against the practice of the last milestones → final revision / Audit A
- The copy of this log in Project knowledge stopped at M01 before this close; it was
  replaced by this file → closed

**Commit**
`m03-sources` → `feat(staging): declare tpch sources with freshness policies`
