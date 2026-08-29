# Changelog

## v1.2.0 — Whiteboard Storytelling preset

Backward-compatible feature release. The existing Standard workflow remains the default for desktop tutorials, real-software demonstrations, talking head, and evidence-led courses.

Added:

- opt-in `WHITEBOARD_STORYTELLING` routing and planning template;
- Draw Before Show, Hand-tip alignment, progressive scene, character, comedy, Knowledge Hero, caption, voice/visual, and SFX rules;
- whiteboard-specific QC and failure-pattern references;
- deterministic draw-on, voice/visual, SFX, character-anchor, caption, and mode-aware PPT-risk validators;
- tests D–I plus regression tests A–C for the original route;
- abstract positive/negative ground-truth examples derived from production evidence without carrying episode-specific shells into the preset.

Known limits:

- story quality, comedy, drawing naturalness, character taste, semantic alignment, and release approval retain a human gate;
- validators require structured manifests and cannot infer hidden source pixels or repair incomplete assets;
- the preset does not call paid generation, upload media, or alter a user's project without explicit authorization.

## v1.1.0 — Production validation update

First production-validation update from an independent real-world AI knowledge-video workflow.

Added or strengthened:

- project-specific canonical terminology validation;
- verified product identity and logo routing;
- Clean A-roll lock before visual and motion timing;
- motherboard extraction and asset-background leakage review;
- Real Evidence hierarchy for failures, software states, results, and repositories;
- stronger Annotation Geometry and completeness gates;
- named Screen Hygiene QC;
- rolling 10-second PPT Risk detection;
- reusable templates, deterministic validators, and a production-regression test.

The update is designed to reduce repeated correction cycles. It does not remove the need for semantic, aesthetic, privacy, or release review by a person.

## v1.0.0

Initial open-source release.
