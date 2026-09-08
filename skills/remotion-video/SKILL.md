---
name: remotion-video
description: Build 16:9 spoken-video compositions as standalone Remotion projects with React, TypeScript, frame-based animation, estimated durations, and direct mp4 rendering. Use when the user wants video files, Remotion, mp4 export, frame-accurate motion, post-production voiceover, or theme-driven video templates; do not use for click-driven web presentations.
---
# Remotion 确定性视频制作
把文章、脚本、笔记或明确大纲做成 **16:9、逐帧可控、可直接导出 mp4 的 Remotion 视频项目**。不在流程内合成音频，适合后期统一配音。

## 核心产出
```
my-video/
├── article.md / script.md / outline.md / notes.md
└── remotion/
    ├── src/Root.tsx
    ├── src/Composition.tsx
    ├── src/chapters/<NN>-<id>/
    ├── public/assets/
    ├── preview-stills/
    └── out/
```

## 执行强度
| 强度 | 适用 | 行为 |
|---|---|---|
| Quick | ≤450字, ≤60s, 草稿演示 | 1章节, 直接实现 |
| Standard | 1-4min, 正常可发布讲解片 | 脚本+大纲, 首章锚定后继续 |
| Strict | >4min, 品牌/商业/高风险内容 | 完整规划, 逐章静帧检查 |

## 工作流
1. **输入门**:用户给源文本/脚本/笔记/明确大纲才开工。
2. **内容文件**:article.md(源材料)、script.md(口播稿)、outline.md(章节规划)。
3. **主题选择**:三套内置主题——
   - `command-film`:深色命令室,适合 agent/终端/自动化/开发者工具
   - `studio-white`:干净白色产品棚,适合 SaaS 演示/发布/课程/产品教程
   - `research-desk`:冷静分析台,适合文章/报告/论文/商业分析
4. **模板选择**:`luxury-perspective-gallery`(深色3D高端画廊)等。
5. **Remotion 项目**:`npx create-video@latest --yes --blank --no-tailwind remotion`。
6. **时序**:不合成音频,从旁白和视觉复杂度估算时长。默认 fps=30, 1920×1080。
7. **实现**:用 `useCurrentFrame()` + `interpolate()` + `Easing` + `Sequence` 做动画。不用 CSS transition/GSAP。
8. **验证**:lint → 每章至少一张静帧 → 静帧正确后渲染 mp4。
9. **记录**:notes.md 记录 fps/分辨率/总帧数/估算时长/检查过的静帧/渲染路径。

## 规则
- 用 `Composition` 在 Root.tsx,用 `Sequence` 放节拍。
- 静态资源放 `remotion/public/assets/`,用 `staticFile()` 引用。
- 最终渲染前必须做静帧检查。
- 最终 mp4 默认无声,音频/字幕在后期加。

## 与 wayne-video 主管线的衔接
主管线 `gen_segments.py` 用 AI 模型(即梦/H3/火山/小云雀)生成带货镜头;本 skill 用 Remotion 做**确定性 16:9 讲解片段**(产品教程/数据可视化/品牌宣传片)。两者互补:AI 生成实拍感镜头,Remotion 生成可控动画片段,最终在 `assemble.py` 或剪映中合流。
