"""
"""
import requests
from lxml import html

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    )
}

MAKER_URLS = {
    "Toyota":   "https://www.car.net/usedcar/shashu/bTO/index.html",
    "Honda":    "https://www.car.net/usedcar/shashu/bHO/index.html",
    "Suzuki":   "https://www.car.net/usedcar/shashu/bSZ/index.html",
    "Daihatsu": "https://www.car.net/usedcar/shashu/bDA/index.html",
}

SELECTOR_OLD  = '//a[contains(@href, "/usedcar/b") and contains(@href, "/s")]'
# Broader fallback – every link whose href contains /usedcar/b
SELECTOR_BROAD = '//a[contains(@href, "/usedcar/b")]'

for maker, url in MAKER_URLS.items():
    print(f"\n{'='*60}")
    print(f"MAKER: {maker}  URL: {url}")
    resp = requests.get(url, headers=HEADERS, timeout=15)
    tree = html.fromstring(resp.content)

    # Try the original selector
    nodes_old = tree.xpath(SELECTOR_OLD)
    print(f"  [OLD selector] matched {len(nodes_old)} nodes")
    for n in nodes_old[:10]:
        text = "".join(n.itertext()).strip()
        href = n.get("href", "")
        print(f"    href={href!r:60s} text={text!r}")

    if len(nodes_old) == 0:
        # Fall back to broad selector and print first 20
        nodes_broad = tree.xpath(SELECTOR_BROAD)
        print(f"  [BROAD selector] matched {len(nodes_broad)} nodes – first 20:")
        for n in nodes_broad[:20]:
            text = "".join(n.itertext()).strip()
            href = n.get("href", "")
            print(f"    href={href!r:60s} text={text!r}")
