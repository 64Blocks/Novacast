class Stream(dict):
    def __init__(self, url: str, status: str = "UNKNOWN", last_check=None, latency=None, quality=None):
        super().__init__(url=url, status=status, last_check=last_check, latency=latency, quality=quality)
        self.url = url
        self.status = status
        self.last_check = last_check
        self.latency = latency
        self.quality = quality