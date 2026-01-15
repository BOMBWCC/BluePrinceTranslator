from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QSpinBox, QDoubleSpinBox, QLineEdit, QFormLayout)
from PyQt6.QtCore import Qt
from src.config.settings import settings

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置 - 蓝王子翻译助手")
        self.setMinimumWidth(300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        # 字体大小
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(10, 72)
        self.font_size_spin.setValue(settings.get("font_size", 18))
        form.addRow("字体大小:", self.font_size_spin)

        # 背景透明度
        self.opacity_spin = QDoubleSpinBox()
        self.opacity_spin.setRange(0.1, 1.0)
        self.opacity_spin.setSingleStep(0.1)
        self.opacity_spin.setValue(settings.get("background_opacity", 0.7))
        form.addRow("窗口透明度:", self.opacity_spin)

        # 匹配阈值
        self.threshold_spin = QSpinBox()
        self.threshold_spin.setRange(0, 100)
        self.threshold_spin.setValue(settings.get("matching_threshold", 85))
        form.addRow("匹配相似度 (%):", self.threshold_spin)

        # 快捷键 (只读显示或简单编辑)
        self.hotkey_input = QLineEdit(settings.get("hotkey_translate", "alt+q"))
        form.addRow("翻译快捷键:", self.hotkey_input)

        layout.addLayout(form)

        # 按钮
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("保存")
        save_btn.clicked.connect(self.save_settings)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def save_settings(self):
        settings.set("font_size", self.font_size_spin.value())
        settings.set("background_opacity", self.opacity_spin.value())
        settings.set("matching_threshold", self.threshold_spin.value())
        settings.set("hotkey_translate", self.hotkey_input.text().lower())
        
        self.accept()
        # 提示：实际应用中这里可能需要发送信号通知 OverlayWindow 立即更新样式
