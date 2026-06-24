import re

RE_EXTINF_NAME = re.compile(r'tvg-name="([^"]+)"')

RE_EXTINF_LOGO = re.compile(r'tvg-logo="([^"]+)"')

RE_EXTINF_GROUP = re.compile(r'group-title="([^"]+)"')

RE_STREAM_RES = re.compile(r'RESOLUTION=\d+x(\d+)')