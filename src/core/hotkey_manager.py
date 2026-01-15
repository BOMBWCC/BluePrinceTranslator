import keyboard
from src.config.settings import settings

class HotkeyManager:
    def __init__(self, controller):
        self.controller = controller
        self.translate_hk = settings.get("hotkey_translate", "alt+q")
        self.hide_hk = settings.get("hotkey_hide", "esc")

    def register_hotkeys(self):
        try:
            keyboard.add_hotkey(self.translate_hk, self.controller.on_translate_triggered)
            # keyboard.add_hotkey(self.hide_hk, self.controller.on_hide_triggered)
            print(f"Hotkeys registered: Translate={self.translate_hk}")
        except Exception as e:
            print(f"Error registering hotkeys: {e}")

    def unregister_all(self):
        keyboard.unhook_all()
