# Subtitle and Audio

## Knowledge subtitles

Two supported directions:

### Brand Knowledge

White/warm-white text, light outline or shadow, stable placement, one or two lines, optional static brand-color emphasis on truly important terms.

### Dark Motion UI

Yellow/white text on a restrained translucent dark rounded background, stable placement, no active-word animation.

Always prohibit karaoke, word-by-word highlight/color, bounce, and captions that compete with motion. Do not repeat an Overlay sentence verbatim. Protect the face, platform interaction region, current annotation target, and software text.

## Chunking

Break by semantic phrase and natural pause. Merge tiny fragments that would flash. For fast knowledge video, keep each displayed line compact; for courses, prioritize readable phrases over arbitrary character quotas.

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
