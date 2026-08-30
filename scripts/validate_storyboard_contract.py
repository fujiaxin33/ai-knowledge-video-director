#!/usr/bin/env python3
"""Validate v1.3 action-state, punch, lifecycle, scale, and live-drawing declarations."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ENTRY_METHODS = {"true draw", "mask draw", "assembly build", "hand reveal", "comedy pop", "transform", "erase / reset", "real screen"}
REQUIRED_BEAT_FIELDS = ("entry", "action", "impact", "reaction", "hold", "exit")
ACTION_TYPES = {"draw", "move", "enter", "exit", "search", "hit", "reaction", "transform", "erase", "compare", "connect", "write"}
HUMAN_REVIEW_FIELDS = {"comedy", "internet_naturalness", "taste", "character_expression", "cultural_recognition", "release"}


def validate(data: dict) -> dict:
    errors, warnings, rows = [], [], []
    beats = data.get("beats", [])
    layers = {str(value).upper() for value in data.get("layers", [])}
    if not beats:
        errors.append("storyboard must contain beats")
    if data.get("hero_card_for_every_point"):
        errors.append("every knowledge point is routed to a Hero Card")
    duration = float(data.get("duration_seconds", 0))
    punch_count = sum(1 for beat in beats if beat.get("is_punch"))
    if 60 <= duration <= 150 and not 2 <= punch_count <= 6:
        warnings.append(f"internet punch count {punch_count} is outside the suggested 2–6 range")
    for segment in data.get("story_segments", []):
        segment_duration = float(segment.get("duration", 0))
        if 10 <= segment_duration <= 20 and not segment.get("drawing_curiosity_event"):
            warnings.append(f"story segment {segment.get('id', '<unknown>')} has no drawing-curiosity event")
    real_meme = data.get("real_meme_insert", {})
    if real_meme.get("enabled") and not (real_meme.get("explicitly_authorized") and real_meme.get("source_rights_recorded") and real_meme.get("max_duration_seconds")):
        errors.append("real meme insert lacks explicit authorization, source/rights, or duration limit")
    for index, event in enumerate(data.get("sfx_events", [])):
        if event.get("continuous_bed"):
            errors.append(f"SFX {index}: continuous texture/noise bed is prohibited")
        if event.get("orphaned"):
            errors.append(f"SFX {index}: orphaned event has no visible action")
        if event.get("voice_priority") is False:
            errors.append(f"SFX {index}: voice is not primary")
    gate = data.get("pre_render_gate", {})
    if data.get("require_v1_3_gate"):
        if not data.get("speech_locked"):
            errors.append("Storyboard/render gate cannot pass before A-roll LOCK")
        if not gate.get("hero_keyframes_approved"):
            errors.append("hero keyframes are not human-approved")
        keyframe_count = int(gate.get("hero_keyframe_count", 0))
        if not 6 <= keyframe_count <= 10:
            errors.append("complex internet-native gate requires 6–10 hero keyframes")
        budget = gate.get("render_budget", {})
        full_renders = int(budget.get("full_renders_used", 0))
        if full_renders >= 3:
            if not str(budget.get("why_budget_exceeded", "")).strip() or not budget.get("renewed_authorization"):
                errors.append("third full render requires reason and renewed authorization")
            else:
                warnings.append("render budget exceeded with recorded reason and renewed authorization")
        if not gate.get("human_approved"):
            errors.append("human pre-render approval is missing")
        human_review = gate.get("human_review", {})
        missing_human = sorted(field for field in HUMAN_REVIEW_FIELDS if not human_review.get(field))
        if missing_human:
            errors.append("human review fields missing: " + ", ".join(missing_human))
    page_turns = 0
    for index, beat in enumerate(beats):
        bid = str(beat.get("id", index))
        item_errors, item_warnings = [], []
        for field in REQUIRED_BEAT_FIELDS:
            if field not in beat or not str(beat[field]).strip():
                item_errors.append(f"missing {field}")
        method = str(beat.get("entry_method", "")).strip().lower()
        if beat.get("uses_complete_asset") and method not in ENTRY_METHODS:
            item_errors.append("complete asset lacks a supported entry method")
        if beat.get("high_quality_asset") and not beat.get("final_quality_preserved"):
            item_errors.append("high-quality final asset is not preserved")
        if beat.get("only_text_arrow_box"):
            item_errors.append("beat is only Text + Arrow + Box")
        if not beat.get("knowledge_hero"):
            action_type = str(beat.get("action_type", "")).strip().lower()
            if action_type not in ACTION_TYPES:
                item_errors.append("non-Hero beat lacks a meaningful action type")
        if beat.get("is_punch"):
            for field in ("setup", "action", "impact", "reaction", "knowledge_purpose"):
                if not str(beat.get(field, "")).strip():
                    item_errors.append(f"punch missing {field}")
        primary = beat.get("primary_scale_ratio")
        if primary is not None and not .35 <= float(primary) <= .90:
            item_errors.append("primary scale is outside the story/hero/impact system")
        if beat.get("caption_primary"):
            item_errors.append("caption is declared primary over action")
        support_ratio, caption_ratio = beat.get("supporting_scale_ratio"), beat.get("caption_height_ratio")
        if support_ratio is not None and caption_ratio is not None and float(support_ratio) < float(caption_ratio):
            item_errors.append("supporting element is smaller than the caption")
        if beat.get("independent_example") and not beat.get("reset_before"):
            item_errors.append("independent example lacks semantic reset")
        if beat.get("progressive_build") and not str(beat.get("semantic_chain_id", "")).strip():
            item_errors.append("progressive build lacks a semantic scene/object chain")
        if beat.get("unjustified_residue"):
            item_errors.append("previous-scene residue has no story reason")
        if beat.get("page_turn_reset"):
            page_turns += 1
        else:
            page_turns = 0
        if page_turns >= 5:
            item_errors.append("five consecutive page-turn resets")
        if beat.get("callback") and float(beat.get("duration", 0)) > float(beat.get("callback_limit", 6.0)):
            item_errors.append("callback exceeds declared duration limit")

        if "LIVE_DRAWING_STORYTELLING" in layers and beat.get("live_drawing", False):
            for field in ("spoken_cue", "hand_actor_action", "transition"):
                if not str(beat.get(field, "")).strip():
                    item_errors.append(f"live drawing missing {field}")
            stages = beat.get("becoming_stages", [])
            if len(stages) < 2:
                item_errors.append("live drawing needs at least two becoming states")
            if not beat.get("hand_tip_sync"):
                item_errors.append("Hand tip/reveal front sync is not declared")
            if not beat.get("anticipatory_empty_space"):
                item_errors.append("anticipatory empty space is not declared")
            empty_ratio = float(beat.get("empty_space_ratio", 0))
            hand_delay = float(beat.get("hand_entry_delay", 0))
            if empty_ratio >= .70 and not (0.5 <= hand_delay <= 2.0):
                item_errors.append("large empty space is not anticipatory within 0.5–2.0s")
            if empty_ratio >= .70 and float(beat.get("static_wait_duration", 0)) >= 5.0:
                item_errors.append("large empty space holds a static character for 5s")
            if beat.get("reveal_continues_after_hand_stop"):
                item_errors.append("reveal continues after Hand stops")
            if not beat.get("knowledge_residue_reason") and str(beat.get("exit", "")).lower() not in {"erase", "clear", "reset", "exit"}:
                item_warnings.append("live drawing residue has no stated reason")
        errors.extend(f"{bid}: {message}" for message in item_errors)
        warnings.extend(f"{bid}: {message}" for message in item_warnings)
        rows.append({"id": bid, "status": "FAIL" if item_errors else ("WARN" if item_warnings else "PASS"),
                     "errors": item_errors, "warnings": item_warnings})
    return {
        "pass": not errors, "beat_count": len(beats), "errors": errors, "warnings": warnings, "beats": rows,
        "automated_scope": "declared action states, punch structure, entry methods, asset quality, scale, page turns, callbacks, and live-drawing contracts",
        "human_review_required": ["story clarity", "comedy timing", "drawing curiosity", "visual taste", "whether residue improves learning"],
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
