---
name: cinematic-prompt
description: "Turn a full script, story, or voiceover draft into structured, cinematic video-generation prompts — automatically segmented scene-by-scene. Best for structured-prompt video tools like Seedance 2.0, Kling, and Jimeng (即梦). Use this skill whenever a user pastes a script / story / 口播稿 / 分镜脚本 and wants it turned into video prompts, asks to write a video prompt, generate a storyboard, split a script into shots, or describe a cinematic scene for video AI. Each segment gets a complete prompt: 基础设定 (characters), 道具 (props), 场景 (scene), 声音 (sound), 氛围与画质 (mood & quality), 画面内容 (shots — auto-decomposed into a shot list or a long take, each with 景别/构图/运镜)."
---
# 脚本转结构化视频提示词
把一段脚本（故事、口播稿、场景描述，甚至一句粗略想法）**自动拆成板块**，每个板块产出一条完整、可直接复制的电影级视频提示词。
主战场是结构化分镜类工具：**Seedance 2.0 / Kling / 即梦**。
核心理念：
1. **一个板块 = 一次生成单元**。
2. **每个板块由三根支柱构成** —— 谁在哪（基础设定+道具+场景+声音）、什么感觉（氛围与画质）、发生什么（画面内容）。

## 工作流程
### Step 1: 解析脚本，自动分段（板块化）
切分边界：场景/地点变化、明显时间跳跃、故事节拍或情绪大转折、主体/视角切换。
先给分段概览让用户确认，避免在错误的分段上浪费整篇输出。

### Step 2: 为每个板块构建完整结构
每个板块包含 6 个部分：
- **基础设定（角色）**：外貌体型、服装、标志性特征、气质/性格。有参考图用 `{{Portrait N}}` 标记。
- **道具**：关键物件的状态和与角色/事件的关系。
- **场景**：环境类型、时间、天气、空间布局、氛围细节。
- **声音**：默认「不需要配乐，仅保留同期声」。
- **氛围与画质**：风格核心 + 视觉基调（摄影机+镜头）+ 色彩与影调 + 风格参考。
- **画面内容**：自动判断分镜 or 长镜头。

### Step 3: 画面内容 —— 自动判断分镜 or 长镜头
- **长镜头（一镜到底）**：单一连续动作、沉浸式氛围渲染。用运镜带动景别变化。
- **多分镜**：动作多、主体多、情绪有转折。拆 3-5 个镜头。
每个镜头写四要素：景别、构图、运镜手法、画面内容。

### Step 4: 跨板块一致性
角色、风格核心、画幅在第一个板块定义清楚，后续板块直接复用，只写变化。

### Step 5: 呈现与迭代
输出全部板块的完整提示词，然后问是否需要调整。

## 写作原则
- **视觉要超具体**：不是「漂亮的日落」，而是「金色夕阳穿过百叶窗投下长影」。
- **动作要有物理精度**：不是「角色很害怕」，而是「双手缓缓抬至下巴前方呈防御姿态」。
- **必须有摄影语言**：每个镜头都含景别 + 构图 + 运镜。
- **道具要交代状态**：道具单列，写清样子、状态和关系。
- **节奏设计**：紧张场景短镜头快切，抒情场景长镜头慢推。

## 与 wayne-video 主管线的衔接
本 skill 产出的电影化板块和镜头想象，是主管线 `plan_segments.py` 分段规划的创意上游；主管线的 `h3_prompt.py` 会将这些创意转成可执行的六段式生产提示词，并由 `director.py --strict` 做约束闸检查。
