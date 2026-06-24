import mpv
from PyQt6.QtCore import QObject, pyqtSignal
from utils.headers import get_random_user_agent
from config.constants import DEFAULT_VOLUME

class MPVManager(QObject):
    time_pos_changed = pyqtSignal(float)
    duration_changed = pyqtSignal(float)
    buffering_changed = pyqtSignal(int)
    cache_used_changed = pyqtSignal(int)
    idle_active_changed = pyqtSignal(bool)
    track_list_changed = pyqtSignal(list)
    volume_changed = pyqtSignal(int)
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.player = None

    def initialize(self, window_id: int):
        try:
            self.player = mpv.MPV(
                wid=window_id, loglevel="warn", force_window="immediate", idle="yes", keep_open="yes",
                title="IPTV Modern Player", input_default_bindings=True, input_vo_keyboard=True,
                vo="gpu", gpu_api="d3d11", hwdec="auto", profile="fast", video_sync="audio",
                framedrop="vo", network_timeout="5", cache="yes", cache_secs="2",
                demuxer_readahead_secs="1", demuxer_max_bytes="16MiB", force_seekable="no",
                ao="wasapi", audio_buffer="0.1",
                demuxer_lavf_o="fflags=+discardcorrupt+genpts+igndts",
                stream_lavf_o="reconnect=1,reconnect_on_network_error=1,reconnect_delay_max=2",
                user_agent=get_random_user_agent(), sub_visibility=True, sub_delay=0,
                volume=DEFAULT_VOLUME, hr_seek="absolute", hr_seek_framedrop="no"
            )
            self._setup_observers()
        except Exception as e:
            self.error_occurred.emit(str(e))

    def _setup_observers(self):
        p = self.player
        p.observe_property('time-pos', lambda _, v: self.time_pos_changed.emit(v) if v is not None else None)
        p.observe_property('duration', lambda _, v: self.duration_changed.emit(v) if v is not None else None)
        p.observe_property('cache-buffering-state', lambda _, v: self.buffering_changed.emit(v) if v is not None else None)
        p.observe_property('cache-used', lambda _, v: self.cache_used_changed.emit(v) if v is not None else None)
        p.observe_property('idle-active', lambda _, v: self.idle_active_changed.emit(v) if v is not None else None)
        p.observe_property('track-list', lambda _, v: self.track_list_changed.emit(v) if v else None)
        p.observe_property('volume', lambda _, v: self.volume_changed.emit(int(v)) if v is not None else None)

    def play(self, url: str):
        if self.player: self.player.play(url)

    def set_pause(self, pause: bool):
        if self.player: self.player.pause = pause

    def is_paused(self) -> bool:
        return self.player.pause if self.player else True

    def seek(self, position: float):
        if self.player: self.player.seek(position)

    def set_volume(self, value: int):
        if self.player: self.player.volume = value

    def set_audio_track(self, track_id: str):
        if self.player: self.player.audio = track_id

    def set_sub_track(self, track_id: str):
        if self.player:
            self.player.sub = track_id
            self.player.sub_visibility = (track_id != "no")

    def set_video_track(self, track_id: str):
        if self.player: self.player.video = track_id

    def get_track_list(self) -> list:
        return self.player.track_list or [] if self.player else []

    def terminate(self):
        if self.player:
            try: self.player.terminate()
            except: pass