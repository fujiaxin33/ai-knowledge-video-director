# Annotation Geometry and Review Gate

Annotations include boxes, guide lines, arrows, labels, markers, callouts, cursor markers, and focus masks. They bind to a real visible target on the final canvas; do not position by impression.

## Coordinate contract

- Canvas, frame range, target, annotation, label, subtitle zone, and face zones use final-canvas integer pixels and integer frames.
- `source_frame` must identify the reviewed original/freeze frame.
- `target_rect` describes the visible UI object, not the desired decoration.
- `annotation_rect` describes the actual box/line geometry.
- Recalculate coordinates after every crop, scale, inset, or layout change.

Use [ANNOTATION_MANIFEST_TEMPLATE.json](../templates/ANNOTATION_MANIFEST_TEMPLATE.json).

## Boxes

- Fully contain the target without including a large unrelated region.
- Keep all edges parallel to the UI panel.
- Preferred padding: 8–20px; opposite-edge padding should not differ by more than about 4px.
- On a 1920×1080 canvas, aim for target/annotation edge error within about ±4px after the chosen padding.
- Do not crop the box, target, or label at the canvas edge.

## Lines, labels, and spoken mapping

- A guide line starts from or terminates at the real target edge; its label aligns with the other end.
- Lines stay horizontal/vertical unless the target relationship genuinely requires another direction.
- Spoken points determine annotation count: three taught items normally receive three semantic marks, not one generic line or five decorative marks.
- Labels use compressed action/result copy and remain outside subtitles, face zones, and important UI.

## Dynamic targets

If the page scrolls, switches, or moves, do one of:

- freeze the frame;
- recompute the target rectangle;
- track the annotation with the target.

Never leave an annotation at an old coordinate after the target moves.

## Required review sheet

For every annotation, show:

1. Full frame
2. Annotation overlay
3. Enlarged target crop
4. Annotation name
5. Spoken point
6. Start/end frame

The gate passes only when target coverage, box alignment, semantic line count, label visibility, subtitle/face safety, frame timing, and visual/spoken agreement all pass. Run `validate_annotation_bounds.py`, `validate_layout_safe_zones.py`, and `make_annotation_review_sheet.py` before render.
