import requests

from utils.headers import get_browser_headers

from config.constants import DEFAULT_TIMEOUT


_http_session = None


def get_http_session() -> requests.Session:
    global _http_session
    if _http_session is None:
        _http_session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=20, max_retries=2)
        _http_session.mount('http://', adapter)
        _http_session.mount('https://', adapter)
    return _http_session


def fetch_url_text(url: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    session = get_http_session()
    headers = get_browser_headers()
    resp = session.get(url, headers=headers, timeout=timeout, verify=False)
    resp.raise_for_status()
    return resp.text