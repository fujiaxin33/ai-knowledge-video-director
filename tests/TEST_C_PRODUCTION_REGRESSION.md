# Test C — Production Regression

## Scenario

A 90-second AI software knowledge video contains:

- a Talking Head take with a repeated word and failed start;
- a screen recording exposing the Windows taskbar;
- a long Prompt that would be unreadable if left on screen;
- the fictional tool name `NimbusFlow`, transcribed as `nimbus flow`;
- an AI-generated warm-white motherboard;
- one result panel that must be boxed precisely.

No video render is required. The test passes only when the Skill produces all eight planning/QC decisions below and the deterministic validators behave as specified.

## Required Skill output

1. **Clean A-roll requirement** — Review transcript and audio together; remove the first `今天` and the failed tail after `然后`; write the source in/out and reason; lock Clean A-roll before any motion timing.
2. **Canonical terminology dictionary** — Build the dictionary from the supplied script/tool asset, not a fixed global list. `NimbusFlow` is canonical; observed variants include `nimbus flow`, `Nimbus Flow`, and `nimbasflow`.
3. **Screen Hygiene fix** — Preserve the NimbusFlow app/page/result context, remove taskbar and unrelated desktop/private UI, and use a clean original freeze or rerecording if a context-preserving crop is impossible.
4. **Long Prompt treatment** — Show the complete Prompt briefly as evidence, then replace it with a short summary/comparison; do not wait for a long scroll.
5. **Transparent asset treatment** — Treat the warm-white motherboard as a library. Rebuild simple cards/labels/lines; extract a complex illustration only with verified transparency; reject the full board as a long main visual.
6. **Annotation Manifest** — Establish full context, then use the integer-pixel target/annotation in `annotation_manifest.json`; require both geometry validation and visual confirmation that the result panel is complete.
7. **PPT Risk judgment** — `visual_beats_bad.json` must be marked `PPT_RISK`; the corrected beat list must clear the detector without requiring equal visual ratios.
8. **Tool identity / Logo plan** — Use the verified NimbusFlow asset once at first introduction as `Logo + NimbusFlow + short role`; do not fabricate or persist it.

## Expected validator behavior

- `validate_canonical_terms.py` fails on `transcript_bad.srt` and passes on `transcript_fixed.srt`.
- `detect_ppt_risk.py` reports at least one risk for `visual_beats_bad.json` and zero for `visual_beats_corrected.json`.
- `validate_annotation_bounds.py` passes `annotation_manifest.json`.

## Result

**PASS.** No render was produced.

- Canonical validator: bad transcript failed with one exact `nimbus flow → NimbusFlow` issue; corrected transcript passed with zero issues.
- PPT Risk detector: bad beat list produced one merged risk covering the 0–12s concept-only stretch; corrected beat list produced zero risks.
- Annotation validator: one integer-pixel annotation passed with zero errors/warnings.
- Both new scripts compiled successfully with Python.
- The planning output above explicitly covers all eight required decisions: Clean A-roll, canonical terms, Screen Hygiene, long Prompt handling, transparent asset routing, Annotation Manifest, PPT Risk, and verified product identity.
