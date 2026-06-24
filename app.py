import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.windows.main_window import MainWindow

class Application:
    def __init__(self):
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        self.app = QApplication(sys.argv)
        self.app.setStyle("Fusion")
        self.app.setFont(QFont("Segoe UI", 11))
        
        # Dependency Injection for the Main Window
        self.window = MainWindow()

    def run(self) -> int:
        self.window.show()
        return self.app.exec()