from PyQt6.QtCore import QObject, pyqtSignal
from src.gui.overlay_window import OverlayWindow
from src.gui.tray_icon import TrayIcon
from src.core.hotkey_manager import HotkeyManager
from src.services.screen_capture import capture_service
from src.services.ocr_engine import get_ocr_engine
from src.services.translator import translator_service
import threading

class AppController(QObject):
    # Signals for thread-safe UI updates
    translation_done = pyqtSignal(str)
    request_loading = pyqtSignal()

    def __init__(self, app):
        super().__init__()
        self.app = app
        
        # Initialize UI
        self.overlay = OverlayWindow()
        self.tray = TrayIcon()
        self.tray.show()
        
        # Connect signals
        self.translation_done.connect(self.overlay.set_text)
        self.request_loading.connect(self.overlay.show_loading)
        self.tray.settings_updated.connect(self.overlay.reload_styles)
        self.tray.database_changed.connect(translator_service.reload_db)
        
        # Initialize Hotkeys
        self.hotkey_manager = HotkeyManager(self)
        self.hotkey_manager.register_hotkeys()
        
        # OCR Engine (initialized lazily)
        self.ocr_engine = None

    def on_translate_triggered(self):
        """Called when Alt+Q is pressed"""
        print("Translate triggered...")
        self.request_loading.emit()
        
        # Run OCR and Translation in a background thread
        thread = threading.Thread(target=self._process_translation)
        thread.daemon = True
        thread.start()

    def _process_translation(self):
        try:
            # 1. Capture
            image = capture_service.capture_active_window()
            if not image:
                self.translation_done.emit("无法截取窗口")
                return

            # 2. OCR
            if self.ocr_engine is None:
                self.ocr_engine = get_ocr_engine()
            
            text = self.ocr_engine.recognize(image)
            print(f"OCR Result: {text}")
            
            if not text:
                self.translation_done.emit("未识别到文字")
                return

            # 3. Translate/Match
            result = translator_service.translate(text)
            
            # 4. Show Result
            self.translation_done.emit(result)
            
        except Exception as e:
            print(f"Error in translation process: {e}")
            self.translation_done.emit(f"错误: {str(e)}")

    def on_hide_triggered(self):
        self.overlay.hide()

    def quit(self):
        self.hotkey_manager.unregister_all()
        self.app.quit()
        
def start_app(app):
    controller = AppController(app)
    return controller
