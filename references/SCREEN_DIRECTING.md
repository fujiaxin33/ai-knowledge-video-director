# Screen Directing

## Core grammar

For important software teaching, use:

1. **Live** — 0.5–1.0s (up to about 1.5s when orientation is hard): show app identity, page, and operation context.
2. **Freeze** — extract a clean frame from the original high-resolution recording, never an old Preview.
3. **Explain** — move attention with a calibrated line, marker, thin box, callout, dim+focus, arrow, step number, or cursor marker.
4. **Continue** — return to the real operation and show the result.

Freeze provides reading time. It may remove unrelated desktop chrome, empty area, other apps, and inactive panels while keeping software identity, page identity, navigation path, and the current semantic target.

## Information screen decisions

- Whole structure matters: show full context.
- One detail matters: full context first, then context-preserving focus.
- Human remains the trust anchor: Screen Stage with a fixed small PIP.
- If the crop cannot answer “why does the viewer only need this now?”, do not crop.

## Zoom

- Zoom is not the default focus tool.
- Use only after context, when normal size is unreadable and one region is the current teaching target.
- Typical 1.1×–1.5×; rare maximum about 1.8×.
- Never chain multiple zooms or enlarge a low-quality Preview.
- Prefer Freeze + Annotation when zoom would destroy context.

## Long Prompt and output

- A complete Prompt/output is evidence for roughly 0.8–1.2s, not a reading assignment.
- Follow with a short evidence card, summary, comparison, highlight, or concept motion.
- Do not wait for a long scroll to finish or leave the old Prompt on screen after narration advances.

## Timing and completeness

- Current visuals enter within about 0–0.3s of the corresponding spoken idea.
- Keep the visual until the semantic point finishes; allow a 0.2–0.4s buffer between concepts when natural.
- If speech says “complete workspace,” show every region needed to support that claim. Use overview + detail, multiple freezes, or a concept diagram rather than one misleading crop.

## Source integrity

Original Screen is evidence. Do not fabricate buttons, menus, prompts, responses, project results, or state changes. Preview/Final media is never a source for the next version.

## Screen Hygiene gate

Before a screen enters the timeline, inspect and record:

- current app and page identity;
- current teaching focus and required context;
- desktop, wallpaper, taskbar, system tray, notifications, and unrelated windows;
- unrelated browser tabs, bookmarks, address/search bars, projects, conversations, or personal data;
- private/client/company information;
- stale annotation, baked subtitles, and labels inherited from reused evidence;
- whether the proposed crop removes noise without removing orientation or semantic boundaries.

The goal is `Context Preserved + Noise Removed`. Do not solve hygiene by zooming so far that the viewer cannot identify the app, path, page, or complete target. If a safe live crop is impossible, use a clean original freeze or rerecording rather than a low-quality Preview.

Use [SCREEN_HYGIENE_QC_TEMPLATE.md](../templates/SCREEN_HYGIENE_QC_TEMPLATE.md).
