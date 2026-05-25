import sys
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

from src.psychology.knowledge_base import PsychologyKnowledgeBase

def main():
    print("🚀 Membuat / Update Knowledge Base...")
    kb = PsychologyKnowledgeBase()
    kb.add_documents("data/knowledge")
    print("✅ Knowledge Base berhasil dibuat!")

if __name__ == "__main__":
    main()