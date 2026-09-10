"""
Scrapes the full spinner-verb dictionary from https://claudionary.com/
and saves it as JSON for downstream Lithuanian-localization work.

Usage:
    python scrape_claudionary.py
Outputs:
    claudionary.json  -- list of entry dicts
"""
import json
import re
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup

URL = "https://claudionary.com/"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUT_HTML = DATA_DIR / "claudionary_raw.html"
OUT_JSON = DATA_DIR / "claudionary_source.json"


def fetch_html():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8", errors="replace")
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    return html


def parse_entries(html):
    soup = BeautifulSoup(html, "html.parser")
    entries = []
    for article in soup.select("article[id]"):
        word_id = article.get("id")

        h3 = article.select_one("h3 a")
        word = h3.get_text(strip=True) if h3 else None

        header_div = article.select_one("div.flex.items-center.gap-3.mt-1")
        ipa = None
        pos = None
        if header_div:
            spans = header_div.find_all("span")
            for sp in spans:
                cls = sp.get("class", [])
                text = sp.get_text(strip=True)
                if "font-mono" in cls and text.startswith("/"):
                    ipa = text
                elif "italic" in cls:
                    pos = text

        cat_span = article.select_one("span.text-xs.px-2.py-0\\.5")
        category = cat_span.get_text(strip=True) if cat_span else None

        etym_p = article.select_one("p.italic")
        etymology = None
        if etym_p:
            full = etym_p.get_text(" ", strip=True)
            etymology = re.sub(r"^Etym\.?\s*", "", full).strip()

        def_p = article.select_one("p.text-zinc-200")
        definition = def_p.get_text(" ", strip=True) if def_p else None

        img = article.select_one("img")
        diagram_caption = img.get("title") if img else None

        quote = article.select_one("blockquote")
        example = quote.get_text(" ", strip=True).strip('"“”') if quote else None

        entries.append({
            "id": word_id,
            "word": word,
            "ipa": ipa,
            "pos": pos,
            "category": category,
            "etymology": etymology,
            "definition": definition,
            "diagram_caption": diagram_caption,
            "example": example,
        })
    return entries


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    html = fetch_html()
    entries = parse_entries(html)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    print(f"Scraped {len(entries)} entries -> {OUT_JSON}")


if __name__ == "__main__":
    main()
