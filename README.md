# Redthread

Redthread 是一个面向 Codex 的图像创作 Skill。它将一张人物照片制作成 3:4 竖版双场景拼贴：上半部分保留原始环境并呈现发光剪影，下半部分使用真实人物剪影与取自原图的主题纸张色彩，再用酒红色手绘线连接两个场景。

## 主要特点

- 只需要一张人物照片
- 输出一张完成的 3:4 竖版 PNG
- 上下场景复用同一个人物剪影，尽量保持真实面部、姿态、服装与配饰
- 使用随原图变化的纸张主题色
- 使用 DartsFont 制作英文与日文手写文字
- 使用酒红色彩铅质感的红线连接上下人物
- 自动检查最终画面，只交付成品，不展示抠图、蒙版等中间文件

## 安装

Redthread 目前通过 GitHub 发布，尚未上架 OpenAI 的公共 Plugins Directory。因此，第一次安装时需要把仓库地址一起发给 Codex；只发送 `redthread` 这个名字无法让尚未安装它的 AI 自动找到仓库。

把下面整段文字复制给 Codex：

```text
Use $skill-installer to install https://github.com/HuHana77/redthread from path skills/redthread with the name redthread.
```

也可以直接把这个地址发给 Codex，并让它安装其中的 Skill：

```text
https://github.com/HuHana77/redthread/tree/main/skills/redthread
```

安装完成后，请在下一轮对话或新任务中使用；如果没有出现，重启 Codex 后再试。

## 使用方法

上传一张照片，然后发送：

```text
使用 $redthread，把这张照片制作成红线双场景拼贴。
```

也可以直接描述你想调整的内容，例如：

```text
使用 $redthread，把下半部分的纸张改成从照片中提取的暖灰色，保留人物和红线位置。
```

```text
使用 $redthread，重新调整英文和日文文字的位置，不要遮挡人物的脸和手。
```

## 适合的照片

- 人物主体清晰、轮廓完整
- 脸、手、衣服和随身物品没有被严重裁切
- 背景保留一定空间，方便放置发光剪影和文字
- 原图分辨率越高，最终细节通常越好

如果小指清晰可见，红线会优先连接上下场景中对应的小指；如果小指不可识别，则会选择同一个清晰的人物轮廓尖端作为连接点。

## 输出规则

Redthread 默认只展示和交付一张最终 PNG。人物抠图、透明蒙版、红线图层和质量检查缩略图都属于内部工作文件，不会单独输出。

## 项目结构

```text
redthread/
├── .codex-plugin/plugin.json
├── assets/
└── skills/
    └── redthread/
        ├── SKILL.md
        ├── assets/
        ├── references/
        └── scripts/
```

## 授权与素材

项目代码及 Redthread 自制纸张纹理采用 [MIT License](LICENSE)。

DartsFont v2.17 由 DAICHI / ProjectDARTS 制作，并依据 SIL Open Font License 1.1 重新分发。字体授权文件位于 `skills/redthread/assets/fonts/dartsfont/OFL.txt`，字体来源见 [ProjectDARTS](https://www.p-darts.jp/font/dartsfont/)。

## 支持与政策

- [使用支持](SUPPORT.md)
- [隐私说明](PRIVACY.md)
- [服务条款](TERMS.md)

## 项目地址

https://github.com/HuHana77/redthread
