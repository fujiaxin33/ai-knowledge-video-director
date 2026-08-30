# Production Evidence — EP03 to EP05

This document records reusable production findings from three completed whiteboard projects. It contains no source media, private paths, personal data, or episode-specific creative assets. The reports named below were read-only evidence; the projects were not modified.

## Evidence standard

A rule enters v1.3.0 only when it is reusable across projects or when one severe failure exposes a missing release gate. Automated PASS labels are not treated as proof when later full-length human review contradicts them.

## EP03 — speech, residue, density, and audio

Evidence reports: `EP03_BLIND_TEST_REPORT.md`, `EP03_V2_SPEECH_AUDIT.md`, `EP03_V3_APPROVED_SCRIPT_COVERAGE.md`, `EP03_V4_REPEAT_AUDIT.md`, `EP03_V5_RESIDUE_AUDIT.md`, `EP03_FINAL_MASTER_V6_REPORT.md`.

- A transcript-level clean pass missed phrase repeats, sentence restarts, failed starts, and meaning duplicates. ASR sometimes collapsed repeated clauses into one token span. Result: semantic retake detection and a start-to-end listening gate are both required.
- Removing speech for pace can damage the approved ending. Result: approved-script coverage must be verified by meaning, not only by duration or word count.
- Progressive reveal alone did not prevent PPT-like direction. Result: each beat needs an event, character action, state change, or deliberate hero hold.
- Thirty-seven stale elements were later removed. Result: every object needs an entry, useful life, and exit/reset plan.
- Caption needs varied by beat, and pace changes required local rather than global speed routing. Result: captions and voice speed must be routed semantically, then all downstream timing regenerated.
- Continuous broadband drawing texture became audible as an artifact. Result: SFX must be event-based, independently mixed, and removable without touching voice.

## EP04 — semantic alignment and action direction

Evidence reports: `EP04_BLIND_TEST_REPORT.md`, `EP04_V2_REPEAT_AUDIT.md`, `EP04_V2_VOICE_VISUAL_ALIGNMENT.md`, `EP04_V2_CHARACTER_ACTION_MAP.md`, `EP04_V2_PPT_RISK_AUDIT.md`, `EP04_V3_REPEAT_FIX.md`, `EP04_FINAL_MASTER_V3_REPORT.md`.

- Two complete deliveries of the same RAG clause survived an earlier clean pass; the bad take was not safely removed until a human identified the exact restart. Result: detect `bad take -> good take` at clause level and retain only the intended delivery.
- Action count increased from 14 to 31 during repair while the automated PPT score stayed LOW. Result: a low card-count score is insufficient; action density and static-hold risk require independent checks.
- A retrieval explanation improved only after it became a detective action sequence rather than repeated cards. Result: knowledge should be expressed through action whenever the teaching meaning permits it.
- Voice referred to four characters while the visible speech bubble contained five. Result: facts, counts, names, polarity, and relations must match between voice and picture.
- Definition pages and retrieval demos could pass technical checks while remaining static. Result: Storyboard and keyframes require human approval before render.

## EP05 — internet-native direction, captions, scale, and callbacks

Evidence reports: `EP05_FIRST_CUT_V1_REPORT.md`, `EP05_FIRST_CUT_V2_REPORT.md`, `EP05_INTERNET_PUNCH_MAP_V2.md`, `EP05_V3_SPEECH_AUDIT.md`, `EP05_V3_CAPTION_ROUTING.md`, `EP05_V3_MEME_INSERT_MAP.md`, `EP05_FINAL_MASTER_V4_REPORT.md`, `EP05_FINAL_V5_REPORT.md`, `EP05_CLEAN_FINAL_REPORT.md`, `EP05_V5_FINAL_SPEECH_LISTEN_QC.md`.

- Correctly named punch assets still produced information-graphic thinking until setup, action, impact, and reaction were staged as events. Result: internet-native storytelling is an optional directing layer, not a sticker library.
- Complex comedy assets became weaker when redrawn as placeholders. Result: use progressive reveal or assembly while preserving the approved final asset quality.
- Two authorized real-meme flashes increased recognition but broke visual coherence and were removed from the clean final. Result: real meme inserts default OFF; references normally supply cultural DNA and composition only.
- Captions were first removed too aggressively, then later competed with the action. Result: route captions adaptively and keep them subordinate to character/action.
- Ctrl+F, Truman, RAG callback, and group chat improved when sequential actions replaced simultaneous layouts; the callback was shortened to a few seconds. Result: one primary action per moment, time-bounded callback, and transform rather than cut when carrying knowledge forward.
- Primary scale drift and a late-video energy drop appeared even with high-quality art. Result: scale the active character/action consistently and audit the latter half independently for static holds.
- The final listening pass remained separate from transcript review and regenerated all downstream timing after local speed changes. Result: speed is local, natural voice is primary, and every timing map must ripple from the locked audio.

## Rules promoted to v1.3.0

1. Semantic retake audit plus independent start-to-end listening approval.
2. Approved-script coverage and voice/visual semantic consistency gates.
3. Optional `INTERNET_NATIVE_STORYTELLING` and `LIVE_DRAWING_STORYTELLING` layers.
4. Event-first punches, cultural-reference policy, and real-meme default OFF.
5. High-quality final-asset preservation with progressive reveal.
6. Scene lifecycle, continuous-canvas, scale hierarchy, caption hierarchy, and page-turn checks.
7. Local speed routing, callback duration, event-based SFX, render budget, and human approval.
