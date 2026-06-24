from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from repositories.playlist_repository import PlaylistRepository

class SearchController(QObject):
    search_results = pyqtSignal(list, int)

    def __init__(self, repo: PlaylistRepository):
        super().__init__()
        self.repo = repo
        self._pending_text = ""
        self._base_channels = []
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(250)
        self._timer.timeout.connect(self._do_filter)

    def set_query(self, text: str, base_channels: list):
        self._pending_text = text
        self._base_channels = base_channels
        self._timer.start()

    def _do_filter(self):
        text = self._pending_text.lower().strip()
        if not text:
            self.search_results.emit(self._base_channels, 0)
            return

        filtered = []
        for ch in self._base_channels:
            if text in ch['name'].lower() or any(text in s['url'].lower() for s in ch.get('streams', [])):
                filtered.append(ch)
                if len(filtered) >= 2000: break
        self.search_results.emit(filtered, len(filtered))