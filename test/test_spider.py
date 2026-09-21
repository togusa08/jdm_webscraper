import requests, re
from lxml import html

TARGET_MODELS = {
    # Toyota
    "ヤリス":             "Toyota_Yaris",
    "カローラ":           "Toyota_Corolla",
    "シエンタ":           "Toyota_Sienta",
}

def _match_target(raw_model: str):
    if raw_model in TARGET_MODELS:
        return TARGET_MODELS[raw_model]
    for key, label in TARGET_MODELS.items():
        if key in raw_model or raw_model in key:
            return label
    return None

url = 'https://www.car.net/usedcar/shashu/bTO/index.html'
resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
tree = html.fromstring(resp.content)
model_nodes = tree.xpath('//a[contains(@href, "/b") and contains(@href, "/s") and contains(@href, "index.html") and not(contains(@href, "sp"))]')

seen_links = set()
for node in model_nodes:
    raw_model = "".join(node.itertext()).strip()
    if not raw_model:
        continue

    link = node.get("href", "")
    if not link or link in seen_links:
        continue
    seen_links.add(link)

    std_label = _match_target(raw_model)
    if std_label:
        print(f"MATCH: {raw_model} -> {std_label}")
