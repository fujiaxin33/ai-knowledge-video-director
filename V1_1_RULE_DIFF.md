# v1.1 Rule Promotion Review

Version reviewed: v1.0 → v1.1.0
Evidence base: first independent production run, including First Cut, V2 Cleanup, Clean A-roll EDL/QC, Screen Hygiene QC, Annotation manifest/review sheet/QC, Asset Transparency QC, Visual Variety QC, Layout Lock, Subtitle/Logo Fix, contact sheets, and recorded user corrections.

## Promotion criteria

Each candidate was checked for: transferability, likelihood in other AI knowledge/software teaching videos, existing v1.0 coverage, whether the change strengthens rather than duplicates, and whether it changes future decisions enough to justify inclusion.

| Candidate | Decision | v1.0 coverage | v1.1 action | Reason |
|---|---|---|---|---|
| Canonical terminology dictionary and validation | **NEW** | Subtitle rules cover style/chunking but not ASR proper nouns | Add dynamic `CANONICAL_TERMS.json` workflow, template, validator, and Final QC gate | Product/tool names are predictable high-impact ASR failures across software videos; dictionary must come from each project, not a fixed 004 list |
| Product identity / real Logo routing | **NEW** | Tool responsibilities exist; identity assets do not | Add `PRODUCT_IDENTITY_PLAN.md` template and first-introduction rule | A real logo can reduce recognition time, but only when it exists, is verified, and does not become persistent branding |
| Motherboard extraction / transparency | **STRENGTHEN** | Alpha is discussed for motion assets; full-board leakage is not | Add `Motherboard ≠ Final Visual`, extraction hierarchy, background-leakage checks, and manifest fields | Large AI boards are useful libraries but repeatedly fail when imported as final frames |
| Real Evidence hierarchy | **STRENGTHEN** | Original Screen is already the primary proof source | Add explicit ordering for failure cases, software state, historical work, and public repositories | Prevents AI illustration from replacing available factual evidence; does not prohibit motion explanation |
| Clean A-roll before Motion Lock | **STRENGTHEN** | Master Take/source lineage are covered; semantic cleanup order is not | Add transcript+audio semantic cleanup, Clean A-roll lock, EDL/QC gate before visual beats and motion | Motion built before speech cleanup creates systemic retiming and correction work |
| Annotation Geometry review gate | **STRENGTHEN** | Manifest, integer coordinates, validators, review sheet, safe zones already exist | Add high-risk gate and explicit proof obligation when narration claims a “complete” interface/workspace | Existing rule is correct; production evidence justifies stronger gating, not a duplicate geometry section |
| Screen Hygiene gate | **STRENGTHEN** | Context-preserving crop and removal of unrelated chrome exist | Add explicit app/focus/desktop/taskbar/private/unrelated/burned-caption checklist and QC template | Hygiene needs a named pre-timeline gate; over-crop remains prohibited |
| PPT Risk detector | **STRENGTHEN** | Two-concept-page limit already exists | Add rolling 10-second visual-type audit and `PPT_RISK` warning; keep semantic judgment | Detects long static stretches without imposing artificial equal visual ratios |
| Wrong → Fix on the same evidence state | **STRENGTHEN (conditional)** | Compare and real evidence are supported | Add as preferred failure-proof pattern when the underlying state can remain identical | Makes the correction legible, but is not mandatory when the state itself must change |
| Historical evidence with burned subtitles | **STRENGTHEN (hygiene item)** | Duplicate subtitle collision is indirectly covered | Add a reused-evidence check for prior burned captions/labels | Transferable to any reused completed clip; belongs in Screen Hygiene, not a new standalone rule |
| Annotation target vs subtitle/face zones | **ALREADY COVERED** | Explicit in annotation/layout validators and review gate | No duplicate rule; retain as a Test C assertion | Production confirmed the existing rule rather than revealing a missing rule |
| Fixed 14%–18% Presenter PIP | **ALREADY COVERED** | Layout system and hard rules already specify this range | No change beyond regression coverage | 004 validated the rule but did not change it |
| Full Context → Focus → Highlight → Hold | **ALREADY COVERED** | Screen grammar and timing already require context before focus | No duplicate rule; use in Test C | Existing rule is sufficient |
| Dynamic annotation must update after scroll | **ALREADY COVERED** | Freeze/recompute/track rule already exists | No duplicate rule | Existing rule exactly matches the failure |
| Single-line subtitles everywhere | **PROJECT SPECIFIC / REJECT** | Skill supports one or two lines by format | Do not universalize | Courses and vertical formats sometimes need two semantic lines |
| 6Mbps CBR-like export settings | **PROJECT SPECIFIC / REJECT** | Skill already gates information screens below 4Mbps and prefers CRF 18–20 | Do not hard-code one project’s encoder settings | Readability and decode/QC matter more than one fixed bitrate recipe |
| Windows headless browser workers opening terminal windows | **ENVIRONMENT SPECIFIC / REJECT** | Tool fallback and source preservation already exist | Keep in project memory only | This is an environment/tool-runner issue, not a directing rule |
| Exact 004 colors, coordinates, timings, filenames, and logo crops | **PROJECT SPECIFIC / REJECT** | Layout and identity rules are already parameterized | Do not include | They do not transfer safely to another brand, canvas, or asset |

## Approved v1.1 rule set

Promote eight production-learning areas:

1. Canonical terminology validation.
2. Product identity planning with verified real logos.
3. Motherboard extraction and asset-background leakage checks.
4. Real Evidence hierarchy.
5. Clean A-roll lock before Motion Lock.
6. Stronger Annotation Geometry gate.
7. Named Screen Hygiene gate.
8. Rolling PPT Risk detection.

The `SKILL_FEEDBACK_CANDIDATES.md` mechanism remains unchanged: later observations stay candidates until explicit promotion review.
