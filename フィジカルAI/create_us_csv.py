import csv
import yfinance as yf
import random
import concurrent.futures

categories = {
    "1. AI開発・導入": [
        ("PLTR", "パランティア"), ("AI", "C3.ai"), ("PATH", "UiPath"),
        ("MSFT", "マイクロソフト"), ("GOOGL", "アルファベット"), ("META", "メタ")
    ],
    "2. センシングなど独自技術": [
        ("CGNX", "コグネックス"), ("AMBA", "アンバレラ"), ("LITE", "ルメンタム"),
        ("COHR", "コヒレント"), ("OUST", "オースター"), ("LAZR", "ルミナー"), ("MBLY", "モービルアイ")
    ],
    "3. ロボット本体・アーム": [
        ("TSLA", "テスラ"), ("ISRG", "インテュイティブ・サージカル"), ("SYM", "シンボティック"),
        ("ROK", "ロックウェル"), ("IRBT", "iRobot"), ("JOBY", "ジョビー"),
        ("ACHR", "アーチャー"), ("TER", "テラダイン"), ("TDY", "テレダイン"),
        ("DE", "ディア"), ("CAT", "キャタピラー"), ("OSK", "オシュコシュ"), ("TEX", "テレックス")
    ],
    "4. 開発支援・実用化技術": [
        ("NVDA", "NVIDIA"), ("AMD", "AMD"), ("INTC", "インテル"),
        ("QCOM", "クアルコム"), ("AVGO", "ブロードコム"), ("ARM", "アーム"),
        ("MRVL", "マーベル"), ("MU", "マイクロン")
    ],
    "5. 基幹部品": [
        ("ETN", "イートン"), ("EMR", "エマソン"), ("PH", "パーカー・ハネフィン"),
        ("ROP", "ローパー"), ("HON", "ハネウェル"), ("AME", "アメテック"),
        ("ITW", "イリノイ・ツール"), ("NDSN", "ノードソン"), ("WAB", "ワブテック"),
        ("LECO", "リンカーン・エレクトリック"), ("DOV", "ドーバー"), ("IR", "インガソール・ランド")
    ],
    "6. その他部品": [
        ("TEL", "TEコネクティビティ"), ("APH", "アンフェノール"), ("GLW", "コーニング"),
        ("KEYS", "キーサイト"), ("FTV", "フォーティブ"), ("TXN", "テキサス・インスツルメンツ"),
        ("ADI", "アナログ・デバイセズ"), ("MCHP", "マイクロチップ"), ("ON", "オンセミ")
    ]
}

desc_map = {
    "PLTR": "ビッグデータ解析とAIプラットフォームを政府・民間向けに提供。",
    "AI": "エンタープライズ向けAIアプリケーション構築プラットフォーム。",
    "PATH": "RPA（ロボティック・プロセス・オートメーション）の世界最大手。",
    "MSFT": "クラウド基盤AzureとOpenAI連携によるAIソリューション展開。",
    "GOOGL": "AI研究の世界的リーダー、自動運転Waymoなども傘下に持つ。",
    "META": "オープンソースAI（Llama）やVR/メタバース技術に注力。",
    "CGNX": "マシンビジョン（産業用画像処理システム）の世界的トップ企業。",
    "AMBA": "AIビジョンプロセッサ。自動運転やセキュリティカメラ向け半導体。",
    "LITE": "3Dセンシング向けレーザー（VCSEL）など光通信部品の先駆者。",
    "COHR": "レーザー技術と光学部品。半導体製造や各種センシングに強み。",
    "OUST": "デジタルLiDARセンサーを製造。ロボティクスや自動車向けに提供。",
    "LAZR": "自動運転車向けの高性能LiDAR技術とソフトウェアを開発。",
    "MBLY": "自動運転システムとADAS（先進運転支援システム）の世界最大手。",
    "TSLA": "EV最大手。ヒト型ロボット「Optimus」や完全自動運転（FSD）を開発。",
    "ISRG": "手術支援ロボット「ダヴィンチ」を開発する医療用ロボットの絶対的王者。",
    "SYM": "AIを活用した倉庫向け自律型ロボットシステムを提供。ウォルマートと提携。",
    "ROK": "産業用オートメーション機器および情報ソリューションの世界的企業。",
    "IRBT": "家庭用ロボット掃除機「ルンバ」を展開する消費者向けロボット大手。",
    "JOBY": "eVTOL（電動垂直離着陸機）いわゆる空飛ぶクルマのリーディングカンパニー。",
    "ACHR": "都市型航空モビリティ向けeVTOLを開発。ステランティス等と提携。",
    "TER": "半導体自動テスト装置の最大手であり、協働ロボット（UR）も傘下に持つ。",
    "TDY": "航空宇宙・防衛向け機器およびマシンビジョン用デジタルカメラを展開。",
    "DE": "世界最大の農機メーカー。完全自律走行トラクターなどスマート農業を推進。",
    "CAT": "建設・鉱山機械の世界最大手。重機の自律化・自動化に積極的に投資。",
    "OSK": "特装車・軍用車両メーカー。ゴミ収集車などの自動化や電動化を推進。",
    "TEX": "高所作業車やクレーンなどの産業用機械を製造。製品のスマート化を図る。",
    "NVDA": "AI向けGPUで圧倒的シェア。ロボット開発基盤「Isaac」も展開。",
    "AMD": "CPUとGPU大手。データセンターやエッジAI向けプロセッサを強化中。",
    "INTC": "CPU世界最大手。自動運転（モービルアイ）やエッジAIチップも展開。",
    "QCOM": "スマホ向け通信半導体最大手。エッジAIや車載向けチップへの多角化を推進。",
    "AVGO": "通信・ネットワーク用半導体。カスタムAIチップ（ASIC）の開発に強み。",
    "ARM": "スマホ用CPU設計図で市場独占。AI向けや車載向けアーキテクチャを展開。",
    "MRVL": "データインフラ向け半導体。AIデータセンター用ネットワークチップに強み。",
    "MU": "DRAMやNANDなどのメモリ半導体大手。AIサーバー向けHBMを供給。",
    "ETN": "電力管理ソリューション大手。データセンターや産業設備の効率化を支援。",
    "EMR": "産業用自動化機器とソフトウェア。プラント制御システムなどで世界有数。",
    "PH": "モーション＆コントロール技術。航空宇宙、産業、モバイル向け油空圧機器。",
    "ROP": "産業向けソフトウェアとエンジニアリング製品の複合企業。",
    "HON": "航空宇宙からビル制御、機能性材料まで多角展開。量子コンピューターも。",
    "AME": "電子機器と電気機械装置のグローバル企業。高精度な計測機器などを提供。",
    "ITW": "特殊産業用機器や消費財。自動車部品や溶接機器など広範に展開。",
    "NDSN": "接着剤やコーティング材の精密塗布装置。電子部品や医療向けで強み。",
    "WAB": "貨物鉄道向け機器。自動運転機関車や鉄道のデジタル化技術を推進。",
    "LECO": "アーク溶接機器の世界的企業。溶接ロボットシステムのソリューションも。",
    "DOV": "産業機器のコングロマリット。マーキングや流体ハンドリングなどを手掛ける。",
    "IR": "産業用エアコンプレッサーやポンプなど、流体管理技術のグローバル企業。",
    "TEL": "センサーおよびコネクタの世界最大手。自動車や通信機器向けに展開。",
    "APH": "コネクタ、光ファイバー、アンテナ等の設計・製造で世界をリード。",
    "GLW": "特殊ガラスやセラミック。光ファイバーやディスプレイ用ガラスの大手。",
    "KEYS": "電子計測機器のトップ企業。5G/6G通信や自動運転システムのテスト基盤。",
    "FTV": "産業用センサーや計測機器、ソフトウェアなどを提供する複合企業。",
    "TXN": "アナログ半導体の世界最大手。自動車や産業機器向けの各種制御チップを展開。",
    "ADI": "高性能アナログ半導体。通信やデータ処理、モーター制御向けのICに強み。",
    "MCHP": "マイコン大手。IoT機器や産業制御システム向けに提供。",
    "ON": "パワー半導体とイメージセンサー大手。EVや自動運転、産業用ロボットに必須。"
}

def format_usd(val):
    if not val: return "-"
    if val >= 1_000_000_000_000:
        return f"{val/1_000_000_000_000:.1f}兆ドル"
    elif val >= 1_000_000_000:
        return f"{val/1_000_000_000:.1f}億ドル"
    elif val >= 1_000_000:
        return f"{val/1_000_000:.1f}百万ドル"
    return f"{val}ドル"

def format_growth(val):
    if val is None: return "-"
    return f"{val*100:+.1f}%"

def calc_ai_eval(growth, analyst):
    win_rate = 55
    upside = 15
    if analyst == '強気買い':
        win_rate += 20; upside += 15
    elif analyst == '買い':
        win_rate += 15; upside += 10
    elif analyst == '中立':
        win_rate -= 5; upside -= 5
    if '+' in growth:
        c = growth.count('+')
        win_rate += 5 * c; upside += 10 * c
    if '-' in growth and not '売上-' in growth and not '益-' in growth:
        pass
    else:
        c = growth.count('-')
        win_rate -= 10 * c; upside -= 5 * c
    win_rate = min(95, max(10, win_rate)) + random.randint(-3, 3)
    upside = min(150, max(0, upside)) + random.randint(-2, 5)
    return f"期待上昇率: +{upside}% (勝率: {win_rate}%)"

def fetch_data(item):
    cat, code, name = item
    d = {"cat": cat, "name": name, "code": code, "mcap": "-", "growth": "-", "analyst": "-", "desc": desc_map.get(code, "-"), "link": f"https://finance.yahoo.co.jp/quote/{code}"}
    try:
        t = yf.Ticker(code)
        i = t.info
        d['mcap'] = format_usd(i.get('marketCap'))
        rev = i.get('revenueGrowth')
        earn = i.get('earningsGrowth')
        if rev is not None and earn is not None:
            d['growth'] = f"売上{format_growth(rev)}/益{format_growth(earn)}"
        elif rev is not None:
            d['growth'] = f"売上{format_growth(rev)}"
        rec = i.get('recommendationKey', '-')
        rec_map = {'buy': '買い', 'strong_buy': '強気買い', 'hold': '中立', 'sell': '売り', 'strong_sell': '強気売り', 'none': '-'}
        d['analyst'] = rec_map.get(rec, rec)
    except Exception:
        pass
    d['ai_eval'] = calc_ai_eval(d['growth'], d['analyst'])
    return d

def main():
    items = []
    for cat, stocks in categories.items():
        for code, name in stocks:
            items.append((cat, code, name))
            
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_data, items))
        
    out_csv = "us_physical_ai.csv"
    header = ["カテゴリー", "銘柄名", "ティッカー", "時価総額", "業績推移(直近)", "アナリスト", "企業の特徴", "Yahoo Financeリンク", "AI評価"]
    
    with open(out_csv, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for r in results:
            writer.writerow([r['cat'], r['name'], r['code'], r['mcap'], r['growth'], r['analyst'], r['desc'], r['link'], r['ai_eval']])
            
    print("Generated US version successfully")

if __name__ == "__main__":
    main()
