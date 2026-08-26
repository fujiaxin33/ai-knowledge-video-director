# AI Knowledge Video Director

一个面向 Codex 的开源 Skill，用来规划、导演、剪辑和质检 AI 知识视频与真实软件教学视频。

它不是“一装就自动生成神片”的按钮。它解决的是更基础、也更容易被忽略的问题：先把内容分级、画面路由、屏幕取景、Annotation 几何和最终 QC 规则讲清楚，让 AI 在 First Cut 阶段尽量少犯重复错误。

> Community project. Not an official OpenAI product.

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
Pre-production → First Cut → Polish → Final
```

它会帮助 Codex：

1. 判断内容等级、横竖画布和主要证据类型；
2. 为每句关键信息分配 Human、Original Screen、HyperFrames、Remotion 或 NO EFFECT；
3. 使用 `Full Context → Focus → Highlight → Hold` 组织软件教学；
4. 把 Annotation 绑定到最终画布中的真实像素目标；
5. 保留原始素材血缘与单一 Master Take 连续性；
6. 在导出前检查安全区、闪帧、黑帧、码率、字幕和音频。

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
│   ├── MOTION_DESIGN.md
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

## Validation Scripts

仓库包含：

- `validate_annotation_bounds.py`
- `validate_layout_safe_zones.py`
- `make_annotation_review_sheet.py`
- `make_timeline_contact_sheet.py`
- `detect_flash_frames.py`
- `ffprobe_quality_check.py`

运行这些脚本通常需要 Python 3、FFmpeg/FFprobe，以及 Pillow 和 NumPy。脚本提供可审查证据，但最终语义完整性和发布仍需人工确认。

## Design Principles

- Original Screen 是证据，不伪造软件按钮、Prompt、结果或 GitHub 页面。
- Information Screen 默认保留语义上下文；裁切必须有教学理由。
- Annotation 坐标在最终画布中测量，不凭感觉放框。
- Motion copy 是压缩后的教学标签，不是第二套字幕。
- Human first 是信任原则，不代表人物长期占据大画面。
- 自动化目标是减少重复返工，不是取消人的最终判断。

## License

MIT License. See [LICENSE](LICENSE).

