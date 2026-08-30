# Whiteboard Failure Patterns

## v1.3 additions

- **Final state used as first state** — Storyboard keyframe is pasted whole into the timeline. Rebuild with an explicit Entry Method.
- **Draw Before Show without Draw While Talking** — Object is drawn early and narration merely describes a finished board. Align becoming states to spoken cues.
- **Hand as cursor** — Hand only follows paths. Give it a purposeful action: compare, hesitate, point, stamp, erase, move, or reveal.
- **Knowledge residue becomes clutter** — Keep only relationships needed by the next beat; erase or transform the rest.
- **Asset quality collapse** — Finished comedy art becomes a stick-figure/debug placeholder. Reveal the approved final asset progressively instead.
- **Internet annotation system** — Multiple jokes become persistent labels. Limit to one brief annotation per beat.

Each row defines symptom, reason, detection and correction. Automated checks only cover structured evidence; contact-sheet and playback review remain necessary.

| Failure | Symptom | Why it fails | Detection | Fix |
| --- | --- | --- | --- | --- |
| Fake Handwriting | Hand moves while content fades independently | breaks physical causality | tip/front manifest or frame review | bind Hand tip to stroke/mask front |
| Draw Without Hand Tracking | drawing grows away from pen tip | looks automated, not drawn | tip distance exceeds tolerance | derive both from one progress value |
| Pop Instead of Draw | drawable object appears complete | removes anticipation and build | start/end frames show no intermediate states | use stroke, mask, or assembly build |
| Slide Thinking | every sentence creates a new page | story never accumulates | repeated hard resets/contact sheet | grow one scene until viewer task changes |
| Static Character | character stands while labels change | character is decoration | no action/reaction in beat manifest | direct start, action, reaction, result |
| Missing Reaction | impact ends immediately | punch has no release | comedy phase manifest lacks reaction | add visible reaction and hold |
| Premature Reveal | next object appears before voice | spoils narration and splits attention | voice/visual timing delta | delay reveal or use brief anticipation only |
| Late Reveal | voice moves on before object completes | audience loses mapping | voice/visual timing delta | start earlier or simplify the drawing |
| Voice-Visual Drift | current picture teaches another sentence | meaning becomes false/unclear | beat-map semantic review | retime from locked A-roll |
| PPT Card Sequence | repeated complete cards dominate | reads as animated slides | PPT score/card-layout repetition | replace with scene action/relationship growth |
| Caption Dominance | subtitle is largest/strongest object | story becomes secondary | box/font/area candidate + human review | shorten, lower contrast, protect story hierarchy |
| Overloaded Frame | many labels/arrows/props compete | no primary meaning | element-count/priority review | split beats or delete auxiliaries |
| Excessive Brand Color | accent fills most elements | emphasis loses meaning | palette/contact-sheet review | reserve one/few accents for state change |
| UI Residue | SaaS cards/toggles appear in a drawn story | breaks world and feels templated | `ui_like_structure` PPT dimension | use sketch, bubble, physical choice, or real UI only |
| SFX Drift | sound misses visible impact | weakens causality | SFX/impact delta | move transient to impact frame |
| Continuous SFX Noise | draw/motion sound continues without action | tires viewer and masks voice | SFX duration exceeds motion | trim to pen-down/action interval |
| Pose Anchor Drift | feet/base jumps on pose swap | destroys character continuity | anchor delta validator | normalize transparent bounds and lock base anchor |
| Mirror Text | character asset flip reverses text/logo | visibly wrong evidence | mirror-safety review | separate character and text layers |
| Asset Background Leakage | white rectangle/halo enters canvas | looks pasted from a sheet | native-size alpha/contact review | reclean alpha or rebuild element |
| Story Shell Overfitting | prior episode setting/objects recur by habit | skill learns template, not method | generalization test | choose a shell from the new knowledge goal |
| Forced Meme | trendy reference is unrelated | dates and weakens knowledge | human relevance review | remove or make meme serve the concept |
| Excessive Comedy | jokes interrupt factual sequence | knowledge becomes secondary | beat-purpose review | reduce punches and preserve accuracy |
| Term Before Understanding | jargon appears before visual conflict | creates definition-first lecture | beat-order review | story/conflict first, terminology after understanding |
| Overlong Episode | repeated holds/explanations exceed need | pacing and retention fall | duration/repetition audit | remove repeats, PPT holds and redundant captions |
| Repetitive Visual State | same completed composition persists/repeats | motion has no new meaning | contact-sheet similarity + beat intent | add meaningful action/build or shorten |
