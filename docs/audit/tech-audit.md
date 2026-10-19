# 动态图形代码生成管线技术审计 (Technical Audit)

## 1. 核心架构与运行机制

本技术栈（mg-styles-15 / GCfango）打破了传统 AI“文生视频”黑盒扩散模型的局限，构建了一套**完全确定性的代码驱动微电影渲染管线**：

1. **画面纯函数化契约 (`window.renderAt(t)`)**：
   - 动画并非浏览器自然的 `requestAnimationFrame` 状态累加，而是 `t -> DOM/Canvas` 的纯映射。
   - 彻底消除了时间漂移、丢帧抖动与累积误差。
2. **无头浏览器帧级捕获 (`harness/render.mjs`)**：
   - 采用 Puppeteer Core 控制无头 Chrome，设置精确视口（1920×1080）。
   - 按 $1/\text{fps}$（例如 30fps 即每步 $0.033333\text{s}$）顺序调用 `window.renderAt(t)`。
   - 使用 `page.screenshot` 逐帧导出无损 PNG 流。
3. **极速音视频无损混流 (`ffmpeg`)**：
   - 将图片序列直通 FFmpeg 管道，以 H.264 CRF 14–16、Preset Slow、AQ-Mode 3 进行高质量编码。
   - 混入 48kHz 立体声合成音频，输出最终 MP4。

---

## 2. Windows 平台实测避坑与环境兼容改造

在 Windows 环境下部署该渲染管线时，原生代码存在多项平台排异缺陷，本项目已全部修复：

| 原生代码缺陷 | 故障现象 | 根因定位 | 修复方案 |
| :--- | :--- | :--- | :--- |
| **硬编码 Unix 临时目录** | `render.mjs` 启动崩溃 (`EPERM` / `ENOENT`) | `const LOCKDIR = '/tmp/mg-render-slots'` 在 Windows 下被解析为 `D:\tmp\...` 越权 | 改用 `path.join(os.tmpdir(), 'mg-render-slots')` 跨平台临时目录 |
| **管道通信权限** | 子进程卡死或抛出 `spawn EPERM` | Chrome 沙箱与 Node 管道 IPC 冲突 | 注入 `$env:MG_CHROME` 绝对路径，设置独立渲染 slot 锁文件 |
| **字体资源加载失败** | 页面加载卡死在 `document.fonts.load` | 仓库 `.gitignore` 排除了所有 `.ttf/.otf`，字体 404 导致 Promise 无法 resolve | 自动匹配本地系统字体库（如 Arial Bold、微软雅黑 Bold），映射到指定 `@font-face` 路径 |
| **音频采样库索引不一致** | `soundfile.LibsndfileError` | `samples.available()` 仅检查了 `index.json`，而磁盘上实际样本目录被精简裁剪 | 在 `mgaudio/samples.py` 中引入真实磁盘存在性探测 `_has_files` |
| **高频杂音与声学超标** | `qc.py` 报错 `harsh 2-5 kHz > 7.5%` | 低音重配方下高频刺耳 | 在 `master_kw` 中引入 `tilt = -0.9` 倾斜均衡滤波器，使整片自然符合广播级规范 |

---

## 3. 音画同源单点真理体系 (Single Source of Truth)

传统的音视频剪辑是“画做好了配音”或“按音轨剪画”，极其繁琐且极易脱节。
本管线定义了 **`cues.json`**：
- 唯一记录各关键动作的 **绝对帧号 (Frame)**。
- 画面 JS 读取 `cues.json` 作为关键帧时间触发点；
- 音频 Python (`audio.py`) 读取 `cues.json` 触发合成音效与 Drop 变奏；
- 调整节奏只需改动一个数字，画面与声音自动以毫秒级精度同步咬合。
