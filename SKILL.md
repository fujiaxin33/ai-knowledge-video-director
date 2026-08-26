---
name: ai-knowledge-video-director
description: Direct, plan, edit, and audit AI knowledge videos and real software tutorials, including Prompt, Codex, Obsidian, ChatGPT, GitHub Skill, screen-recording, teaching-motion, annotation, subtitle, audio, ChatCut, HyperFrames, and Remotion workflows. Use for horizontal courses or vertical knowledge videos; do not use for unrelated vlogs, fiction, music edits, entertainment montages, or effects-led films.
---

# AI Knowledge Video Director

Turn an approved teaching idea and original media into a readable, evidence-led video through `Pre-production -> First Cut -> Polish -> Final`. Preserve user intent, approved facts, original media, prior versions, and explicit authorization boundaries.

## Start here

1. Read the script, asset inventory, references, and any project `DESIGN.md` / editing rules.
2. Classify the content level and canvas with [CONTENT_AND_FORMAT_ROUTER.md](references/CONTENT_AND_FORMAT_ROUTER.md).
3. Choose a small stable layout family with [LAYOUT_SYSTEM.md](references/LAYOUT_SYSTEM.md).
4. Produce the Phase B documents from `templates/` before editing.
5. Audit original takes and screens with [TAKE_AND_MEDIA_SELECTION.md](references/TAKE_AND_MEDIA_SELECTION.md).
6. Route each visual beat to Human, Original Screen, HyperFrames, Remotion, or `NO EFFECT`; one main carrier per beat.
7. For software teaching, read [SCREEN_DIRECTING.md](references/SCREEN_DIRECTING.md). For any box, line, label, arrow, or marker, also read [ANNOTATION_GEOMETRY.md](references/ANNOTATION_GEOMETRY.md).
8. Before rendering, generate the timeline contact sheet, annotation manifest/review sheet, motion hero frames, and screen-focus review. Do not render while a review gate fails.
9. Build an editable multi-track timeline where available; run [EXPORT_AND_QC.md](references/EXPORT_AND_QC.md) before delivery.

## Required phases

### A - Intake

Determine audience, learning outcome, content level, canvas, target duration, source-of-truth script, brand preset, available originals, and reference intent. References teach organization and rhythm, never copied logos, wording, identity, or distinctive branding.

### B - Pre-production

Create:

- `CONTENT_CLASSIFICATION.md`
- `LAYOUT_PLAN.md`
- `VISUAL_BEAT_PLAN.md`
- `SCREEN_DIRECTION_PLAN.md`
- `MOTION_ROUTING_PLAN.md`
- `SFX_PLAN.md`
- `ASSET_GAP.md`

Every key sentence maps to one current visual beat. The next concept must not enter early, and old evidence must not remain after its spoken point ends.

### C - Media audit

Use original Talking Head, original Screen, and source motion projects. Choose one Master Take; use alternates only for missing or unusable speech and cover every cross-take edit completely. Never use a Preview or Final as a source for the next version.

### D - Asset production

- Original Screen proves real software behavior and results.
- HyperFrames handles light titles, labels, cards, lines, markers, progress, and simple steps.
- Remotion handles real state change, reorder, comparison, data, timeline, process flow, or multi-component build.
- ChatCut is the editable timeline layer when callable; local video-use/FFmpeg remains the fallback.
- Do not make two engines explain the same beat.

Read [MOTION_DESIGN.md](references/MOTION_DESIGN.md) and [MOTION_COPY.md](references/MOTION_COPY.md) when motion is used. Read [REFERENCE_MOTION_UI_PRESET.md](references/REFERENCE_MOTION_UI_PRESET.md) only when a reference-led Presenter Motion UI or Dark Motion UI direction is requested.

### E - Pre-render review

Required evidence:

- Timeline contact sheet
- `ANNOTATION_MANIFEST.json`
- Annotation review sheet with full frame, overlay, target close-up, name, spoken point, and frame range
- Motion start/change/end hero frames
- Screen focus review

Use the scripts in `scripts/`. A failed or missing review is not a render pass.

### F - Timeline

Keep independently editable tracks:

- V1: Talking Head base
- V2: Screen / B-roll / Information Screen
- V3: Presenter PIP / helper video
- V4: HyperFrames / Remotion assets
- Captions: independent subtitle system
- Audio: voice, BGM, and SFX separated

Adjacent overlays use integer-frame boundaries and must not expose the lower layer for one frame.

### G - QC and H - Export

Run annotation, safe-zone, flash-frame, contact-sheet, ffprobe, decode, black-frame, subtitle, audio, and bitrate checks. Export from originals and source assets at the target canvas. Software teaching under 4 Mbps video bitrate is not a quality PASS. Human review remains the release gate.

## Hard rules

- Human first does not mean human dominant. In software teaching, content and real UI are primary; ordinary Presenter PIP is about 14%-18% width and fixed or hidden.
- Use `Live -> Freeze -> Explain -> Continue`, not repeated crop/zoom. Show context before focus.
- Information screens preserve the complete semantic context; crop only with a stated teaching reason.
- Annotation geometry binds to a visible target in final-canvas integer pixels. No guessed boxes.
- Long Prompt/output is brief evidence, then becomes summary, comparison, or concept motion.
- Motion copy compresses speech; it is not a second subtitle.
- Important motion has `Start -> Change -> End`; build quickly and hold the complete result.
- No more than two consecutive pure concept pages before real evidence, Presenter, or a meaningful screen state.
- Subtitles are stable one or two lines; no karaoke, word-by-word color, bounce, or competition with motion.
- Original voice is preferred. If the processing chain changes materially, provide a five-second Raw/Processed comparison before applying it broadly.
- SFX follows the impact frame, stays below speech, and is not added to every card.
- Do not call paid generation or external upload without authorization.

## Conditional references

- Stable stages, PIP, face safety, grids: [LAYOUT_SYSTEM.md](references/LAYOUT_SYSTEM.md)
- Real screen grammar, long Prompt handling, zoom: [SCREEN_DIRECTING.md](references/SCREEN_DIRECTING.md)
- Target rectangles, manifests, review gate: [ANNOTATION_GEOMETRY.md](references/ANNOTATION_GEOMETRY.md)
- Motion routing, state progression, density: [MOTION_DESIGN.md](references/MOTION_DESIGN.md)
- Short concept copy: [MOTION_COPY.md](references/MOTION_COPY.md)
- Subtitle, voice, loudness, SFX: [SUBTITLE_AND_AUDIO.md](references/SUBTITLE_AND_AUDIO.md)
- Original lineage, Master Take, B-roll: [TAKE_AND_MEDIA_SELECTION.md](references/TAKE_AND_MEDIA_SELECTION.md)
- Codec, bitrate, flash/black frames, QC evidence: [EXPORT_AND_QC.md](references/EXPORT_AND_QC.md)
- Known anti-patterns: [FAILURE_PATTERNS.md](references/FAILURE_PATTERNS.md)

## Learning boundary

After each completed video, create `SKILL_FEEDBACK_CANDIDATES.md`. Do not modify this Skill automatically. Recommend a rule only when it is demonstrably reusable or has appeared in at least two projects; update only after explicit user confirmation.
