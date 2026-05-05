import re

html_template = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>フィジカルAI 関連銘柄ダッシュボード</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f172a;
            --surface: rgba(30, 41, 59, 0.7);
            --primary: #3b82f6;
            --accent: #10b981;
            --text-main: #f8fafc;
            --text-muted: #cbd5e1;
            --border: rgba(255, 255, 255, 0.1);
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', 'Noto Sans JP', sans-serif;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.15) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-main);
            line-height: 1.6;
            padding-bottom: 50px;
        }

        header {
            padding: 40px 20px;
            text-align: center;
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        h1 {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(to right, #60a5fa, #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .category-nav {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            margin: 30px 0;
        }

        .nav-btn {
            background: var(--surface);
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s ease;
            font-size: 0.9rem;
            font-weight: 500;
        }

        .nav-btn:hover {
            background: rgba(59, 130, 246, 0.2);
            color: white;
            border-color: rgba(59, 130, 246, 0.5);
            transform: translateY(-2px);
        }

        .category-section {
            margin-bottom: 60px;
            scroll-margin-top: 150px;
        }

        .category-title {
            font-size: 1.8rem;
            margin-bottom: 10px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(59, 130, 246, 0.3);
            display: inline-block;
        }

        .category-desc {
            color: var(--text-muted);
            margin-bottom: 25px;
            font-size: 1rem;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 20px;
        }

        .card {
            background: var(--surface);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 25px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(to bottom, #3b82f6, #10b981);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            border-color: rgba(255, 255, 255, 0.2);
        }

        .card:hover::before {
            opacity: 1;
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }

        .stock-name {
            font-size: 1.4rem;
            font-weight: 700;
            color: white;
            margin-bottom: 5px;
        }

        .stock-code {
            font-family: 'Inter', sans-serif;
            color: #94a3b8;
            font-size: 0.9rem;
            background: rgba(255, 255, 255, 0.1);
            padding: 2px 8px;
            border-radius: 4px;
        }

        .badge-container {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 15px;
        }

        .badge {
            font-size: 0.8rem;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .badge.rating-buy {
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border-color: rgba(16, 185, 129, 0.3);
        }
        
        .badge.rating-strong {
            background: rgba(59, 130, 246, 0.15);
            color: #60a5fa;
            border-color: rgba(59, 130, 246, 0.3);
        }

        .badge.rating-hold {
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            border-color: rgba(245, 158, 11, 0.3);
        }

        .card-body {
            flex-grow: 1;
        }

        .stat-row {
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding: 8px 0;
            font-size: 0.9rem;
        }

        .stat-label {
            color: var(--text-muted);
        }

        .stat-val {
            font-weight: 600;
        }

        .growth-pos { color: #34d399; }
        .growth-neg { color: #f87171; }

        .desc {
            margin-top: 15px;
            font-size: 0.9rem;
            color: #cbd5e1;
            background: rgba(0, 0, 0, 0.2);
            padding: 12px;
            border-radius: 8px;
            border-left: 2px solid rgba(255, 255, 255, 0.1);
        }

        .card-footer {
            margin-top: 20px;
        }

        .link-btn {
            display: block;
            text-align: center;
            background: rgba(255, 255, 255, 0.05);
            color: white;
            text-decoration: none;
            padding: 10px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.2s;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .link-btn:hover {
            background: var(--primary);
            border-color: var(--primary);
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .card {
            animation: fadeIn 0.5s ease backwards;
        }
    </style>
</head>
<body>

<header>
    <h1>Physical AI Stocks</h1>
    <p style="color: var(--text-muted); font-size: 1.1rem;">フィジカルAI・ロボティクス関連銘柄の最新ダッシュボード</p>
    <div class="category-nav" id="nav-container">
        <!-- Nav Links -->
    </div>
</header>

<div class="container" id="main-content">
    <!-- Content injected here -->
</div>

<script>
    // Delay animations for smooth staggered loading
    document.addEventListener("DOMContentLoaded", () => {
        const cards = document.querySelectorAll('.card');
        cards.forEach((card, i) => {
            card.style.animationDelay = `${i * 0.05}s`;
        });
    });
</script>
</body>
</html>
"""

def parse_markdown(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = re.split(r'##\s+', content)[1:]
    categories = []
    
    for sec in sections:
        lines = sec.strip().split('\n')
        title_line = lines[0].strip()
        
        # 1. AI開発・導入  -> Idx: 1, Name: AI開発・導入
        cat_id = f"cat-{len(categories)}"
        title = title_line
        
        desc = ""
        for line in lines[1:]:
            if line.startswith('|'):
                break
            if line.strip() and not line.startswith('---'):
                desc += line.strip() + " "
                
        stocks = []
        for line in lines:
            if line.startswith('|') and not line.startswith('| 銘柄名') and not line.startswith('| :---'):
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 7:
                    name = parts[0].replace('**', '')
                    code = parts[1]
                    mcap = parts[2]
                    growth = parts[3]
                    analyst = parts[4]
                    c_desc = parts[5]
                    link_match = re.search(r'href="(.*?)"|\]\((.*?)\)', parts[6])
                    link = link_match.group(1) or link_match.group(2) if link_match else f"https://kabutan.jp/stock/?code={code}"
                    
                    stocks.append({
                        'name': name, 'code': code, 'mcap': mcap, 
                        'growth': growth, 'analyst': analyst, 
                        'desc': c_desc, 'link': link
                    })
        
        categories.append({
            'id': cat_id,
            'title': title,
            'desc': desc.strip(),
            'stocks': stocks
        })
        
    return categories

def colorize_growth(text):
    if '-' in text and not '売上-' in text and not '益-' in text:
        return text
    
    res = text
    # Very simple highlight
    res = re.sub(r'(\+[0-9.]+\%)', r'<span class="growth-pos">\1</span>', res)
    res = re.sub(r'(\-[0-9.]+\%)', r'<span class="growth-neg">\1</span>', res)
    return res

def get_rating_class(rating):
    if '強気買い' in rating: return 'rating-strong'
    if '買い' in rating: return 'rating-buy'
    if '中立' in rating: return 'rating-hold'
    return ''

def generate_html():
    categories = parse_markdown('matome_new.md')
    
    nav_html = ""
    content_html = ""
    
    for cat in categories:
        nav_html += f'<a href="#{cat["id"]}" class="nav-btn">{cat["title"]}</a>\n'
        
        content_html += f'''
        <div class="category-section" id="{cat["id"]}">
            <h2 class="category-title">{cat["title"]}</h2>
            <p class="category-desc">{cat["desc"]}</p>
            <div class="grid">
        '''
        
        for s in cat["stocks"]:
            rating_class = get_rating_class(s['analyst'])
            rating_badge = f'<span class="badge {rating_class}">{s["analyst"]}</span>' if s['analyst'] != '-' else ''
            
            content_html += f'''
                <div class="card">
                    <div class="card-header">
                        <div>
                            <div class="stock-name">{s['name']}</div>
                            <div class="stock-code">{s['code']}</div>
                        </div>
                    </div>
                    <div class="badge-container">
                        <span class="badge">時価総額: {s['mcap']}</span>
                        {rating_badge}
                    </div>
                    <div class="card-body">
                        <div class="stat-row">
                            <span class="stat-label">業績推移(直近)</span>
                            <span class="stat-val">{colorize_growth(s['growth'])}</span>
                        </div>
                        <div class="desc">{s['desc']}</div>
                    </div>
                    <div class="card-footer">
                        <a href="{s['link']}" target="_blank" class="link-btn">Kabutanで詳細を見る ↗</a>
                    </div>
                </div>
            '''
        
        content_html += '''
            </div>
        </div>
        '''
        
    final_html = html_template.replace('<!-- Nav Links -->', nav_html).replace('<!-- Content injected here -->', content_html)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)

if __name__ == '__main__':
    generate_html()
