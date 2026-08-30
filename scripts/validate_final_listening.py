#!/usr/bin/env python3
"""Validate semantic speech lock, approved coverage, and final listening evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ISSUE_TYPES = {
    "word repeat", "phrase repeat", "phrase restart", "sentence restart", "failed start", "failed lead-in",
    "self correction", "bad take -> good take", "repeated complete take", "meaning duplicate", "broken ending",
}
REQUIRED_COVERAGE = {"hook", "setup", "teaching", "ending"}
REQUIRED_LISTEN_CHECKS = {"stutter", "repeat", "failed start", "unnatural splice", "breath jump", "meaning duplicate", "broken ending"}


def check_listening(label: str, listening: dict, errors: list[str]) -> None:
    if not listening.get("start_to_end"):
        errors.append(f"{label} was not listened to start-to-end")
    if listening.get("asr_only") or listening.get("transcript_only"):
        errors.append(f"{label} ASR/transcript-only review cannot pass")
    if str(listening.get("reviewer", "")).strip().lower() in {"", "automation", "asr"}:
        errors.append(f"{label} human reviewer is required")
    duration = listening.get("master_duration")
    heard = listening.get("duration_heard")
    if isinstance(duration, (int, float)) and isinstance(heard, (int, float)) and heard + .25 < duration:
        errors.append(f"{label} listening duration does not cover the full master")
    checks = {str(value).strip().lower() for value in listening.get("checks", [])}
    missing_checks = sorted(REQUIRED_LISTEN_CHECKS - checks)
    if missing_checks:
        errors.append(f"{label} checks missing: " + ", ".join(missing_checks))
    if listening.get("unresolved_issues"):
        errors.append(f"{label} contains unresolved issues")
    if not listening.get("approved"):
        errors.append(f"{label} is not approved")


def validate(data: dict) -> dict:
    errors, warnings = [], []
    if not data.get("original_source_verified"):
        errors.append("original source lineage is not verified")
    audit = data.get("semantic_retake_audit", [])
    for index, issue in enumerate(audit):
        kind = str(issue.get("issue_type", "")).strip().lower()
        if kind not in ISSUE_TYPES:
            warnings.append(f"audit {index}: unrecognized issue type {kind or '<empty>'}")
        if not issue.get("resolved"):
            errors.append(f"audit {index}: unresolved semantic retake")
        if kind == "bad take -> good take" and not (issue.get("failed_clause_removed") and issue.get("good_take_retained")):
            errors.append(f"audit {index}: bad/good take pair was not resolved at clause level")
    coverage = data.get("approved_script_coverage", {})
    required_coverage = {str(value).strip().lower() for value in data.get("approved_sections", REQUIRED_COVERAGE)}
    missing = sorted(name for name in required_coverage if not coverage.get(name))
    if missing:
        errors.append("approved-script coverage missing: " + ", ".join(missing))
    if not data.get("speech_locked"):
        errors.append("speech is not locked")
    speed = data.get("local_speed_routing", {})
    if speed.get("global_speed_applied"):
        errors.append("global speed routing is prohibited")
    if speed.get("applied"):
        timing = speed.get("timing_maps_regenerated", {})
        missing_maps = [name for name in ("voice", "captions", "visual_anchors", "sfx") if not timing.get(name)]
        if missing_maps:
            errors.append("local speed did not regenerate timing maps: " + ", ".join(missing_maps))
        for segment in speed.get("segments", []):
            rate = float(segment.get("rate", 0))
            kind = str(segment.get("type", "ordinary")).lower()
            protected = segment.get("protected") or kind in {"comedy", "punch", "hero", "ending", "reaction", "meme"}
            if protected and abs(rate - 1.0) > .001:
                errors.append(f"protected segment {segment.get('id', '<unknown>')} is not 1.00x")
            elif kind == "ordinary" and not 1.0 <= rate <= 1.12:
                errors.append(f"ordinary segment {segment.get('id', '<unknown>')} exceeds 1.00–1.12x")
            elif kind == "dense" and not 1.0 <= rate <= 1.20:
                errors.append(f"dense segment {segment.get('id', '<unknown>')} exceeds 1.00–1.20x")

    clean_listen = data.get("clean_aroll_listening", data.get("final_listening", {}))
    check_listening("Clean A-roll", clean_listen, errors)
    if str(data.get("stage", "release")).lower() == "release":
        final_listen = data.get("final_master_listening", data.get("final_listening", {}))
        check_listening("final master", final_listen, errors)
    return {
        "pass": not errors, "errors": errors, "warnings": warnings,
        "audit_count": len(audit), "coverage": coverage,
        "automated_scope": "declared source lineage, retake resolution, approved sections, lock, local-speed ripple, and two listening records",
        "human_review_required": ["actual Clean A-roll listening", "actual final-master listening", "natural cadence", "semantic completeness"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        result = validate(json.loads(args.manifest.read_text(encoding="utf-8-sig")))
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        result = {"pass": False, "errors": [str(exc)], "warnings": []}
    output = json.dumps(result, ensure_ascii=False, indent=2)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    return 0 if result.get("pass") else 1


if __name__ == "__main__":
    sys.exit(main())
