# Production Gates

The pipeline is `A Intake -> B Speech Lock -> C Pre-render Direction -> D Asset and Motion Build -> E Timeline and Render -> F Final Listening and Release`.

## Gate B — speech lock

Required:

- original-source lineage;
- semantic retake audit covering Word Repeat, Phrase Repeat/Restart, Sentence Restart, Failed Lead-in/Start, Self Correction, Bad Take -> Good Take, Repeated Complete Take, Meaning Duplicate, and Broken Ending;
- only the intended complete clause retained;
- approved-script coverage by section and meaning, including INTRO, BODY, KNOWLEDGE HERO, LIMIT, ENDING, and NEXT HOOK whenever present in the approved source;
- a start-to-end listen of the complete Clean A-roll checking stutter, repeat, failed start, unnatural splice, breath jump, meaning duplicate, and broken ending;
- a locked voice master.

Transcript, waveform, or ASR review alone cannot pass this gate.

## Gate C — pre-render direction

Create, as applicable:

- storyboard/contact sheet showing action states;
- Internet Punch Map;
- Caption Routing;
- Asset Manifest with source, license/authorization, final-quality target, and entry method;
- per-beat Entry, Action, Impact, Reaction, Exit;
- hero keyframes showing final visual quality;
- live-drawing voice/stroke/Hand map;
- render budget with preview count and full-render authorization.

Do not render when a keyframe is a placeholder, a punch is a static card, a full image has no entry method, or the human gate is not approved.

## Gate D — build

Build from locked audio. Preserve high-quality approved assets, continuous-canvas logic, scale hierarchy, caption hierarchy, and scene lifecycle. Local speed changes must regenerate voice, caption, visual-anchor, and SFX timing maps.

## Gate E — timeline and render

Maintain editable tracks and version lineage. Full renders consume the declared budget. A technical render PASS is not release approval.

## Gate F — final listening and release

Listen again from start to finish to the actual final master, not a transcript or isolated cuts. Confirm no restart, repeated clause, bad-take/good-take pair, unnatural splice, breath jump, broken ending, timing drift, orphan SFX, or caption mismatch. Reconfirm approved-script coverage and voice/visual semantic consistency. This release listen is separate from the pre-lock Clean A-roll listen. Human approval is required.

## Render budget

Default target: one pre-render review, one First Cut render, and at most one Final Precision render. Prefer short representative segments before a full render. A third full render is a process warning, not an automatic hard failure, but it must record `Why Render Budget Exceeded` and obtain renewed authorization.
