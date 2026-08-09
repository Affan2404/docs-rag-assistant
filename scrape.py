import os, re, time, requests
from bs4 import BeautifulSoup

ARTICLE_URLS = [
    "https://support.freshdesk.com/support/solutions/articles/225162-is-there-way-to-add-tickets-automatically-to-the-solutions-or-knowledge-base-",
    "https://support.freshdesk.com/support/solutions/articles/226362-what-is-multilingual-knowledge-base-which-plan-can-i-see-this-in-",
    "https://support.freshdesk.com/support/solutions/articles/226370-how-to-add-an-article-in-its-translated-version-",
    "https://support.freshdesk.com/support/solutions/articles/228029-how-to-create-articles-in-multiple-languages-",
    "https://support.freshdesk.com/support/solutions/articles/226364-can-i-change-the-primary-language-after-enabling-multilingual-support-",
      # Knowledge Base structure/management (new)
    "https://support.freshdesk.com/support/solutions/articles/213271-manage-your-knowledge-base",
    "https://support.freshdesk.com/support/solutions/articles/37611-create-and-organize-knowledge-base",
    "https://support.freshdesk.com/en/support/solutions/articles/50000004736-structuring-your-knowledge-base-with-flexible-hierarchy-up-to-5-folder-levels-",

    # Automation rules (new - genuinely different topic)
    "https://support.freshdesk.com/support/solutions/articles/207276-overview-of-automation-rules",
    "https://support.freshdesk.com/support/solutions/articles/37614-setting-up-automation-rules-to-run-on-ticket-creation",
    "https://support.freshdesk.com/support/solutions/articles/99047-automation-rules-that-run-on-ticket-updates",
    "https://support.freshdesk.com/support/solutions/articles/37615",
]
OUTPUT_DIR = "data/raw"
BOILERPLATE_MARKER = "Freshdesk Omni 2023 Knowledge Base"

def slugify(url):
    last = url.rstrip("/").split("/")[-1]
    return re.sub(r"[^a-zA-Z0-9\-]", "", last)[:80]

# Isolate text between "Modified on:" and "Related articles", then cut
# everything up to the fixed boilerplate marker so only real content remains
def extract_article_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "form"]):
        tag.decompose()
    full_text = soup.get_text("\n", strip=True)

    match = re.search(r"Modified on:.*?\n(.*?)Related articles", full_text, re.DOTALL)
    if not match:
        return None
    body = match.group(1).strip()

    marker_pos = body.find(BOILERPLATE_MARKER)
    if marker_pos != -1:
        body = body[marker_pos + len(BOILERPLATE_MARKER):].strip()

    if not body:
        return None
    return body

def scrape_article(url):
    print(f"Fetching: {url}")
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  FAILED: {e}")
        return

    text = extract_article_text(resp.text)
    if not text:
        print("  WARNING: could not isolate article body, check page manually.")
        return

    path = os.path.join(OUTPUT_DIR, slugify(url) + ".txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"  Saved {len(text)} characters to {path}")

# Loop through all target URLs with a delay between requests to avoid hammering the server
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for url in ARTICLE_URLS:
        scrape_article(url)
        time.sleep(1)
    print("\nDone. Check data/raw/")

if __name__ == "__main__":
    main()