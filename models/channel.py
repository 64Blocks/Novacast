class Channel(dict):
    def __init__(self, name: str, logo: str = "", group: str = "Uncategorized", streams: list = None):
        streams = streams or []
        super().__init__(name=name, logo=logo, group=group, streams=streams)
        self.name = name
        self.logo = logo
        self.group = group
        self.streams = streams