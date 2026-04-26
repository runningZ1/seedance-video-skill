# Seedance 2.0 Prompt Playbook

## 1) Core Prompt Structure

Write prompts in this order (required elements first):

1. **Subject + action** (required) — who does what; the logical foundation
2. **Scene + visual style** (optional) — location, lighting, art direction, color palette
3. **Camera language** (optional) — shot type, movement, rhythm
4. **Audio** (optional) — background music, voice, SFX, subtitle sync
5. **Output constraints** (optional) — text overlays, subtitles, clean frame, no watermark

## 2) Multimodal Referencing Rules

- Keep upload order deterministic.
- Refer with exact ordinal tokens: `图片1`, `图片2`, `视频1`, `音频1` (based on upload order within each modality type).
- Do NOT reference assets by their asset ID in the prompt — always use ordinal tokens.
- Tie each reference to a clear target:
  - Image reference: `参考/提取/结合 图片1 中的 [被参考元素]`
  - Camera reference: `参考 视频1 的运镜`
  - Action reference: `参考 视频1 的动作`
  - Effect reference: `参考 视频1 的特效`
  - Timbre reference: `音色参考 音频1`
  - Music/rhythm reference: `全程使用音频1作为背景音乐`

If strict first/last frame consistency is required, use API roles `first_frame` and `last_frame` instead of only textual hints.

## 3) Reusable Templates

### A) Text-to-video

```
[主体] 在 [场景] 中执行 [动作]，整体风格 [风格]，镜头 [运镜描述]，音频为 [音频描述]。
```

### B) Multimodal reference generation (R2V)

**Single image reference:**
```
参考/提取/结合 图片1 中的 [主体]，生成 [画面描述]，保持 [主体] 特征一致。
```

**Multi-image reference (multiple subjects or elements):**
```
参考/提取/结合/按照/生成+图片n 中的 [被参考元素]，生成 [画面描述]，保持 [被参考元素] 特征一致。
```

**Storyboard / grid shot reference:**
```
参考图片中的分镜图，生成 [画面描述]。图片中的各个分镜构图要按照顺序出现，之后 [继续剧情]。
```

**Video action reference:**
```
参考 视频1 的 [动作描述]，生成 [画面描述]，保持动作细节一致。
```

**Video camera reference:**
```
参考 视频1 的 [运镜描述]，生成 [画面描述]，保持运镜一致。
```

**Video effect reference:**
```
参考 视频1 的 [特效描述]，生成 [画面描述]，保持特效一致。
```

**Combined modalities (image + video + audio):**
```
全程使用视频1的 [构图/运镜]，全程使用音频1作为背景音乐。[主体描述]；首帧为图片1，[分段时间轴剧情描述]。
```

### C) Video editing (V2V)

**Add element:**
```
在 视频1 的 [时间位置] [空间位置]，增加 [元素描述]。
```

**Remove element:**
```
删除 视频1 中的 [被删除元素]，视频其他内容保持不变。
清除 视频1 [位置] 上的 [被删除元素]，保持 [保留内容] 不变。
```

**Replace element:**
```
将 视频1 中的 [对象A] 替换为 图片1 中的 [对象B]，动作和运镜不变。
将 视频1 [位置] 中的 [对象A] 替换成 [对象B]，运镜不变。
```

### D) Video extension (extend / track fill)

**Extend forward (before):**
```
向前延长 视频1，[延长内容描述]。
```

**Extend backward (after):**
```
生成 视频1 之后的内容：[延长段落剧情和镜头说明]，动作和风格与前段连续。
```

**Track completion (2–3 clips with transitions):**
```
视频1，[过渡画面描述]，接视频2，[过渡画面描述]，接视频3。
```

Example:
```
视频1中的拱形窗户打开，进入美术馆室内，接视频2，之后镜头进入画内，接视频3。
```

### E) On-screen text

**Slogan / logo:**
```
「文字内容」+「出现时机」+「出现位置」+「出现方式」，「文字特征（颜色、风格）」
```

**Subtitle synchronized to audio:**
```
画面底部出现字幕，字幕内容为"……"，字幕需与音频节奏完全同步。
```

**Speech bubble:**
```
「角色」说："……"，角色说话时周围出现气泡，气泡里写着台词。
```

### F) Character dialogue (multi-person)

```
[人物A]说："[台词A]"，镜头切到[人物B]，[人物B]回答："[台词B]"，[人物A/B]说话时，对话随意自然，画面底部出现对应台词字幕。
```

## 4) Audio Reference Patterns

- **Timbre/voice reference:** `「角色」说："「台词」"，音色参考 音频1。`
- **Music/rhythm reference:** `全程使用音频1作为背景音乐。`
- **Audio content at ideal moment:** `[理想出现时机] + 音频1。`

## 5) Image Reference Use Cases

| Use case | Pattern |
|---|---|
| Product 360° showcase | `提取图片1/2/3的[产品]，背景换成[背景]，以[产品]为主体缓慢旋转，清晰展示正面侧面背面。` |
| Character style transfer | `参考图片1/2/3中的[角色]形象，生成[场景]画面。` |
| Logo in scene | `画面逐渐模糊，后出现图片1的Logo。` |
| Multi-character scene | `参考图片1中的[角色A]，参考图片2中的[角色B]，在[场景]中[动作描述]。` |
| Multi-element assembly | `图片1中的[角色]身着图片2中的[服装]，在图片4中的[场景]内，[图片5中的标识]始终显示在画面[位置]。` |

## 6) Quality Checklist

- Avoid ambiguous pronouns and missing subjects.
- Prefer common Chinese characters; avoid rare symbols.
- Do not overload one sentence with conflicting camera instructions.
- Keep subject identity constraints explicit when multiple people appear.
- For on-screen text, use common characters; rare symbols degrade rendering.
- Always note "纯净无任何字幕" if clean frame is required.
- When specifying face center framing: `要求画面中人物居中，完整展示人物的整个脑袋和上半身，始终对焦人脸，人脸始终清晰。`

## 7) Debug Strategy

- If style drifts: strengthen reference bindings (`参考 图片1...`).
- If motion drifts: constrain camera path and speed in short phrases.
- If subtitles fail: explicitly ask for subtitle position, timing, and sync.
- If output looks cropped: align requested `ratio` with input image ratio.
- If character appearance inconsistent across frames: add multi-angle reference images.
- If on-screen text rendering is wrong: use logo-reference pattern (3.2 multi-image, Logo参考).

## 8) Prompt Formula Summary (from official guide)

**Multimodal reference:**
- Image: `参考/提取/结合 + 「图片n」中的「主体/被参考元素」，生成「画面描述」，保持特征一致。`
- Video action: `参考「视频n」的「动作描述」，生成「画面描述」，保持动作细节一致。`
- Video camera: `参考「视频n」的「运镜描述」，生成「画面描述」，保持运镜一致。`
- Audio timbre: `「角色」说："「台词」"，音色参考「音频n」。`
- Audio content: `「理想出现时机」+「音频n」。`

**Video editing:**
- Add: `清晰描述「元素特征」+「出现时机」+「出现位置」`
- Remove: `点明需要删除的元素，对于保持不变的元素，在提示词中加以强调`
- Replace: `清晰描述更换元素即可`

**Video extension:**
- Single clip: `向前/向后延长「视频n」+「需延长的视频描述」`
- Track fill: `「视频1」+「过渡画面描述」+接「视频2」+「过渡画面描述」+接「视频3」`

## Sources

- https://www.volcengine.com/docs/82379/2222480?lang=zh
- https://www.volcengine.com/docs/82379/2291680?lang=zh
