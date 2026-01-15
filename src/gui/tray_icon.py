from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QFileDialog
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QCoreApplication, pyqtSignal
from src.gui.settings_window import SettingsWindow
from src.config.settings import settings
import os

class TrayIcon(QSystemTrayIcon):
    # 定义信号，方便通知 AppController 处理复杂逻辑
    show_settings_signal = pyqtSignal()
    restart_service_signal = pyqtSignal()
    settings_updated = pyqtSignal()  # 新增：设置已更新信号
    database_changed = pyqtSignal()  # 新增：翻译库已变更信号

    def __init__(self, parent=None):
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")
        ico_path = os.path.join(assets_dir, "icon.ico")
        png_path = os.path.join(assets_dir, "icon.png")
        
        if os.path.exists(ico_path) and os.path.getsize(ico_path) > 0:
            icon = QIcon(ico_path)
        elif os.path.exists(png_path) and os.path.getsize(png_path) > 0:
            icon = QIcon(png_path)
        else:
            icon = QIcon.fromTheme("applications-others")
            
        super().__init__(icon, parent)
        self.setToolTip("蓝王子翻译助手")
        self.init_menu()

    def init_menu(self):
        menu = QMenu()
        
        # 设置
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.show_settings)
        menu.addAction(settings_action)

        # 选择翻译库
        select_db_action = QAction("选择翻译库", self)
        select_db_action.triggered.connect(self.select_database)
        menu.addAction(select_db_action)

        menu.addSeparator()

        # 重启服务
        restart_action = QAction("重启服务", self)
        restart_action.triggered.connect(lambda: self.restart_service_signal.emit())
        menu.addAction(restart_action)

        # 退出
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(QCoreApplication.instance().quit)
        menu.addAction(exit_action)

        self.setContextMenu(menu)

    def show_settings(self):
        self.dialog = SettingsWindow()
        if self.dialog.exec():
            # 如果点击了保存
            print("[DEBUG] Settings saved.")
            self.settings_updated.emit()

    def select_database(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None, "选择翻译库 JSON 文件", "data", "JSON Files (*.json)"
        )
        if file_path:
            settings.set("translation_db_path", file_path)
            print(f"[DEBUG] Database changed to: {file_path}")
            # 触发 Translator 重新加载 DB
            self.database_changed.emit()

