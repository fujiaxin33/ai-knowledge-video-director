# v1.2.0 — Whiteboard Storytelling Preset

## New

- Optional `WHITEBOARD_STORYTELLING` route for story-led whiteboard knowledge and comedy explainers.
- Draw Before Show, Hand-tip/reveal-front, progressive scene, character direction, comedy timing, Knowledge Hero, caption, voice/visual, SFX, and full-canvas rules.
- Whiteboard plan template, QC reference, failure-pattern catalog, and abstract ground-truth examples.
- Five deterministic validators for draw-on, voice/visual alignment, SFX timing, character anchors, and semantic captions.
- Tests D–I plus negative mutations for common contract failures.

## Changed

- Mode-aware PPT-risk scoring now distinguishes repeated static/UI cards from progressive action and intentional Knowledge Hero holds.
- Content routing, A-roll pause classification, motion, captions/audio, final QC, and examples now support the optional Whiteboard route.
- Version metadata and discovery copy updated to v1.2.0.

## Validators and tests

- Tests A–C protect Standard routing, annotation geometry, canonical terminology, and prior PPT-risk behavior.
- Tests D–I cover progressive drawing, alignment, comedy, mode-aware PPT risk, captions, and story-shell generalization.
- Full result: 9/9 behavioral tests, 8/8 existing tool smoke tests, 5/5 new validator smoke tests.

## Compatibility

- Backward compatible: desktop tutorials, real-software demonstrations, talking head, courses, and evidence-led workflows remain `STANDARD`.
- Whiteboard rules load only after routing to `WHITEBOARD_STORYTELLING`.
- Existing files, validators, CLI entry points, and v1.1.0 release remain available.

## Known limits

- Story, humor, drawing naturalness, character taste, semantic alignment, SFX mix, and release approval still require a person.
- Validators consume structured manifests; they cannot recover incomplete source pixels or repair visual assets.
- The Skill does not call paid generation, upload media, or modify a project without explicit authorization.
