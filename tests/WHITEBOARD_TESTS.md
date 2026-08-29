# Whiteboard Storytelling Tests D–I

These fixtures are independent of all blind-test episodes. They test structured directing decisions and deterministic validators rather than matching prose headings.

| Test | Input | Observable expectation |
| --- | --- | --- |
| D — Draw Before Show | coffee cup → coffee → steam → drinker | progressive stroke/mask/assembly states; Hand follows reveal front; no four-image sequence |
| E — Voice Visual | three voice/visual beats A/B/C | no premature/late concept; each reveal completes in its keyword contract |
| F — Comedy | cat-whisker knowledge situation | Setup → Anticipation → Pause → Impact → Reaction; anchor and SFX validators pass |
| G — PPT Risk | static UI-card plan versus character-action plan | card plan HIGH; action plan LOW; intentional Knowledge Hero remains LOW |
| H — Semantic Caption | long condensation explanation | one shorter semantic line inside safe zone |
| I — Story Shell Generalization | sea-breeze explanation | new shell, progressive scene and character arc; no prior story topics or forbidden technical shells |

Run A–I together:

```bash
python tests/run_skill_tests.py --report tests/results/skill_test_results.json
```

The run does not read or modify EP03, EP04, or EP05.
