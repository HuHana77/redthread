# Redthread

Turn one supplied portrait into a finished 3:4 red-thread dual-scene collage. The upper panel keeps the original environment and reuses the subject as a warm glowing silhouette; the lower panel places the real subject on source-colored fiber paper, with bilingual hand-lettering and a wine-red pencil connector linking the two scenes.

中文版说明见下方。

## What it does

- Builds a polished 3:4 vertical collage from one user-supplied portrait.
- Reuses one canonical subject cutout in both panels to preserve identity, pose, clothing, accessories, and props.
- Derives the lower paper color from the source while preserving the bundled paper texture.
- Uses the bundled DartsFont for short English and Japanese hand-lettered fragments.
- Connects corresponding subject anchors with a loose wine-red colored-pencil line.
- Delivers only one inspected final PNG and keeps cutouts, masks, connector layers, and QA images private.

## Install

### Option 1 — Ask Codex to install it

Ask Codex:

```text
Use $skill-installer to install the skill at https://github.com/HuHana77/redthread/tree/main/skills/redthread
```

The skill will be available in the next Codex task. If it does not appear, restart Codex and try again.

### Option 2 — Install manually

```bash
git clone https://github.com/HuHana77/redthread.git
mkdir -p ~/.codex/skills
cp -R redthread/skills/redthread ~/.codex/skills/
```

Start a new Codex task after installation.

## Use

Attach one portrait, then ask in Chinese or English:

```text
Use $redthread to turn this portrait into a red-thread dual-scene collage.
```

You can also request a focused revision:

```text
Use $redthread to move the bilingual lettering away from the face and hands while preserving the subject and connector anchors.
```

## Requirements

- Codex, or another compatible host, with an available image-editing or compositing backend.
- One user-supplied portrait or lifestyle photo.
- No pre-installation of optional Python packages is required when another compatible image backend is available.

## Privacy

The skill uses the supplied photo only to create the requested collage. It does not instruct Codex to browse for, share, or publish the source image. Subject cutouts, masks, connector layers, and QA thumbnails remain private working files; only the final PNG is exposed. If the selected image backend is an external generation or editing service, that service receives the source image and the instructions needed to complete the edit.

## License and assets

The project source and the bundled Redthread paper texture are released under the [MIT License](LICENSE).

DartsFont v2.17 is created by DAICHI / ProjectDARTS and redistributed under the SIL Open Font License 1.1. The bundled license is at `skills/redthread/assets/fonts/dartsfont/OFL.txt`; the authoritative font source is [ProjectDARTS](https://www.p-darts.jp/font/dartsfont/).

---

# 中文说明

Redthread 是一个把单张人物照片制作成 3:4 竖版红线双场景拼贴的 Codex Skill。上半部分保留原始环境，并将同一个人物剪影处理成暖白色发光轮廓；下半部分把真实人物放在从原图提取主题色的纤维纸上，再加入英日双语手写文字与酒红色彩铅红线，让两个场景形成呼应。

## 它能做什么

- 使用一张人物照片制作完成度较高的 3:4 竖版拼贴。
- 上下场景复用同一个人物抠图，尽量保持面部、姿态、服装、配饰和随身物品真实一致。
- 从原图提取主题色重新着色下半部分纸张，同时保留内置纤维纸纹理。
- 使用内置 DartsFont 制作简短的英文和日文手写文字。
- 使用酒红色彩铅质感的曲线连接上下场景中对应的人物锚点。
- 只交付一张检查完成的最终 PNG，不展示人物抠图、蒙版、红线图层或检查缩略图。

## 安装

### 方式一：让 Codex 安装（推荐）

直接对 Codex 说：

```text
Use $skill-installer to install the skill at https://github.com/HuHana77/redthread/tree/main/skills/redthread
```

安装完成后，在下一次 Codex 任务中即可使用。如果没有出现，请重启 Codex 后再试。

### 方式二：手动安装

```bash
git clone https://github.com/HuHana77/redthread.git
mkdir -p ~/.codex/skills
cp -R redthread/skills/redthread ~/.codex/skills/
```

安装完成后，新开一个 Codex 任务。

## 使用方式

上传一张人物照片后输入：

```text
用 $redthread 把这张照片制作成红线双场景拼贴
```

也可以提出局部修改要求：

```text
用 $redthread 调整英日文字的位置，不要遮挡人物的脸和手，同时保留人物与红线锚点
```

如果照片中的小指清晰可见，红线会优先连接上下场景中对应的小指；如果小指不可识别，则会选择同一个清晰的人物轮廓尖端作为连接点。

## 使用条件

- 需要具备图片编辑或合成能力的 Codex，或其他兼容运行环境。
- 需要由用户上传一张人物或生活方式照片。
- 如果当前环境已有其他兼容图片后端，无需预先安装可选 Python 软件包。

## 隐私

Skill 只使用用户提供的照片制作本次拼贴，不会要求 Codex 搜索、分享或公开原图。人物抠图、蒙版、红线图层和检查缩略图只作为私有工作文件，最终只展示一张成品 PNG。如果运行环境选择了外部图片生成或编辑服务，该服务会接收完成编辑所需的原图和指令。

## 许可与素材

项目代码及内置 Redthread 纸张纹理使用 [MIT License](LICENSE) 开源。

DartsFont v2.17 由 DAICHI / ProjectDARTS 制作，并依据 SIL Open Font License 1.1 重新分发。字体授权文件位于 `skills/redthread/assets/fonts/dartsfont/OFL.txt`，字体来源见 [ProjectDARTS](https://www.p-darts.jp/font/dartsfont/)。

## 支持与政策

- [使用支持](SUPPORT.md)
- [隐私说明](PRIVACY.md)
- [服务条款](TERMS.md)
