from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from managers.mpv_manager import MPVManager
from repositories.playlist_repository import PlaylistRepository
from utils.helpers import format_time

class PlayerController(QObject):
    loading_state_changed = pyqtSignal(bool)
    status_update = pyqtSignal(dict)
    channel_name_requested = pyqtSignal(str)

    def __init__(self, mpv_manager: MPVManager, repo: PlaylistRepository):
        super().__init__()
        self.mpv = mpv_manager
        self.repo = repo
        self.current_url = ""
        self.current_channel_index = -1
        self.is_playing_attempt = False
        self.stream_status = "Ready"
        
        self._current_time = 0.0
        self._total_duration = 0.0
        self._buffering_state = 0
        self._cache_used = 0
        self._last_progress_value = -1
        
        self._pending_time_pos = None
        self._pending_duration = None
        self._pending_buffering = None
        self._pending_cache_used = None
        self._pending_status_text = ""

        self._throttle_timer = QTimer(self)
        self._throttle_timer.setInterval(250)
        self._throttle_timer.timeout.connect(self._flush_updates)
        self._throttle_timer.start()

        self.mpv.time_pos_changed.connect(self._on_time_pos)
        self.mpv.duration_changed.connect(self._on_duration)
        self.mpv.buffering_changed.connect(self._on_buffering)
        self.mpv.cache_used_changed.connect(self._on_cache)
        self.mpv.idle_active_changed.connect(self._on_idle)

    def play_channel(self, url: str):
        self.current_url = url
        self._reset_playback_state()
        self.loading_state_changed.emit(True)
        self.is_playing_attempt = True
        self.stream_status = "Loading"
        self._emit_status()
        
        try:
            self.mpv.play(url)
            channel = self.repo.get_channel_by_url(url)
            name = channel['name'] if channel else "Unknown Channel"
            self.channel_name_requested.emit(name)
        except Exception as e:
            self.loading_state_changed.emit(False)
            print(f"Playback error: {e}")

    def _reset_playback_state(self):
        self._current_time = 0.0
        self._total_duration = 0.0
        self._buffering_state = 0
        self._cache_used = 0
        self._last_progress_value = -1

    def toggle_play_pause(self):
        self.mpv.set_pause(not self.mpv.is_paused())

    def play_next(self):
        channels = self.repo.get_channels()
        if not channels: return
        self.current_channel_index = 0 if self.current_channel_index == -1 else min(self.current_channel_index + 1, len(channels) - 1)
        streams = channels[self.current_channel_index].get("streams", [])
        if streams: self.play_channel(streams[0]["url"])

    def play_prev(self):
        channels = self.repo.get_channels()
        if channels and self.current_channel_index > 0:
            self.current_channel_index -= 1
            streams = channels[self.current_channel_index].get("streams", [])
            if streams: self.play_channel(streams[0]["url"])

    def seek(self, value: int):
        if self._total_duration > 0:
            self.mpv.seek((value / 100.0) * self._total_duration)

    def set_volume(self, value: int):
        self.mpv.set_volume(value)

    def _on_time_pos(self, value):
        if value is not None:
            self._pending_time_pos = value
            if value > 0.5 and self.is_playing_attempt:
                self.loading_state_changed.emit(False)
                self.is_playing_attempt = False
                self.stream_status = "Playing"

    def _on_duration(self, value):
        if value is not None: self._pending_duration = value

    def _on_buffering(self, value):
        if value is not None: self._pending_buffering = value

    def _on_cache(self, value):
        if value is not None: self._pending_cache_used = value

    def _on_idle(self, value):
        if value and self.is_playing_attempt:
            self.loading_state_changed.emit(False)
            self.is_playing_attempt = False
            self.stream_status = "Error"
            self._emit_status()

    def _flush_updates(self):
        updated = False
        if self._pending_time_pos is not None:
            self._current_time = self._pending_time_pos
            self._pending_time_pos = None
            updated = True
        if self._pending_duration is not None:
            self._total_duration = self._pending_duration
            self._pending_duration = None
            updated = True
        if self._pending_buffering is not None:
            self._buffering_state = self._pending_buffering
            self._pending_buffering = None
            updated = True
        if self._pending_cache_used is not None:
            self._cache_used = self._pending_cache_used
            self._pending_cache_used = None
            updated = True
        if updated: self._emit_status()

    def _emit_status(self):
        time_str = f"{format_time(self._current_time)} / {format_time(self._total_duration)}" if self._total_duration > 0 else format_time(self._current_time)
        cache_mb = self._cache_used / (1024 * 1024) if self._cache_used else 0
        new_text = f"{self.stream_status} | Played: {time_str} | Buffered: {self._buffering_state}% | Cache: {cache_mb:.1f} MB"
        
        progress_val = int((self._current_time / self._total_duration) * 100) if self._total_duration > 0 else 0
        if progress_val == self._last_progress_value: progress_val = -1
        else: self._last_progress_value = progress_val

        if new_text != self._pending_status_text:
            self._pending_status_text = new_text
            self.status_update.emit({
                "text": new_text, "progress": progress_val,
                "time_label": format_time(self._current_time),
                "duration_label": format_time(self._total_duration)
            })