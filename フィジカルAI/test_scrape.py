import requests
from bs4 import BeautifulSoup

url = "https://minkabu.jp/stock/6981"
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

print("Title:", soup.title.string if soup.title else "No title")

# Try to find market cap
try:
    # Minkabu's market cap is usually in a table or under a specific class
    # Let's just print all text inside elements that might contain '時価総額'
    elems = soup.find_all(string=lambda text: '時価総額' in text if text else False)
    for e in elems:
        print("Market Cap Context:", e.parent.parent.text.replace('\n', ' ').strip()[:100])
except Exception as e:
    print(e)

# Try to find analyst rating
try:
    elems = soup.find_all(string=lambda text: 'アナリスト' in text if text else False)
    for e in elems:
        print("Analyst Context:", e.parent.parent.text.replace('\n', ' ').strip()[:100])
except Exception as e:
    print(e)

