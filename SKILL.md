# GCfango — Code-Driven Motion Graphics Skill
> **Deterministic, Pure-Code Animation & Algorithmic Audio Synthesis Pipeline**

GCfango 是基于纯代码驱动的高精度动态图形（Motion Graphics, MG）创作与音视频合成 Skill。区别于概率性扩散/文生视频模型（画面易形变、闪烁、文字崩溃、无法毫秒级定点修改），本架构将整部片子抽象为**纯时间函数**，实现 100% 确定性、无损矢量边缘、以及音画帧级咬合。

---

## 核心设计哲学 (Core Philosophy)

### 1. 纯时间函数契约 (Pure Function of Time)
```javascript
window.renderAt = async (t) => { ... }
```
- **绝对无状态 (Stateless)**：任意时刻 `t`（秒）的画面是完全由 `t` 计算得出的唯一定态。禁止依赖 `requestAnimationFrame` 累加变量、内部轮询或随机数累加（所有随机必须是伪随机种子 `rng(seed)`）。
- **时间任意穿梭 (Scrubbable)**：可以毫秒级渲染任意单帧，单帧修改只调对应时间区间的数学公式，绝不影响前后帧。

### 2. 运动物理与过冲曲线 (Spring & Overshoot Math)
MG 动画灵动感的核心在于**非线性物理反馈**：
- **阻尼弹簧 (Damped Spring)**:
  $$s(t) = 1 - e^{-a t} \left(\cos(b t) + \frac{a}{b} \sin(b t)\right)$$
- **挤压与拉伸 (Squash & Stretch)**:
  速度最大时发生形变，到达极值时反弹。
- **经典过冲 (Pop / outB)**:
  物体到达目标位置时会先冲过约 10%–20%，再拉回稳定，模拟机械或橡胶弹性。

### 3. 音画单点真理 (Single Source of Truth: cues.json)
- 画面与声音共享一份 `cues.json`，只记录**帧号 (Frame Number)**。
- 画面在 `frame: 24` 发生落地，音频就在 `T('seed_land') = 24 / fps` 触发打击音效。
- 任何节奏调整只需在 `cues.json` 改动一次，双端自动同步，杜绝“改了画面声音漂移”。

### 4. 广播级声学合成 (Algorithmic Audio & QC)
- 基于 Python `mgaudio`，不依赖外部版权音乐库。
- 自动和弦进行、Drop 能量曲线、滤波器包络自动化、母带动态压缩与响度规整（-14 LUFS，True Peak ≤ -1.5 dBFS）。

---

## 经典实战工程结构 (`demos/30-tree`)

以 30 秒扁平矢量影片《一棵树的三十秒》为例：
```
demos/30-tree/
├── cues.json      # 共享时间轴与打击点帧号清单
├── index.html     # SVG 矢量世界 + 摄影机组 + 纯时间渲染函数
├── audio.py       # Pop/EDM 结构配乐 + 物理音效合成脚本
└── out/           # 渲染输出目录 (video.mp4, audio.wav, stills/)
```

### 运行与渲染指南

1. **安装环境依赖**：
   ```bash
   npm install
   pip install -r requirements.txt
   ```
2. **生成配乐与音效**：
   ```bash
   python demos/30-tree/audio.py
   ```
3. **渲染无损视频并合成音频**：
   ```bash
   node harness/render.mjs demos/30-tree --crf 16
   ```
4. **快速导出关键帧静帧（调色与构图检查）**：
   ```bash
   node harness/render.mjs demos/30-tree --stills 2.0,8.2,15.8,22.8,29.5
   ```
