import requests, re
from lxml import html

url = 'https://www.car.net/usedcar/shashu/bTO/index.html'
resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
tree = html.fromstring(resp.content)
nodes = tree.xpath('//a[contains(@href, "/b") and contains(@href, "/s") and contains(@href, "index.html") and not(contains(@href, "sp"))]')
print(f'Matched {len(nodes)} nodes')
for a in nodes[:10]:
    print(a.get('href'), "".join(a.itertext()).strip())
