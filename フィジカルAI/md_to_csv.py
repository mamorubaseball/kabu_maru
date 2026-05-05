import csv
import re

md_file = "/Users/mamoru/kabu_maru/フィジカルAI/matome_new.md"
csv_file = "/Users/mamoru/kabu_maru/フィジカルAI/matome_new.csv"

with open(md_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

data = []
header = ["カテゴリー", "銘柄名", "証券コード", "時価総額", "業績推移(直近)", "アナリスト", "企業の特徴", "株探リンク"]

current_category = ""
for line in lines:
    line = line.strip()
    if line.startswith("## "):
        current_category = line[3:].strip()
    elif line.startswith("|") and not line.startswith("| :---") and not line.startswith("| 銘柄名"):
        parts = [p.strip() for p in line.split('|')[1:-1]]
        if len(parts) >= 7:
            name = parts[0].replace('**', '')
            code = parts[1]
            mcap = parts[2]
            growth = parts[3]
            analyst = parts[4]
            desc = parts[5]
            
            # Extract URL from markdown link [Text](URL) or raw text
            link_match = re.search(r'\]\((.*?)\)', parts[6])
            link = link_match.group(1) if link_match else parts[6]
            
            data.append([current_category, name, code, mcap, growth, analyst, desc, link])

with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)

print(f"CSV converted successfully: {csv_file}")
