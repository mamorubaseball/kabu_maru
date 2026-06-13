---
name: fetch-youtube-stats
description: YouTube Data APIを使用して、指定したチャンネルの登録者数や総再生回数などの統計情報を取得します。
---

# YouTube Stats Fetcher

このスキルは、YouTube Data API v3 を使用してチャンネルの登録者数などの統計情報を取得します。

## 実行手順

1. **環境変数の確認**
   `.env` ファイルに `YOUTUBE_API_KEY` が設定されているか確認してください。

2. **スクリプトの実行**
   `fetch_youtube_stats.py` を実行して、データを取得します。

   ```bash
   python fetch_youtube_stats.py
   ```
   // turbo

3. **データの活用**
   取得したデータは標準出力されるか、指定されたJSONファイルに保存されます。
