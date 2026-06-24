from PyQt6.QtCore import QThread, pyqtSignal
from services.network_service import NetworkService

class M3ULoaderThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, url: str):
        super().__init__()
        self.url = url
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        try:
            content = NetworkService.fetch_text(self.url)
            if not self._cancelled:
                self.finished.emit(content)
        except Exception as e:
            if not self._cancelled:
                self.error.emit(str(e))