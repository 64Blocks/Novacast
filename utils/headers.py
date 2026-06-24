import random

from config.constants import USER_AGENTS


def get_random_user_agent() -> str:
    return random.choice(USER_AGENTS)


def get_browser_headers() -> dict:
    return {
        'User-Agent': get_random_user_agent(),
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache'
    }