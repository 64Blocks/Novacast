from urllib.parse import urlparse


def is_master_m3u8_url(url: str) -> bool:
    parsed = urlparse(url)
    path = parsed.path.lower()
    return path.endswith('.m3u8') or path.endswith('.m3u')