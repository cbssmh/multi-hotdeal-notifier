import re
import time
import requests
from bs4 import BeautifulSoup

FMKOREA_MOBILE_URL = "https://m.fmkorea.com/index.php?mid=hotdeal&order_type=desc&sort_index=pop"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Referer": "https://m.fmkorea.com/",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
}

session = requests.Session()
session.headers.update(HEADERS)


def extract_document_srl(href: str):
    match = re.search(r"document_srl=(\d+)", href)
    return match.group(1) if match else None


def is_noise_text(text: str) -> bool:
    text = text.strip()
    if not text:
        return True

    noise_patterns = [
        r"^\d[\d,]*원$",
        r"^무료$",
        r"^가격별상이$",
        r"^[A-Za-z0-9]{1,10}$",
    ]

    for pattern in noise_patterns:
        if re.match(pattern, text):
            return True

    return False


def is_notice_title(text: str) -> bool:
    notice_keywords = [
        "통합공지",
        "게시판 통합공지",
        "금지",
        "공지",
    ]
    return any(keyword in text for keyword in notice_keywords)


def fetch_page():
    for attempt in range(3):
        try:
            response = session.get(FMKOREA_MOBILE_URL, timeout=10)

            if response.status_code in (429, 430):
                print(f"[WARN] FM코리아 차단 응답: {response.status_code}")
                time.sleep(3)
                continue

            response.raise_for_status()
            return response.text

        except requests.RequestException as e:
            print(f"[WARN] FM코리아 요청 실패 (시도 {attempt + 1}/3): {e}")
            time.sleep(3)

    return None


def get_fmkorea_posts(limit=10):
    html = fetch_page()
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")

    posts = []
    seen_ids = set()

    for a_tag in soup.select("a"):
        href = a_tag.get("href", "").strip()
        text = a_tag.get_text(" ", strip=True)

        if not href or not text:
            continue

        if "document_srl=" not in href:
            continue

        if "search_target=title" in href:
            continue

        post_id = extract_document_srl(href)
        if not post_id:
            continue

        if post_id in seen_ids:
            continue

        if is_noise_text(text):
            continue

        if is_notice_title(text):
            continue

        if href.startswith("/"):
            url = "https://m.fmkorea.com" + href
        elif href.startswith("http"):
            url = href
        else:
            continue

        seen_ids.add(post_id)
        posts.append({
            "id": post_id,
            "title": text,
            "url": url,
        })

        if len(posts) >= limit:
            break

    return posts