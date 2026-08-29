# Motion Design

## Router

1. If Human or real Screen already teaches the point: `NO EFFECT`.
2. Light title, keyword, label, badge, line, marker, callout, short card, progress, or simple step: HyperFrames.
3. Time/state/data change, reorder, multi-component relationship, Before/After, timeline, process flow, or build: Remotion.
4. A single beat uses one motion engine for one explanation.

Remotion should normally answer YES to at least two: real state/time/data change exists; HyperFrames is clearly insufficient; animation materially improves understanding.

## State contract

Every important motion defines:

- **Start** — what exists before the idea changes.
- **Change** — reveal, reorder, link, compare, eliminate, count, or build.
- **End** — the complete readable result.

“Appear → stay still” is not an explanatory state progression.

## Timing

- Meaningful visual event roughly every 2–4s, not a mandatory cut every 2–4s.
- Single-element entrance: about 0.25–0.45s.
- Empty intermediate state: preferably under 0.5s.
- Complete hero/result: at least 1.5–2.5s; complex result may hold 2–3s.
- Land the visual payoff near the spoken payoff; do not reveal the next concept early.
- Build fast, hold result.

## Density and alternation

- At most two consecutive pure concept/motion pages.
- After two, prefer real Screen, Freeze Evidence, Presenter, demo, comparison, or a real result.
- Use card reveal, reorder, link build, highlight, focus, result lock, and PIP change to explain—not merely decorate.

Run a rolling 10-second visual-type audit before First Cut approval. Mark `PPT_RISK` when a window contains only Concept Card / Static Motion Page and no Presenter, Real Screen, Freeze Evidence, Real Case, Compare, or meaningful real result. This is a warning for semantic review, not a quota requiring equal visual percentages. Use `scripts/detect_ppt_risk.py` when a beat manifest is available.

For `WHITEBOARD_STORYTELLING`, a persistent scene with progressive drawing, character action/reaction, physical interaction, or accumulating relationships is not a pure concept page. Evaluate whether meaning depends on time change. An intentional Knowledge Hero hold is an allowed static exception.

## Independent asset contract

- Motion files remain independent of Talking Head and Screen.
- Exact canvas, 30fps unless project says otherwise, exact duration, no unintended audio, no black first/last frame.
- Hold the last readable frame at least one second where the edit needs a cut handle.
- Preserve source projects and record each asset in the motion manifest.
- External alpha must be verified in the destination editor; metadata alone is not proof. If unsupported, keep the alpha master and supply a standalone branded full-screen fallback.

## SFX relationship

Motion may request a soft whoosh/pop, click, sweep, tick, connection blip, build, subtle section rise, or restrained success tone. Align the transient to the impact frame. Do not add a sound to every card.
