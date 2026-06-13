import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

def fetch_youtube_stats():
    # Load .env from the root of the project
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    env_path = os.path.join(project_root, ".env")
    load_dotenv(dotenv_path=env_path)

    API_KEY = os.getenv("YOUTUBE_API_KEY")
    CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")

    if not API_KEY or not CHANNEL_ID:
        print("Error: YOUTUBE_API_KEY and YOUTUBE_CHANNEL_ID must be set in .env")
        return

    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={CHANNEL_ID}&key={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if "items" not in data or len(data["items"]) == 0:
            print(f"Error: Channel with ID {CHANNEL_ID} not found.")
            return
            
        stats = data["items"][0]["statistics"]
        
        result = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "subscriberCount": int(stats.get("subscriberCount", 0)),
            "viewCount": int(stats.get("viewCount", 0)),
            "videoCount": int(stats.get("videoCount", 0))
        }
        
        print("Current YouTube Stats:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Save to history file in the project root's data directory
        data_dir = os.path.join(project_root, "data")
        os.makedirs(data_dir, exist_ok=True)
        filename = os.path.join(data_dir, "youtube_stats_history.json")
        
        history = []
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                history = json.load(f)
                
        # Append only if date doesn't already exist to avoid duplicates for the same day
        if not any(entry.get("date") == result["date"] for entry in history):
            history.append(result)
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            print(f"✅ Data saved and appended to {filename}")
        else:
            print(f"ℹ️ Data for {result['date']} already exists in {filename}. Not appending.")
        
    except Exception as e:
        print(f"Failed to fetch YouTube stats: {e}")

if __name__ == "__main__":
    fetch_youtube_stats()
