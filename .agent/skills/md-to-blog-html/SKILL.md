---
name: md-to-blog-html
description: MD→HTML ブログ記事生成ワークフロー
---

# MD→HTML ブログ記事生成ワークフロー

## 概要
`/Users/mamoru/techmoney/{month}/` 配下のディレクトリにある台本（.mdファイル）を読み込み、
`design.md` のデザインガイドに準拠した統一デザインのHTMLブログ記事を生成するワークフロー。

## 実行方法

### 単一ディレクトリの場合
```
以下の手順でHTMLブログ記事を生成してください:

1. 対象ディレクトリ: /Users/mamoru/techmoney/{month}/{directory_name}/
2. 台本ファイル: {directory_name}.md（ディレクトリ名と同名のmdファイル）
3. デザインガイド: /Users/mamoru/techmoney/.agent/workflow/design.md を読み込み、それに準拠したHTMLを生成
4. 出力先: 同ディレクトリ内に blog_{directory_name}.html として保存
```

### 月単位で一括生成する場合
```
/Users/mamoru/techmoney/{month}/ 配下のすべてのディレクトリを走査し、
各ディレクトリ名と一致する.mdファイルからHTMLブログ記事を一括生成してください。
デザインは /Users/mamoru/techmoney/.agent/workflow/design.md に準拠すること。
```

## 処理フロー

```mermaid
graph TD
    A[月ディレクトリを指定] --> B[配下のサブディレクトリを走査]
    B --> C{ディレクトリ名.md が存在するか?}
    C -->|Yes| D[台本ファイルを読み込み]
    C -->|No| E[スキップ]
    D --> F[design.md のガイドを適用]
    F --> G[Speaker形式の台本を記事構造に変換]
    G --> H[HTMLファイルを生成]
    H --> I[blog_{name}.html として保存]
```

## 変換ルール

### 台本 → 記事への変換
1. **Speaker 1 の発言** → 記事の本文として採用
2. **Speaker 2 の発言** → 記事には含めない（相槌・リアクションのため）
3. **「第X章」のパターン** → `<section>` と `<h2>` に変換
4. **銘柄名・ティッカー** → `<span class="ticker">` でマークアップ
5. **数値データ** → `<span class="highlight">` でマークアップ

### 必須要素
- `<meta description>` : 台本の冒頭から自動生成
- 目次（Table of Contents）: 章構成から自動生成
- 免責事項（Footer）: 投資助言ではない旨を必ず記載
- レスポンシブ対応: `design.md` のブレークポイントに準拠

## ディレクトリ構造（出力例）

```
techmoney/
  5月/
    spaceX+20260506/
      spaceX.md              ← 入力（台本）
      blog_spaceX.html       ← 出力（ブログ記事）
    google決算+20260501/
      google決算.md           ← 入力（台本）
      blog_google決算.html    ← 出力（ブログ記事）
```

## 注意事項
- 既にHTMLファイルが存在する場合は上書き確認を行うこと
- chapX.md は個別チャプターファイルであり、変換対象は「ディレクトリ名.md」のみ
- design.md を変更すれば、以降生成されるすべてのHTMLに反映される
