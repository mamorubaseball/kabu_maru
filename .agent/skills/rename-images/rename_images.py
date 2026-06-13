import os
import glob
import time
import google.generativeai as genai

def rename_images():
    image_dir = "/Users/mamoru/techmoney/画像"
    images = glob.glob(os.path.join(image_dir, "*.jpeg"))
    
    # UUIDっぽい名前（ハイフンが含まれていて長いもの）を抽出
    images_to_rename = [img for img in images if len(os.path.basename(img)) > 20 and '-' in os.path.basename(img)]
    
    if not images_to_rename:
        print("変更が必要なUUID形式の画像は見つかりませんでした。")
        return

    print(f"{len(images_to_rename)}件の画像の名前をAIで判定して変更します...")
    
    # 環境変数からAPIキーを取得
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
    else:
        # 見つからない場合は.envファイルを探すか、ユーザーに設定を促す
        print("⚠️ GEMINI_API_KEYが設定されていません。")
        print("ターミナルで `export GEMINI_API_KEY='あなたのAPIキー'` を実行するか、スクリプトに直接設定してください。")
        return

    model = genai.GenerativeModel('gemini-1.5-flash')
    
    for img_path in images_to_rename:
        try:
            print(f"アップロード＆解析中: {os.path.basename(img_path)}")
            sample_file = genai.upload_file(path=img_path)
            
            prompt = "この画像の内容を端的に表す、日本語のファイル名を考えてください。拡張子(.jpeg)を含めて、空白なしの出力にしてください。例: 宇宙船の打ち上げ.jpeg, 株価チャート_上昇.jpeg"
            response = model.generate_content([prompt, sample_file])
            new_name = response.text.strip().replace("```", "").strip()
            
            # クリーンアップとサニタイズ
            new_name = new_name.replace(" ", "_").replace("/", "／").replace("\n", "")
            if not new_name.endswith(".jpeg"):
                new_name += ".jpeg"
                
            new_path = os.path.join(image_dir, new_name)
            
            # 既存のファイル名と被る場合は連番をつける
            counter = 1
            while os.path.exists(new_path):
                name, ext = os.path.splitext(new_name)
                new_path = os.path.join(image_dir, f"{name}_{counter}{ext}")
                counter += 1
                
            os.rename(img_path, new_path)
            print(f"✅ 名前を変更しました: {os.path.basename(img_path)} -> {os.path.basename(new_path)}")
            
            # APIのファイルクリーンアップ
            genai.delete_file(sample_file.name)
            
            # API制限対策の待機
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ エラーが発生しました ({os.path.basename(img_path)}): {e}")

if __name__ == "__main__":
    rename_images()
