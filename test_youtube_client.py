import asyncio
import os
from dotenv import load_dotenv
from src.utils.youtube_client import search_videos

# Load .env so we get the YOUTUBE_API_KEY
load_dotenv()

async def test():
    print("🔍 Searching for 'pranayama for beginners' videos...\n")
    results = await search_videos("pranayama for beginners", channel_ids=None, max_results=2)
    
    if not results:
        print("❌ No videos found.")
        return
    
    for i, v in enumerate(results, start=1):
        print(f"{i}. {v['title']}")
        print(f"   Channel: {v['channelTitle']}")
        print(f"   URL: {v['url']}")
        print(f"   Thumbnail: {v['thumbnail']}\n")

if __name__ == "__main__":
    asyncio.run(test())
