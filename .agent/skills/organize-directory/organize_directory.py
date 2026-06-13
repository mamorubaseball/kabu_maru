import os
import shutil
import glob
import re
from pathlib import Path

# 対象となるルートディレクトリ
ROOT_DIR = Path("/Users/mamoru/techmoney")

# 作成するディレクトリ構造
TARGET_DIRS = {
    "images": ROOT_DIR / "assets" / "images",
    "docs": ROOT_DIR / "assets" / "docs",
    "prompts": ROOT_DIR / "templates" / "prompts",
    "formats": ROOT_DIR / "templates" / "formats",
    "scripts": ROOT_DIR / "scripts_draft",
}

# 移動してはいけないファイル
EXCLUDE_FILES = ["rules.md", "ディレクトリ構造.md", "README.md"]

def setup_directories():
    """必要なディレクトリを作成する"""
    for dir_path in TARGET_DIRS.values():
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 ディレクトリを確認/作成しました: {dir_path.relative_to(ROOT_DIR)}")

def move_files():
    """ルールに従ってファイルを移動する"""
    moved_count = 0
    
    # 1. 画像ファイルの移動
    for ext in ['*.jpeg', '*.jpg', '*.png', '*.webp']:
        for file_path in ROOT_DIR.glob(ext):
            shutil.move(str(file_path), str(TARGET_DIRS["images"] / file_path.name))
            print(f"🖼️ 画像を移動しました: {file_path.name} -> assets/images/")
            moved_count += 1

    # 2. ドキュメント(PDF, DOCX)の移動
    for ext in ['*.pdf', '*.docx']:
        for file_path in ROOT_DIR.glob(ext):
            shutil.move(str(file_path), str(TARGET_DIRS["docs"] / file_path.name))
            print(f"📄 ドキュメントを移動しました: {file_path.name} -> assets/docs/")
            moved_count += 1

    # 3. テンプレート・MDファイルの移動
    for file_path in ROOT_DIR.glob('*.md'):
        if file_path.name in EXCLUDE_FILES:
            continue
        
        name_lower = file_path.name.lower()
        if 'prompt' in name_lower:
            shutil.move(str(file_path), str(TARGET_DIRS["prompts"] / file_path.name))
            print(f"📝 プロンプトを移動しました: {file_path.name} -> templates/prompts/")
        elif 'gaiyou' in name_lower or 'design' in name_lower:
            shutil.move(str(file_path), str(TARGET_DIRS["formats"] / file_path.name))
            print(f"📋 フォーマットを移動しました: {file_path.name} -> templates/formats/")
        else:
            shutil.move(str(file_path), str(TARGET_DIRS["scripts"] / file_path.name))
            print(f"✍️ 台本草稿を移動しました: {file_path.name} -> scripts_draft/")
        moved_count += 1
        
    # 4. name+YYYYMMDD 形式のファイル/ディレクトリの移動
    pattern = re.compile(r'.*\+20\d{6}$')
    for path in ROOT_DIR.iterdir():
        if pattern.match(path.name):
            # 末尾から8文字目〜3文字目(YYYYMM)を取得
            yyyymm = path.name[-8:-2]
            target_month_dir = ROOT_DIR / f"{yyyymm}"
            target_month_dir.mkdir(exist_ok=True)
            
            shutil.move(str(path), str(target_month_dir / path.name))
            print(f"📦 プロジェクトを移動しました: {path.name} -> {yyyymm}/")
            moved_count += 1
            
    return moved_count

def main():
    print("🚀 ディレクトリ整理ツールを開始します...")
    setup_directories()
    count = move_files()
    print(f"✨ 整理完了！合計 {count} 個のファイルを適切なディレクトリに移動しました。")
    print("ディレクトリ構造.md のルールに従ってルートディレクトリがクリーンになりました。")

if __name__ == "__main__":
    main()
