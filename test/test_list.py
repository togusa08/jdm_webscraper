import requests
from lxml import html

url = 'https://www.car.net/usedcar/bTO/s229/index.html'
resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
tree = html.fromstring(resp.content)
car_links = tree.xpath('//a[contains(@href, "/usedcar/detail/")]/@href')
print(f"Found {len(car_links)} car links")
for link in car_links[:5]:
    print(link)
