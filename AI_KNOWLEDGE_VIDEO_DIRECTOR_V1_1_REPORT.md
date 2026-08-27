# AI Knowledge Video Director v1.1.0 Report

Status: **PASS**

## 1. v1.0 → v1.1 rules

v1.1.0 promotes eight reusable production-learning areas:

1. Project-specific canonical terminology validation.
2. Product identity planning with verified real logos.
3. Clean A-roll lock before visual and motion timing.
4. Motherboard extraction and asset-background leakage review.
5. Real Evidence hierarchy for failures, software states, results, and repositories.
6. Stronger Annotation Geometry and completeness gates.
7. A named Screen Hygiene QC gate.
8. Rolling 10-second `PPT_RISK` detection.

The detailed NEW / STRENGTHEN / ALREADY COVERED / REJECT decisions are recorded in `V1_1_RULE_DIFF.md`.

## 2. Production feedback rejected from the universal Skill

- Mandatory single-line subtitles: rejected because one or two semantic lines remain valid by format.
- A fixed 6 Mbps encoder recipe: rejected because source quality, canvas, codec, bitrate/readability gates, and native-size inspection matter more than one project setting.
- Windows headless-browser terminal popups: rejected as an environment/tool-runner issue.
- Exact project colors, coordinates, timings, filenames, and logo crops: rejected because they do not transfer safely across brands, canvases, or assets.

Existing rules for 14%–18% Presenter PIP, `Full Context → Focus → Highlight → Hold`, dynamic annotation tracking, and subtitle/face safe zones were retained without duplication.

## 3. Canonical Terms mechanism

Pre-production reads the approved script, tool/product list, verified brand assets, and proper nouns to create a project-specific `CANONICAL_TERMS.json`. The dictionary records canonical spelling plus variants observed in the current project. `validate_canonical_terms.py` checks transcripts and final subtitle/title/label/CTA copy; a variant blocks the gate until corrected or explicitly waived. No historical project-specific error list is hard-coded globally.

## 4. Asset Transparency mechanism

An AI-generated motherboard is treated as an asset library:

`Extract → Clean → Transparent → Rebuild or Animate → Review`

Simple cards, labels, lines, arrows, boxes, and UI containers are rebuilt deterministically. Complex details may remain transparent PNG/WebP only after alpha and background-leakage review. Full motherboards are not used as long-duration main visuals. `ASSET_EXTRACTION_MANIFEST.json` records provenance, crop/target, output, route, transparency, beat, and leakage checks.

## 5. Annotation Gate strengthening

High-risk annotations now require both deterministic geometry validation and visual review. The gate checks final-canvas integer geometry, balanced containment, line/baseline accuracy, spoken-point mapping, dynamic target behavior, frame timing, and safe zones. If narration claims a complete interface or workspace, the full-context source must visibly prove completeness; numeric validation cannot restore missing pixels.

## 6. Test A

**PASS.** Reference and Presenter sources were re-probed at their original properties. Fresh 7-frame and 5-frame contact sheets were generated. Full Presenter Scene, Motion Canvas, Circular PIP, Motion Event Plan, and SFX Plan outputs remained complete. No video was rendered and no source media was modified.

## 7. Test B

**PASS.** The known-bad manifest produced the expected three blocking geometry errors. The corrected manifest passed annotation validation with zero errors/warnings, its layout passed safe-zone validation, and a fresh synthetic non-private two-row review sheet was visually inspected. Human semantic-completeness review remains mandatory.

## 8. Test C

**PASS.** The production regression covers all eight required decisions: Clean A-roll, dynamic canonical terms, Screen Hygiene, long Prompt summary, transparent motherboard treatment, Annotation Manifest, `PPT_RISK`, and verified product identity. The bad terminology fixture produced exactly one `nimbus flow → NimbusFlow` issue; the fixed fixture passed. The bad concept-only timeline produced one merged 0–12s risk; the corrected timeline passed. Annotation validation passed with zero errors/warnings. No video was rendered.

## 9. Skill Discovery

**PASS.** The Codex discovery entry remains a Junction to the installed Skill. Quick Validator passed through the discovery path. Repository-to-installed-source comparison covered 53 source files with zero hash mismatches; discovered version is `1.1.0`.

## 10. GitHub repository

Existing public repository, updated in place without creating a duplicate:

https://github.com/fujiaxin33/ai-knowledge-video-director

The publication scope contains Skill source, references, templates, scripts, examples, tests, README, and CHANGELOG. It contains no project video, raw media, motherboard image, private log, local configuration, personal data, secret, or API key.

## 11. Commit SHA

Skill source commit: `a00bae9b8343dd257a56c4c59cd48264be5b4dab`

## 12. Release Tag

Published release tag: `v1.1.0`

Release: https://github.com/fujiaxin33/ai-knowledge-video-director/releases/tag/v1.1.0

Release phrase: **First production-validation update**. The release is designed to reduce repeated correction cycles and does not claim zero editing.

## 13. Current limitations

- Canonical validation detects known project variants; it does not infer every possible ASR error.
- Geometry validation cannot prove semantic completeness when the source recording omitted pixels.
- Screen Hygiene and motherboard leakage checks still require native-size visual inspection.
- `PPT_RISK` depends on accurate beat classification and is a warning, not an automatic composition score.
- The Skill routes work and validates evidence; editor/plugin/tool availability and authorization remain environment-dependent.
- The Skill does not replace final aesthetic, privacy, factual, or release judgment.

## 14. Human decisions still required

- Whether delivery and pacing feel natural after semantic cleanup.
- Whether the selected evidence truly proves the spoken claim.
- Whether a crop preserves enough orientation for the intended audience.
- Whether annotation emphasis matches the spoken meaning rather than merely passing bounds.
- Whether a logo moment helps recognition without becoming advertising.
- Whether motion density, audio processing, subtitle rhythm, and overall taste are release-ready.
- Final privacy and publication approval.

Remote `main`, source commit, tag, and GitHub Release were verified before this gate was written.

# PASS
