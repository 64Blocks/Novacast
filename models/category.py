class Category(dict):
    def __init__(self, name: str, channels: list = None):
        channels = channels or []
        super().__init__(name=name, channels=channels)
        self.name = name
        self.channels = channels