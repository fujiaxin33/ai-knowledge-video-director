#!/usr/bin/env python3
"""Validate project copy against a project-specific canonical term dictionary."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def load_terms(path: Path) -> dict[str, list[str]]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    terms = data.get("terms", data)
    if not isinstance(terms, dict) or not terms:
        raise ValueError("dictionary must contain a non-empty 'terms' object")
    normalized: dict[str, list[str]] = {}
    for canonical, variants in terms.items():
        if not isinstance(canonical, str) or not canonical.strip():
            raise ValueError("canonical term names must be non-empty strings")
        if not isinstance(variants, list) or not all(isinstance(v, str) for v in variants):
            raise ValueError(f"variants for {canonical!r} must be a string list")
        normalized[canonical] = [v for v in variants if v and v != canonical]
    return normalized


def pattern_for(value: str, *, ignore_case: bool = False) -> re.Pattern[str]:
    escaped = re.escape(value)
    if re.fullmatch(r"[A-Za-z0-9_ .+/#-]+", value):
        escaped = rf"(?<![A-Za-z0-9_]){escaped}(?![A-Za-z0-9_])"
    return re.compile(escaped, re.IGNORECASE if ignore_case else 0)


def line_column(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    last = text.rfind("\n", 0, offset)
    return line, offset - last


def validate(dictionary: Path, files: list[Path]) -> dict:
    terms = load_terms(dictionary)
    issues: list[dict] = []
    seen: set[tuple[str, int, int, str, str]] = set()

    for file_path in files:
        text = file_path.read_text(encoding="utf-8-sig")
        for canonical, variants in terms.items():
            candidates = [(variant, pattern_for(variant)) for variant in variants]
            candidates.append(("wrong_case", pattern_for(canonical, ignore_case=True)))
            for label, pattern in candidates:
                for match in pattern.finditer(text):
                    actual = match.group(0)
                    if actual == canonical:
                        continue
                    line, column = line_column(text, match.start())
                    key = (str(file_path), line, column, actual, canonical)
                    if key in seen:
                        continue
                    seen.add(key)
                    issues.append(
                        {
                            "file": str(file_path),
                            "line": line,
                            "column": column,
                            "found": actual,
                            "canonical": canonical,
                            "source": label,
                        }
                    )

    return {
        "pass": not issues,
        "dictionary": str(dictionary),
        "files": [str(p) for p in files],
        "canonical_term_count": len(terms),
        "issue_count": len(issues),
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dictionary", type=Path)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    try:
        result = validate(args.dictionary, args.files)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {"pass": False, "errors": [str(exc)], "issues": []}

    output = json.dumps(result, ensure_ascii=False, indent=2)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    return 0 if result.get("pass") else 1


if __name__ == "__main__":
    sys.exit(main())
