import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from src.core.app_controller import AppController

def main():
    # Set high DPI scaling if needed (optional for PyQt6)
    # QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    
    # Ensure the app doesn't quit when the last window is closed (since we have a tray icon)
    app.setQuitOnLastWindowClosed(False)
    
    # Initialize the controller
    controller = AppController(app)
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
