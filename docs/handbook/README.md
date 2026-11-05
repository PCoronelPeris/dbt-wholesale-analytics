# Project Handbook

How this project was built, one chapter per milestone. Every milestone has the same ID
everywhere: branch `mNN-...`, pull request `MNN — ...`, log entry `## MNN`, and chapter
`mNN-....md`. Errors are `E-MNN-n`, decisions are `D-MNN-n`.

**How to read it.** Start with the chapters in order. Every chapter has the same nine
sections: the problem, where it sits, how it was built, how to verify it, what went
wrong, decisions, exam map, new terms, and check-yourself questions.

**This file is generated** by `make handbook` (`scripts/build_handbook_index.py`).
Do not edit it by hand.

## Chapters

| Chapter | Status | Hours |
|---|---|---|
| [M00 — Prove the stack before building on it](m00-stack-verification.md) | Done · 2026-09-30 | 1.5 estimated · 4.0 actual |
| [M01 — Project skeleton, `dbt_project.yml`, handbook tooling](m01-project-skeleton.md) | Done · 2026-10-09 | 1.5 estimated · 4.0 actual |

## Errors — every failure met while building

| ID | Symptom | Fix | Chapter |
|---|---|---|---|
| E-M00-1 | `fatal: unable to read config file '/home/pedro/.gitconfig': No such file or directory` | Ran the three commands again in the Ubuntu terminal | [M00 — Prove the stack before building on it](m00-stack-verification.md) |
| E-M00-2 | `error: wrong number of arguments, should be 0` | One command per line | [M00 — Prove the stack before building on it](m00-stack-verification.md) |
| E-M00-3 | The prompt kept printing `>` and Enter never ran the heredoc | Ctrl+C to abort, then pasted the block with no `\` | [M00 — Prove the stack before building on it](m00-stack-verification.md) |
| E-M00-4 | `Syntax error: Unexpected string literal "roles/bigquery.dataViewer" at [5:7]` | Backticks around the role, double quotes around the grantee | [M00 — Prove the stack before building on it](m00-stack-verification.md) |
| E-M00-5 | `cp: missing destination file operand after '/home/pedro/projects/_contexto-dbt/README.md'` | Added `.` (the current folder) as the destination | [M00 — Prove the stack before building on it](m00-stack-verification.md) |
| E-M00-6 | A hand-typed probe contained `dbgen(df=1)` | Aborted with Ctrl+C before it ran; pasted the block instead | [M00 — Prove the stack before building on it](m00-stack-verification.md) |
| E-M01-1 | `ls: cannot access 'transform': No such file or directory` | Renamed the folder with mv | [M01 — Project skeleton, `dbt_project.yml`, handbook tooling](m01-project-skeleton.md) |
| E-M01-2 | `mv: cannot stat 'whole_analytics': No such file or directory` | Typed the first letters and used Tab completion | [M01 — Project skeleton, `dbt_project.yml`, handbook tooling](m01-project-skeleton.md) |
| E-M01-3 | `[WARNING]: Configuration paths exist in your dbt_project.yml file which do not apply to any resources.` | Nothing to fix; the warning disappears when models arrive in M04 to M06 | [M01 — Project skeleton, `dbt_project.yml`, handbook tooling](m01-project-skeleton.md) |
| E-M01-4 | `-bash: /home/pedro/projects/dbt-wholesale-analytics: Is a directory` | Typed `cd` before the path | [M01 — Project skeleton, `dbt_project.yml`, handbook tooling](m01-project-skeleton.md) |

## Decisions

| ID | Decision | Chapter |
|---|---|---|
| D-M00-1 | Grants run on BigQuery | [M00 — Prove the stack before building on it](m00-stack-verification.md) |
| D-M00-2 | Work only inside the Linux filesystem | [M00 — Prove the stack before building on it](m00-stack-verification.md) |
| D-M00-3 | Optional keys commented out in `.env.example` | [M00 — Prove the stack before building on it](m00-stack-verification.md) |
| D-M00-4 | GitHub token stored in plain text | [M00 — Prove the stack before building on it](m00-stack-verification.md) |
| D-M00-5 | Multi-line blocks are pasted, not typed | [M00 — Prove the stack before building on it](m00-stack-verification.md) |
| D-M00-6 | TPC-H probe as a measured script | [M00 — Prove the stack before building on it](m00-stack-verification.md) |
| D-M00-7 | Git identity with the GitHub noreply address | [M00 — Prove the stack before building on it](m00-stack-verification.md) |
| D-M00-8 | M18 moves to after the exam | [M00 — Prove the stack before building on it](m00-stack-verification.md) |
| D-M01-1 | `profiles.yml` lives in `transform/` and is committed | [M01 — Project skeleton, `dbt_project.yml`, handbook tooling](m01-project-skeleton.md) |
| D-M01-2 | Delete `transform/.gitignore` and `transform/README.md` | [M01 — Project skeleton, `dbt_project.yml`, handbook tooling](m01-project-skeleton.md) |
| D-M01-3 | Materializations by layer | [M01 — Project skeleton, `dbt_project.yml`, handbook tooling](m01-project-skeleton.md) |
| D-M01-4 | The macro uses `target.name`, with a fallback to `target.schema` | [M01 — Project skeleton, `dbt_project.yml`, handbook tooling](m01-project-skeleton.md) |
| D-M01-5 | The Makefile calls `.venv/bin/*` by absolute path | [M01 — Project skeleton, `dbt_project.yml`, handbook tooling](m01-project-skeleton.md) |
| D-M01-6 | Names are completed with Tab | [M01 — Project skeleton, `dbt_project.yml`, handbook tooling](m01-project-skeleton.md) |
| D-M01-7 | Files are created from the terminal with heredocs | [M01 — Project skeleton, `dbt_project.yml`, handbook tooling](m01-project-skeleton.md) |
| D-M01-8 | `.user.yml` is added to `.gitignore` | [M01 — Project skeleton, `dbt_project.yml`, handbook tooling](m01-project-skeleton.md) |
| D-M01-9 | `make clean` also removes the `.wal` file, and `make setup` does not upgrade pip | [M01 — Project skeleton, `dbt_project.yml`, handbook tooling](m01-project-skeleton.md) |
| D-M01-10 | The index script is run, not imported, and is not compiled in advance | [M01 — Project skeleton, `dbt_project.yml`, handbook tooling](m01-project-skeleton.md) |
| D-M01-11 | `transform/models/.gitkeep` is added | [M01 — Project skeleton, `dbt_project.yml`, handbook tooling](m01-project-skeleton.md) |

## Glossary

| Term | Meaning | First used in |
|---|---|---|
| `.gitignore` | A file of patterns naming untracked files that Git will not stage | [M00](m00-stack-verification.md) |
| `.gitkeep` | An empty file, by convention, that lets Git keep a folder that would otherwise be empty | [M01](m01-project-skeleton.md) |
| `.PHONY` | A Makefile line that tells make a target is a recipe name and not a file | [M01](m01-project-skeleton.md) |
| `dbt_project.yml` | The file that names a dbt project and sets its folder paths, defaults and version limits | [M01](m01-project-skeleton.md) |
| `env_var` | A Jinja function that reads an environment variable and accepts a default value | [M01](m01-project-skeleton.md) |
| `generate_schema_name` | The macro dbt calls to decide the schema of every model; defining it in a project replaces the built-in one | [M01](m01-project-skeleton.md) |
| `GRANT` | A data control language statement that gives an identity a role on a resource | [M00](m00-stack-verification.md) |
| `profiles.yml` | The file that holds connection settings; dbt reads it from the current folder first and then from `~/.dbt` | [M01](m01-project-skeleton.md) |
| `require-dbt-version` | A `dbt_project.yml` key that limits which dbt versions may run the project | [M01](m01-project-skeleton.md) |
| Adapter | The dbt package that translates dbt's work into one database engine, such as dbt-duckdb or dbt-bigquery | [M00](m00-stack-verification.md) |
| BigQuery sandbox | The free, no-billing mode of BigQuery: 10 GiB storage, 1 TiB of queries a month, tables expire after 60 days, no DML | [M00](m00-stack-verification.md) |
| Custom schema | A schema set with `+schema` on a model or folder, which dbt combines with the target through `generate_schema_name` | [M01](m01-project-skeleton.md) |
| dbt project | A folder that contains a `dbt_project.yml` file; dbt finds it in the current folder or in a parent folder, never in a subfolder | [M01](m01-project-skeleton.md) |
| Dry run | A run that prints the commands without executing them; `make -n` does this | [M01](m01-project-skeleton.md) |
| Exit code | The number a command returns when it ends; 0 means success and any other number means failure | [M01](m01-project-skeleton.md) |
| Heredoc | A shell construct that feeds the lines up to a closing word into a command as its input | [M00](m00-stack-verification.md) |
| IAM role | A named set of permissions in Google Cloud, such as `roles/bigquery.dataViewer` | [M00](m00-stack-verification.md) |
| Jinja | The templating language dbt uses; `{{ }}` prints a value and `{% %}` runs logic | [M01](m01-project-skeleton.md) |
| Linux distribution | A Linux kernel plus the everyday programs and package manager around it; Ubuntu is one | [M00](m00-stack-verification.md) |
| Macro | A reusable block of Jinja code, written in a `.sql` file inside `macros/` | [M01](m01-project-skeleton.md) |
| Make target | The name before the colon in a Makefile, such as `test`; `make test` runs its recipe | [M01](m01-project-skeleton.md) |
| Makefile | A file named `Makefile` with named recipes that the program `make` runs | [M01](m01-project-skeleton.md) |
| Materialization | The way dbt stores a model in the warehouse: view, table, ephemeral, incremental and others | [M01](m01-project-skeleton.md) |
| Partial parsing | dbt reuses the saved result of the last parse and re-reads only what changed; a change of target or profile forces a full parse | [M01](m01-project-skeleton.md) |
| Profile | A named block in `profiles.yml`; the project picks one with the `profile` key | [M01](m01-project-skeleton.md) |
| Regular expression | A pattern that describes text to find, used by the index script to locate headings and IDs | [M01](m01-project-skeleton.md) |
| Remote | Another copy of the same Git repository, registered by name and URL in `.git/config`; here `origin` is GitHub | [M00](m00-stack-verification.md) |
| Service account | A Google Cloud identity for programs; without a key nobody can sign in as it | [M00](m00-stack-verification.md) |
| Shell | A program that reads a line of text and runs the program it names; bash is the shell used here | [M00](m00-stack-verification.md) |
| Staging area | The list of files and contents that the next commit will contain, stored in `.git/index` | [M00](m00-stack-verification.md) |
| Target | One named connection setting inside a profile, such as `dev` or `prod`, chosen with `--target` | [M01](m01-project-skeleton.md) |
| Threads | The number of models dbt may build at the same time on a target | [M01](m01-project-skeleton.md) |
| TPC-H | A standard benchmark schema of a wholesale business, generated deterministically at a chosen scale factor | [M00](m00-stack-verification.md) |
| Virtual environment | A folder with its own set of Python packages, activated per terminal so that python, pip and dbt resolve to it | [M00](m00-stack-verification.md) |
| WSL2 | A Windows feature that runs a real Linux kernel in a lightweight virtual machine and connects it to Windows for files, network and terminal | [M00](m00-stack-verification.md) |
| YAML | A text format of keys and values where indentation, made only of spaces, shows nesting | [M01](m01-project-skeleton.md) |
