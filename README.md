# Seedance 2.0 视频生成 Skill

> English version: [README.en.md](README.en.md)

基于 [Volcengine Ark](https://www.volcengine.com/product/ark) Video Generation API 的 Seedance 2.0 命令行工具。用于视频生成、编辑、续写与任务轮询。

## 项目能做什么

1. 文生视频（Text-to-Video）
2. 图生视频（Image-to-Video）
3. 多模态参考生成（文本 + 图片 + 视频 + 音频）
4. 视频编辑与视频续写（含多片段衔接）
5. 草稿到正式任务流程（Draft-to-final）
6. 文本任务联网搜索（Web Search）
7. 自动轮询任务状态并输出结果

## 命令入口

统一入口：

```bash
python scripts/seedance_cli.py --help
```

核心命令：

- `video`：通用视频任务（功能最全）
- `image-to-video`：图生视频快捷任务

## 目录结构

```text
seedance-video-skill/
├── SKILL.md
├── .env
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── seedance_cli.py
│   ├── run_seedance_task.py
│   ├── run_seedance_image_to_video.py
│   ├── init_environment.py
│   ├── preview.html
│   └── init_dev_env/
│       ├── setup_windows.ps1
│       ├── setup_windows.bat
│       └── setup_mac.sh
├── references/
│   ├── api-workflow.md
│   └── prompt-playbook.md
└── outputs/
```

## 运行前准备

- `ARK_API_KEY`（可写在 `.env` 或系统环境变量）
- Python 3.10+
- 输入媒体建议使用公网 URL
- 本地图片可用 `--image-file`（自动转 base64，单图最大 30MB）

## 环境初始化

### Windows

```powershell
cd scripts/init_dev_env
.\setup_windows.ps1
# 或
python ..\init_environment.py --quiet
```

### macOS / Linux

```bash
cd scripts/init_dev_env
./setup_mac.sh
# 或
python ../init_environment.py --quiet
```

## 快速开始

### 1) 文生视频

```bash
python scripts/seedance_cli.py video \
  --model doubao-seedance-2-0-260128 \
  --prompt "一只玻璃蛙栖息在雨后的热带叶片上，微距镜头，晨光折射" \
  --ratio 16:9 \
  --duration 5 \
  --generate-audio
```

### 2) 图生视频

```bash
python scripts/seedance_cli.py image-to-video \
  --prompt "参考图片生成产品广告镜头" \
  --image-url "https://example.com/product_front.png" \
  --image-file "D:/materials/product_back.png" \
  --ratio 1:1 \
  --duration 6
```

### 3) 视频编辑

```bash
python scripts/seedance_cli.py video \
  --prompt "将视频1中的香水替换成图片1中的面霜，动作和运镜不变" \
  --video-url "https://example.com/original.mp4" \
  --image-file "D:/materials/cream.png" \
  --ratio 16:9 \
  --duration 5
```

### 4) 视频续写/衔接

```bash
python scripts/seedance_cli.py video \
  --prompt "视频1中的拱形窗户打开，进入美术馆室内，接视频2，之后镜头进入画内，接视频3" \
  --video-url "https://example.com/clip1.mp4" \
  --video-url "https://example.com/clip2.mp4" \
  --video-url "https://example.com/clip3.mp4" \
  --ratio 16:9 \
  --duration 10
```

### 5) 开启联网搜索（仅文本任务）

```bash
python scripts/seedance_cli.py video \
  --prompt "联网搜索玻璃蛙的容貌特征并生成微距镜头" \
  --web-search \
  --ratio 16:9 \
  --duration 11
```

### 6) 草稿到正式

```bash
# 第一步：生成草稿
python scripts/seedance_cli.py video \
  --model doubao-seedance-2-0-260128 \
  --prompt "..." \
  --draft

# 第二步：基于 draft_task_id 出正式结果
python scripts/seedance_cli.py video \
  --model doubao-seedance-2-0-260128 \
  --draft-task-id cgt-xxxx
```

## 参数说明（通用任务 `video`）

基础参数：

- `--model`
- `--prompt`

参考输入：

- `--image-url`（可重复）
- `--image-file`（可重复）
- `--video-url`（可重复）
- `--audio-url`（可重复）
- `--first-frame-url` / `--first-frame-file`
- `--last-frame-url` / `--last-frame-file`

生成控制：

- `--resolution`
- `--ratio`
- `--duration`
- `--frames`（与 `--duration` 二选一）
- `--seed`

功能开关（写上即开启，不写即关闭）：

- `--generate-audio`
- `--no-generate-audio`（显式关闭音频）
- `--camera-fixed`
- `--watermark`
- `--web-search`
- `--return-last-frame`
- `--draft`
- `--no-poll`

任务控制：

- `--draft-task-id`
- `--callback-url`
- `--service-tier`
- `--execution-expires-after`
- `--poll-interval`
- `--timeout`
- `--output-json`

## 参数说明（图生视频 `image-to-video`）

- 必填：`--prompt`
- 输入：`--image-url` / `--image-file`（至少一个）
- 生成：`--model` `--resolution` `--ratio` `--duration` `--frames` `--seed`
- 开关：`--generate-audio` `--camera-fixed` `--watermark` `--no-poll`
- 任务：`--callback-url` `--poll-interval` `--timeout` `--output-json`

## 提示与限制

- 任务与结果 URL 一般约 24 小时有效，建议尽快转存。
- 真实人脸素材受平台规则限制，必要时请使用合规资产方案。
- 图像比例与目标比例不一致时，可能发生居中裁切。
- 大素材优先使用公网 URL，避免请求体过大。

需要更深入的 API 字段和提示词模板，可查看：

- `references/api-workflow.md`
- `references/prompt-playbook.md`
