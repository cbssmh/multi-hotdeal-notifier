import requests
from config import DISCORD_WEBHOOK_URL


def send_discord_message(content: str):
    if not DISCORD_WEBHOOK_URL:
        raise ValueError("DISCORD_WEBHOOK_URL이 설정되지 않았습니다.")

    response = requests.post(
        DISCORD_WEBHOOK_URL,
        json={"content": content},
        timeout=10
    )
    response.raise_for_status()


def format_post_message(site_label: str, post: dict) -> str:
    return (
        f"사이트: {site_label}\n"
        f"제목: {post['title']}\n"
        f"링크: {post['url']}"
    )