import os
import sys
import re
import itertools
from datetime import datetime

def is_separator(line):
    line_str = line.strip()
    if not line_str:
        return False
    # 装飾線: ━, ─, - が3回以上連続
    if re.match(r'^[━─\-]+$', line_str) and len(line_str) >= 3:
        return True
    # 章タイトルメタデータ: 【...】 または （...）
    # ただしセリフ行（Speaker 1: など）は除く
    if re.match(r'^【[^】\n]+】$', line_str) and not line_str.startswith("Speaker"):
        return True
    if re.match(r'^（[^）\n]+）$', line_str) and not line_str.startswith("Speaker"):
        return True
    return False

def is_metadata_footer(line):
    line_str = line.strip()
    # 【文字数：...】 や （文字数：...） など
    if re.match(r'^【文字数：[^】\n]+】$', line_str):
        return True
    if re.match(r'^（文字数：[^）\n]+）$', line_str):
        return True
    return False

def is_chapter_trigger(line):
    line_str = line.strip()
    if not line_str:
        return False
    # セリフ行の冒頭（発言内容の開始部分）に「第X章」「最終章」「結論」「まとめ」などがある場合のみマッチ
    # 例: "Speaker 1: では第一章..." や "Speaker 2: 第二章..."
    if line_str.startswith("Speaker"):
        # 話者プレフィックス（"Speaker 1:" など）を除去した発言内容の冒頭部分を判定
        content = re.sub(r'^Speaker\s+\d+:\s*', '', line_str)
        match = re.match(r'^(では)?(第[一二三四五六七八九十\d]+章|最終章|導入|結論・まとめ)', content)
        if match:
            return True
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 split_script.py <input_file_path> [num_splits]")
        sys.exit(1)
        
    input_path = os.path.abspath(sys.argv[1])
    num_splits = 2
    if len(sys.argv) >= 3:
        try:
            num_splits = int(sys.argv[2])
        except ValueError:
            print(f"Warning: invalid split count '{sys.argv[2]}'. Using default (2).")
            
    if not os.path.exists(input_path):
        print(f"Error: file '{input_path}' not found.")
        sys.exit(1)
        
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    # Analyze and group into chapters
    header_lines = []
    chapters = []
    current_chap = []
    first_speaker_seen = False
    
    for line in lines:
        if is_metadata_footer(line):
            continue
            
        if not first_speaker_seen:
            # Check if line contains speaker prefix
            if line.strip().startswith("Speaker"):
                first_speaker_seen = True
                current_chap.append(line)
            else:
                if not is_separator(line):
                    header_lines.append(line)
        else:
            if is_separator(line):
                # End current chapter if it has content
                if any(l.strip() for l in current_chap):
                    chapters.append(current_chap)
                    current_chap = []
            elif is_chapter_trigger(line):
                # Trigger new chapter, but KEEP this line in the new chapter!
                if any(l.strip() for l in current_chap):
                    chapters.append(current_chap)
                current_chap = [line]
            else:
                current_chap.append(line)
                
    if any(l.strip() for l in current_chap):
        chapters.append(current_chap)
        
    if not chapters:
        print("Error: Could not identify any chapters or dialog contents.")
        sys.exit(1)
        
    # Format chapters
    formatted_chapters = []
    # For chap1, prepend header_lines
    chap1_content = "".join(header_lines).strip() + "\n\n" + "".join(chapters[0]).strip()
    formatted_chapters.append(chap1_content)
    
    for chap in chapters[1:]:
        formatted_chapters.append("".join(chap).strip())
        
    # Output Dir name: [topic]+[YYYYMMDD]
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    today_str = datetime.now().strftime("%Y%m%d")
    output_dir_name = f"{base_name}+{today_str}"
    output_dir = os.path.join(os.path.dirname(input_path), output_dir_name)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Write chap files
    for i, content in enumerate(formatted_chapters):
        chap_file = os.path.join(output_dir, f"chap{i+1}.md")
        with open(chap_file, "w", encoding="utf-8") as f:
            f.write(content + "\n")
        print(f"Created chapter file: {chap_file}")
        
    # Divide chapters into num_splits parts optimally
    # Let's find the best split points to minimize the variance of group sizes (character count)
    chap_lens = [len(content) for content in formatted_chapters]
    n_chaps = len(formatted_chapters)
    
    if num_splits > n_chaps:
        num_splits = n_chaps
        print(f"Adjusted splits count to {num_splits} because it exceeds chapter count.")
        
    # We want to find M-1 split points in range [1, n_chaps-1]
    # Represented as indices of chapter list where each group starts.
    # Group 1: formatted_chapters[0 : p1]
    # Group 2: formatted_chapters[p1 : p2]
    # ...
    # Group M: formatted_chapters[p_{M-1} : n_chaps]
    # There are combinations of choosing M-1 split points from n_chaps-1 points.
    best_split = None
    min_score = float('inf')
    
    # generate all possible split points
    possible_points = list(range(1, n_chaps))
    for splits in itertools.combinations(possible_points, num_splits - 1):
        # splits is a tuple like (p1, p2, ...)
        indices = [0] + list(splits) + [n_chaps]
        group_sizes = []
        for j in range(len(indices) - 1):
            start = indices[j]
            end = indices[j+1]
            group_size = sum(chap_lens[start:end])
            group_sizes.append(group_size)
            
        # Score = max(group_sizes) - min(group_sizes)
        score = max(group_sizes) - min(group_sizes)
        if score < min_score:
            min_score = score
            best_split = indices
            
    if best_split is None:
        # Fallback to simple bucket division if search fails
        best_split = [0] + [int(n_chaps * k / num_splits) for k in range(1, num_splits)] + [n_chaps]
        
    # Write combined script files
    for idx in range(num_splits):
        start = best_split[idx]
        end = best_split[idx+1]
        group_chaps = formatted_chapters[start:end]
        combined_content = "\n\n---\n\n".join(group_chaps) + "\n"
        
        script_file = os.path.join(output_dir, f"台本{idx+1}.md")
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(combined_content)
        print(f"Created script file: {script_file} (combining chapters {list(range(start+1, end+1))})")
        
if __name__ == "__main__":
    main()
