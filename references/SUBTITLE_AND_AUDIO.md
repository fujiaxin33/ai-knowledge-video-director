# Subtitle and Audio

## Adaptive caption routing

Route Caption ON/SHORT for ordinary explanation, abstract concepts, faster knowledge delivery, or meaning that the picture cannot fully carry. Route Caption OFF for meme flash, comedy impact, pure reaction, central complete handwriting, readable literal evidence, a clean hero, and the ending question.

Prefer one semantic line, about 55–65% maximum frame width and 4–5.5% frame height in the lower safe area. Caption is third in hierarchy after Character/Action and Knowledge Object. If central handwriting already states the same meaning, remove the duplicate caption.

## Local speed routing

Use natural voice first. Ordinary explanation may be a modest local candidate; dense knowledge may be slightly faster only after listening. Meme, comedy setup, punch, reaction, hero, and ending normally remain 1.00x. Never apply one multiplier to the whole video. Any applied speed change regenerates final voice, caption, visual-anchor, and SFX timing maps.

## SFX V2

SFX serves Impact, Action, and Reaction. Keep voice dominant, use event-level clips, and keep them on a separate removable track. Avoid continuous scribble/noise, a marker sound on every stroke, or impacts without a visible event. Deleting an image/flash must also delete its orphaned SFX.

## Knowledge subtitles

Two supported directions:

### Brand Knowledge

White/warm-white text, light outline or shadow, stable placement, one or two lines, optional static brand-color emphasis on truly important terms.

### Dark Motion UI

Yellow/white text on a restrained translucent dark rounded background, stable placement, no active-word animation.

Always prohibit karaoke, word-by-word highlight/color, bounce, and captions that compete with motion. Do not repeat an Overlay sentence verbatim. Protect the face, platform interaction region, current annotation target, and software text.

### Whiteboard Storytelling

Default to a semantic single-line caption, usually 6–16 Chinese characters and approximately 20–22 as a hard-length candidate. Compress meaning rather than shrinking the type. Visual priority is `Story > Character > Hand > Knowledge Word > Caption`; captions must not become the first visual center.

## Chunking

Break by semantic phrase and natural pause. Merge tiny fragments that would flash. For fast knowledge video, keep each displayed line compact; for courses, prioritize readable phrases over arbitrary character quotas.

Before subtitle lock, validate product/tool/model/repository/Skill names against the project-specific `CANONICAL_TERMS.json`. Correct ASR spelling, spacing, capitalization, and transliteration without turning one project's errors into a permanent global replacement list. Run the canonical validator again after title/overlay copy is finalized.

## Voice

- Prefer the real voice.
- Do not default to AI voice, voice change, aggressive isolation, aggressive denoise, or large gain homogenization.
- A practical target is about -16 LUFS integrated and about -1.0dBTP while retaining natural tone.
- Remove hum/noise conservatively. If the chain changes materially, export a five-second Raw/Processed comparison before broad application.

## SFX

- Place on a separate track where possible.
- Align to the motion impact frame.
- Typical peak is 12–18dB below speech; confirm by listening, not number alone.
- About 1–3 meaningful effects per 5–8s is an upper working range, not a quota.
- Reuse sound families for repeated action families.
- Use licensed/local known sources. If unavailable, write `SFX_REQUEST.md` with action, time, duration, suggested source, and payment status; do not call paid generation without approval.
- In whiteboard mode, classify each cue as `DRAW`, `MOTION`, `IMPACT`, `COMEDY`, or `REVEAL` and bind it to a visible event. Draw sound follows pen-down velocity and stops at pen lift; impact sound lands on the impact frame.
