---
name: design
description: TechMoney ブログ記事 HTML デザインガイド
---

# TechMoney ブログ記事 HTML デザインガイド

## 概要
台本（.mdファイル）からブログ公開用のHTMLファイルを生成する際のデザイン仕様書。
すべての記事で統一されたビジュアルとUXを保つこと。

---

## カラーパレット

```css
:root {
    --bg-dark: #050510;
    --bg-gradient: linear-gradient(180deg, #0a0a1a 0%, #050510 100%);
    --primary: #00f2fe;        /* メインアクセント: シアン */
    --secondary: #4facfe;      /* サブアクセント: ブルー */
    --accent: #b06ab3;         /* 強調アクセント: パープル */
    --text-main: #ffffff;
    --text-muted: #a0a0b0;
    --card-bg: rgba(255, 255, 255, 0.03);
    --card-border: rgba(255, 255, 255, 0.08);
}
```

## タイポグラフィ

- **フォント**: `'Inter', 'Noto Sans JP', sans-serif`
- **Google Fonts URL**: `https://fonts.googleapis.com/css2?family=Inter:wght@300;500;800&family=Noto+Sans+JP:wght@300;500;700;900&display=swap`
- **h1**: 2.8〜3.5rem, font-weight: 900, グラデーション文字 (primary → accent)
- **h2**: 1.8rem, font-weight: 800, 左ボーダー付き（primary色, 4px）
- **h3**: 1.3rem, font-weight: 700
- **本文**: 1rem, line-height: 1.7, color: var(--text-muted)
- **強調テキスト**: color: var(--text-main) or var(--primary)

## レイアウト

- **最大幅**: 1100px, margin: 0 auto
- **パディング**: 左右 2rem
- **セクション間**: margin-bottom: 80px
- **レスポンシブ**: max-width: 768px でフォントサイズ・パディング縮小

## カードコンポーネント

```css
.card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 30px;
    backdrop-filter: blur(10px);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
    border-color: rgba(0, 242, 254, 0.25);
}
```

## ヘッダー

- パディング: 上120px 下80px
- テキスト中央揃え
- h1はグラデーション文字（`-webkit-background-clip: text`）
- サブタイトル: 1.2rem, var(--text-muted)

## 記事構造（HTML テンプレート）

```
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{記事の要約}">
  <title>{記事タイトル} - TechMoney</title>
  <!-- Google Fonts -->
  <!-- CSS Variables & Styles -->
</head>
<body>
  <div class="container">
    <header>
      <h1>{記事タイトル}</h1>
      <p class="subtitle">{サブタイトル・日付}</p>
    </header>

    <nav class="toc">
      <!-- 目次（台本の章構成から自動生成） -->
    </nav>

    <main>
      <section id="chapter-1">
        <h2>{章タイトル}</h2>
        <div class="card">{本文}</div>
      </section>
      <!-- 以降の章を繰り返し -->
    </main>

    <footer>
      <p class="disclaimer">※ 情報提供目的であり、投資助言ではありません。</p>
      <p class="copyright">© TechMoney</p>
    </footer>
  </div>
</body>
</html>
```

## アニメーション

- **カードホバー**: translateY(-4px) + box-shadow
- **フェードイン**: `@keyframes fadeInUp` で各セクションを下からフェードイン
- **ボーダーグロー**: ホバー時に border-color を primary に変化

```css
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
```

## 重要な銘柄・数値のスタイル

- **ティッカーシンボル**: `<span class="ticker">CBRS</span>` → color: var(--primary), font-weight: 700
- **数値ハイライト**: `<span class="highlight">+68%</span>` → color: var(--primary), font-size: 1.1em
- **リスク警告**: background: rgba(255, 100, 100, 0.1), border-left: 4px solid #ff6464

## レスポンシブ対応

```css
@media (max-width: 768px) {
    h1 { font-size: 2rem; }
    h2 { font-size: 1.4rem; }
    header { padding: 80px 0 50px; }
    .container { padding: 0 1rem; }
    .card { padding: 20px; }
}
```

## WordPress / ブログ公開向けの注意

- CSSはすべて `<style>` タグ内にインライン化すること（外部CSSファイルに依存しない）
- JavaScriptは最小限に。なくても機能するデザインにすること
- Google Fontsの `<link>` タグはそのまま `<head>` 内に記述してOK
- 画像は絶対パスまたはBase64エンコードで埋め込むこと
