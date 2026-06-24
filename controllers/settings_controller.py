import hashlib
from PyQt6.QtCore import QObject
from managers.mpv_manager import MPVManager
from utils.helpers import get_quality_label

class SettingsController(QObject):
    def __init__(self, mpv_manager: MPVManager):
        super().__init__()
        self.mpv = mpv_manager
        self._last_hash = None
        self._sub_auto_selected = False

    def reset_subtitle_state(self):
        self._sub_auto_selected = False

    def change_audio(self, combo):
        self.mpv.set_audio_track(str(combo.currentData() or "auto"))

    def change_sub(self, combo):
        data = combo.currentData()
        if data is not None: self.mpv.set_sub_track(str(data))

    def change_quality(self, combo, current_url_getter, play_url_callback):
        data = combo.currentData()
        if data is None: return
        if isinstance(data, str) and data.startswith("URL::"):
            new_url = data[5:]
            if new_url != current_url_getter():
                play_url_callback(new_url)
        elif data != "auto":
            self.mpv.set_video_track(str(data))
        else:
            self.mpv.set_video_track("auto")

    def process_track_list(self, track_list, audio_combo, sub_combo, quality_combo):
        if not track_list: return
        track_sig = tuple(sorted((t.get('id'), t.get('type'), t.get('lang'), t.get('title'), t.get('h'), t.get('fps')) for t in track_list))
        new_hash = hashlib.md5(str(track_sig).encode()).hexdigest()
        
        if new_hash == self._last_hash:
            if not self._sub_auto_selected: self._try_auto_sub(sub_combo)
            return
        
        self._last_hash = new_hash
        self._rebuild_combos(track_list, audio_combo, sub_combo, quality_combo)
        if not self._sub_auto_selected: self._try_auto_sub(sub_combo)

    def _rebuild_combos(self, track_list, audio_combo, sub_combo, quality_combo):
        for combo in [audio_combo, sub_combo, quality_combo]: combo.blockSignals(True)
        
        audio_combo.clear(); audio_combo.addItem("Auto")
        sub_combo.clear(); sub_combo.addItem("No Subtitle"); sub_combo.addItem("Auto Select")
        
        master_items = [(quality_combo.itemText(i), quality_combo.itemData(i)) for i in range(quality_combo.count()) if isinstance(quality_combo.itemData(i), str) and str(quality_combo.itemData(i)).startswith("URL::")]
        quality_combo.clear(); quality_combo.addItem("Auto")
        for text, data in master_items: quality_combo.addItem(text, data)

        video_tracks = []
        for track in track_list:
            try:
                t_type, t_id = track.get('type'), str(track.get('id', ''))
                title, lang = track.get('title', '') or '', track.get('lang', '') or ''
                name = " - ".join(p for p in (title, lang.upper()) if p) or f"Track {t_id}"
                if t_type == 'audio': audio_combo.addItem(f" {name} ", t_id)
                elif t_type == 'sub':
                    is_cc = any(x in title.lower() for x in ['cc', 'closed caption', '608', '708'])
                    sub_combo.addItem(f"{'📺' if is_cc else '📝'} {name} {'[CC]' if is_cc else ''} ", t_id)
                elif t_type == 'video':
                    h, fps = track.get('h', 0) or 0, track.get('fps', 0) or 0
                    if h >= 360: video_tracks.append({'id': t_id, 'label': get_quality_label(h, fps), 'height': h})
            except Exception: pass
        
        for t in sorted(video_tracks, key=lambda x: x['height'], reverse=True):
            quality_combo.addItem(f"🎬 {t['label']} ", t['id'])
            
        for combo in [audio_combo, sub_combo, quality_combo]: combo.blockSignals(False)

    def _try_auto_sub(self, sub_combo):
        self._sub_auto_selected = True
        tracks = self.mpv.get_track_list()
        
        for track in tracks:
            if track.get("type") == "sub":
                lang = (track.get("lang") or "").lower()
                title = (track.get("title") or "").lower()
                if lang in ["en", "eng"] and "cc" not in title and "608" not in title and "708" not in title:
                    self.mpv.set_sub_track(str(track["id"]))
                    self._update_combo_index(sub_combo, str(track["id"]))
                    return
                    
        for track in tracks:
            if track.get("type") == "sub":
                title = (track.get("title") or "").lower()
                if "cc" not in title and "608" not in title and "708" not in title:
                    self.mpv.set_sub_track(str(track["id"]))
                    self._update_combo_index(sub_combo, str(track["id"]))
                    return
                    
        for track in tracks:
            if track.get("type") == "sub":
                self.mpv.set_sub_track(str(track["id"]))
                self._update_combo_index(sub_combo, str(track["id"]))
                return

    def _update_combo_index(self, combo, track_id):
        for i in range(combo.count()):
            if combo.itemData(i) == track_id:
                combo.setCurrentIndex(i)
                break