# Redthread

Redthread 是一个兼容 Agent Skills 标准的图像创作 Skill，可用于豆包专业版、Codex 及其他支持 `SKILL.md` 的 Agent。它能把单张人物照片制作成 3:4 竖版红线双场景拼贴：上半部分保留原始环境，并将同一个人物剪影处理成暖白色发光轮廓；下半部分把真实人物放在从原图提取主题色的纤维纸上，再加入英日双语手写文字与酒红色彩铅红线，让两个场景形成呼应。

## 它能做什么

- 使用一张人物照片制作完成度较高的 3:4 竖版拼贴。
- 上下场景复用同一个人物抠图，尽量保持面部、姿态、服装、配饰和随身物品真实一致。
- 从原图提取主题色重新着色下半部分纸张，同时保留内置纤维纸纹理。
- 使用内置 DartsFont 制作简短的英文和日文手写文字。
- 使用酒红色彩铅质感的曲线连接上下场景中对应的人物锚点。
- 只交付一张检查完成的最终 PNG，不展示人物抠图、蒙版、红线图层或检查缩略图。

## 安装

### 方式一：让豆包专业版安装（推荐）

在豆包专业版的办公任务模式中，直接发送下面这句话：

```text
请安装 GitHub 上 HuHana77/redthread 仓库根目录的 redthread Skill，并读取根目录的 SKILL.md。首次运行时，如果环境缺少 Pillow，我允许你在当前任务环境中安装一次 Pillow。请使用内置字体、纸张和红线素材进行确定性合成，不要调用生图模型生成最终图片。
```

仓库根目录的 `SKILL.md` 是豆包专业版等 Agent 的直接安装入口。安装完成后，上传照片并说“用 redthread 把这张照片制作成红线双场景拼贴”即可调用。

如果第一次搜索没有命中，请让豆包直接访问 GitHub 上的 `HuHana77/redthread` 仓库，不要只搜索 `redthread` 这个名称。

Redthread 在豆包专业版中使用 Pillow 精确渲染内置 DartsFont、纤维纸和红线模板。首次缺少 Pillow 时只安装一次；如果安装失败或超时，任务应停止并报告原因，不得改用生图模型制作近似版本。

### 方式二：让 Codex 安装

直接对 Codex 说：

```text
Use $skill-installer to install the skill at https://github.com/HuHana77/redthread/tree/main/skills/redthread
```

安装完成后，在下一次 Codex 任务中即可使用。如果没有出现，请重启 Codex 后再试。

### 方式三：手动安装

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

- 需要豆包专业版、Codex 或其他具备图片编辑或合成能力并支持 Agent Skills 的运行环境。
- 需要由用户上传一张人物或生活方式照片。
- 豆包专业版需要可用的 Python 与 Pillow；首次运行可按上述安装文字授权安装 Pillow。
- 还需要能够保留原始像素的人物抠图或背景移除能力。

## 隐私

Skill 只使用用户提供的照片制作本次拼贴，不会要求运行它的 Agent 搜索、分享或公开原图。人物抠图、蒙版、红线图层和检查缩略图只作为私有工作文件，最终只展示一张成品 PNG。如果运行环境选择了外部图片生成或编辑服务，该服务会接收完成编辑所需的原图和指令。

## 许可与素材

项目代码及内置 Redthread 纸张纹理使用 [MIT License](LICENSE) 开源。

DartsFont v2.17 由 DAICHI / ProjectDARTS 制作，并依据 SIL Open Font License 1.1 重新分发。字体授权文件位于 `skills/redthread/assets/fonts/dartsfont/OFL.txt`，字体来源见 [ProjectDARTS](https://www.p-darts.jp/font/dartsfont/)。

## 支持与政策

- [使用支持](SUPPORT.md)
- [隐私说明](PRIVACY.md)
- [服务条款](TERMS.md)
