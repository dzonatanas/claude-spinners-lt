#!/usr/bin/env python3
"""
Pulls real Lithuanian verb candidates from the live DLKZ (Dabartines lietuviu
kalbos zodynas, https://ekalba.lt/dabartines-lietuviu-kalbos-zodynas/) for
brainstorming new spinner-word candidates -- see spinner_verbs_lt_progress.json
for the actual word pool this feeds into.

WHY THIS EXISTS / lessons learned (2026-09-14):
- The site is an AngularJS single-page app. A plain HTTP fetch only gets the
  static shell (title/meta), not the word list -- it MUST be driven with a
  real browser. This script uses Playwright + headless Chromium.
- The old http://lkz.lt (the big historical/dialectal dictionary, a DIFFERENT
  dictionary from DLKZ) is deprecated -- its own homepage says "no longer
  updated, see ekalba.lt instead". Not used here.
- The site's "Detalioji paieska" advanced search has a part-of-speech-ish tag
  ("Pazyma" = "vksm." for verb), but it's an unreliable manual annotation --
  filtering by it returned only 16 hits SITE-WIDE, nowhere near all verbs.
  DO NOT rely on it. Instead this script pages through the plain alphabetical
  headword list and keeps entries whose FIRST headword form ends in the
  Lithuanian infinitive suffix "-ti" or the reflexive "-tis" -- a reliable,
  simple heuristic (Lithuanian infinitives are the dictionary's own citation
  form, and non-verbs essentially never end this way).

Usage (run with the project's dedicated venv, see install/README -- this venv
already has playwright + chromium installed, do not reinstall):
    ../.venv_scraper/Scripts/python.exe scrape_dlkz.py --prefix ab
    ../.venv_scraper/Scripts/python.exe scrape_dlkz.py --prefix ab,ac,ad --out candidates.txt
    ../.venv_scraper/Scripts/python.exe scrape_dlkz.py --all --max-pages 5   (quick partial test)
    ../.venv_scraper/Scripts/python.exe scrape_dlkz.py --all                (full dictionary sweep,
                                                                              ~49 pages at 1000/page,
                                                                              several minutes)

With --prefix, ALL pages are still scanned (no alphabetical early-exit --
simpler and safer than trying to guess where a prefix's range ends), so a
narrow prefix test on the full dictionary is still a full sweep under the
hood. Use --max-pages for a fast partial check instead.

Output: one candidate per line, "headword | full dictionary line", sorted,
deduplicated. Cross-reference the output against
data/spinner_verbs_lt_progress.json yourself before adding anything -- this
only finds REAL dictionary verbs, it says nothing about whether a word fits
the spinner tone (see style guidelines in README.md).
"""
import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

DLKZ_URL = "https://ekalba.lt/dabartines-lietuviu-kalbos-zodynas/"


def is_verb_headword(word: str) -> bool:
    w = word.strip()
    return w.endswith("ti") or w.endswith("tis")


def extract_entries(body_text: str) -> list[str]:
    """Pulls just the word-list lines out of the page's full visible text."""
    lines = body_text.split("\n")
    entries = []
    started = False
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("Paieškos rezultatai"):
            started = True
            continue
        if started:
            if line in ("Rodyti", "50", "100", "500", "1000", "Pereiti į"):
                break
            entries.append(line)
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--prefix", help="Comma-separated headword prefixes to keep (case-insensitive), e.g. 'ab,ac'. Omit with --all.")
    parser.add_argument("--all", action="store_true", help="Scan the whole dictionary, no prefix filter.")
    parser.add_argument("--max-pages", type=int, default=None, help="Stop after this many pages (for quick tests).")
    parser.add_argument("--out", help="Write results to this file instead of stdout.")
    args = parser.parse_args()

    if not args.all and not args.prefix:
        parser.error("pass --prefix a,b,c or --all")

    prefixes = None
    if args.prefix:
        prefixes = tuple(p.strip().lower() for p in args.prefix.split(",") if p.strip())

    found = {}  # headword -> full line, dedup

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(DLKZ_URL, wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(1500)
        page.select_option("#results-show", "1000")
        page.wait_for_timeout(2000)

        page_count_text = page.locator("span.block_nav__label_number").inner_text()
        total_pages = int(page_count_text.strip())
        if args.max_pages:
            total_pages = min(total_pages, args.max_pages)
        print(f"Scanning {total_pages} page(s) at 1000 entries/page...", file=sys.stderr)

        for page_num in range(1, total_pages + 1):
            if page_num > 1:
                page_input = page.locator("#results-page")
                page_input.fill(str(page_num))
                page_input.press("Enter")
                page.wait_for_timeout(1500)

            body_text = page.inner_text("body")
            entries = extract_entries(body_text)
            for line in entries:
                headword = line.split(",")[0].strip()
                if prefixes and not headword.lower().startswith(prefixes):
                    continue
                if is_verb_headword(headword):
                    found[headword] = line

            print(f"  page {page_num}/{total_pages}: {len(found)} verb candidates so far", file=sys.stderr)

        browser.close()

    output_lines = [f"{hw} | {line}" for hw, line in sorted(found.items())]
    output = "\n".join(output_lines)

    if args.out:
        Path(args.out).write_text(output + "\n", encoding="utf-8")
        print(f"Wrote {len(found)} candidates to {args.out}", file=sys.stderr)
    else:
        print(output)
        print(f"\n{len(found)} candidates total", file=sys.stderr)


if __name__ == "__main__":
    main()
