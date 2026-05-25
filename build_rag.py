from src.psychology.knowledge_base import PsychologyKnowledgeBase

def main():
    print("🚀 Membuat / Update Knowledge Base...")
    kb = PsychologyKnowledgeBase()
    kb.add_documents("data/knowledge")
    print("✅ Knowledge Base berhasil dibuat!")

if __name__ == "__main__":
    main()