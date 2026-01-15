from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizeGrip
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QColor, QFont, QPalette
from src.config.settings import settings

class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.old_pos = None

    def init_ui(self):
        # Window properties
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Layout
        self.layout = QVBoxLayout()
        self.label = QLabel("等待识别...")
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Font and Style
        font_size = settings.get("font_size", 18)
        self.label.setFont(QFont("Microsoft YaHei", font_size))
        self.label.setStyleSheet(f"color: white; background-color: rgba(0, 0, 0, {int(settings.get('background_opacity', 0.7) * 255)}); border-radius: 10px; padding: 10px;")
        
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # Initial size and position
        pos = settings.get("window_pos", [100, 100])
        size = settings.get("window_size", [400, 200])
        self.move(pos[0], pos[1])
        self.resize(size[0], size[1])

        # Size grip for resizing
        self.sizegrip = QSizeGrip(self)
        self.sizegrip.setFixedSize(20, 20)
        self.update_sizegrip_pos()

    def update_sizegrip_pos(self):
        self.sizegrip.move(self.width() - 20, self.height() - 20)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_sizegrip_pos()
        settings.set("window_size", [self.width(), self.height()])

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()
            settings.set("window_pos", [self.x(), self.y()])

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    def set_text(self, text):
        if text:
            self.label.setText(text)
        else:
            self.label.setText("未找到匹配翻译")
        self.show()

    def show_loading(self):
        self.label.setText("正在识别中...")
        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.hide()

    def reload_styles(self):
        """Reload font size and background opacity from settings"""
        font_size = settings.get("font_size", 18)
        self.label.setFont(QFont("Microsoft YaHei", font_size))
        
        opacity = settings.get("background_opacity", 0.7)
        self.label.setStyleSheet(f"color: white; background-color: rgba(0, 0, 0, {int(opacity * 255)}); border-radius: 10px; padding: 10px;")
        
        # Adjust window size if font changed significantly? 
        # For now, let user resize manually or keep existing size.
        self.label.adjustSize()
        print(f"[DEBUG] Overlay styles reloaded: Font={font_size}, Opacity={opacity}")
