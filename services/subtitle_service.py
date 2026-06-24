class SubtitleService:
    @staticmethod
    def auto_select(player, sub_combo) -> bool:
        if player is None: return False
        tracks = player.track_list or []
        
        for track in tracks:
            if track.get("type") == "sub":
                lang = (track.get("lang") or "").lower()
                title = (track.get("title") or "").lower()
                if lang in ["en", "eng"] and "cc" not in title and "608" not in title and "708" not in title:
                    player.sub = str(track["id"])
                    player.sub_visibility = True
                    for i in range(sub_combo.count()):
                        if sub_combo.itemData(i) == str(track["id"]):
                            sub_combo.setCurrentIndex(i)
                            break
                    return True
                    
        for track in tracks:
            if track.get("type") == "sub":
                title = (track.get("title") or "").lower()
                if "cc" not in title and "608" not in title and "708" not in title:
                    player.sub = str(track["id"])
                    player.sub_visibility = True
                    for i in range(sub_combo.count()):
                        if sub_combo.itemData(i) == str(track["id"]):
                            sub_combo.setCurrentIndex(i)
                            break
                    return True
                    
        for track in tracks:
            if track.get("type") == "sub":
                player.sub = str(track["id"])
                player.sub_visibility = True
                for i in range(sub_combo.count()):
                    if sub_combo.itemData(i) == str(track["id"]):
                        sub_combo.setCurrentIndex(i)
                        break
                return True
        return False