# v1.1.0 Regression Tests

All tests were executed locally with the bundled Python runtime and existing FFmpeg/FFprobe. No complete video was rendered and no historical project was modified.

## Test A — Reference-style planning regression

**PASS**

- Reference source re-probed: 1920×1080, 30fps, H.264, 94.9s.
- Presenter source re-probed: 3840×2160, 60000/1001fps, HEVC, 26.816s.
- Fresh contact sheets generated: 7 reference frames and 5 presenter frames.
- Required plan outputs remain present: Full Presenter Scene, Motion Canvas, Circular PIP, Motion Event Plan, and SFX Plan.
- The test remains planning-only and transfers hierarchy/rhythm rather than branding.

## Test B — Annotation precision regression

**PASS**

- Known bad manifest produced the expected three blocking errors: incomplete target containment, wrong underline span, and wrong baseline.
- Corrected manifest passed annotation validation with zero errors/warnings.
- Corrected layout passed safe-zone validation.
- A fresh 1500×960 two-row annotation review sheet was generated from a new synthetic, non-private software-screen fixture and visually inspected.
- Human semantic-completeness gate remains required; numeric geometry cannot restore missing pixels.

## Test C — Production regression

**PASS**

- Bad canonical transcript produced one exact `nimbus flow → NimbusFlow` issue; corrected transcript produced zero.
- Bad visual beat manifest produced one merged 0–12s `PPT_RISK`; corrected manifest produced zero.
- Test C annotation manifest passed with zero errors/warnings.
- The production plan covers Clean A-roll, canonical terms, Screen Hygiene, long Prompt summary, transparent motherboard treatment, Annotation Manifest, PPT Risk, and verified product identity.

See [TEST_C_PRODUCTION_REGRESSION.md](TEST_C_PRODUCTION_REGRESSION.md) and its sanitized fixtures.
