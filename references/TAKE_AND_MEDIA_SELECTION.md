# Take and Media Selection

## Semantic retake audit — v1.3 gate

Do not equate a clean transcript with a clean performance. Review the original audio and transcript together at clause boundaries. Mark and resolve Word Repeat, Phrase Repeat, Phrase Restart, Sentence Restart, Failed Lead-in/Start, Self Correction, Bad Take -> Good Take, Repeated Complete Take, Meaning Duplicate, and Broken Ending.

When a failed clause is followed by a complete new delivery, remove the failed clause as a unit and retain one intended take. Do not hide it with global speed, keep two near-duplicate takes, or splice arbitrary half-sentences. ASR may collapse repeated speech, so waveform/transcript evidence never replaces listening.

Before lock, produce approved-script coverage by semantic section. When present in the approved source this includes INTRO, BODY, KNOWLEDGE HERO, LIMIT, ENDING, and NEXT HOOK. A faster edit fails if an approved meaning or complete ending disappears. Then listen to the complete Clean A-roll from start to end for stutter, repeat, failed start, unnatural splice, breath jump, meaning duplicate, and broken ending. Only after this listen passes may A-roll become LOCKED. Any later speech or local-speed change reopens this gate plus caption, visual-anchor, transition, and SFX timing.

## Source lineage

Inventory and identify:

- Original Talking Head
- Original Screen
- Original B-roll
- Source HyperFrames/Remotion projects and renders
- Cached word-level transcript
- Existing Preview/Final (reference only)

Never feed Preview/Final back into the next render. Preserve originals and every approved prior version.

## Master Take

Compare natural delivery, voice, light, focus, composition, and complete wording. Choose one Master Take for the A-roll. Visual continuity is more valuable than selecting the micro-best sentence from many incompatible takes.

Use an alternate only for a missing sentence, serious verbal error, or unusable Master region. Cover the entire cross-take edit with a meaningful Screen, Freeze, B-roll, or Motion asset. The cover begins at least one frame before and ends at least one frame after the take change.

## Clean A-roll lock

Lock speech before visual and motion timing:

```text
Transcript + Audio Review
→ Semantic Cleanup
→ Clean A-roll EDL / QC
→ Clean A-roll Master
→ Visual Beats
→ Motion Lock
```

Semantic cleanup removes failed starts, word repeats, sentence restarts, meaning duplicates, half-sentence NGs, and non-teaching pauses while preserving natural breathing, emphasis, and human cadence. Do not use silence detection alone.

For whiteboard storytelling, classify meaningful gaps before trimming:

- `NG_PAUSE`: accidental search/restart; remove or compress.
- `COMEDY_PAUSE`: setup-to-punch timing; preserve unless a human directs otherwise.
- `REVEAL_PAUSE`: space for a visual completion; preserve.
- `REACTION_PAUSE`: lets character/audience reaction land; preserve.
- `KNOWLEDGE_HOLD`: lets the core idea read; preserve.

Do not globally accelerate whiteboard narration. Remove repeats/NGs and non-teaching gaps first; use only local light speed changes when cadence remains natural.

Record source take, in/out, retained meaning, and removal reason. Check every cut by listening; short audio fades may prevent clicks but must not hide a word-boundary error. If approved speech changes after lock, reopen subtitles, screen timing, motion, SFX, and frame-boundary review instead of leaving the old timeline in place.

Use [CLEAN_AROLL_LOCK_TEMPLATE.md](../templates/CLEAN_AROLL_LOCK_TEMPLATE.md).

## Screen selection

- Select states that prove the spoken action/result.
- Keep an original full-context handle before every intended focus.
- Confirm the needed page, text, cursor action, and result actually exist.
- Do not use old evidence to fill silence after narration advances.

## B-roll

Use only to hide an edit, change rhythm, or add real working context. Opening a computer, typing, mouse operation, and working states are useful only when they support the current narrative.

## Media audit record

For every chosen source record filename, original/derived status, duration, resolution, fps, audio state, intended beat, and any limitation. Mark any derived Preview/Final as forbidden lineage input.
