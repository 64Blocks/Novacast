import requests
from utils.headers import get_browser_headers
from config.constants import DEFAULT_TIMEOUT

class NetworkService:
    _session = None

    @classmethod
    def get_session(cls) -> requests.Session:
        if cls._session is None:
            cls._session = requests.Session()
            adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=20, max_retries=2)
            cls._session.mount('http://', adapter)
            cls._session.mount('https://', adapter)
        return cls._session

    @classmethod
    def fetch_text(cls, url: str, timeout: int = DEFAULT_TIMEOUT) -> str:
        session = cls.get_session()
        headers = get_browser_headers()
        resp = session.get(url, headers=headers, timeout=timeout, verify=False)
        resp.raise_for_status()
        return resp.text