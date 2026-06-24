from PyQt6.QtCore import QObject, pyqtSignal
from services.playlist_service import PlaylistService
from repositories.playlist_repository import PlaylistRepository
from managers.thread_manager import ThreadManager

class PlaylistController(QObject):
    playlist_loaded = pyqtSignal(int)
    categories_updated = pyqtSignal(list)
    channels_updated = pyqtSignal(list, bool, int)
    loading_state_changed = pyqtSignal(bool)
    error_occurred = pyqtSignal(str)

    def __init__(self, service: PlaylistService, repo: PlaylistRepository, thread_mgr: ThreadManager):
        super().__init__()
        self.service = service
        self.repo = repo
        self.thread_mgr = thread_mgr
        self.current_category_name = None
        self.current_category_channels = []
        self._pending_url = ""

    def load_file(self, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self._process_content(f.read())
        except Exception as e:
            self.error_occurred.emit(f"Failed to read file:\n{e}")

    def load_url(self, url: str):
        self._pending_url = url
        if url.lower().endswith(('.mp4', '.mkv', '.avi', '.ts', '.mp3', '.m3u8')) or ('m3u8' in url):
            self.playlist_loaded.emit(-1)
            return
        self.loading_state_changed.emit(True)
        self.thread_mgr.start_loader(url, self._on_url_loaded, self._on_url_error)

    def get_pending_url(self) -> str:
        return self._pending_url

    def _on_url_loaded(self, content: str):
        if '#EXT-X-VERSION' in content or '#EXT-X-TARGETDURATION' in content or not content.strip().startswith('#EXTM3U'):
            self.loading_state_changed.emit(False)
            self.playlist_loaded.emit(-1)
            return
        self._process_content(content)

    def _on_url_error(self, error_msg: str):
        self.loading_state_changed.emit(False)
        self.error_occurred.emit(f"Failed to fetch URL:\n{error_msg}")

    def _process_content(self, content: str):
        self.loading_state_changed.emit(True)
        result = self.service.process_content(content)
        if result == "SINGLE_STREAM":
            self.loading_state_changed.emit(False)
            self.playlist_loaded.emit(-1)
            return
        if result == "NO_CHANNELS":
            self.loading_state_changed.emit(False)
            self.error_occurred.emit("No channels found in this file.")
            return
        
        channels = self.repo.get_channels()
        channels.sort(key=lambda x: x.get('name', 'Unknown').lower())
        self.repo.set_data(channels, self.repo._url_to_channel)
        self.loading_state_changed.emit(False)
        self.playlist_loaded.emit(len(channels))
        self._populate_categories()

    def _populate_categories(self):
        channels = self.repo.get_channels()
        categories = {}
        for ch in channels:
            categories.setdefault(ch["group"], []).append(ch)
        
        cat_list = []
        for group_name in sorted(categories.keys()):
            cat_list.append({"name": group_name, "channels": categories[group_name]})
        self.categories_updated.emit(cat_list)

    def select_category(self, category_name: str, channels: list):
        self.current_category_name = category_name
        self.current_category_channels = channels
        self.populate_channel_list(channels)

    def populate_channel_list(self, channels: list, is_search: bool = False, match_count: int = 0):
        self.channels_updated.emit(channels, is_search, match_count)