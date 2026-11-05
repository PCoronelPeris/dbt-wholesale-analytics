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
