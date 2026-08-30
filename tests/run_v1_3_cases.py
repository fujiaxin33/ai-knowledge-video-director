#!/usr/bin/env python3
"""Run the exact abstract Production 1–12 and Live Drawing A–H cases."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from detect_ppt_risk import score_beats, DEFAULT_CONCEPT_TYPES  # noqa: E402
from validate_draw_on import validate as validate_draw  # noqa: E402
from validate_final_listening import validate as validate_listening  # noqa: E402
from validate_storyboard_contract import validate as validate_storyboard  # noqa: E402
from validate_voice_visual_alignment import validate as validate_alignment  # noqa: E402
from validate_whiteboard_captions import validate as validate_captions  # noqa: E402


FIXTURES = ROOT / "tests" / "fixtures" / "v1_3"


def read(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8-sig"))


def row(case_id: str, expected: str, passed: bool, evidence: object) -> dict:
    return {"case": case_id, "expected": expected, "status": "PASS" if passed else "FAIL", "evidence": evidence}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    results = []
    listening = read("final_listening_pass.json")
    storyboard = read("storyboard_contract_pass.json")

    # Production 1 — Bad Take -> Good Take must be resolved at clause level.
    data = copy.deepcopy(listening)
    data["semantic_retake_audit"][0]["failed_clause_removed"] = False
    out = validate_listening(data)
    results.append(row("Production-1", "unremoved failed clause fails", not out["pass"], out["errors"]))

    # Production 2 — Approved ending cannot be removed for duration.
    data = copy.deepcopy(listening)
    data["approved_script_coverage"]["ending"] = False
    out = validate_listening(data)
    results.append(row("Production-2", "missing approved ending fails", not out["pass"], out["errors"]))

    # Production 3 — voice count and visual count must match.
    alignment = {"beats": [{
        "id": "COUNT", "voice_start": 0, "voice_end": 2, "visual_start": 0, "visual_end": 2,
        "intended_meaning": "four characters", "visual_event": "characters appear",
        "voice_facts": {"counts": {"characters": 4}}, "visual_facts": {"counts": {"characters": 5}}
    }]}
    out = validate_alignment(alignment)
    results.append(row("Production-3", "voice four vs visual five fails", not out["pass"], out["errors"]))

    # Production 4 — mountain -> temple -> monk is one valid semantic chain.
    data = copy.deepcopy(storyboard)
    beat = data["beats"][0]
    beat.update({"id": "MOUNTAIN-TEMPLE-MONK", "progressive_build": True, "semantic_chain_id": "one-mountain-location"})
    out = validate_storyboard(data)
    results.append(row("Production-4", "semantic object hierarchy may progressively build", out["pass"], out["errors"]))

    # Production 5 — independent examples reset rather than accumulate.
    data = copy.deepcopy(storyboard)
    data["beats"] = []
    for index in range(3):
        beat = copy.deepcopy(storyboard["beats"][1])
        beat.update({"id": f"EXAMPLE-{index + 1}", "independent_example": True, "reset_before": True})
        data["beats"].append(beat)
    good = validate_storyboard(data)
    data["beats"][1]["reset_before"] = False
    bad = validate_storyboard(data)
    results.append(row("Production-5", "independent examples pass only with reset", good["pass"] and not bad["pass"], bad["errors"]))

    # Production 6 — high-quality assets cannot degrade to placeholders.
    data = copy.deepcopy(storyboard)
    data["beats"][0]["final_quality_preserved"] = False
    out = validate_storyboard(data)
    results.append(row("Production-6", "asset-quality degradation fails", not out["pass"], out["errors"]))

    # Production 7 — captions cannot become primary.
    captions = read("caption_scale_pass.json")
    captions["captions"][0]["primary_visual_area_ratio"] = .01
    out = validate_captions(captions)
    results.append(row("Production-7", "caption larger than primary visual fails", not out["pass"], out["errors"]))

    # Production 8 — real meme defaults OFF; unauthorized enablement fails.
    good = validate_storyboard(copy.deepcopy(storyboard))
    data = copy.deepcopy(storyboard)
    data["real_meme_insert"] = {"enabled": True}
    bad = validate_storyboard(data)
    results.append(row("Production-8", "real meme OFF passes and unauthorized ON fails", good["pass"] and not bad["pass"], bad["errors"]))

    # Production 9 — static comic card remains HIGH risk.
    static = [{"id": "STATIC-COMIC", "start": 0, "end": 4, "visual_type": "concept motion", "static": True,
               "same_composition_duration": 4, "high_quality_asset": True, "meaningful_action": False,
               "character_action": False, "progressive_build": False, "complete_information_single_frame": True}]
    scored = score_beats(static, DEFAULT_CONCEPT_TYPES)
    results.append(row("Production-9", "static high-quality comic is HIGH risk", scored[0]["level"] == "HIGH", scored[0]))

    # Production 10 — callback cannot reteach for too long.
    data = copy.deepcopy(storyboard)
    data["beats"][1]["duration"] = 8.0
    out = validate_storyboard(data)
    results.append(row("Production-10", "callback beyond 6s fails", not out["pass"], out["errors"]))

    # Production 11 — punch requires both Action and Reaction.
    data = copy.deepcopy(storyboard)
    data["beats"][0]["reaction"] = ""
    out = validate_storyboard(data)
    results.append(row("Production-11", "punch without reaction fails", not out["pass"], out["errors"]))

    # Production 12 — ASR cannot approve a repeat the ear has not reviewed.
    data = copy.deepcopy(listening)
    data["clean_aroll_listening"]["asr_only"] = True
    data["semantic_retake_audit"].append({"issue_type": "Repeated Complete Take", "resolved": False})
    out = validate_listening(data)
    results.append(row("Production-12", "ASR-only review with unresolved repeat fails", not out["pass"], out["errors"]))

    # Shared Live Drawing sequence.
    draw = {
        "max_tip_distance": 40,
        "sequences": [{
            "id": "MOUNTAIN", "mode": "true draw", "start": 0, "end": 3, "voice_start": 0, "voice_end": 3,
            "draw_start": 0, "draw_end": 3, "live_drawing": True,
            "becoming_stages": ["mountain", "temple", "monk"], "final_quality_preserved": True,
            "samples": [
                {"reveal": 0, "hand_present": True, "hand_moving": True, "hand_tip": [0, 0], "reveal_front": [0, 0]},
                {"reveal": .5, "hand_present": True, "hand_moving": True, "hand_tip": [50, 50], "reveal_front": [52, 50]},
                {"reveal": 1, "hand_present": True, "hand_moving": True, "hand_tip": [100, 100], "reveal_front": [100, 100]}
            ]
        }]
    }

    out = validate_draw(copy.deepcopy(draw))
    results.append(row("Live-A", "Draw While Talking semantic chain passes", out["pass"], out["errors"]))

    data = copy.deepcopy(draw)
    for sample in data["sequences"][0]["samples"]:
        sample["reveal"] = 1.0
    out = validate_draw(data)
    results.append(row("Live-B", "complete visual before voice fails", not out["pass"], out["errors"]))

    data = copy.deepcopy(draw); data["sequences"][0]["samples"][1]["hand_tip"] = [0, 0]
    data["sequences"][0]["samples"][1]["reveal_front"] = [500, 500]
    out = validate_draw(data)
    results.append(row("Live-C", "Hand and reveal on opposite sides fail", not out["pass"], out["errors"]))

    data = copy.deepcopy(storyboard); data["beats"] = [copy.deepcopy(storyboard["beats"][0]) for _ in range(5)]
    for index, beat in enumerate(data["beats"]): beat.update({"id": f"PAGE-{index + 1}", "page_turn_reset": True})
    out = validate_storyboard(data)
    results.append(row("Live-D", "five Clear Canvas -> New Frame beats fail", not out["pass"], out["errors"]))

    data = copy.deepcopy(storyboard); beat = data["beats"][0]
    beat.update({"empty_space_ratio": .70, "hand_entry_delay": 1.0, "static_wait_duration": 0.0})
    out = validate_storyboard(data)
    results.append(row("Live-E", "70% empty space with imminent Hand passes", out["pass"], out["errors"]))

    data = copy.deepcopy(storyboard); beat = data["beats"][0]
    beat.update({"empty_space_ratio": .70, "hand_entry_delay": 5.0, "static_wait_duration": 5.0})
    out = validate_storyboard(data)
    results.append(row("Live-F", "70% empty space with static character for 5s fails", not out["pass"], out["errors"]))

    data = copy.deepcopy(storyboard); beat = data["beats"][0]
    beat.update({"knowledge_residue_reason": "term is written beside the story and anchors the next relation", "exit": "transform"})
    out = validate_storyboard(data)
    results.append(row("Live-G", "knowledge term emerging beside story passes", out["pass"], out["errors"]))

    data = copy.deepcopy(storyboard); data["hero_card_for_every_point"] = True
    out = validate_storyboard(data)
    results.append(row("Live-H", "Hero Card for every point fails", not out["pass"], out["errors"]))

    payload = {"pass": all(item["status"] == "PASS" for item in results), "case_count": len(results), "cases": results}
    output = json.dumps(payload, ensure_ascii=False, indent=2)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
