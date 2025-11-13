import asyncio
from src.config import HealthcareConfig
from src.chains.specialized_chains import YogaChain

async def main():
    print("🧘 Testing Yoga Agent directly...\n")

    # Initialize config and retriever
    config = HealthcareConfig()
    llm = config.llm
    retriever = config.rag_retriever

    # Create YogaChain instance
    yoga_agent = YogaChain(llm, retriever)

    # 🔍 Query examples
    queries = [
        "suggest me some yoga for back pain",
        "what yoga helps in anxiety",
        "show breathing exercises for stress relief"
    ]

    for q in queries:
        print(f"\n💬 Query: {q}")
        result = await yoga_agent.run_async(q)

        print("\n🧩 Yoga Agent Response:")
        print("Text:", result["text"][:500], "...\n")  # Show first 500 chars
        if result["video"]:
            print("🎥 Video Title:", result["video"]["title"])
            print("Channel:", result["video"]["channelTitle"])
            print("URL:", result["video"]["url"])
            print("Thumbnail:", result["video"]["thumbnail"])
        else:
            print("⚠️ No video found.")

if __name__ == "__main__":
    asyncio.run(main())
