import os
import sys
import re
import asyncio
from pathlib import Path
import google.generativeai as genai

# HTMLファイルを生成するためのプロンプト（デザイン）変数
# ユーザーが自由に編集してデザインを変更できます
HTML_DESIGN_TEMPLATE = """あなたはプロのWebデザイナー兼アナリストです。
提供された台本から、動画の内容が一目でわかる美しいHTMLレポートを生成してください。
以下の要件に必ず従ってください。

【デザイン要件】
- モダンで洗練されたデザイン (ダークモード推奨、CSSは<style>タグに記述)
- タイトル、見出し、カードレイアウトを用いて視覚的にわかりやすく
- スマホ対応 (レスポンシブデザイン)
- 1次情報（具体的な数値、企業名、ティッカー、引用されたデータなど）をしっかり強調して載せること
- マークダウンのコードブロック(```html)は除外して、<html>から完全なコードを出力してください。
"""

async def extract_tickers_and_timeline(script_text):
    """
    台本から銘柄（ティッカー）とタイムラインを抽出する非同期関数
    """
    prompt = f"""
    以下の動画台本から、以下の2つの情報を抽出してください。
    
    1. 【銘柄リスト】: 言及されているすべての銘柄のティッカーシンボル（米国株ならアルファベット、日本株なら数字4桁など）。
    2. 【タイムライン】: 台本の流れに沿ったタイムライン（目次）の作成。動画の尺を仮に10分とし、各章の開始想定タイム（MM:SS）とタイトルを出力。
    
    出力フォーマット:
    【銘柄リスト】
    ・TICKER1
    ・TICKER2
    
    【タイムライン】
    00:00 オープニング
    01:30 第1章：〇〇
    ...
    
    台本:
    {script_text}
    """
    model = genai.GenerativeModel('gemini-2.5-pro')
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text

async def generate_html_report(script_text, output_path):
    """
    HTML_DESIGN_TEMPLATE変数を利用して、台本からHTMLファイルを非同期生成する
    """
    prompt = f"""
    {HTML_DESIGN_TEMPLATE}
    
    【台本内容】
    {script_text}
    """
    model = genai.GenerativeModel('gemini-2.5-pro')
    response = await asyncio.to_thread(model.generate_content, prompt)
    # コードブロックのマークダウン記法を取り除く
    html_content = response.text.replace('```html', '').replace('```', '').strip()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ HTMLレポートを生成しました: {output_path}")

async def process_directory(target_path):
    target = Path(target_path)
    if not target.exists():
        print(f"エラー: {target} が見つかりません。")
        return

    script_text = ""
    # ディレクトリが指定された場合、最初のマークダウンファイルを台本として読み込む
    if target.is_dir():
        md_files = list(target.glob("*.md"))
        if not md_files:
            print("エラー: ディレクトリ内にMarkdownの台本ファイルが見つかりません。")
            return
        with open(md_files[0], 'r', encoding='utf-8') as f:
            script_text = f.read()
    elif target.is_file() and target.suffix == '.md':
        with open(target, 'r', encoding='utf-8') as f:
            script_text = f.read()
        target = target.parent
    else:
        print("エラー: Markdownファイル、またはMarkdownが含まれるディレクトリを指定してください。")
        return

    print("🤖 台本を解析し、銘柄とタイムラインを抽出中...")
    extracted_info = await extract_tickers_and_timeline(script_text)
    
    # 抽出結果のパース
    tickers = []
    timeline = []
    current_section = None
    for line in extracted_info.split('\n'):
        if '【銘柄リスト】' in line:
            current_section = 'tickers'
            continue
        elif '【タイムライン】' in line:
            current_section = 'timeline'
            continue
            
        if current_section == 'tickers' and line.strip().startswith('・'):
            ticker = line.replace('・', '').strip()
            tickers.append(ticker)
        elif current_section == 'timeline' and re.match(r'\d{2}:\d{2}', line.strip()):
            timeline.append(line.strip())

    # かぶたんURLの生成 (銘柄ごと)
    kabutan_links = []
    for ticker in tickers:
        # アルファベットのみなら米国株、数字が含まれるなら日本株と判定
        if re.match(r'^[A-Za-z]+$', ticker):
            kabutan_links.append(f"- {ticker}: https://us.kabutan.jp/stocks/{ticker}/chart")
        elif re.match(r'^\d+$', ticker):
            kabutan_links.append(f"- {ticker}: https://kabutan.jp/stock/chart?code={ticker}")
        else:
            kabutan_links.append(f"- {ticker}: URL生成不可（手動でご確認ください）")

    # 概要テンプレートの読み込み
    template_path = Path("/Users/mamoru/techmoney/gaiyou.md")
    if not template_path.exists():
        template_path = Path("/Users/mamoru/techmoney/templates/formats/gaiyou.md")

    gaiyou_template = ""
    if template_path.exists():
        with open(template_path, 'r', encoding='utf-8') as f:
            gaiyou_template = f.read()
    else:
        print("⚠️ テンプレートが見つかりません。デフォルトのフォーマットを使用します。")
        gaiyou_template = "▼目次▼\n----------------------------------------------"

    # テンプレートの ▼目次▼ セクションを抽出データで置換
    timeline_str = "\n".join(timeline)
    links_str = "\n".join(kabutan_links)
    
    parts = gaiyou_template.split('▼目次▼')
    if len(parts) > 1:
        before_toc = parts[0]
        after_toc = parts[1].split('----------------------------------------------', 1)
        rest = after_toc[1] if len(after_toc) > 1 else ""
            
        new_gaiyou = (
            f"{before_toc}▼目次▼\n"
            f"{timeline_str}\n\n"
            f"▼関連銘柄のチャート（株探）▼\n"
            f"{links_str}\n\n"
            f"----------------------------------------------{rest}"
        )
    else:
        new_gaiyou = f"{gaiyou_template}\n\n▼目次▼\n{timeline_str}\n\n▼関連銘柄のチャート（株探）▼\n{links_str}"

    output_gaiyou_path = target / "generated_gaiyou.md"
    with open(output_gaiyou_path, 'w', encoding='utf-8') as f:
        f.write(new_gaiyou)
    print(f"✅ 動画概要欄を生成しました: {output_gaiyou_path}")

    # 非同期でHTMLレポートを生成
    # (ここで別の非同期タスクとして実行させているためメイン処理をブロックしません)
    print("🌐 HTMLレポートを非同期で生成中...")
    html_output_path = target / "video_summary.html"
    task = asyncio.create_task(generate_html_report(script_text, html_output_path))
    await task  # タスクの完了を待機

async def main():
    if len(sys.argv) < 2:
        print("使い方: python generate_video_gaiyou.py <ディレクトリパス または 台本Markdownファイル>")
        sys.exit(1)
        
    # Gemini APIキーの存在チェック
    if not os.environ.get("GEMINI_API_KEY"):
        print("警告: GEMINI_API_KEY 環境変数が設定されていません。")
        print("実行前にターミナルで export GEMINI_API_KEY='your_api_key' を設定してください。")
        sys.exit(1)

    target_path = sys.argv[1]
    await process_directory(target_path)

if __name__ == "__main__":
    asyncio.run(main())
