# Whiteboard Storytelling QC

## v1.3 pre-render additions

Require an action-state storyboard/contact sheet, Caption Routing, Asset Manifest, per-image Entry Method, hero keyframes at approved final quality, and a render budget. When internet-native or live-drawing layers are routed in, require their Punch Map or voice-to-drawing map.

Reject when a full asset appears without Draw/Mask/Build/Transform/intentional Impact; the final asset is degraded into a placeholder; a beat is only Text + Arrow + Box; Hand tip and reveal front separate; reveal continues after the Hand stops; scenes behave like slide pages; captions dominate action; voice and picture disagree; reaction is missing; callback becomes a lesson; SFX continues without an event; or a full render is requested before human keyframe approval.

Use with [WHITEBOARD_STORYTELLING.md](WHITEBOARD_STORYTELLING.md). Automated checks produce evidence and candidates; encoded-output contact sheets and human semantic/aesthetic review remain mandatory.

## Required evidence

- locked Clean A-roll EDL/QC and pause classification;
- Whiteboard plan with one primary meaning per beat;
- draw-on manifest and Start/25/50/75/100 frames for priority objects;
- voice/visual beat map with keyword and reveal events;
- character anchor/pose manifest;
- SFX impact/draw manifest;
- semantic caption manifest;
- pre-render story, draw, character, PPT/UI, and layout contact sheets;
- final-encode contact sheets and technical QC bound to output path and hash.

## Speech

- Remove word/phrase repeats, restarts, failed starts, corrections, half sentences, meaning duplicates, stutters, and non-teaching gaps.
- Preserve natural breath and classified comedy, reveal, reaction, and knowledge holds.
- Lock before motion. A later speech change reopens visuals, captions, SFX, and frame reviews.

## Story

- Hook contains conflict/question/surprise/action in the first 1–3 seconds.
- Story shell serves the knowledge goal and is not copied from a prior episode.
- Recurring character has an arc; every punch includes reaction.
- Every beat has one primary meaning.
- At least one Knowledge Hero is recommended when the topic has one core lock.

## Draw

- Draw Before Show level is declared for each drawable object.
- Hand tip follows stroke endpoint/mask front.
- Reveal progresses monotonically and the completed result is held.
- Instant pop is justified as an intentional impact.
- No fake handwriting or static full-image substitution.

Run `scripts/validate_draw_on.py`; visual review still judges stroke naturalness and semantic build order.

## Character

- Base/feet anchor and scale remain stable across pose swaps.
- Entry and impact frames preserve the full intended silhouette.
- One temporal character state unless duplication is intentional.
- Face/expression/critical gesture are protected except intentional punch occlusion.
- Text/logo/directional props are not mirrored.

Run `scripts/validate_character_anchors.py`; human review confirms identity, taste, silhouette and intentional occlusion.

## Caption

- Semantic single line by default; compress long wording.
- Stable bottom safe region; no face, Hand, Hero, or story-action collision.
- No transcript duplication, repeated consecutive caption, karaoke, bounce, or dominance.

Run `scripts/validate_whiteboard_captions.py`; human review confirms semantic compression and visual priority.

## SFX

- Every cue maps to `DRAW`, `MOTION`, `IMPACT`, `COMEDY`, or `REVEAL`.
- Impact transient lands on the impact frame.
- Drawing starts/stops with pen-down/pen-lift.
- Voice remains dominant; continuous decorative noise is rejected.

Run `scripts/validate_sfx_timing.py`. Default guidance is ≤80ms PASS, 80–150ms WARN, and >150ms FAIL candidate, with per-event/type overrides when perception requires them.

## Voice / visual

- Each important voice span maps to one intended meaning and visual event.
- No premature next-concept reveal or stale prior visual.
- Keyword completion occurs within the declared anticipation/lead window.

Run `scripts/validate_voice_visual_alignment.py`; human review confirms that visual semantics, not only timestamps, match the voice.

## Visual and PPT/UI risk

- Full canvas; no visible course divider unless explicitly designed.
- Scene grows through time; repeated complete cards and static PNG sequences are warnings/failures.
- Knowledge Hero static hold is exempt when isolated and intentionally timed.
- No UI residue unless the story requires real UI.
- Empty space is allowed and should not be mistaken for missing design.

Run `scripts/detect_ppt_risk.py` and review its LOW/MEDIUM/HIGH dimensions against contact sheets.

## Final technical gate

Run full decode, expected frame/duration, black/flash/solid, subtitle safe-zone/overlap, bitrate, audio loudness/true peak, splice, boundary and hash checks from source assets. Bind QC to an immutable versioned filename. Human review decides final release.
