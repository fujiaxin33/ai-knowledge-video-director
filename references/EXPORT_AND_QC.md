# Export and QC

## Final listening release gate

After the final export, listen from first frame to last frame to the actual master. Do not substitute transcript review, ASR confidence, waveform scanning, or segment spot checks. Confirm no word/phrase repeat, restart, failed start, self-correction pair, bad-take/good-take pair, meaning duplicate, or broken ending; approved sections are present; local speed sounds natural; captions/anchors/SFX align; removed objects have no orphan SFX; and voice/picture agree on facts, counts, names, terms, brands, polarity, and relations.

Record reviewer, date, full duration heard, unresolved issues, and PASS/STOP. A technical export PASS cannot override this gate.

## Default delivery

- Target canvas: project requirement, commonly 1920×1080 or 1080×1920.
- 30fps CFR for screen teaching unless another frame rate is explicitly required.
- H.264 High, yuv420p, BT.709 where supported.
- CRF about 18–20 or a verified 8–12Mbps-class export.
- AAC LC, 48kHz.
- Software text readability has priority over smallest file size.
- Information-screen video below 4Mbps is not a quality PASS without stronger visual evidence proving readability.

## Required checks

### Human

Presenter scale, fixed PIP, face/gesture safety, and cross-take continuity.

### Screen

Context completeness, semantic crop, zoom restraint, unique current focus, long Prompt dwell, source lineage, and real result.

### Annotation

Target coverage, alignment/padding, line meaning/count, label visibility, dynamic-target validity, spoken mapping, subtitle and face safety.

### Motion

Explanatory state change, short intermediate state, readable result hold, no black endpoint, no duplicated engine.

### Timing

Speech↔visual, subtitle↔speech, SFX↔impact, integer-frame boundaries, and no old evidence after the concept changes.

### Technical

ffprobe, full decode, expected duration/frame count, flash frames, black/solid frames, subtitle safe zone, loudness/true peak, bitrate, and fine software text at native output size.

## Flash-frame rule

Inspect every overlay/clip boundary at frames `-1 / 0 / +1` (and ±3 for suspect points). Adjacent cover layers must meet on integer frames. Fix source timing/root composition; do not add a fade to hide a one-frame leak. Automatic detectors produce candidates; visual confirmation decides intent.

## Pre-render and final evidence

Use:

- `make_timeline_contact_sheet.py`
- `make_annotation_review_sheet.py`
- `validate_annotation_bounds.py`
- `validate_layout_safe_zones.py`
- `detect_flash_frames.py`
- `ffprobe_quality_check.py`

Keep manifests, reports, contact sheets, hero frames, command outputs, and hashes beside the version. `PASS` requires direct evidence for every requested gate; absence of a detected issue alone is not proof.
