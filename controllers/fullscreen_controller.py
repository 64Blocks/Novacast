from PyQt6.QtCore import QObject, pyqtSignal

class FullscreenController(QObject):
    fullscreen_state_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.is_fullscreen = False

    def toggle(self):
        self.is_fullscreen = not self.is_fullscreen
        self.fullscreen_state_changed.emit(self.is_fullscreen)