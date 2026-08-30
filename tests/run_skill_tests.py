#!/usr/bin/env python3
"""Run Standard, Whiteboard, internet-native, production-gate, and live-drawing regressions."""

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

    # J — Backward-compatible primary modes plus composable optional layers.
    v13 = FIXTURES / "v1_3"
    j_ok, j = cli("validate_content_routing.py", [v13 / "routing_cases.json"], 0)
    j_bad = read(v13 / "routing_cases.json")
    j_bad["cases"][0]["route"]["layers"] = ["INTERNET_NATIVE_STORYTELLING"]
    j_bad_ok, j_bad_result = cli_data("validate_content_routing.py", j_bad, 1)
    j_pass = j_ok and j_bad_ok and j.get("pass") and not j_bad_result.get("pass")
    tests.append(result("J — Routing A–E + layers", "Standard behavior remains; internet/live layers require explicit traits",
                        f"cases={len(j.get('cases', []))}, bad_route_rejected={not j_bad_result.get('pass')}", j_pass,
                        {"cases": j.get("cases")}))

    # K — Production cases 1, 2, 10, 12: semantic retakes, full listen, speed ripple, gate.
    k_data = read(v13 / "final_listening_pass.json")
    k_ok, k = cli_data("validate_final_listening.py", k_data, 0)
    k_bad_take = json.loads(json.dumps(k_data))
    k_bad_take["semantic_retake_audit"][0]["failed_clause_removed"] = False
    k_bad_take_ok, k_bad_take_r = cli_data("validate_final_listening.py", k_bad_take, 1)
    k_no_listen = json.loads(json.dumps(k_data))
    k_no_listen["clean_aroll_listening"]["start_to_end"] = False
    k_no_listen_ok, k_no_listen_r = cli_data("validate_final_listening.py", k_no_listen, 1)
    k_bad_speed = json.loads(json.dumps(k_data))
    k_bad_speed["local_speed_routing"]["timing_maps_regenerated"]["sfx"] = False
    k_bad_speed_ok, k_bad_speed_r = cli_data("validate_final_listening.py", k_bad_speed, 1)
    k_pass = all((k_ok, k_bad_take_ok, k_no_listen_ok, k_bad_speed_ok, k.get("pass"),
                  not k_bad_take_r.get("pass"), not k_no_listen_r.get("pass"), not k_bad_speed_r.get("pass")))
    tests.append(result("K — Speech Lock and Final Listen", "bad take, incomplete listen, and missing speed ripple fail",
                        f"pass={k.get('pass')}; negative_cases=3", k_pass,
                        {"bad_take_errors": k_bad_take_r.get("errors"), "listen_errors": k_no_listen_r.get("errors"),
                         "speed_errors": k_bad_speed_r.get("errors")}))

    # L — Production case 3: timing can pass while declared visual facts contradict voice.
    l_data = read(FIXTURES / "whiteboard" / "test_e_voice_visual.json")
    for beat in l_data["beats"]:
        beat["voice_facts"] = {"counts": {"items": 4}}
        beat["visual_facts"] = {"counts": {"items": 4}}
    l_ok, l = cli_data("validate_voice_visual_alignment.py", l_data, 0)
    l_bad = json.loads(json.dumps(l_data))
    l_bad["beats"][0]["visual_facts"]["counts"]["items"] = 5
    l_bad_ok, l_bad_r = cli_data("validate_voice_visual_alignment.py", l_bad, 1)
    l_pass = l_ok and l_bad_ok and l.get("pass") and not l_bad_r.get("pass")
    tests.append(result("L — Voice/Visual Semantic Consistency", "voice four vs visual five fails despite valid timing",
                        f"good={l.get('pass')}, mismatch_rejected={not l_bad_r.get('pass')}", l_pass,
                        {"mismatch_errors": l_bad_r.get("errors")}))

    # M — Production cases 4–6, 8–9, 11–12 and live cases D–H.
    m_data = read(v13 / "storyboard_contract_pass.json")
    m_ok, m = cli_data("validate_storyboard_contract.py", m_data, 0)
    negative_mutations = {}
    bad_entry = json.loads(json.dumps(m_data)); bad_entry["beats"][0]["entry_method"] = ""
    negative_mutations["asset_entry"] = bad_entry
    bad_exit = json.loads(json.dumps(m_data)); bad_exit["beats"][0].pop("exit")
    negative_mutations["lifecycle_exit"] = bad_exit
    page_turn = json.loads(json.dumps(m_data)); page_turn["beats"] = [json.loads(json.dumps(m_data["beats"][0])) for _ in range(5)]
    for idx, beat in enumerate(page_turn["beats"]): beat["id"], beat["page_turn_reset"] = f"PAGE-{idx}", True
    negative_mutations["page_turn"] = page_turn
    long_callback = json.loads(json.dumps(m_data)); long_callback["beats"][1]["duration"] = 9.0
    negative_mutations["callback"] = long_callback
    meme = json.loads(json.dumps(m_data)); meme["real_meme_insert"] = {"enabled": True}
    negative_mutations["real_meme"] = meme
    sfx = json.loads(json.dumps(m_data)); sfx["sfx_events"][0]["continuous_bed"] = True
    negative_mutations["sfx"] = sfx
    budget = json.loads(json.dumps(m_data)); budget["pre_render_gate"]["render_budget"]["full_renders_used"] = 3
    negative_mutations["render_budget"] = budget
    no_actor = json.loads(json.dumps(m_data)); no_actor["beats"][0]["hand_actor_action"] = ""
    negative_mutations["hand_actor"] = no_actor
    no_space = json.loads(json.dumps(m_data)); no_space["beats"][0]["anticipatory_empty_space"] = False
    negative_mutations["empty_space"] = no_space
    quality = json.loads(json.dumps(m_data)); quality["beats"][0]["final_quality_preserved"] = False
    negative_mutations["asset_quality"] = quality
    unlocked = json.loads(json.dumps(m_data)); unlocked["speech_locked"] = False
    negative_mutations["speech_lock"] = unlocked
    keyframes = json.loads(json.dumps(m_data)); keyframes["pre_render_gate"]["hero_keyframe_count"] = 4
    negative_mutations["hero_keyframes"] = keyframes
    human = json.loads(json.dumps(m_data)); human["pre_render_gate"]["human_review"]["taste"] = False
    negative_mutations["human_review"] = human
    action = json.loads(json.dumps(m_data)); action["beats"][0]["action_type"] = "wiggle"
    negative_mutations["action_density"] = action
    negative_results = {}
    negatives_ok = True
    for name, fixture in negative_mutations.items():
        ok, payload = cli_data("validate_storyboard_contract.py", fixture, 1)
        negative_results[name] = payload.get("errors", [])
        negatives_ok = negatives_ok and ok and not payload.get("pass")
    reasoned_budget = json.loads(json.dumps(m_data))
    reasoned_budget["pre_render_gate"]["render_budget"] = {
        "full_renders_used": 3, "why_budget_exceeded": "source corruption required a corrected export",
        "renewed_authorization": True}
    reasoned_ok, reasoned = cli_data("validate_storyboard_contract.py", reasoned_budget, 0)
    reasoned_warn = any("render budget exceeded" in item for item in reasoned.get("warnings", []))
    m_pass = m_ok and m.get("pass") and negatives_ok and reasoned_ok and reasoned.get("pass") and reasoned_warn
    tests.append(result("M — Storyboard/Live Contract", "entry, lifecycle, page-turn, callback, meme, SFX, budget, Hand, space, and quality gates work",
                        f"positive={m.get('pass')}, rejected={len(negative_results)}/{len(negative_mutations)}", m_pass,
                        {"negative_errors": negative_results, "reasoned_budget_warnings": reasoned.get("warnings", [])}))

    # N — Production case 7: caption remains subordinate and scaled.
    n_data = read(v13 / "caption_scale_pass.json")
    n_ok, n = cli_data("validate_whiteboard_captions.py", n_data, 0)
    n_bad = json.loads(json.dumps(n_data)); n_bad["captions"][0]["width"] = 1500
    n_bad_ok, n_bad_r = cli_data("validate_whiteboard_captions.py", n_bad, 1)
    n_pass = n_ok and n_bad_ok and n.get("pass") and not n_bad_r.get("pass")
    tests.append(result("N — Caption Scale and Hierarchy", "subordinate caption passes; oversized caption fails",
                        f"good={n.get('pass')}, oversized_rejected={not n_bad_r.get('pass')}", n_pass,
                        {"oversized_errors": n_bad_r.get("errors")}))

    # O — Live cases A–C plus production case 4: while-talking build, absent start, moving Hand, static asset risk.
    o_data = read(FIXTURES / "whiteboard" / "test_d_draw_before_show.json")
    seq = o_data["sequences"][0]
    seq.update({"live_drawing": True, "becoming_stages": ["outline", "fill", "detail"],
                "voice_start": seq["start"], "voice_end": seq["end"], "draw_start": seq["start"], "draw_end": seq["end"],
                "high_quality_asset": True, "final_quality_preserved": True})
    for sample in seq["samples"]: sample["hand_moving"] = True
    o_ok, o = cli_data("validate_draw_on.py", o_data, 0)
    o_present = json.loads(json.dumps(o_data)); o_present["sequences"][0]["samples"][0]["reveal"] = .5
    o_present_ok, o_present_r = cli_data("validate_draw_on.py", o_present, 1)
    o_stopped = json.loads(json.dumps(o_data)); o_stopped["sequences"][0]["samples"][1]["hand_moving"] = False
    o_stopped_ok, o_stopped_r = cli_data("validate_draw_on.py", o_stopped, 1)
    ppt = {"beats": [{"id": "STATIC", "start": 0, "end": 4, "visual_type": "concept motion", "static": True,
                       "high_quality_asset": True, "meaningful_action": False, "progressive_build": False,
                       "character_action": False, "complete_information_single_frame": True}]}
    o_ppt_ok, o_ppt = cli_data("detect_ppt_risk.py", ppt, 0)
    o_pass = all((o_ok, o_present_ok, o_stopped_ok, o_ppt_ok, o.get("pass"),
                  not o_present_r.get("pass"), not o_stopped_r.get("pass"), o_ppt.get("risk_level") == "HIGH"))
    tests.append(result("O — Live Drawing A–H / Static Asset", "meaning becomes during voice; prebuilt start, stopped Hand, and static asset fail",
                        f"live={o.get('pass')}, start_fail={not o_present_r.get('pass')}, hand_fail={not o_stopped_r.get('pass')}, ppt={o_ppt.get('risk_level')}", o_pass,
                        {"start_errors": o_present_r.get("errors"), "hand_errors": o_stopped_r.get("errors"), "ppt_scores": o_ppt.get("beat_scores")}))

    # P — Exact objective matrix: Production 1–12 and Live Drawing A–H.
    p_process = subprocess.run([sys.executable, str(ROOT / "tests" / "run_v1_3_cases.py")],
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        p = json.loads(p_process.stdout)
    except json.JSONDecodeError:
        p = {"pass": False, "cases": [], "errors": [p_process.stdout[-300:] or p_process.stderr[-300:]]}
    p_pass = p_process.returncode == 0 and p.get("pass") and len(p.get("cases", [])) == 20
    tests.append(result("P — Exact v1.3 Case Matrix", "Production 1–12 and Live Drawing A–H all match expected gates",
                        f"cases={len(p.get('cases', []))}, pass={p.get('pass')}", p_pass,
                        {"cases": p.get("cases"), "errors": p.get("errors", [])}))

    payload = {"pass": all(item["status"] == "PASS" for item in tests), "test_count": len(tests), "tests": tests}
    output = json.dumps(payload, ensure_ascii=False, indent=2)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
