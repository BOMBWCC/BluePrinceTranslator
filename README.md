# Blue Prince Translator (蓝王子翻译助手)

一个基于 Python 的轻量级游戏翻译辅助工具。专为“蓝王子”类游戏设计，通过 OCR 识别游戏画面文本，并**离线匹配**预存的翻译库，以半透明悬浮窗形式显示剧情翻译。

## 📖 Vibe Coding 架构

本项目严格遵循 **Vibe Coding** 开发范式：
1.  **Memory Bank**: 所有核心决策、架构设计和进度追踪均维护在 `memory-bank/` 目录下。
2.  **规划驱动**: AI 编写代码前必须先阅读 `product-requirements.md` 和 `architecture.md`。
3.  **模块化**: 严禁生成单体巨石代码，遵循职责分离原则。

## ✨ 核心功能

*   **系统托盘驻留**: 低内存占用，后台静默运行。
*   **一键翻译**: 全局快捷键触发（默认 Alt+Q），自动截取活动窗口并识别。
*   **智能截图**: 自动识别活动窗口，支持配置 ROI (感兴趣区域) 以专注于字幕区域。
*   **离线模糊匹配**: 针对 OCR 误差优化，通过模糊算法检索本地 JSON 翻译库，无需联网。
*   **现代化 UI**:
    *   半透明、无边框悬浮窗，支持拖拽移动。
    *   **设置界面**: 可视化调整字体大小、透明度、匹配阈值等。
    *   **热切换**: 支持运行时切换不同的翻译库文件。
*   **轻量级 OCR**: 使用 **RapidOCR (ONNX Runtime)**，启动快、体积小、精度高。

## 🛠 技术栈 (Tech Stack)

*   **语言**: Python 3.10+
*   **GUI 框架**: PyQt6 (用于实现透明置顶窗口、托盘图标及设置界面)
*   **输入监听**: keyboard (全局快捷键)
*   **OCR 引擎**: **RapidOCR (ONNX Runtime)** (替代了笨重的 PaddleOCR)
*   **数据匹配**: TheFuzz (字符串模糊匹配)
*   **截图**: mss + pygetwindow

## 📂 目录结构

```text
BluePrinceTranslator/
├── .venv/                   # 虚拟环境
├── memory-bank/             # [AI 大脑] 项目上下文与记忆库
├── src/                     # 源代码
│   ├── main.py              # 入口
│   ├── gui/                 # 界面逻辑 (Overlay, Tray, Settings)
│   ├── services/            # 业务逻辑 (OCR, Capture, Matcher)
│   └── config/              # 配置处理
├── data/                    # 翻译数据库
└── requirements.txt
```

## 🚀 快速开始

### 1. 环境准备
确保已安装 Python 3.10+ (推荐 3.10-3.12)。
```bash
# 创建虚拟环境
python -m venv .venv

# 激活环境 (Windows)
.venv\Scripts\activate

# 安装依赖 (推荐使用国内镜像以加速下载)
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### 2. 准备翻译库
在 `data/` 目录下放置 `translation_db.json`，格式如下：
```json
{
  "Hello World": "你好世界",
  "Game Start": "游戏开始"
}
```

### 3. 运行
```bash
python src/main.py
```
*   **Alt+Q**: 截屏并翻译
*   **Esc**: 隐藏悬浮窗
*   **托盘右键**: 打开设置、切换翻译库或退出

## 🤝 开发指南
如果你是辅助开发的 AI Agent，请严格遵守以下流程：
1. 启动前：阅读 `memory-bank/` 下的所有文件。
2. 编码时：先更新 `memory-bank/progress.md`，保持模块化。
3. OCR 引擎：目前已切换为 RapidOCR，请勿引入 paddlepaddle 依赖。

## 📜 许可证
MIT License