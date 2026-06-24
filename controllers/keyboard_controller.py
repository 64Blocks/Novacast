from PyQt6.QtCore import QObject, Qt
from config.constants import DEFAULT_VOLUME

class KeyboardController(QObject):
    def __init__(self, player_ctrl, playlist_ctrl, settings_ctrl, fullscreen_ctrl, volume_slider):
        super().__init__()
        self.player = player_ctrl
        self.playlist = playlist_ctrl
        self.settings = settings_ctrl
        self.fullscreen = fullscreen_ctrl
        self.volume_slider = volume_slider
        self._prev_volume = DEFAULT_VOLUME

    def handle_key(self, event):
        key = event.key()
        if key == Qt.Key.Key_Escape and self.fullscreen.is_fullscreen:
            self.fullscreen.toggle()
        elif key == Qt.Key.Key_F:
            self.fullscreen.toggle()
        elif key == Qt.Key.Key_Space:
            self.player.toggle_play_pause()
        elif key == Qt.Key.Key_Right:
            self.player.play_next()
        elif key == Qt.Key.Key_Left:
            self.player.play_prev()
        elif key == Qt.Key.Key_Up:
            self.volume_slider.setValue(min(100, self.volume_slider.value() + 5))
        elif key == Qt.Key.Key_Down:
            self.volume_slider.setValue(max(0, self.volume_slider.value() - 5))
        elif key == Qt.Key.Key_M:
            self._toggle_mute()
        else:
            return False
        return True

    def _toggle_mute(self):
        if self.volume_slider.value() > 0:
            self._prev_volume = self.volume_slider.value()
            self.volume_slider.setValue(0)
        else:
            self.volume_slider.setValue(self._prev_volume)