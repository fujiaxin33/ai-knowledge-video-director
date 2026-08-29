#!/usr/bin/env python3
"""Run Standard regressions A-C and Whiteboard behavioral tests D-I."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURES = ROOT / "tests" / "fixtures"


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def cli(script: str, args: list[Path | str], expected: int) -> tuple[bool, dict]:
    command = [sys.executable, str(SCRIPTS / script), *[str(value) for value in args]]
    process = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        payload = json.loads(process.stdout)
    except json.JSONDecodeError:
        payload = {"pass": False, "errors": [process.stdout[-300:] or process.stderr[-300:]]}
    return process.returncode == expected, payload


def cli_data(script: str, data: dict, expected: int) -> tuple[bool, dict]:
    """Run a validator against an isolated negative/positive JSON mutation."""
    with tempfile.TemporaryDirectory(prefix="skill-validator-") as folder:
        path = Path(folder) / "fixture.json"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return cli(script, [path], expected)


def result(name: str, expected: str, actual: str, passed: bool, evidence: dict) -> dict:
    return {"test": name, "expected": expected, "actual": actual,
            "status": "PASS" if passed else "FAIL", "evidence": evidence}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    tests = []

    # A — Standard routing remains available and is not polluted by Whiteboard.
    a = read(FIXTURES / "test_a" / "standard_plan.json")
    a_pass = (a["mode"] == "STANDARD" and a["primary_carrier"] == "Original Screen"
              and a["screen_grammar"] == ["Live", "Freeze", "Explain", "Continue"]
              and not a["whiteboard_forced"])
    tests.append(result("A — Standard routing regression", "desktop tutorial stays STANDARD with real screen grammar",
                        f"mode={a['mode']}, carrier={a['primary_carrier']}, whiteboard_forced={a['whiteboard_forced']}",
                        a_pass, {"screen_grammar": a["screen_grammar"]}))

    # B — Existing annotation precision behavior still distinguishes bad/good geometry.
    b_bad_ok, b_bad = cli("validate_annotation_bounds.py", [FIXTURES / "test_b" / "annotation_bad.json"], 1)
    b_good_ok, b_good = cli("validate_annotation_bounds.py", [FIXTURES / "test_b" / "annotation_corrected.json"], 0)
    b_pass = b_bad_ok and b_good_ok and not b_bad.get("pass") and b_good.get("pass")
    tests.append(result("B — Annotation precision regression", "bad geometry fails and corrected geometry passes",
                        f"bad_pass={b_bad.get('pass')}, corrected_pass={b_good.get('pass')}", b_pass,
                        {"bad_error_count": len(b_bad.get("errors", [])), "corrected_error_count": len(b_good.get("errors", []))}))

    # C — Existing production validators remain functional.
    c_root = FIXTURES / "test_c"
    c_bad_terms_ok, c_bad_terms = cli("validate_canonical_terms.py", [c_root / "CANONICAL_TERMS.json", c_root / "transcript_bad.srt"], 1)
    c_good_terms_ok, c_good_terms = cli("validate_canonical_terms.py", [c_root / "CANONICAL_TERMS.json", c_root / "transcript_fixed.srt"], 0)
    c_bad_ppt_ok, c_bad_ppt = cli("detect_ppt_risk.py", [c_root / "visual_beats_bad.json", "--fail-on-risk"], 1)
    c_good_ppt_ok, c_good_ppt = cli("detect_ppt_risk.py", [c_root / "visual_beats_corrected.json", "--fail-on-risk"], 0)
    c_ann_ok, c_ann = cli("validate_annotation_bounds.py", [c_root / "annotation_manifest.json"], 0)
    c_pass = all((c_bad_terms_ok, c_good_terms_ok, c_bad_ppt_ok, c_good_ppt_ok, c_ann_ok))
    tests.append(result("C — Production regression", "canonical bad/fixed, PPT bad/fixed, and annotation validators retain behavior",
                        f"term issues {c_bad_terms.get('issue_count')}→{c_good_terms.get('issue_count')}; "
                        f"PPT {c_bad_ppt.get('risk_level')}→{c_good_ppt.get('risk_level')}; annotation={c_ann.get('pass')}",
                        c_pass, {"bad_term_issues": c_bad_terms.get("issue_count"), "fixed_term_issues": c_good_terms.get("issue_count"),
                                 "bad_ppt_level": c_bad_ppt.get("risk_level"), "fixed_ppt_level": c_good_ppt.get("risk_level")}))

    # D — Draw Before Show on a new coffee process.
    d_path = FIXTURES / "whiteboard" / "test_d_draw_before_show.json"
    d_data = read(d_path)
    d_cli_ok, d = cli("validate_draw_on.py", [d_path], 0)
    d_bad_data = json.loads(json.dumps(d_data))
    d_bad_data["sequences"][0]["samples"][1]["hand_tip"] = [900, 900]
    d_bad_ok, d_bad = cli_data("validate_draw_on.py", d_bad_data, 1)
    d_pass = (d_cli_ok and d_bad_ok and d.get("pass") and not d_bad.get("pass")
              and d_data["progressive_nested_scene"] and not d_data["complete_image_sequence"])
    tests.append(result("D — Draw Before Show", "cup→coffee→steam→drinker builds progressively, not four complete images",
                        f"sequence_count={d.get('sequence_count')}, progressive={d_data['progressive_nested_scene']}", d_pass,
                        {"scene_order": d_data["scene_order"], "good_pass": d.get("pass"),
                         "fake_handwriting_rejected": not d_bad.get("pass")}))

    # E — Voice/visual A/B/C contract.
    e_path = FIXTURES / "whiteboard" / "test_e_voice_visual.json"
    e_data = read(e_path)
    e_cli_ok, e = cli("validate_voice_visual_alignment.py", [e_path], 0)
    e_bad_data = json.loads(json.dumps(e_data))
    e_bad_data["beats"][1]["reveal_time"] = 4.1
    e_bad_ok, e_bad = cli_data("validate_voice_visual_alignment.py", e_bad_data, 1)
    e_pass = (e_cli_ok and e_bad_ok and e.get("pass") and not e_bad.get("pass")
              and all(row["status"] in {"PASS", "WARN"} for row in e.get("beats", [])))
    tests.append(result("E — Voice Visual", "A/B/C reveals stay within their own voice/keyword spans",
                        f"beat statuses={[row['status'] for row in e.get('beats', [])]}", e_pass,
                        {"beat_count": e.get("beat_count"), "error_count": len(e.get("errors", [])),
                         "late_reveal_rejected": not e_bad.get("pass")}))

    # F — Comedy requires the full five-phase situation plus anchor/SFX continuity.
    f_path = FIXTURES / "whiteboard" / "test_f_comedy.json"
    f = read(f_path)
    phases = ["setup", "anticipation", "pause", "impact", "reaction"]
    punch = f["punches"][0]
    phase_ok = all(name in punch for name in phases) and all(
        float(punch[phases[i]]["end"]) <= float(punch[phases[i + 1]]["start"]) for i in range(len(phases) - 1))
    anchor_ok, anchor = cli("validate_character_anchors.py", [f_path], 0)
    sfx_ok, sfx = cli("validate_sfx_timing.py", [f_path], 0)
    f_bad_anchor = json.loads(json.dumps(f))
    f_bad_anchor["characters"][0]["states"][1]["anchor_x"] = 700
    bad_anchor_ok, bad_anchor = cli_data("validate_character_anchors.py", f_bad_anchor, 1)
    f_bad_sfx = json.loads(json.dumps(f))
    f_bad_sfx["events"][0]["sfx_time"] = 2.4
    bad_sfx_ok, bad_sfx = cli_data("validate_sfx_timing.py", f_bad_sfx, 1)
    f_pass = (phase_ok and punch["visual_situation"] and anchor_ok and sfx_ok
              and bad_anchor_ok and bad_sfx_ok and anchor.get("pass") and sfx.get("pass")
              and not bad_anchor.get("pass") and not bad_sfx.get("pass"))
    tests.append(result("F — Comedy", "Setup→Anticipation→Pause→Impact→Reaction with anchored character and synced SFX",
                        f"phases={phases}, anchor={anchor.get('pass')}, sfx={sfx.get('pass')}", f_pass,
                        {"knowledge_job": punch["knowledge_job"], "sfx_statuses": [row["status"] for row in sfx.get("events", [])],
                         "anchor_jump_rejected": not bad_anchor.get("pass"), "late_sfx_rejected": not bad_sfx.get("pass")}))

    # G — PPT/UI risk scores cards higher than character action; Knowledge Hero is exempt.
    g_high_path = FIXTURES / "whiteboard" / "test_g_ppt_high.json"
    g_low_path = FIXTURES / "whiteboard" / "test_g_ppt_low.json"
    g_high_ok, g_high = cli("detect_ppt_risk.py", [g_high_path, "--fail-on-risk"], 1)
    g_low_ok, g_low = cli("detect_ppt_risk.py", [g_low_path, "--fail-on-risk"], 0)
    hero = next(item for item in g_low.get("beat_scores", []) if item["id"] == "HERO")
    g_pass = g_high_ok and g_low_ok and g_high.get("risk_level") == "HIGH" and g_low.get("risk_level") == "LOW" and hero["level"] == "LOW"
    tests.append(result("G — PPT Risk", "card/UI plan scores HIGH; action plan LOW; Knowledge Hero remains LOW",
                        f"card={g_high.get('risk_level')}, action={g_low.get('risk_level')}, hero={hero['level']}", g_pass,
                        {"high_scores": g_high.get("beat_scores"), "hero_reasons": hero["reasons"]}))

    # H — Long voice becomes one short semantic caption.
    h_path = FIXTURES / "whiteboard" / "test_h_captions.json"
    h_data = read(h_path)
    h_cli_ok, h = cli("validate_whiteboard_captions.py", [h_path], 0)
    h_bad_data = json.loads(json.dumps(h_data))
    h_bad_data["captions"][0]["line_count"] = 2
    h_bad_data["captions"][0]["semantic"] = False
    h_bad_ok, h_bad = cli_data("validate_whiteboard_captions.py", h_bad_data, 1)
    caption = h_data["captions"][0]["text"]
    h_pass = (h_cli_ok and h_bad_ok and h.get("pass") and not h_bad.get("pass")
              and len(caption) < len(h_data["voice"]) and h_data["captions"][0]["semantic"])
    tests.append(result("H — Semantic Caption", "long voice maps to a short, semantic, single-line caption",
                        f"voice_chars={len(h_data['voice'])}, caption_chars={len(caption)}, validator={h.get('pass')}", h_pass,
                        {"caption": caption, "warning_count": len(h.get("warnings", [])),
                         "transcript_caption_rejected": not h_bad.get("pass")}))

    # I — New story shell proves no EP template leakage.
    i_data = read(FIXTURES / "whiteboard" / "test_i_generalization.json")
    serialized = json.dumps(i_data, ensure_ascii=False).lower()
    banned = ["奶茶", "考试", "恋爱", "公司", "semantic search", "rag", "llm"]
    found = [term for term in banned if term.lower() in serialized]
    i_pass = (i_data["mode"] == "WHITEBOARD_STORYTELLING" and len(i_data["progressive_scene"]) >= 4
              and len(i_data["character_arc"]) >= 5 and not i_data["uses_repeated_cards"]
              and not i_data["uses_complete_png_sequence"] and not found)
    tests.append(result("I — Story Shell Generalization", "new topic uses a new shell and the directing method, not EP story objects",
                        f"topic={i_data['topic']}, steps={len(i_data['progressive_scene'])}, banned_found={found}", i_pass,
                        {"story_shell": i_data["story_shell"], "knowledge_hero": i_data["knowledge_hero"]}))

    payload = {"pass": all(item["status"] == "PASS" for item in tests), "test_count": len(tests), "tests": tests}
    output = json.dumps(payload, ensure_ascii=False, indent=2)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
