---
name: split-script
description: 台本Markdownファイルを章ごとに分割し、最適な文字数で2〜3分割した結合台本ファイルを自動生成するスキル
---

# split-script

台本Markdownファイルを解析し、自動で各章（`chap1.md`〜`chapX.md`）に分割したうえで、指定された分割数（デフォルトは2）に最適にマージした台本ファイル（`台本1.md`〜`台本Y.md`）を生成します。

## 実行方法

Pythonスクリプトに、対象の台本ファイルと分割数を指定して実行します。

```bash
python3 /Users/mamoru/techmoney/.agent/skills/split-script/split_script.py <台本Markdownのパス> [分割数]
```

### 例: 2分割する場合
```bash
python3 /Users/mamoru/techmoney/.agent/skills/split-script/split_script.py /Users/mamoru/techmoney/naddaq100.md 2
```

### 例: 3分割する場合
```bash
python3 /Users/mamoru/techmoney/.agent/skills/split-script/split_script.py /Users/mamoru/techmoney/naddaq100.md 3
```

## 出力結果
台本ファイルと同じ場所に、`[台本名]+[今日の日付]` の新規ディレクトリ（例: `naddaq100+20260606`）が作成され、その中に以下のファイルが出力されます。
- `chap1.md` 〜 `chapX.md` (章ごとの分割ファイル。不要なデコレーションや文字数フッターは自動除去)
- `台本1.md` 〜 `台本Y.md` (各グループの文字数が均等になるように最適に結合された台本ファイル。チャプター間は `---` で接続)
