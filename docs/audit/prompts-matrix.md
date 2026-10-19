# 动态设计风格与提示词工程全景矩阵 (Prompts Matrix)

本矩阵归纳了 GCfango 体系中的核心设计风格、技术选型底层原理与提示词关键参数：

| 风格序号 & 名称 | 核心技术选型 | 视觉标志 (Signature Features) | 音乐与音效配方 | 适用场景 |
| :--- | :--- | :--- | :--- | :--- |
| **01 · Flat Vector (扁平矢量)** | SVG + DOM Transform | 经典高饱和色块、硬阴影、阻尼弹簧过冲、挤压拉伸 | Pop/EDM, F 大调 120BPM, Bubble Pop, Marimba 碎音 | 品牌广告、互联网产品秀、SaaS 功能演示 |
| **02 · Line Art (极简线条)** | SVG Path + Dashoffset | 一笔到底、连续线条描边、流体几何、优雅留白 | 氛围极简 Piano/Chime, 柔和白噪声滑擦 | 高端美学、艺术展宣发、设计工作室短片 |
| **03 · Isometric 2.5D (等轴测视界)** | Canvas 2.5D / SVG 投影 | 30° 等轴测网格、箱庭微缩世界、建筑模块层级弹出 | Synth Funk, 木琴跳跃, 机械方块拼接打击声 | 智慧城市、工业互联、数据流架构、游戏概念 |
| **04 · 3D Render (C4D/Blender 充气质感)** | Blender Cycles + Three.js | 柔和黏土、充气气囊膨胀、柔和景深、微距材质 | Chillhop / Lo-Fi, 气球摩擦、软胶撞击 | 年轻潮流、潮玩手办、萌系品牌 IP |
| **05 · Cel Boil (逐帧手绘线颤)** | HTML5 Canvas + 噪声噪点 | 抽帧 Line Boil（线宽微颤）、纸张肌理、水墨颗粒 | 独立动画灵动短打, 铅笔手绘磨砂声 | 叙事短片、匠人访谈、复古文创 |
| **06 · Collage (拼贴波普艺术)** | 混合图层 + 撕纸遮罩 | 复古报刊撕边、怪诞比例重组、胶带贴纸叠加 | 拼贴爵士 (Jazz Hop), 剪刀裁纸、胶带撕拉 | 时尚先锋、音乐节片头、独立文化杂志 |
| **07 · Liquid Motion (流体有机动态)** | WebGL SDF / Raymarching | 黏性液体融合、表面张力破裂、水滴凝结与弹跳 | Future Bass, 气泡破裂 (Bubble Pop), 水滴溅射 | 饮品广告、护肤品分子展示、能量补给 |
| **08 · Shape Morph (纯粹几何形变)** | SVG 贝塞尔顶点重映射 | 圆形无缝演进为星形、多边形、立方体，形意流转 | 律动电子 (Minimal Tech), 咔哒机械锁扣 | 概念设计、Logo 演绎演进、哲学观念传达 |
| **10 · 80s Synthwave (复古合成波)** | WebGL Shader + 霓虹发光 | 荧光粉紫激光网格、铬合金折射、CRT 扫描线扫描 | 80s 复古合成器 (Synthwave/Outrun), 电子鼓咚声 | 复古赛博、夜驰音乐节、电竞游戏活动 |
| **12 · Aurora Glass (极光流光玻璃)** | WebGL 物理折射 + 磨砂模糊 | 拟物磨砂毛玻璃（Glassmorphism）、色散虹彩 | 空灵环境音 (Ambient), 水晶磬声 (Glass Chime) | 现代高端 OS 界面、AI 算力引擎概念、未来视界 |
| **22 · Cyberpunk HUD / FUI (科幻界面)** | SVG + 纯代码坐标网格 | 战术雷达扫描、实时坐标测距、数据流跑马灯 | 暗黑电子 (Darksynth), 雷达蜂鸣、机械锁定 | 科幻电影 UI、军事工业、无人机地面站 |
| **30 · Thirty Seconds of a Tree (30s 矢量长视频)** | SVG + 四季调色矩阵 | 四季色轮流转、风霜雨雪、摄影机长运镜、生命闭环 | 四幕剧情式 Pop, 盛夏 Drop, 严冬静夜弦乐 | 长篇品牌叙事、ESG 环保主题、企业成长史 |
| **99 · Ink Wash (水墨山水)** | Canvas 多八度 Perlin 噪声 | 宣纸墨韵浸润、湿边缘（Wet Edge）、印章落款 | 古筝刮奏 (Guzheng Gliss), 萧笛悠扬, 钤印落声 | 中华传统文化、东方美学、国风游戏影视 |
