# Asset and Evidence Routing

Use this reference for historical failures, software proof, public repository claims, completed-work examples, AI-generated motherboards, illustrations, and derived visual assets.

## Evidence hierarchy

For a factual claim, prefer the highest safe and available tier:

1. Real historical video/frame showing the actual failure or result.
2. Original real screen recording of the current software state/action.
3. Real screenshot or verified public page.
4. Motion that explains the real evidence or a concept not directly visible.
5. AI illustration used only as explanation or atmosphere, never as fabricated proof.

Public/open-source/repository status requires a real public page or another authoritative state. Do not synthesize a fake repository, UI result, Prompt response, testimonial, or failure case.

When presenting a correction, prefer `Wrong → Fix` on the same underlying evidence state when it makes the difference clearer. Use different states only when the state change itself is the fact being taught.

## Motherboard is not a final visual

Treat a large AI-generated visual board as an asset library:

```text
Extract → Clean → Transparent → Rebuild or Animate → Review
```

Routing priority:

1. Rebuild simple text, labels, cards, badges, lines, arrows, boxes, and UI containers with HyperFrames, SVG, HTML/CSS, or the chosen deterministic motion system.
2. Keep complex illustration/detail as a tightly extracted transparent PNG/WebP when rebuilding would reduce fidelity.
3. Do not use the full board as a long-duration main visual. A brief full-board view is allowed only when the board itself is the explicit subject.

Record source image, crop/target, output, transparency state, intended beat, engine, and verification in `ASSET_EXTRACTION_MANIFEST.json` using the supplied template.

## Asset background leakage gate

At native output size, inspect every extracted asset for:

- warm-white/white rectangular canvas remnants;
- source-board edges or neighboring elements;
- white or dark halo around alpha edges;
- rough cutout edges and unintended shadow blocks;
- baked text, captions, or labels that duplicate the current timeline;
- false transparency that the destination editor renders as a rectangle.

If automatic extraction is unreliable, rebuild the simple element or keep it out. Do not hide leakage with a matching background unless the container is an intentional part of the design.

Historical completed clips are evidence, not automatically clean assets. Check for baked subtitles, platform UI, private content, and labels before adding the current subtitle/overlay system.
