def get_quality_label(height: int, fps: int = 0) -> str:
    if height >= 2160: label = "4K (2160p)"
    elif height >= 1440: label = "QHD (1440p)"
    elif height >= 1080: label = "FHD (1080p)"
    elif height >= 720: label = "HD (720p)"
    elif height >= 480: label = "SD (480p)"
    elif height >= 360: label = "360p"
    else: label = f"{height}p"
    return f"{label} @ {int(fps)}fps" if fps > 0 else label


def format_time(seconds: float) -> str:
    if seconds <= 0: return "00:00"
    mins = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{mins:02d}:{secs:02d}"