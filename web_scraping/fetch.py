import urllib.request

url = ''

req = urllib.request.Request(
    url, 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
)

with urllib.request.urlopen(req) as response:
    html = response.read()

with open('prius.html', 'wb') as f:
    f.write(html)
