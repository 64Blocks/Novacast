from services.parser_service import ParserService
from repositories.playlist_repository import PlaylistRepository

class PlaylistService:
    def __init__(self, repo: PlaylistRepository):
        self.repo = repo
        self.parser = ParserService()

    def process_content(self, content: str) -> str:
        if '#EXT-X-VERSION' in content or '#EXT-X-TARGETDURATION' in content or not content.strip().startswith('#EXTM3U'):
            return "SINGLE_STREAM"
        
        channels, url_map = self.parser.parse_m3u(content)
        if not channels:
            return "NO_CHANNELS"
            
        self.repo.set_data(channels, url_map)
        return "SUCCESS"