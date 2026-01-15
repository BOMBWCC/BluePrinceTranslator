# 系统架构 (Architecture)

## 模块设计

项目遵循职责分离原则，分为以下核心层级：

### 1. 入口层 (Entry Point)
- `src/main.py`: 程序的启动入口，初始化 `AppController` 并启动事件循环。

### 2. 控制层 (Core Logic)
- `src/core/app_controller.py`: 核心中控，协调 GUI、快捷键、OCR 和翻译服务。
- `src/core/hotkey_manager.py`: 封装全局快捷键的注册与监听逻辑。

### 3. UI 层 (Presentation)
- `src/gui/tray_icon.py`: 系统托盘逻辑，管理右键菜单和后台运行状态。
- `src/gui/overlay_window.py`: 核心 UI 窗口，实现半透明、置顶、可拖拽的翻译结果显示。

### 4. 服务层 (Services)
- `src/services/screen_capture.py`: 负责获取活动窗口坐标并进行局部/全屏截图。
- `src/services/ocr_engine.py`: 封装 OCR 逻辑，将图像转换为文本。
- `src/services/translator.py`: 负责本地 JSON 数据库的检索与模糊匹配逻辑。

### 5. 工具与配置 (Utils & Config)
- `src/config/settings.py`: 处理 `config.json` 的读写与默认值。
- `src/utils/helpers.py`: 提供通用的辅助函数（如日志、路径处理）。

## 工作流 (Workflow)

1. **启动**: `main.py` 启动 -> 初始化配置 -> 注册托盘 -> 注册全局快捷键 (Alt+Q)。
2. **触发**: 用户按下 Alt+Q。
3. **截图**: `screen_capture` 获取当前活动窗口区域并截图。
4. **识别**: `ocr_engine` 对截图进行 OCR 处理，提取文字。
5. **匹配**: `translator` 使用 `TheFuzz` 将文字与本地 `translation_db.json` 进行模糊匹配。
6. **显示**: `overlay_window` 更新内容并以半透明置顶形式显示。
7. **隐藏**: 用户按下 Esc/Alt+W 或点击关闭 -> 隐藏 `overlay_window`。

## 数据流 (Data Flow)
`Screen (Pixels) -> OCR (Text) -> Fuzzy Match (Matched Text) -> Overlay (HTML/Rich Text)`
