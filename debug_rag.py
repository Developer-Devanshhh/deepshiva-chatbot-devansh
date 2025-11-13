from src.config import HealthcareConfig

config = HealthcareConfig()
retriever = config.rag_retriever

print("🔍 Checking retriever type:", type(retriever))

# List metadata of first few documents
print("\n📄 Fetching sample documents from vector DB...")
sample = retriever.vectorstore.get(limit=5)

for i, doc in enumerate(sample, 1):
    print(f"\n--- Document {i} ---")
    print("Metadata:", doc.metadata)
    print("Content preview:", doc.page_content[:200])
