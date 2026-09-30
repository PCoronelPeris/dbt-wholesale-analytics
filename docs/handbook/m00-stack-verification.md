# M00 — Prove the stack before building on it

| Field | Value |
|---|---|
| Status | Done · 2026-09-30 |
| Hours | 1.5 estimated · 4.0 actual |
| Branch | `main` (initial commit, no branch) |
| Exam sections | None (viability gate) |

## In one paragraph
The laptop now has a Linux environment (WSL2 with Ubuntu) with Git, the GitHub CLI and a
Python virtual environment that holds dbt Core 1.11.15 with the DuckDB and BigQuery
adapters. DuckDB generated the full TPC-H dataset at scale factor 1 in 8.9 seconds. A
BigQuery sandbox project exists with two keyless service accounts, and it accepted a
`GRANT` statement, so grants will run on BigQuery in M12. The public repository exists on
GitHub with its first commit.

## 1. The problem this solves
The plan rests on two technical assumptions. The first is that dbt Core 1.11 and both
adapters install together on this laptop (risk R1). The second is that the free BigQuery
sandbox accepts `GRANT` statements (risk R2). Google's documentation says nothing about
the second one. If either assumption were false and found out late, work already built on
top of it would have to change. This milestone tests both before any model exists. It
also creates the repository with a `.gitignore` in place before any secret or data file
exists, so nothing private can be committed by accident.

## 2. Where it sits
Everything below lives inside the Linux filesystem of WSL2, not on the Windows drive.

```
/home/pedro/                                   Linux home (written ~)
├── .gitconfig                                 NEW · Git identity and credential helper
├── .config/gh/hosts.yml                       NEW · GitHub CLI login token
└── projects/
    ├── _contexto-dbt/                         NEW · private planning files, not a Git repo
    └── dbt-wholesale-analytics/               NEW · the repository
        ├── .git/                              NEW · Git database, created by the clone
        ├── .gitignore                         NEW · committed
        ├── .env                               NEW · local only, ignored
        ├── .env.example                       NEW · committed
        ├── .venv/                             NEW · local only, ignored
        ├── requirements.txt                   NEW · committed
        ├── README.md                          NEW · committed
        ├── data/                              NEW · empty, so Git does not track it
        └── docs/
            ├── PROJECT_CHARTER.md             NEW · committed
            ├── MILESTONES.md                  NEW · committed
            ├── PROJECT_LOG.md                 NEW · committed
            └── handbook/
                └── m00-stack-verification.md  NEW · this chapter
```

Outside the laptop:

- **GitHub:** repository `PCoronelPeris/dbt-wholesale-analytics`, public, no licence.
- **Google Cloud:** one project in BigQuery sandbox mode (no billing), with service
  accounts `dbt-reporter` and `dbt-finance` (no keys, no roles).

Position in the DAG: none yet. This milestone builds the environment that every later
model runs in.

## 3. How it was built

### Step 1 — Open the Linux environment
WSL2 (Windows Subsystem for Linux, version 2) is a Windows feature that runs a real Linux
kernel inside a lightweight virtual machine. Ubuntu is the Linux distribution running in
it. Its whole disk is one file on the Windows drive (`ext4.vhdx`).

The terminal is opened from the Windows Start menu, entry **Ubuntu**. The prompt
`pedro@ZENBOOKDUO:~$` means bash is ready and the current folder is `/home/pedro`.

All project work happens under `~`, never under `/mnt/c`. `/mnt/c` is the Windows `C:`
drive seen from Linux, and every file operation there crosses a slower file-sharing
protocol.

### Step 2 — Install Python, venv, Git and the GitHub CLI
```bash
sudo apt update && sudo apt install -y python3 python3-venv python3-pip git gh
```
`apt` is Ubuntu's package manager. `sudo` runs it as administrator. The programs land in
`/usr/bin/`.

### Step 3 — Set the Git identity
This step was added; the milestone did not list it. Without it, the first
`git commit` fails with `Author identity unknown`.

```bash
git config --global user.name "Pedro Coronel"
git config --global user.email "175746172+PCoronelPeris@users.noreply.github.com"
git config --global init.defaultBranch main
```

`--global` writes `~/.gitconfig`, which applies to every repository of this Linux user.
The email is GitHub's private "noreply" address, so no personal email is published in a
public repository.

The first attempt ran in a Windows terminal and wrote a different file,
`C:\Users\pedro\.gitconfig` (E-M00-1).

### Step 4 — Log in to GitHub from the terminal
```bash
gh auth login
gh auth status
```
`gh` is the GitHub CLI, a program that talks to GitHub's API over HTTPS. The login used
GitHub's device flow:

1. `gh` printed a one-time code.
2. The code was entered at `https://github.com/login/device` in the Windows browser.
3. GitHub handed a token to `gh`.

`gh` could not open the browser by itself (`wslview` is not installed), which is expected
under WSL.

The token is stored in plain text in `~/.config/gh/hosts.yml` (D-M00-4). Its scopes are
`gist`, `read:org`, `repo` and `workflow`.

Answering "Yes" to "Authenticate Git with your GitHub credentials?" added this block to
`~/.gitconfig`:

```
[credential "https://github.com"]
        helper =
        helper = !/usr/bin/gh auth git-credential
```

From then on, when `git` talks to github.com, it asks `gh` for the token.

### Step 5 — Copy the planning files into a private folder
```bash
mkdir -p ~/projects/_contexto-dbt
cp /mnt/c/Users/pedro/Downloads/{AI_OPERATING_BRIEF.md,MILESTONES.md,PROJECT_CHARTER.md,PROJECT_INSTRUCTIONS.txt,PROJECT_LOG.md,README.md,SESSION_PROTOCOL.md,WALKTHROUGH.md} ~/projects/_contexto-dbt/
```
Bash expands the braces into eight paths before `cp` runs. This folder is not a Git
repository, so nothing in it can be pushed.

### Step 6 — Create the repository and clone it
```bash
cd ~/projects
gh repo create dbt-wholesale-analytics --public --clone
cd dbt-wholesale-analytics
git remote -v
```

This command acts in two places:
- **On GitHub**, it creates an empty public repository. There is no `--license` flag, so
  no licence file is created and default copyright applies.
- **On the laptop**, it clones that repository into a folder that contains only `.git/`.

`git remote -v` shows that the GitHub copy is registered under the name `origin`.

### Step 7 — Write `.gitignore` before anything else
```bash
cat > .gitignore <<'EOF'
.venv/
.env
data/*.duckdb
data/*.duckdb.wal
AI_OPERATING_BRIEF.md
SESSION_PROTOCOL.md
WALKTHROUGH.md
PROJECT_INSTRUCTIONS.txt
EOF
```

`.gitignore` must exist before the files it protects. Adding a pattern later does not
remove a file that was already committed.

The block is a heredoc: bash feeds every line up to the line `EOF` into `cat`, which
writes them to the file. The first attempt put a `\` at the end of each line. That joined
the lines together, so the heredoc never closed (E-M00-3).

### Step 8 — Create the virtual environment and install pinned packages
```bash
python3 -m venv .venv
source .venv/bin/activate
cat > requirements.txt <<'EOF'
dbt-core==1.11.*
dbt-duckdb==1.11.*
dbt-bigquery==1.11.*
pandas
EOF
pip install -r requirements.txt
```

**The virtual environment.** A virtual environment is a folder (`.venv/`) with its own
list of Python packages. Ubuntu refuses `pip install` into the system Python, so the venv
is required.

`source` runs `activate` inside the current bash process. That puts `.venv/bin` first in
`PATH`, so `python`, `pip` and `dbt` resolve to the venv. Every new terminal must run
`source .venv/bin/activate` again.

**The requirements file.** `==1.11.*` accepts any patch release of 1.11 and never 1.12,
because the exam tests 1.11.

**The install.** `pip` downloaded the packages from PyPI (the public Python package
index) and unpacked them into `.venv/lib/.../site-packages/`.

### Step 9 — Check dbt and its adapters
```bash
dbt --version
```

```
Core:
  - installed: 1.11.15
  - latest:    1.12.5  - Update available!
Plugins:
  - bigquery: 1.11.3 - Update available!
  - duckdb:   1.11.0 - Up to date!
```

An adapter (dbt calls it a plugin) is the package that translates dbt's work into one
database engine. The "Update available" lines are ignored on purpose. Risk R1 is retired
on this laptop.

### Step 10 — Probe DuckDB with TPC-H
```bash
mkdir -p data
python - <<'EOF'
import time
from pathlib import Path

import duckdb

db_path = Path("data/probe.duckdb")
start = time.perf_counter()
con = duckdb.connect(str(db_path))
con.sql("INSTALL tpch; LOAD tpch; CALL dbgen(sf=1);")
row_count = con.sql("select count(*) from lineitem").fetchone()[0]
con.close()
elapsed = time.perf_counter() - start
size_mb = db_path.stat().st_size / 1024 / 1024
print(f"lineitem rows: {row_count:,}")
print(f"elapsed seconds: {elapsed:.1f}")
print(f"file size MB: {size_mb:.1f}")
EOF
rm -f data/probe.duckdb data/probe.duckdb.wal
```

```
lineitem rows: 6,001,215
elapsed seconds: 8.9
file size MB: 252.0
```

DuckDB is an SQL engine that runs as a library inside the Python process. It has no
server and no port, and it stores a whole database in one file.

`INSTALL tpch` downloads the TPC-H extension once, to `~/.duckdb/extensions/`.
`CALL dbgen(sf=1)` generates the eight TPC-H tables locally and deterministically. No data
comes from the internet.

The milestone asked for a Python REPL. This script measures the time and file size
instead of estimating them (D-M00-6). The 8.9 seconds come from the second run, after the
extension was already downloaded. Scale factor 1 is fast enough on this laptop, so risk R3
does not apply.

### Step 11 — Probe BigQuery: sandbox, service accounts, GRANT
This step happens in the Google Cloud web console, not in the terminal.

1. **The sandbox project.** At `https://console.cloud.google.com/bigquery`, a project was
   created. No billing was enabled. The page shows the sandbox notice.
2. **The service accounts.** In IAM and Admin, Service Accounts, two accounts were
   created: `dbt-reporter` and `dbt-finance`. They have no roles and no keys. A service
   account is an identity for programs. Without a key, nobody can sign in as it. Here it
   only exists to receive grants.
3. **The GRANT probe.** In the query editor:

```sql
drop schema if exists probe cascade;
create schema probe options (location = 'US');
create table probe.t as select 1 as x;
grant `roles/bigquery.dataViewer` on table probe.t
  to "serviceAccount:dbt-reporter@<your-project-id>.iam.gserviceaccount.com";
drop schema probe cascade;
```

All statements succeeded, so the sandbox accepts `GRANT` (D-M00-1). Risk R2 is retired.

The quotes matter:
- **The role** is an identifier, so it goes in backticks.
- **The grantee** is a string, so it goes in double quotes.

The first attempt put the role in double quotes (E-M00-4). The first line was added so
the script can be re-run after a partial failure.

### Step 12 — Write `.env` and `.env.example`
```bash
cat > .env <<'EOF'
GCP_PROJECT_ID=<your-project-id>
EOF
cat > .env.example <<'EOF'
GCP_PROJECT_ID=
# TPCH_SCALE_FACTOR=1
# DUCKDB_PATH=/absolute/path/to/warehouse.duckdb
EOF
```

`.env` holds this machine's values and is ignored by Git. `.env.example` is the public
template: every key, no values. The optional keys are commented out rather than left
empty (D-M00-3).

### Step 13 — Copy the plan documents into the repository
```bash
mkdir -p docs/handbook
cp ~/projects/_contexto-dbt/{PROJECT_CHARTER.md,MILESTONES.md,PROJECT_LOG.md} docs/
cp ~/projects/_contexto-dbt/README.md .
```
From now on the copies in `docs/` are the master copies. The first `cp` of `README.md`
left out the destination (E-M00-5).

### Step 14 — Stage and run the pre-publish check
```bash
git add -A
git status
git ls-files --cached | grep -iE "AI_OPERATING_BRIEF|WALKTHROUGH|SESSION_PROTOCOL|PROJECT_INSTRUCTIONS|(^|/)\.env$|\.duckdb$|\.pem$|credentials|key\.json$" \
  && echo "STOP: private file tracked" || echo "OK: no private files tracked"
git grep --cached -nIE "(api[_-]?key|secret|password|token)[[:space:]]*[:=]" -- . ':!*.example' | grep -v "env_var" \
  && echo "STOP: possible secret in code" || echo "OK: no secret patterns"
```

**The staging area.** The staging area (the index, `.git/index`) lists exactly what the
next commit will contain. `git add -A` adds everything that `.gitignore` does not
exclude.

**What `git status` showed.** Seven staged files, and no `.env`, `.venv/` or `.duckdb`
file.

**The pre-publish check.** Line one looks for private file names among the staged files.
Line two looks for secret-like assignments inside the staged content. Both printed `OK`.

### Step 15 — Commit and push to `main`
```bash
git commit -m "chore: pin toolchain and verify local and cloud stack"
git branch -M main
git push -u origin main
```

This is the only commit made straight to `main`. A pull request needs an existing base
branch, and a new repository has none. `-u` records `origin/main` as the branch this
local `main` pushes to and pulls from.

## 4. How to verify it
| Command | Expected result |
|---|---|
| `dbt --version` (venv active) | core 1.11.15, plugins bigquery 1.11.3 and duckdb 1.11.0 |
| `gh auth status` | `Logged in to github.com account PCoronelPeris` |
| `gh repo view dbt-wholesale-analytics --json visibility,licenseInfo` | `"licenseInfo": null` and `"visibility": "PUBLIC"` |
| `git check-ignore -v .env .venv` | each path printed next to the `.gitignore` rule that ignores it |
| `git status` | `nothing to commit, working tree clean` |
| `git log --oneline` | one commit: `chore: pin toolchain and verify local and cloud stack` |

## 5. What went wrong
| ID | Symptom | Cause | Fix |
|---|---|---|---|
| E-M00-1 | `fatal: unable to read config file '/home/pedro/.gitconfig': No such file or directory` | The `git config --global` commands first ran in a Windows terminal, which wrote `C:\Users\pedro\.gitconfig` instead | Ran the three commands again in the Ubuntu terminal |
| E-M00-2 | `error: wrong number of arguments, should be 0` | Two commands were typed on one line, so `git config --list` received `cat` and a path as extra arguments | One command per line |
| E-M00-3 | The prompt kept printing `>` and Enter never ran the heredoc | A `\` at the end of each line joined the lines, so the closing word was no longer `EOF` | Ctrl+C to abort, then pasted the block with no `\` |
| E-M00-4 | `Syntax error: Unexpected string literal "roles/bigquery.dataViewer" at [5:7]` | The role was written in double quotes; `GRANT` needs the role as an identifier in backticks | Backticks around the role, double quotes around the grantee |
| E-M00-5 | `cp: missing destination file operand after '/home/pedro/projects/_contexto-dbt/README.md'` | The destination argument was left out | Added `.` (the current folder) as the destination |
| E-M00-6 | A hand-typed probe contained `dbgen(df=1)` | Typing a long block by hand introduced a typo | Aborted with Ctrl+C before it ran; pasted the block instead |

## 6. Decisions

### D-M00-1 — Grants run on BigQuery
**Context.** M12 needs a warehouse that applies `grants`. DuckDB has no roles. It was
unknown whether the BigQuery sandbox accepts `GRANT`.
**Decision.** The probe succeeded, so M12 runs grants on BigQuery as planned.
**Consequences.** No PostgreSQL and no Docker in the project. Risk R2 is retired.

### D-M00-2 — Work only inside the Linux filesystem
**Context.** Windows and Linux can both see each other's files, but crossing between them
is slow and changes file behaviour (line endings, permissions, letter case).
**Decision.** The repository lives under `~/projects`. Ubuntu is opened from the Start
menu, or with `wsl ~` from PowerShell. Plain `wsl` starts in `/mnt/c/...`.
**Consequences.** Local behaviour matches the Linux CI runners of M15. Windows programs
reach the repo through `\\wsl.localhost\...`.

### D-M00-3 — Optional keys commented out in `.env.example`
**Context.** An empty `KEY=` line still defines the variable, with an empty value. dbt's
`env_var('KEY', 'default')` returns the default only when the variable does not exist.
**Decision.** `GCP_PROJECT_ID=` is present with no value. `TPCH_SCALE_FACTOR` and
`DUCKDB_PATH` are present but commented out.
**Consequences.** Copying the template to `.env` never produces an empty DuckDB path.
Every key is still listed.

### D-M00-4 — GitHub token stored in plain text
**Context.** WSL has no system keyring, so `gh` saves its token unencrypted in
`~/.config/gh/hosts.yml`.
**Decision.** Accepted. The file is outside the repository, and its content is never
pasted anywhere.
**Consequences.** Any process of this Linux user can read the token. Revoking it on
GitHub (Settings, Applications) is the recovery path.

### D-M00-5 — Multi-line blocks are pasted, not typed
**Context.** Three of the six errors came from typing: a stray `\`, two commands on one
line, and a typo.
**Decision.** Every multi-line block is copied and pasted whole. Single commands go one
per line, each run before the next.
**Consequences.** The `>` continuation prompt is expected during a paste. Ctrl+C aborts an
unfinished command.

### D-M00-6 — TPC-H probe as a measured script
**Context.** The milestone asked for a REPL and a hand-noted time and file size.
**Decision.** A heredoc script measures elapsed seconds and file size and prints them.
**Consequences.** The numbers in this chapter were computed, not estimated. The first
run's time was not recorded, so 8.9 s is the time with the extension already
downloaded.

### D-M00-7 — Git identity with the GitHub noreply address
**Context.** Every commit stores its author's name and email forever, and the repository
is public.
**Decision.** `user.email` is the address GitHub provides under Settings, Emails, "Keep my
email addresses private".
**Consequences.** Commits link to the GitHub account without exposing a personal email.

### D-M00-8 — M18 moves to after the exam
**Context.** M00 took 4.0 h against 1.5 h. The plan's rule says: if actual hours exceed
the cumulative estimate by more than 30%, M18 moves to after the exam immediately.
**Decision.** The rule applies. M18 (dashboard and final README) moves to after
2026-10-30.
**Consequences.** M00 to M17 keep 100% exam coverage. Audit A, after M06, re-checks the
drift.

## 7. Exam map
| Outline bullet | Where in this chapter | Question |
|---|---|---|
| None directly (viability gate) | Section 1 | Q1 to Q3 below cover the setup facts later milestones rely on |

## 8. New terms
| Term | Meaning |
|---|---|
| WSL2 | A Windows feature that runs a real Linux kernel in a lightweight virtual machine and connects it to Windows for files, network and terminal |
| Linux distribution | A Linux kernel plus the everyday programs and package manager around it; Ubuntu is one |
| Shell | A program that reads a line of text and runs the program it names; bash is the shell used here |
| Heredoc | A shell construct that feeds the lines up to a closing word into a command as its input |
| Virtual environment | A folder with its own set of Python packages, activated per terminal so that python, pip and dbt resolve to it |
| Adapter | The dbt package that translates dbt's work into one database engine, such as dbt-duckdb or dbt-bigquery |
| Remote | Another copy of the same Git repository, registered by name and URL in `.git/config`; here `origin` is GitHub |
| Staging area | The list of files and contents that the next commit will contain, stored in `.git/index` |
| `.gitignore` | A file of patterns naming untracked files that Git will not stage |
| BigQuery sandbox | The free, no-billing mode of BigQuery: 10 GiB storage, 1 TiB of queries a month, tables expire after 60 days, no DML |
| Service account | A Google Cloud identity for programs; without a key nobody can sign in as it |
| IAM role | A named set of permissions in Google Cloud, such as `roles/bigquery.dataViewer` |
| `GRANT` | A data control language statement that gives an identity a role on a resource |
| TPC-H | A standard benchmark schema of a wholesale business, generated deterministically at a chosen scale factor |

## 9. Check yourself
<details><summary>Q1. The requirements file pins `dbt-core==1.11.*`. What does `dbt --version` saying "Update available" to 1.12 change for this project?</summary>

Nothing. `1.11.*` accepts any 1.11 patch release and never 1.12. The exam tests dbt Core
1.11, so the project stays on 1.11 on purpose. Upgrading "because a newer version exists"
is the tempting wrong move: 1.12 may behave differently from what the exam asks.

</details>

<details><summary>Q2. Why must `.gitignore` be written before `.env` exists, and not added afterwards?</summary>

`.gitignore` only stops Git from staging untracked files. If `.env` were committed once,
adding it to `.gitignore` later would not remove it from history. The value would stay
public in the old commit. Creating the ignore rule first means the file can never be
staged by `git add -A`.

</details>

<details><summary>Q3. The BigQuery sandbox accepted `GRANT`. Why can incremental models still not run there after their first build?</summary>

The sandbox does not support DML (`INSERT`, `UPDATE`, `DELETE`, `MERGE`). An incremental
run after the first one inserts or merges rows, and that is DML. On BigQuery the project
therefore builds with `--full-refresh`, which creates tables with `create table as
select` (DDL). The tempting wrong answer is "grants failing"; grants are DCL and were
accepted.

</details>
