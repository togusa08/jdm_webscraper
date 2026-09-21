import urllib.request
from bs4 import BeautifulSoup
import json

with open('prius.html', 'rb') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

items = []
for container in soup.select('.cassetteMain__inner')[:3]:  # get first 3 for inspection
    title_elem = container.select_one('.cassetteMain__title')
    title = title_elem.text.strip() if title_elem else ''
    
    price_elem = container.select_one('.cassetteMain__priceTotal') or container.select_one('.cassetteMain__price .yen')
    price = price_elem.text.strip() if price_elem else ''
    
    img_elem = container.select_one('img.js-caset_photo')
    # fallback to just any img tag inside
    if not img_elem:
        img_elem = container.select_one('img')
        
    img_src = img_elem.get('data-src') or img_elem.get('src') if img_elem else ''
    
    specs = {}
    spec_table = container.select_one('.cassetteMain__specTable')
    if spec_table:
        for dt, dd in zip(spec_table.select('dt'), spec_table.select('dd')):
            specs[dt.text.strip()] = dd.text.strip()
            
    # look for other price
    base_price = container.select_one('.cassetteMain__priceTotal + p')
    if base_price:
        specs['base_price'] = base_price.text.strip()

    items.append({
        'title': title,
        'price': price,
        'img': img_src,
        'specs': specs,
        'raw_links': [a.get('href') for a in container.select('a') if 'usedcar/detail' in a.get('href', '')]
    })

with open('car_details.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"Extracted properties for {len(items)} items. Saved to car_details.json")
