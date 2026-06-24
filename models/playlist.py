class Playlist(dict):
    def __init__(self, channels: list = None, url_to_channel: dict = None):
        channels = channels or []
        url_to_channel = url_to_channel or {}
        super().__init__(channels=channels, url_to_channel=url_to_channel)
        self.channels = channels
        self.url_to_channel = url_to_channel