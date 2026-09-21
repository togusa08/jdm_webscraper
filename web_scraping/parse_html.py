import urllib.request
from bs4 import BeautifulSoup
import json

with open('prius.html', 'rb') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

items = []

for header in soup.find_all(['h2', 'h3']):
    if header.a and 'usedcar/detail' in header.a.get('href', ''):
        container = header.find_parent('div')
        # Let's inspect this container
        if container:
            items.append({
                'header_class': header.get('class', []),
                'container_class': container.get('class', []),
                'parent_class': container.find_parent().get('class', []),
                'text': header.text.strip()
            })

with open('structure.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"Found {len(items)} items. Saved to structure.json")
