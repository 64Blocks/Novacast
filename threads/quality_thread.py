from PyQt6.QtCore import QThread, pyqtSignal
from services.network_service import NetworkService
from services.parser_service import ParserService

class M3U8QualityThread(QThread):
    finished = pyqtSignal(list)

    def __init__(self, url: str):
        super().__init__()
        self.url = url

    def run(self):
        try:
            content = NetworkService.fetch_text(self.url)
            qualities = ParserService.parse_master_m3u8_from_text(content, self.url)
            self.finished.emit(qualities)
        except Exception as e:
            print(f"⚠️ Error parsing Master M3U8: {e}")
            self.finished.emit([])