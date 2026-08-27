# Terminology and Product Identity

Use this reference when a video names software, AI tools, platforms, repositories, Skills, models, brands, commands, or technical concepts whose spelling matters.

## Canonical terminology pass

During pre-production, read the approved script, product/tool list, brand assets, documentation, and proper nouns. Build a project-specific `CANONICAL_TERMS.json` from those sources; never rely on a fixed global list of mistakes from an earlier project.

For each canonical term record:

- exact display spelling and capitalization;
- likely ASR/spacing/transliteration variants found in the current transcript;
- evidence source such as approved script, official UI, documentation, or supplied brand asset;
- where the term is expected to appear.

Run `scripts/validate_canonical_terms.py` after transcript cleanup and again on final subtitle, title, label, and CTA text. A match to a non-canonical variant blocks the subtitle/copy gate until corrected or explicitly waived with a reason.

Use [CANONICAL_TERMS_TEMPLATE.json](../templates/CANONICAL_TERMS_TEMPLATE.json). The template is intentionally empty of permanent product names.

## Product identity plan

Create `PRODUCT_IDENTITY_PLAN.md` when the video introduces one or more products or platforms.

A meaningful first introduction may use:

```text
Verified Logo + Canonical Product Name + Short Role
```

Examples of roles are short functions such as `Timeline / Captions / Export` or `Flow / Compare / State Change`; they are not advertising claims.

Rules:

- Prefer first introduction, tool routing, or a real evidence/result moment.
- Reuse only when recognition would otherwise be lost; do not keep a logo persistently floating.
- Use an official asset or a user-supplied/project asset whose provenance can be verified.
- Never ask image generation to imitate a real product logo.
- Extract only the identity element needed; do not place a complete motherboard or promotional card as the logo.
- Keep the logo outside face, subtitle, platform UI, annotation-target, and important software-text zones.
- If no reliable asset exists, use canonical text only and record the asset gap.

Use [PRODUCT_IDENTITY_PLAN_TEMPLATE.md](../templates/PRODUCT_IDENTITY_PLAN_TEMPLATE.md).
