#!/usr/bin/env python3
import os
import sys
import re

def clean_filename(name):
    # ファイル名に使用できない・不適切な文字を置換
    # Windows/Mac/Linux共通で安全な文字のみ残す
    name = re.sub(r'[\\/*?:"<>|｜\s]', '_', name)
    return name.strip('_')

def split_markdown(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
        
    # 出力先ディレクトリの決定
    dir_name, file_name = os.path.split(filepath)
    base_name, _ = os.path.splitext(file_name)
    output_dir = os.path.join(dir_name, f"{base_name}_chapters")
    os.makedirs(output_dir, exist_ok=True)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = content.split('\n')
    
    current_chapter_lines = []
    current_chapter_title = "00_タイトル"
    chapter_count = 0
    
    def write_chapter(title, lines_to_write):
        if not lines_to_write:
            return
        # タイトルからファイル名を生成
        clean_title = clean_filename(title)
        filename = f"{clean_title}.md"
        out_path = os.path.join(output_dir, filename)
        with open(out_path, 'w', encoding='utf-8') as out_f:
            out_f.write('\n'.join(lines_to_write))
        print(f"Created: {out_path}")

    for line in lines:
        # 【章タイトル：...】 のパターンを検出
        match = re.search(r'【章タイトル：(.*?)】', line)
        if match:
            # 既存の章があれば書き出す
            if current_chapter_lines:
                write_chapter(current_chapter_title, current_chapter_lines)
                current_chapter_lines = []
            
            # 新しい章の開始
            chapter_count += 1
            chapter_name = match.group(1)
            current_chapter_title = f"{chapter_count:02d}_{chapter_name}"
            current_chapter_lines.append(line)
        else:
            current_chapter_lines.append(line)
            
    # 最後の章を書き出す
    if current_chapter_lines:
        write_chapter(current_chapter_title, current_chapter_lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: split-chapters <markdown_file_path>")
        sys.exit(1)
    split_markdown(sys.argv[1])
