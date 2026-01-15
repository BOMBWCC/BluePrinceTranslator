import pygetwindow as gw
import mss
import numpy as np
from PIL import Image

class ScreenCapture:
    def __init__(self):
        # mss is not thread-safe if shared across threads on Windows.
        # We will instantiate it per capture.
        pass

    def get_active_window_rect(self):
        """获取当前活动窗口的坐标和大小"""
        try:
            window = gw.getActiveWindow()
            if window:
                print(f"[DEBUG] Active Window detected: '{window.title}' | Rect: {window.left}, {window.top}, {window.width}x{window.height}")
                return {
                    "top": window.top,
                    "left": window.left,
                    "width": window.width,
                    "height": window.height,
                    "title": window.title
                }
            else:
                print("[DEBUG] No active window detected (gw.getActiveWindow() returned None).")
        except Exception as e:
            print(f"[DEBUG] Error getting active window: {e}")
        return None

    def capture_active_window(self):
        """截取当前活动窗口 (支持 ROI 区域)"""
        rect = self.get_active_window_rect()
        if not rect:
            print("[DEBUG] Capture failed because rect is None.")
            return None

        # Load ROI settings
        from src.config.settings import settings
        roi = settings.get("capture_roi", None)

        monitor = {}
        if roi:
            # Calculate absolute coordinates based on percentages
            win_w = rect["width"]
            win_h = rect["height"]
            
            top_offset = int(win_h * roi.get("top_percent", 0.0))
            left_offset = int(win_w * roi.get("left_percent", 0.0))
            
            # ROI width/height
            bottom_limit = int(win_h * roi.get("bottom_percent", 1.0))
            right_limit = int(win_w * roi.get("right_percent", 1.0))
            
            cap_width = right_limit - left_offset
            cap_height = bottom_limit - top_offset
            
            monitor = {
                "top": rect["top"] + top_offset,
                "left": rect["left"] + left_offset,
                "width": cap_width,
                "height": cap_height
            }
            print(f"[DEBUG] ROI Capture: top={monitor['top']}, left={monitor['left']}, w={cap_width}, h={cap_height}")
        else:
            monitor = {
                "top": rect["top"],
                "left": rect["left"],
                "width": rect["width"],
                "height": rect["height"]
            }
            print(f"[DEBUG] Full Window Capture")
        
        try:
            # Fix: Create mss instance locally for thread safety
            with mss.mss() as sct:
                screenshot = sct.grab(monitor)
                print(f"[DEBUG] Screenshot taken successfully. Size: {screenshot.size}")
                img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                return img
        except Exception as e:
            print(f"[DEBUG] Error capturing screen with mss: {e}")
            return None

    def capture_region(self, top, left, width, height):
        """截取指定区域"""
        monitor = {"top": top, "left": left, "width": width, "height": height}
        try:
            with mss.mss() as sct:
                screenshot = sct.grab(monitor)
                img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                return img
        except Exception as e:
            print(f"Error capturing region: {e}")
            return None

capture_service = ScreenCapture()
