class PlaylistRepository:
    def __init__(self):
        self._channels = []
        self._url_to_channel = {}

    def set_data(self, channels: list, url_to_channel: dict):
        self._channels = channels
        self._url_to_channel = url_to_channel

    def get_channels(self) -> list:
        return self._channels

    def get_channel_by_url(self, url: str):
        return self._url_to_channel.get(url)
    
    def clear(self):
        self._channels = []
        self._url_to_channel = {}