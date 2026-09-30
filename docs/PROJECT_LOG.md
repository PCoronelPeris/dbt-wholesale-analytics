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
| Last milestone completed | **M00 — Prove the stack before building on it** (2026-09-30) |
| Next milestone | **M01 — Project skeleton, `dbt_project.yml`, handbook tooling** |
| Hours used | 4.0 of 39.65 (cap 40) · remaining plan 29.0 h · buffer left 6.65 h |
| Schedule status | drift +2.5 h (M00: 4.0 h vs 1.5 h) · above the 30% rule → M18 moved to after the exam (D-M00-8) · exam on 2026-10-30 · build must end by 2026-10-24 |
| Repo exists on GitHub | yes · `PCoronelPeris/dbt-wholesale-analytics` · public · no licence · 1 commit on `main` |
| DuckDB file exists | no (TPC-H SF 1 probe generated and deleted; `data/` is empty) |
| BigQuery sandbox project | created · sandbox, no billing · ID in local `.env` only · service accounts `dbt-reporter`, `dbt-finance` (no keys, no roles) |
| Grants engine | **BigQuery** — the sandbox accepted `GRANT` (D-M00-1); R2 retired |
| Raw schema loaded through date | — |
| Handbook chapters | 1 (M00) |
| Plan documents | charter v3, milestones v3, brief v3.1 (DOCS-REVISION 2026-09-29 b) |
| Decisions | D1 exam date **2026-10-30** (confirmed) · D2 capacity 12 h/week (default) · D3 exposure tier A (default) |
| Open blockers | none |

**Commands to restore working state at the start of the next session:**

```bash
# Open Ubuntu from the Windows Start menu (or run `wsl ~` in PowerShell), then:
cd ~/projects/dbt-wholesale-analytics
source .venv/bin/activate
git status        # expect: On branch main, nothing to commit, working tree clean
dbt --version     # expect: core 1.11.15, plugins bigquery 1.11.3 and duckdb 1.11.0
```

---

## Entry template

Copy this block for each new entry and append it at the end of the file. Details,
errors and reasoning go in the handbook chapter, not here.

````markdown
## M{NN} — {title}
**Date:** YYYY-MM-DD · **Estimated:** Xh · **Actual:** Xh · **Hours used so far:** X of 39.65
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
- The BigQuery (charter §3.2, M25) and Fivetran wording decisions of 2026-09-18 were
  not yet in the Project documents. Applied.

**Added**
- Exposure policy, tier A (charter §2.1); licence changed from MIT to all rights reserved
  (README §9); repo created with no licence (M00).
- Capacity table and exam-date risk R7 (charter §2.2, §8, §10).
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
  Copied verbatim into `AI_OPERATING_BRIEF.md` §3.13; every reference now points there.
- M00 created the virtual environment and `requirements.txt` before the repo folder
  existed, and ran `gh auth login` after creating the repo. Reordered: tooling → login →
  repo → `.gitignore` → everything else.
- M00's first commit contradicted "no commits to `main`": a new repo has no base branch
  for a PR. Exception written into brief §3.10 and charter §6; the commit runs at close,
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
- Handbook: one chapter per milestone, template frozen in the brief §3.14, index
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
  WIP closing and audit outputs defined (brief §2.2, §2.4); chapter metadata no longer
  asks for a PR number the chat cannot know.

**Files and versions**
- `PROJECT_CHARTER.md` v3 · `MILESTONES.md` v3 · `AI_OPERATING_BRIEF.md` v3 ·
  `README.md` v0.3 · `PROJECT_LOG.md` (this entry) · private: `SESSION_PROTOCOL.md` v3,
  `WALKTHROUGH.md` v0.1

## DOCS-REVISION — 2026-09-29 (b)

**Why.** During M00 each step could be run but not explained: responses gave the purpose
of a command, not what runs where, and described file edits instead of showing them.

**Changed**
- `AI_OPERATING_BRIEF.md` v3.1: §1.2 item 10 (analogies only when asked in that message,
  never as a fallback); new §1.12 mechanism disclosure (eight points for every new tool,
  file, setting or connection); new §1.13 command anatomy (token by token, one command
  per line, say whether a block is pasted or typed).
- Project instructions block names §1.12, §1.13 and BEFORE/AFTER edits.
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
