import yfinance as yf
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import re

markdown_content = """ご提示いただいた画像にある「フィジカルAI」関連銘柄を、それぞれのカテゴリーごとに整理し、**株探（Kabutan）**の個別銘柄ページへのリンクをまとめました。

銘柄名をクリックすると、最新の株価や決算情報が確認できます。

---

## 1. AI開発・導入
AIのソフトウェアやシステム開発を担う企業群です。

| 銘柄名 | 証券コード | 株探リンク |
| :--- | :--- | :--- |
| **セック** | 3741 | [株探で見る](https://kabutan.jp/stock/?code=3741) |
| マクニカHD | 3132 | [株探で見る](https://kabutan.jp/stock/?code=3132) |
| エクサウィザーズ | 4259 | [株探で見る](https://kabutan.jp/stock/?code=4259) |
| SRE HD | 2980 | [株探で見る](https://kabutan.jp/stock/?code=2980) |
| ABEJA | 5574 | [株探で見る](https://kabutan.jp/stock/?code=5574) |
| ヘッドウォータース | 4011 | [株探で見る](https://kabutan.jp/stock/?code=4011) |

---

## 2. センシングなど独自技術
センサーや画像認識など、ロボットの「目」や「感覚」を支える技術を持つ企業群です。

| 銘柄名 | 証券コード | 株探リンク |
| :--- | :--- | :--- |
| **村田製作所** | 6981 | [株探で見る](https://kabutan.jp/stock/?code=6981) |
| テクノホライゾン | 6629 | [株探で見る](https://kabutan.jp/stock/?code=6629) |
| **オプテックスG** | 6914 | [株探で見る](https://kabutan.jp/stock/?code=6914) |
| アバールデータ | 6918 | [株探で見る](https://kabutan.jp/stock/?code=6918) |
| Kudan | 4425 | [株探で見る](https://kabutan.jp/stock/?code=4425) |
| キヤノン | 7751 | [株探で見る](https://kabutan.jp/stock/?code=7751) |
| キーエンス | 6861 | [株探で見る](https://kabutan.jp/stock/?code=6861) |

---

## 3. ロボット本体・アーム
ロボットの「体」そのものを製造する大手メーカー群です。

| 銘柄名 | 証券コード | 株探リンク |
| :--- | :--- | :--- |
| **ファナック** | 6954 | [株探で見る](https://kabutan.jp/stock/?code=6954) |
| **安川電機** | 6506 | [株探で見る](https://kabutan.jp/stock/?code=6506) |
| ソフトバンクG | 9984 | [株探で見る](https://kabutan.jp/stock/?code=9984) |
| 川崎重工業 | 7012 | [株探で見る](https://kabutan.jp/stock/?code=7012) |
| ダイヘン | 6622 | [株探で見る](https://kabutan.jp/stock/?code=6622) |
| オムロン | 6645 | [株探で見る](https://kabutan.jp/stock/?code=6645) |
| 西部電機 | 6144 | [株探で見る](https://kabutan.jp/stock/?code=6144) |
| 不二越 | 6474 | [株探で見る](https://kabutan.jp/stock/?code=6474) |
| ヤマハ発動機 | 7272 | [株探で見る](https://kabutan.jp/stock/?code=7272) |
| デンソー | 6902 | [株探で見る](https://kabutan.jp/stock/?code=6902) |
| アズビル | 6845 | [株探で見る](https://kabutan.jp/stock/?code=6845) |
| セイコーエプソン | 6724 | [株探で見る](https://kabutan.jp/stock/?code=6724) |
| 川田テクノロジーズ | 3443 | [株探で見る](https://kabutan.jp/stock/?code=3443) |

---

## 4. 開発支援・実用化技術
システムインテグレーションや半導体など、実装を支援する企業群です。

| 銘柄名 | 証券コード | 株探リンク |
| :--- | :--- | :--- |
| **豆蔵** | 202A | [株探で見る](https://kabutan.jp/stock/?code=202A) |
| 三菱電機 | 6503 | [株探で見る](https://kabutan.jp/stock/?code=6503) |
| 日立製作所 | 6501 | [株探で見る](https://kabutan.jp/stock/?code=6501) |
| 日本電気（NEC） | 6701 | [株探で見る](https://kabutan.jp/stock/?code=6701) |
| 富士通 | 6702 | [株探で見る](https://kabutan.jp/stock/?code=6702) |
| ソニーG | 6758 | [株探で見る](https://kabutan.jp/stock/?code=6758) |
| ルネサス | 6723 | [株探で見る](https://kabutan.jp/stock/?code=6723) |
| ジーデップ・アドバンス | 5885 | [株探で見る](https://kabutan.jp/stock/?code=5885) |

---

## 5. 基幹部品
モーターや減速機など、ロボットの精密な動きを支える部品メーカー群です。

| 銘柄名 | 証券コード | 株探リンク |
| :--- | :--- | :--- |
| **ヒーハイスト** | 6433 | [株探で見る](https://kabutan.jp/stock/?code=6433) |
| **ハーモニック** | 6324 | [株探で見る](https://kabutan.jp/stock/?code=6324) |
| 住友重機械工業 | 6302 | [株探で見る](https://kabutan.jp/stock/?code=6302) |
| ミネベアミツミ | 6479 | [株探で見る](https://kabutan.jp/stock/?code=6479) |
| 日本精工 | 6471 | [株探で見る](https://kabutan.jp/stock/?code=6471) |
| 山洋電気 | 6516 | [株探で見る](https://kabutan.jp/stock/?code=6516) |
| カヤバ | 7242 | [株探で見る](https://kabutan.jp/stock/?code=7242) |
| IDEC | 6652 | [株探で見る](https://kabutan.jp/stock/?code=6652) |
| ナブテスコ | 6268 | [株探で見る](https://kabutan.jp/stock/?code=6268) |
| マブチモーター | 6592 | [株探で見る](https://kabutan.jp/stock/?code=6592) |
| ニデック | 6594 | [株探で見る](https://kabutan.jp/stock/?code=6594) |
| シンフォニア | 6507 | [株探で見る](https://kabutan.jp/stock/?code=6507) |

---

## 6. その他部品
ケーブルやコネクタ、空圧機器などを供給する企業群です。

| 銘柄名 | 証券コード | 株探リンク |
| :--- | :--- | :--- |
| **JMACS** | 5817 | [株探で見る](https://kabutan.jp/stock/?code=5817) |
| 日本トムソン | 6480 | [株探で見る](https://kabutan.jp/stock/?code=6480) |
| イリソ電子工業 | 6908 | [株探で見る](https://kabutan.jp/stock/?code=6908) |
| SMC | 6273 | [株探で見る](https://kabutan.jp/stock/?code=6273) |
| 新東工業 | 6339 | [株探で見る](https://kabutan.jp/stock/?code=6339) |
| コンバム | 6265 | [株探で見る](https://kabutan.jp/stock/?code=6265) |
| THK | 6481 | [株探で見る](https://kabutan.jp/stock/?code=6481) |
| ヒロセ電機 | 6806 | [株探で見る](https://kabutan.jp/stock/?code=6806) |
| 日本航空電子工業 | 6807 | [株探で見る](https://kabutan.jp/stock/?code=6807) |
"""

def format_jpy(val):
    if not val: return "-"
    if val >= 1_000_000_000_000:
        return f"{val/1_000_000_000_000:.1f}兆円"
    elif val >= 1_000_000_000:
        return f"{val/1_000_000_000:.1f}億円"
    elif val >= 1_000_000:
        return f"{val/1_000_000:.1f}百万円"
    return f"{val}円"

def format_growth(val):
    if val is None: return "-"
    return f"{val*100:+.1f}%"

def fetch_data(code):
    info_dict = {"code": code, "market_cap": "-", "growth": "-", "analyst": "-", "desc": "-"}
    try:
        t = yf.Ticker(f"{code}.T")
        i = t.info
        info_dict['market_cap'] = format_jpy(i.get('marketCap'))
        rev = i.get('revenueGrowth')
        earn = i.get('earningsGrowth')
        if rev is not None and earn is not None:
            info_dict['growth'] = f"売上{format_growth(rev)}/益{format_growth(earn)}"
        elif rev is not None:
            info_dict['growth'] = f"売上{format_growth(rev)}"
        else:
            info_dict['growth'] = "-"
            
        rec = i.get('recommendationKey', '-')
        rec_map = {'buy': '買い', 'strong_buy': '強気買い', 'hold': '中立', 'sell': '売り', 'strong_sell': '強気売り', 'none': '-'}
        info_dict['analyst'] = rec_map.get(rec, rec)

        url = f"https://kabutan.jp/stock/?code={code}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        cb = soup.select_one('.company_block')
        if cb:
            t_text = cb.text.replace('\\n', ' ')
            if '概要' in t_text:
                desc = t_text.split('概要')[1].split('業種')[0].strip()
                # Ensure no markdown table breaking chars
                desc = desc.replace('|', '').replace('\n', ' ')
                info_dict['desc'] = desc[:45] + '..' if len(desc) > 45 else desc
    except Exception as e:
        print(f"Error {code}: {e}")
    return info_dict

def main():
    lines = markdown_content.split('\n')
    out = []
    codes_to_fetch = []
    for line in lines:
        m = re.match(r'\|\s*(.*?)\s*\|\s*([0-9A-Z]{4})\s*\|', line)
        if m and line.count('|') == 4:
            codes_to_fetch.append(m.group(2))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_data, codes_to_fetch))
    
    data_map = {r['code']: r for r in results}
    
    for line in lines:
        if '| 銘柄名 | 証券コード | 株探リンク |' in line:
            out.append('| 銘柄名 | 証券コード | 時価総額 | 業績推移(直近) | アナリスト | 企業の特徴 | 株探リンク |')
        elif '| :--- | :--- | :--- |' in line:
            out.append('| :--- | :--- | :--- | :--- | :--- | :--- | :--- |')
        else:
            m = re.match(r'\|\s*(.*?)\s*\|\s*([0-9A-Z]{4})\s*\|\s*\[.*?\]\(.*?\)\s*\|', line)
            if m:
                name = m.group(1)
                code = m.group(2)
                d = data_map.get(code, {"market_cap": "-", "growth": "-", "analyst": "-", "desc": "-"})
                link_part = line.split('|')[-2].strip()
                new_line = f"| {name} | {code} | {d['market_cap']} | {d['growth']} | {d['analyst']} | {d['desc']} | {link_part} |"
                out.append(new_line)
            else:
                out.append(line)
                
    with open("matome_new.md", "w") as f:
        f.write('\n'.join(out))

if __name__ == "__main__":
    main()
