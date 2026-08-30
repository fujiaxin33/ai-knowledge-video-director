---
name: ai-knowledge-video-director
description: Direct, plan, edit, and audit AI knowledge videos, real software tutorials, whiteboard explainers, internet-native comedy, and live-drawing storytelling. Covers semantic speech cleanup, evidence, progressive drawing, teaching motion, captions, audio, pre-render gates, rendering, and final listening QC. Use for horizontal or vertical knowledge teaching; do not use for unrelated vlogs, fiction, music edits, entertainment montages, or effects-led films.
metadata:
  version: "1.3.0"
---

# AI Knowledge Video Director

Turn an approved teaching idea and original media into a readable, evidence-led video through `Intake -> Speech Lock -> Pre-render Direction -> Build -> Timeline/Render -> Final Listening/Release`. Preserve user intent, approved facts, original media, prior versions, and explicit authorization boundaries.

## Start here

1. Read the script, asset inventory, references, and any project `DESIGN.md` / editing rules.
2. Build project-specific canonical terminology and product identity plans with [TERMINOLOGY_AND_PRODUCT_IDENTITY.md](references/TERMINOLOGY_AND_PRODUCT_IDENTITY.md).
3. Classify level, canvas, primary mode, and optional layers with [CONTENT_AND_FORMAT_ROUTER.md](references/CONTENT_AND_FORMAT_ROUTER.md). Keep `STANDARD` for real-screen teaching. Select `WHITEBOARD_STORYTELLING` only when a drawn story world is intended. Add `INTERNET_NATIVE_STORYTELLING` and/or `LIVE_DRAWING_STORYTELLING` only when their routing conditions are met.
4. For Whiteboard, read [WHITEBOARD_STORYTELLING.md](references/WHITEBOARD_STORYTELLING.md), [WHITEBOARD_QC.md](references/WHITEBOARD_QC.md), and [WHITEBOARD_FAILURE_PATTERNS.md](references/WHITEBOARD_FAILURE_PATTERNS.md). For optional layers, also read [INTERNET_NATIVE_STORYTELLING.md](references/INTERNET_NATIVE_STORYTELLING.md) and/or [LIVE_DRAWING_STORYTELLING.md](references/LIVE_DRAWING_STORYTELLING.md). Do not import those rules into unrelated Standard work.
5. Produce the Phase B documents from `templates/` before editing.
6. Audit original takes and screens with [TAKE_AND_MEDIA_SELECTION.md](references/TAKE_AND_MEDIA_SELECTION.md), remove semantic retakes at clause level, verify approved-script coverage, listen to the complete Clean A-roll, then lock it before visual/motion timing.
7. Route each visual beat to Human, Original Screen, HyperFrames, Remotion, programmatic whiteboard, or `NO EFFECT`; one main carrier per beat. Use [ASSET_AND_EVIDENCE.md](references/ASSET_AND_EVIDENCE.md) for real evidence and motherboard-derived assets.
8. For software teaching, read [SCREEN_DIRECTING.md](references/SCREEN_DIRECTING.md). For any box, line, label, arrow, or marker, also read [ANNOTATION_GEOMETRY.md](references/ANNOTATION_GEOMETRY.md).
9. Before rendering, follow [PRODUCTION_GATES.md](references/PRODUCTION_GATES.md): generate required manifests, action-state contact sheets, hero frames, render budget, and human review. Do not render while a gate fails.
10. Build an editable multi-track timeline where available; validate final subtitles and voice/visual facts, then perform an independent start-to-end listen of the actual final master before release.

## Required stages

### A - Source + Clean A-roll

Determine audience, learning outcome, content level, canvas, target duration, source-of-truth script, original-media lineage, brand preset, and reference intent. References teach organization and rhythm, never copied logos, wording, identity, or distinctive branding.

Audit the original source at clause level, create the transcript and semantic retake audit, verify approved-script coverage, generate Clean A-roll, then listen to that complete Clean A-roll from start to end. Without Listening Gate PASS and `A-ROLL LOCKED`, Storyboard is prohibited. Create project-specific `CANONICAL_TERMS.json` and a verified `PRODUCT_IDENTITY_PLAN.md` here.

### B - Story + Internet-native pass

Create:

- `CONTENT_CLASSIFICATION.md`
- `LAYOUT_PLAN.md`
- `VISUAL_BEAT_PLAN.md`
- `SCREEN_DIRECTION_PLAN.md`
- `MOTION_ROUTING_PLAN.md`
- `SFX_PLAN.md`
- `ASSET_GAP.md`
- `CANONICAL_TERMS.json`
- `PRODUCT_IDENTITY_PLAN.md`

For `WHITEBOARD_STORYTELLING`, also create a Whiteboard Plan. For internet-native work, add [INTERNET_PUNCH_MAP_TEMPLATE.md](templates/INTERNET_PUNCH_MAP_TEMPLATE.md). For live drawing, add [LIVE_DRAWING_PLAN_TEMPLATE.md](templates/LIVE_DRAWING_PLAN_TEMPLATE.md). Use [PRE_RENDER_GATE_TEMPLATE.md](templates/PRE_RENDER_GATE_TEMPLATE.md) to record the combined route and gate.

Map locked voice through `Knowledge Goal -> Story Beat -> optional Internet Punch/Cultural Candidate -> Character Action -> Visual Beat`. Every key sentence maps to one current beat. The next concept must not enter early, and old evidence must not remain after its spoken point ends. If there is no natural punch, keep the beat clean.

### C - Pre-render gate

Create Storyboard Contact Sheet, Internet Punch Map when routed, Caption Routing, Asset Manifest, per-asset Entry Method, 6–10 hero keyframes for complex internet-native work, and render budget. Every beat declares Entry, Action, Impact, Reaction, Hold, and Exit/reset; use `N/A` only with a reason. A final-state image never authorizes an instant timeline pop. Human APPROVE is required before render.

### D - Animation contract + First Cut

- Original Screen proves real software behavior and results.
- Real historical failures, real screens/screenshots, completed work, and public repository state outrank motion or AI illustration when they exist and are safe to show.
- HyperFrames handles light titles, labels, cards, lines, markers, progress, and simple steps.
- Remotion handles real state change, reorder, comparison, data, timeline, process flow, or multi-component build.
- ChatCut is the editable timeline layer when callable; local video-use/FFmpeg remains the fallback.
- Do not make two engines explain the same beat.
- Treat AI-generated motherboards as asset libraries, not final frames: extract, clean, make transparent, or rebuild before timeline use. Preserve approved high-quality final assets through mask draw, assembly build, Hand reveal, or transform.

Read [MOTION_DESIGN.md](references/MOTION_DESIGN.md) and [MOTION_COPY.md](references/MOTION_COPY.md) when motion is used. Read [REFERENCE_MOTION_UI_PRESET.md](references/REFERENCE_MOTION_UI_PRESET.md) only when a reference-led Presenter Motion UI or Dark Motion UI direction is requested.

Build only from approved Storyboard and locked voice. Keep independently editable video, caption, voice, BGM, and SFX tracks. Render one First Cut within the budget.

### E - First Cut review

Review only Speech, Timing, Visual, Caption, SFX, Residue, Internet Feel, and Knowledge Accuracy. Required evidence includes:

- Timeline contact sheet
- `ANNOTATION_MANIFEST.json`
- Annotation review sheet with full frame, overlay, target close-up, name, spoken point, and frame range
- Motion start/change/end hero frames
- Screen focus review
- Screen Hygiene QC
- Canonical term validation report
- Visual-variety/PPT-risk, page-turn, action-density, lifecycle, scale, and semantic-consistency audits

Use the scripts in `scripts/`. A failed or missing review is not a pass. Allow at most one normal Final Precision pass. A third full render is a documented process warning requiring reason and renewed authorization.

### F - Final master

Keep independently editable tracks:

- V1: Talking Head base
- V2: Screen / B-roll / Information Screen
- V3: Presenter PIP / helper video
- V4: HyperFrames / Remotion assets
- Captions: independent subtitle system
- Audio: voice, BGM, and SFX separated

Adjacent overlays use integer-frame boundaries and must not expose the lower layer for one frame. Run final caption, density, SFX, ending coverage, annotation, safe-zone, flash-frame, contact-sheet, ffprobe, decode, black-frame, subtitle, audio, bitrate, and semantic consistency checks. Then perform a second independent start-to-end listen of the actual Final Master, obtain human release approval, and LOCK.

## Hard rules

- Human first does not mean human dominant. In software teaching, content and real UI are primary; ordinary Presenter PIP is about 14%-18% width and fixed or hidden.
- Use `Live -> Freeze -> Explain -> Continue`, not repeated crop/zoom. Show context before focus.
- Information screens preserve the complete semantic context; crop only with a stated teaching reason.
- A claim such as “complete screen/workspace” must be visibly proven; a validator cannot restore missing source pixels.
- Annotation geometry binds to a visible target in final-canvas integer pixels. No guessed boxes.
- Long Prompt/output is brief evidence, then becomes summary, comparison, or concept motion.
- Motion copy compresses speech; it is not a second subtitle.
- Important motion has `Start -> Change -> End`; build quickly and hold the complete result.
- In `STANDARD`, no more than two consecutive pure concept pages should appear before real evidence, Presenter, or a meaningful screen state. A progressively built whiteboard scene with character action is not a pure concept page.
- Score rolling 10-second `PPT_RISK` windows by mode. In `WHITEBOARD_STORYTELLING`, progressive build, character action/reaction, and an intentional Knowledge Hero hold are valid exceptions; repeated complete cards and UI-like panels are not.
- Subtitles are stable one or two lines; no karaoke, word-by-word color, bounce, or competition with motion.
- Validate subtitle/project copy against the project-specific canonical terminology dictionary.
- Use verified real logos only at meaningful identity moments; do not fabricate or keep them persistently floating.
- Original voice is preferred. If the processing chain changes materially, provide a five-second Raw/Processed comparison before applying it broadly.
- SFX follows the impact frame, stays below speech, and is not added to every card.
- In `WHITEBOARD_STORYTELLING`, draw before show whenever an object can reasonably be established by drawing. Hand tip and stroke/mask reveal front must agree; a nearby moving Hand plus independent fade-in is `FAKE_HANDWRITING` and fails the gate.
- In `LIVE_DRAWING_STORYTELLING`, prefer Draw While Talking: voice cue, Hand action, visible change, and knowledge residue share one timeline. The Hand acts; it does not decorate. Repeated full-page resets fail.
- Whiteboard scenes should grow through actions and relationships on a full canvas. Do not replace every sentence with a new slide, make captions the primary visual, or introduce generic product UI unless the story requires real UI.
- Whiteboard comedy uses `Setup → Anticipation → Pause → Impact → Reaction`; preserve reaction and intentional comedy/reveal/knowledge pauses during speech cleanup.
- Internet-native storytelling is event direction, not a sticker pack. Real meme inserts default OFF and require explicit authorization plus source/rights and duration documentation.
- Every object has Entry, useful action, and Exit/Erase/Transform. Keep one primary action at a time; captions remain subordinate.
- Voice and picture must agree on counts, numbers, names, terms, brands, polarity, and relations. “Four” in voice with five visible objects fails even when timing passes.
- Speed routing is local. Meme, setup, punch, reaction, hero, and ending normally remain 1.00x. Any voice timing change regenerates caption, visual-anchor, and SFX maps.
- SFX is event-based and independently removable. No continuous scribble/noise bed and no marker sound for every stroke.
- A final technical PASS never substitutes for a start-to-end human listen of the actual exported master.
- Whiteboard final approval always retains a human gate for hook, story, comedy, draw naturalness, voice/visual meaning, character taste, SFX and ending.
- Do not call paid generation or external upload without authorization.

## Conditional references

- Stable stages, PIP, face safety, grids: [LAYOUT_SYSTEM.md](references/LAYOUT_SYSTEM.md)
- Canonical terms and verified product/logo identity: [TERMINOLOGY_AND_PRODUCT_IDENTITY.md](references/TERMINOLOGY_AND_PRODUCT_IDENTITY.md)
- Evidence hierarchy and motherboard extraction: [ASSET_AND_EVIDENCE.md](references/ASSET_AND_EVIDENCE.md)
- Real screen grammar, long Prompt handling, zoom: [SCREEN_DIRECTING.md](references/SCREEN_DIRECTING.md)
- Target rectangles, manifests, review gate: [ANNOTATION_GEOMETRY.md](references/ANNOTATION_GEOMETRY.md)
- Motion routing, state progression, density: [MOTION_DESIGN.md](references/MOTION_DESIGN.md)
- Short concept copy: [MOTION_COPY.md](references/MOTION_COPY.md)
- Subtitle, voice, loudness, SFX: [SUBTITLE_AND_AUDIO.md](references/SUBTITLE_AND_AUDIO.md)
- Original lineage, Master Take, B-roll: [TAKE_AND_MEDIA_SELECTION.md](references/TAKE_AND_MEDIA_SELECTION.md)
- Codec, bitrate, flash/black frames, QC evidence: [EXPORT_AND_QC.md](references/EXPORT_AND_QC.md)
- Known anti-patterns: [FAILURE_PATTERNS.md](references/FAILURE_PATTERNS.md)
- Whiteboard mode, Draw Before Show, scene growth, character/comedy grammar: [WHITEBOARD_STORYTELLING.md](references/WHITEBOARD_STORYTELLING.md)
- Whiteboard manifests, validators, automated limits and human gates: [WHITEBOARD_QC.md](references/WHITEBOARD_QC.md)
- Whiteboard-specific failure diagnosis: [WHITEBOARD_FAILURE_PATTERNS.md](references/WHITEBOARD_FAILURE_PATTERNS.md)
- Internet-native events, cultural references, asset quality, and real-meme policy: [INTERNET_NATIVE_STORYTELLING.md](references/INTERNET_NATIVE_STORYTELLING.md)
- Draw While Talking, Hand actor, continuous canvas, residue, and page-turn prevention: [LIVE_DRAWING_STORYTELLING.md](references/LIVE_DRAWING_STORYTELLING.md)
- Speech, storyboard, render-budget, final-listening, and human gates: [PRODUCTION_GATES.md](references/PRODUCTION_GATES.md)
- Object lifecycle, scale, captions, static holds, and callback duration: [VISUAL_LIFECYCLE_AND_SCALE.md](references/VISUAL_LIFECYCLE_AND_SCALE.md)

## Learning boundary

After each completed video, create `SKILL_FEEDBACK_CANDIDATES.md`. Do not modify this Skill automatically. Recommend a rule only when it is demonstrably reusable or has appeared in at least two projects; update only after explicit user confirmation.
