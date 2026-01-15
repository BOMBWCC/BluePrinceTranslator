# 技术栈 (Tech Stack)

## 核心语言
- **Python 3.10+**: 项目的基础编程语言。
  - *注意：由于 ONNX Runtime 兼容性原因，建议使用 Python 3.10 至 3.12 版本，暂不推荐 Python 3.14。*

## GUI 框架
- **PyQt6**: 用于构建主要的 GUI 组件，包括系统托盘图标、半透明悬浮翻译窗口以及设置对话框。
  - 选择理由：支持成熟的透明置顶窗口、托盘管理和富文本渲染。

## OCR 引擎
- **RapidOCR (ONNX Runtime)**: 用于高精度的屏幕文本识别。
  - **变更记录**: 原计划使用 PaddleOCR，但因其体积过大且安装复杂，已切换为 RapidOCR。
  - 优势：轻量级、启动快、无需安装庞大的深度学习框架，且兼容 PaddleOCR 模型。

## 输入与快捷键
- **keyboard**: 用于全局快捷键监听 (如 Alt+Q 触发翻译)。

## 图像处理与截图
- **mss**: 超快速的屏幕截图库（已解决多线程安全问题）。
- **pygetwindow**: 获取当前活动窗口的位置和句柄。
- **Pillow (PIL)**: 用于截图后的图像预处理及调试。

## 数据处理与匹配
- **TheFuzz (fuzz)**: 用于 OCR 文本与翻译库之间的模糊匹配。
- **python-Levenshtein**: 加速模糊匹配算法。

## 配置管理
- **JSON**: 用于存储 `config.json` 和翻译数据库 `translation_db.json`。

## 依赖列表
```text
PyQt6
keyboard
rapidocr_onnxruntime
thefuzz
python-Levenshtein
mss
pygetwindow
Pillow
```