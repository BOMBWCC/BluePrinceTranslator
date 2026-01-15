# 实施计划 (Implementation Plan)

## 阶段 1: 基础架构与配置 (已完成)
- [x] 初始化项目结构
- [x] 定义 `requirements.txt`
- [x] 实现 `src/config/settings.py` 处理配置加载
- [x] 创建基础 `src/main.py` 入口

## 阶段 2: 服务层实现 (已完成)
- [x] **截图服务**: 实现 `screen_capture.py`，支持获取活动窗口坐标与 ROI 配置。
- [x] **OCR 服务**: 实现 `ocr_engine.py`，从 PaddleOCR 迁移至 RapidOCR。
- [x] **匹配服务**: 实现 `translator.py`，支持加载 JSON 库、模糊匹配及运行时重载。

## 阶段 3: GUI 开发 (已完成)
- [x] **托盘图标**: 实现 `tray_icon.py`，支持右键菜单。
- [x] **悬浮窗**: 实现 `overlay_window.py`，支持透明、置顶、拖拽及样式热更新。
- [x] **设置界面**: 实现 `settings_window.py`，支持可视化修改参数。

## 阶段 4: 核心逻辑集成 (已完成)
- [x] **快捷键管理**: 实现 `hotkey_manager.py`。
- [x] **中控集成**: `app_controller.py` 连接所有服务，实现 Screenshot -> OCR -> Translate -> Overlay 流程。
- [x] **信号联动**: 实现设置修改与数据库切换的即时生效。

## 阶段 5: 优化与抛光 (进行中)
- [ ] **多行合并优化**: 针对 OCR 识别出的多行文本，优化合并逻辑以提高匹配率。
- [ ] **穿透模式**: 增加 Click-through 功能。
- [ ] **用户引导**: 首次启动时的简易教程或提示。

## 阶段 6: 测试与发布
- [x] 本地功能验证 (截图、识别、翻译、设置均已跑通)。
- [ ] 编写详细使用说明 (README 已更新)。
- [ ] 打包发布 (如使用 PyInstaller)。