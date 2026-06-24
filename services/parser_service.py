from utils.regex import RE_EXTINF_NAME, RE_EXTINF_LOGO, RE_EXTINF_GROUP, RE_STREAM_RES
from utils.helpers import get_quality_label
from urllib.parse import urljoin
from models.channel import Channel
from models.stream import Stream

class ParserService:
    @staticmethod
    def parse_m3u(content: str) -> tuple:
        channels_dict = {}
        current_channel_info = None
        for line in content.splitlines():
            line = line.strip()
            if not line: continue
            if line.startswith('#EXTINF:'):
                name_match = RE_EXTINF_NAME.search(line)
                logo_match = RE_EXTINF_LOGO.search(line)
                group_match = RE_EXTINF_GROUP.search(line)
                name = name_match.group(1).strip() if name_match else line.split(',')[-1].strip()
                name = name if name else "Unnamed Channel"
                logo = logo_match.group(1).strip() if logo_match else ""
                group = group_match.group(1).strip() if group_match else "Uncategorized"
                current_channel_info = {'name': name, 'logo': logo, 'group': group}
            elif not line.startswith('#'):
                if current_channel_info:
                    name = current_channel_info['name']
                    key = name
                    if key not in channels_dict:
                        channels_dict[key] = Channel(name=name, logo=current_channel_info['logo'], group=current_channel_info['group'], streams=[])
                    stream_entry = Stream(url=line)
                    channels_dict[key]["streams"].append(stream_entry)
                    current_channel_info = None
                else:
                    key = f"Unknown_{len(channels_dict)}"
                    channels_dict[key] = Channel(name=f"Channel {len(channels_dict) + 1}", logo="", group="Other", streams=[Stream(url=line)])
        channels_list = list(channels_dict.values())
        url_to_channel = {}
        for ch in channels_list:
            for stream in ch.get("streams", []):
                url_to_channel[stream["url"]] = ch
        return channels_list, url_to_channel

    @staticmethod
    def parse_master_m3u8_from_text(content: str, base_url: str) -> list:
        qualities = []
        if '#EXT-X-STREAM-INF' not in content: return qualities
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if line.startswith('#EXT-X-STREAM-INF'):
                res_match = RE_STREAM_RES.search(line)
                if res_match:
                    height = int(res_match.group(1))
                    label = get_quality_label(height)
                    if i + 1 < len(lines):
                        stream_url = lines[i + 1].strip()
                        if not stream_url.startswith('http'): stream_url = urljoin(base_url, stream_url)
                        qualities.append({'label': label, 'height': height, 'url': stream_url})
        return qualities