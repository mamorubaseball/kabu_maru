import csv
import yfinance as yf
import concurrent.futures
import re

csv_file = "/Users/mamoru/kabu_maru/フィジカルAI/matome_new.csv"
html_file = "/Users/mamoru/kabu_maru/フィジカルAI/index.html"

# Read existing data
with open(csv_file, 'r', encoding='utf-8-sig') as f:
    reader = list(csv.reader(f))

header = reader[0]
data = reader[1:]

is_new = "PER" not in header
if is_new:
    idx = 4
    header.insert(idx, "PER")
    header.insert(idx+1, "PBR")
    header.insert(idx+2, "配当利回り")

def fetch_metrics(code):
    ticker_str = f"{code}.T"
    per, pbr, div = "-", "-", "-"
    try:
        t = yf.Ticker(ticker_str)
        info = t.info
        _per = info.get('trailingPE') or info.get('forwardPE')
        if _per: per = f"{_per:.1f}倍"
        _pbr = info.get('priceToBook')
        if _pbr: pbr = f"{_pbr:.2f}倍"
        _div = info.get('dividendYield') or info.get('trailingAnnualDividendYield')
        if _div is not None: div = f"{_div*100:.2f}%"
    except Exception:
        pass
    return per, pbr, div

def process_row(row):
    if is_new:
        base_row = row
    elif len(row) == len(header):
        base_row = row[:4] + row[7:]
    else:
        base_row = row
        
    code = base_row[2]
    per, pbr, div = fetch_metrics(code)
    
    new_row = list(base_row)
    new_row.insert(4, per)
    new_row.insert(5, pbr)
    new_row.insert(6, div)
    return new_row

print("Fetching financial metrics from yfinance...")
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    new_data = list(executor.map(process_row, data))

with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(new_data)

print(f"Metrics added to {csv_file}")

# Update HTML
html_template = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>フィジカルAI 関連銘柄ダッシュボード</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f172a; --surface: rgba(30, 41, 59, 0.7);
            --primary: #3b82f6; --accent: #10b981;
            --text-main: #f8fafc; --text-muted: #cbd5e1; --border: rgba(255, 255, 255, 0.1);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Inter', 'Noto Sans JP', sans-serif; background-color: var(--bg-color); background-image: radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%), radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.15) 0px, transparent 50%); background-attachment: fixed; color: var(--text-main); line-height: 1.6; padding-bottom: 50px; }
        header { padding: 40px 20px; text-align: center; background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 100; }
        h1 { font-size: 2.5rem; font-weight: 800; background: linear-gradient(to right, #60a5fa, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .category-nav { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin: 30px 0; }
        .nav-btn { background: var(--surface); border: 1px solid var(--border); color: var(--text-muted); padding: 8px 16px; border-radius: 20px; text-decoration: none; transition: all 0.3s ease; font-size: 0.9rem; font-weight: 500; }
        .nav-btn:hover { background: rgba(59, 130, 246, 0.2); color: white; border-color: rgba(59, 130, 246, 0.5); transform: translateY(-2px); }
        .category-section { margin-bottom: 60px; scroll-margin-top: 150px; }
        .category-title { font-size: 1.8rem; margin-bottom: 25px; padding-bottom: 10px; border-bottom: 2px solid rgba(59, 130, 246, 0.3); display: inline-block; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; }
        .card { background: var(--surface); backdrop-filter: blur(10px); border: 1px solid var(--border); border-radius: 16px; padding: 25px; transition: all 0.3s ease; position: relative; overflow: hidden; display: flex; flex-direction: column; }
        .card::before { content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: linear-gradient(to bottom, #3b82f6, #10b981); opacity: 0; transition: opacity 0.3s ease; }
        .card:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); border-color: rgba(255, 255, 255, 0.2); }
        .card:hover::before { opacity: 1; }
        .card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px; }
        .stock-name { font-size: 1.4rem; font-weight: 700; color: white; margin-bottom: 5px; }
        .stock-code { font-family: 'Inter', sans-serif; color: #94a3b8; font-size: 0.9rem; background: rgba(255, 255, 255, 0.1); padding: 2px 8px; border-radius: 4px; }
        .badge-container { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 15px; }
        .badge { font-size: 0.8rem; font-weight: 600; padding: 4px 10px; border-radius: 12px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); }
        .badge.rating-buy { background: rgba(16, 185, 129, 0.15); color: #34d399; border-color: rgba(16, 185, 129, 0.3); }
        .badge.rating-strong { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border-color: rgba(59, 130, 246, 0.3); }
        .badge.rating-hold { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border-color: rgba(245, 158, 11, 0.3); }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin-bottom: 15px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 8px;
            padding: 10px;
        }
        .metric-box { text-align: center; }
        .metric-label { font-size: 0.7rem; color: #94a3b8; margin-bottom: 2px; }
        .metric-val { font-size: 0.95rem; font-weight: 700; color: #e2e8f0; }

        .card-body { flex-grow: 1; }
        .stat-row { display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding: 8px 0; font-size: 0.9rem; }
        .stat-label { color: var(--text-muted); }
        .stat-val { font-weight: 600; }
        .growth-pos { color: #34d399; }
        .growth-neg { color: #f87171; }
        .desc { margin-top: 15px; font-size: 0.9rem; color: #cbd5e1; background: rgba(0, 0, 0, 0.2); padding: 12px; border-radius: 8px; border-left: 2px solid rgba(255, 255, 255, 0.1); }
        
        .ai-eval { margin-top: 15px; padding: 15px; background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(16, 185, 129, 0.1)); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 8px; position: relative; overflow: hidden; box-shadow: inset 0 0 15px rgba(59, 130, 246, 0.05); }
        .ai-eval::before { content: 'AIの投資評価'; position: absolute; top: 0; left: 0; background: linear-gradient(to right, #3b82f6, #10b981); color: #fff; font-size: 0.7rem; font-weight: 800; padding: 2px 10px; border-bottom-right-radius: 8px; }
        .ai-eval-content { margin-top: 10px; font-size: 1.1rem; font-weight: 700; color: #f8fafc; display: flex; align-items: center; gap: 10px; justify-content: center; text-align: center; }
        .ai-icon { font-size: 1.5rem; }
        .highlight { color: #34d399; font-size: 1.3rem; margin: 0 4px; }
        .card-footer { margin-top: 20px; }
        .link-btn { display: block; text-align: center; background: rgba(255, 255, 255, 0.05); color: white; text-decoration: none; padding: 10px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; transition: all 0.2s; border: 1px solid rgba(255, 255, 255, 0.1); }
        .link-btn:hover { background: var(--primary); border-color: var(--primary); }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .card { animation: fadeIn 0.5s ease backwards; }
    </style>
</head>
<body>
<header>
    <h1>Physical AI Stocks</h1>
    <p style="color: var(--text-muted); font-size: 1.1rem;">フィジカルAI・ロボティクス関連銘柄の最新ダッシュボード（AI評価付き）</p>
    <div class="category-nav" id="nav-container">
        <!-- NAV LINKS -->
    </div>
</header>
<div class="container" id="main-content">
    <!-- CONTENT -->
</div>
<script>
    document.addEventListener("DOMContentLoaded", () => {
        const cards = document.querySelectorAll('.card');
        cards.forEach((card, i) => { card.style.animationDelay = `${i * 0.05}s`; });
    });
</script>
</body>
</html>
"""

def colorize_growth(text):
    if '-' in text and not '売上-' in text and not '益-' in text: return text
    res = text
    res = re.sub(r'(\+[0-9.]+\%)', r'<span class="growth-pos">\1</span>', res)
    res = re.sub(r'(\-[0-9.]+\%)', r'<span class="growth-neg">\1</span>', res)
    return res

def get_rating_class(rating):
    if '強気買い' in rating: return 'rating-strong'
    if '買い' in rating: return 'rating-buy'
    if '中立' in rating: return 'rating-hold'
    return ''

categories = {}
for row in new_data:
    cat = row[0]
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(row)

nav_html = ""
content_html = ""

cat_idx = 0
for cat, stocks in categories.items():
    cat_id = f"cat-{cat_idx}"
    nav_html += f'<a href="#{cat_id}" class="nav-btn">{cat}</a>\\n'
    
    content_html += f'''
    <div class="category-section" id="{cat_id}">
        <h2 class="category-title">{cat}</h2>
        <div class="grid">
    '''
    
    for s in stocks:
        name, code, mcap, per, pbr, div, growth, analyst, desc, link, ai_eval = s[:11]
        
        rating_class = get_rating_class(analyst)
        rating_badge = f'<span class="badge {rating_class}">{analyst}</span>' if analyst != '-' else ''
        
        m = re.search(r'期待上昇率:\s*(\+[0-9]+%)\s*\(勝率:\s*([0-9]+%)\)', ai_eval)
        if m:
            upside = m.group(1); win_rate = m.group(2)
            html_eval = f'期待値<span class="highlight">{upside}</span> / 勝率<span class="highlight">{win_rate}</span>'
        else:
            html_eval = ai_eval
            
        content_html += f'''
            <div class="card">
                <div class="card-header">
                    <div>
                        <div class="stock-name">{name}</div>
                        <div class="stock-code">{code}</div>
                    </div>
                </div>
                <div class="badge-container">
                    <span class="badge">時価総額: {mcap}</span>
                    {rating_badge}
                </div>
                
                <div class="metrics-grid">
                    <div class="metric-box">
                        <div class="metric-label">PER</div>
                        <div class="metric-val">{per}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">PBR</div>
                        <div class="metric-val">{pbr}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">配当利回り</div>
                        <div class="metric-val">{div}</div>
                    </div>
                </div>

                <div class="card-body">
                    <div class="stat-row">
                        <span class="stat-label">業績推移(直近)</span>
                        <span class="stat-val">{colorize_growth(growth)}</span>
                    </div>
                    <div class="desc">{desc}</div>
                    
                    <div class="ai-eval">
                        <div class="ai-eval-content">
                            <span class="ai-icon">🤖</span>
                            <span>{html_eval}</span>
                        </div>
                    </div>
                </div>
                <div class="card-footer">
                    <a href="{link}" target="_blank" class="link-btn">Kabutanで詳細を見る ↗</a>
                </div>
            </div>
        '''
    content_html += '</div></div>'
    cat_idx += 1

final_html = html_template.replace('<!-- NAV LINKS -->', nav_html).replace('<!-- CONTENT -->', content_html)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(final_html)
print("HTML updated with PER/PBR/Dividend metrics.")
