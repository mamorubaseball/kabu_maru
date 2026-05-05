import requests
from bs4 import BeautifulSoup

url = "https://kabutan.jp/stock/?code=6981"
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

print("Title:", soup.title.string)
# Characteristics
try:
    desc = soup.select_one('.company_block').text.replace('\n', ' ').strip()
    print("Kabutan Desc:", desc)
except Exception as e:
    print(e)
