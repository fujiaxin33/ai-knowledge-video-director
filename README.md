# AI Knowledge Video Director

一个面向 Codex 的开源 Skill，用来规划、导演、剪辑和质检 AI 知识视频与真实软件教学视频。

它不是“一装就自动生成神片”的按钮。它解决的是更基础、也更容易被忽略的问题：先把内容分级、画面路由、屏幕取景、Annotation 几何和最终 QC 规则讲清楚，让 AI 在 First Cut 阶段尽量少犯重复错误。

> Community project. Not an official OpenAI product.

Current version: **v1.3.0**

## What changed in v1.3

v1.3 is the **Internet-Native Live Drawing Production Pipeline** update. `STANDARD` and the v1.2 whiteboard route remain backward compatible; two optional, composable layers add event-led internet storytelling and Draw While Talking only when the content warrants them.

The release adds:

- clause-level semantic retake detection, approved-script coverage, and a mandatory start-to-end final listen;
- voice/visual fact checks for counts, numbers, terms, names, brands, polarity, and relations;
- Internet Punch Maps, cultural-reference policy, real-meme default OFF, and high-quality asset preservation;
- Hand-as-actor, Hand-tip/reveal sync, continuous canvas, knowledge residue, anticipatory empty space, and page-turn risk;
- adaptive caption/scale hierarchy, local speed routing, callback duration, event-based SFX, render budgets, hero-keyframe approval, and human gates;
- 16 executable regression groups, including an exact 20-case matrix for Production 1–12 and Live Drawing A–H.

The production evidence is summarized in [PRODUCTION_EVIDENCE_EP03_EP05.md](PRODUCTION_EVIDENCE_EP03_EP05.md) without including private media or project paths.

## What changed in v1.2

v1.2 adds an optional `WHITEBOARD_STORYTELLING` preset while preserving the existing `STANDARD` route for desktop tutorials, real-software demonstrations, talking head, and evidence-led courses.

The preset adds:

- Draw Before Show and Hand-tip/reveal-front contracts;
- progressive scene construction instead of repeated complete cards;
- limited character animation, anchored pose changes, comedy timing, and Knowledge Hero holds;
- semantic single-line captions and event-bound SFX;
- whiteboard-specific QC, failure patterns, planning templates, and deterministic validators;
- regression tests A–C for the original route and whiteboard tests D–I for drawing, alignment, comedy, PPT risk, captions, and generalization.

It does not generate a finished episode by itself, guarantee comedy or taste, or remove human review.

## What changed in v1.1

The first production-validation update adds safeguards that became important during a complete real-world workflow:

- build a project-specific terminology dictionary and validate final subtitles/copy;
- lock semantically clean A-roll before motion timing;
- strengthen annotation precision and “complete screen” proof;
- run an explicit Screen Hygiene gate;
- treat AI motherboards as extractable asset libraries, not final pages;
- prefer real failure, software, result, and repository evidence;
- route verified product logos only at meaningful identity moments;
- flag rolling 10-second concept-only stretches as `PPT_RISK`.

These rules are designed to reduce repeated correction cycles. They do not promise zero editing or replace human aesthetic/release judgment.

## 为什么做这个 Skill

在连续制作知识类视频时，AI 剪辑经常出现这些问题：

- 画面很聪明，但没有人的表达节奏；
- 软件录屏被错误裁切，信息边界不完整；
- 框线、横线和高亮没有准确绑定真实目标；
- 长 Prompt 和长页面停留太久；
- Presenter 太大，软件内容反而看不清；
- 一个小修改也要反复解释和返工；
- Preview 被继续当作新版本源素材，画质逐轮下降。

这个 Skill 把这些真实返工经验沉淀为可以复用的导演规则、模板和验证脚本。

## 它会做什么

```text
Approved Script + Original Media
                ↓
AI Knowledge Video Director Skill
                ↓
Intake → Speech Lock → Pre-render Direction → Build → Timeline/Render → Final Listening/Release
```

它会帮助 Codex：

1. 判断内容等级、横竖画布、主模式，以及可选的 Internet-Native / Live Drawing 层；
2. 在Motion之前完成Clean A-roll，并建立Canonical Terms；
3. 为每句关键信息分配 Human、Original Screen、HyperFrames、Remotion 或 NO EFFECT；
4. 使用 `Full Context → Focus → Highlight → Hold` 组织软件教学；
5. 把 Annotation 绑定到最终画布中的真实像素目标；
6. 按Real Evidence优先级选择真实失败、软件、结果与Repo证据；
7. 在导出前检查Screen Hygiene、PPT Risk、安全区、闪帧、黑帧、码率、字幕和音频；
8. 在白板模式下检查渐进绘制、Hand 对齐、角色锚点、口播画面同步、SFX 命中和单行语义字幕；
9. 在完整渲染前检查动作态 Storyboard、英雄关键帧、资产进入方式和渲染预算；
10. 对最终成片进行从头到尾的听检与人审放行。

## 工具分工

| Layer | Responsibility |
|---|---|
| ChatCut | 可编辑 Timeline、字幕、音频、屏幕/B-roll组织和导出 |
| HyperFrames | 标题、标签、短卡、框线、横线、高亮和轻量信息动效 |
| Remotion | 流程、卡片重组、状态变化、前后对比和复杂动画 |
| FFmpeg / local tools | 本地回退、技术检查和可重复验证 |

Skill 是判断与路由层，不替代这些工具，也不会在未经授权时自动上传素材、调用付费生成或发布内容。

## Repository Structure

```text
ai-knowledge-video-director/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── CONTENT_AND_FORMAT_ROUTER.md
│   ├── LAYOUT_SYSTEM.md
│   ├── SCREEN_DIRECTING.md
│   ├── ANNOTATION_GEOMETRY.md
│   ├── TERMINOLOGY_AND_PRODUCT_IDENTITY.md
│   ├── ASSET_AND_EVIDENCE.md
│   ├── MOTION_DESIGN.md
│   ├── WHITEBOARD_STORYTELLING.md
│   ├── WHITEBOARD_QC.md
│   ├── WHITEBOARD_FAILURE_PATTERNS.md
│   ├── INTERNET_NATIVE_STORYTELLING.md
│   ├── LIVE_DRAWING_STORYTELLING.md
│   ├── PRODUCTION_GATES.md
│   └── ...
├── templates/
├── scripts/
└── examples/
```

## Installation

### Windows PowerShell

```powershell
git clone https://github.com/fujiaxin33/ai-knowledge-video-director.git "$env:USERPROFILE\.codex\skills\ai-knowledge-video-director"
```

### macOS / Linux

```bash
git clone https://github.com/fujiaxin33/ai-knowledge-video-director.git ~/.codex/skills/ai-knowledge-video-director
```

安装后新建一个 Codex 任务，让 Skill 列表重新加载。

## Usage

显式调用：

```text
Use $ai-knowledge-video-director to plan and audit an AI software teaching video.
```

也可以直接描述一个 AI 知识视频、Prompt 教程、Codex/Obsidian/ChatGPT 软件演示或 GitHub Skill 视频任务；默认允许 Codex 在匹配时自动发现该 Skill。

白板模式示例：

```text
Use $ai-knowledge-video-director to plan a funny whiteboard knowledge explainer with progressive drawing and a Knowledge Hero.
```

## Validation Scripts

仓库包含：

- `validate_annotation_bounds.py`
- `validate_layout_safe_zones.py`
- `make_annotation_review_sheet.py`
- `make_timeline_contact_sheet.py`
- `detect_flash_frames.py`
- `ffprobe_quality_check.py`
- `validate_canonical_terms.py`
- `detect_ppt_risk.py`
- `validate_draw_on.py`
- `validate_voice_visual_alignment.py`
- `validate_sfx_timing.py`
- `validate_character_anchors.py`
- `validate_whiteboard_captions.py`
- `validate_content_routing.py`
- `validate_final_listening.py`
- `validate_storyboard_contract.py`

`python tests/run_skill_tests.py` 运行 16 组兼容性、白板、生产门禁、Internet-Native 与 Live Drawing 行为测试；`python tests/run_v1_3_cases.py` 单独运行目标规定的 20 个精确抽象案例。

运行这些脚本通常需要 Python 3、FFmpeg/FFprobe，以及 Pillow 和 NumPy。脚本提供可审查证据，但最终语义完整性和发布仍需人工确认。

## Design Principles

- Original Screen 是证据，不伪造软件按钮、Prompt、结果或 GitHub 页面。
- Information Screen 默认保留语义上下文；裁切必须有教学理由。
- Annotation 坐标在最终画布中测量，不凭感觉放框。
- Motion copy 是压缩后的教学标签，不是第二套字幕。
- Human first 是信任原则，不代表人物长期占据大画面。
- 自动化目标是减少重复返工，不是取消人的最终判断。
- Canonical Terms来自当前项目事实源，不是跨项目硬编码的错词表。
- Verified Logo只在有教学意义的身份节点出现，不做持续品牌挂件。
- AI母板先拆分、清理或重建；真实证据优先于AI示意图。

## License

MIT License. See [LICENSE](LICENSE).
