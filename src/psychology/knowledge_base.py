import os
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from src.config.settings import settings

class PsychologyKnowledgeBase:
    def __init__(self):
        self.persist_directory = "data/vectorstore"
        
        # Model embedding yang benar (update 2026)
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",   # ← Ini yang benar
            google_api_key=settings.GEMINI_API_KEY,
            task_type="RETRIEVAL_DOCUMENT"
        )
        
        self.vectorstore = None
        self.load_or_create()

    def load_or_create(self):
        """Load vectorstore jika sudah ada"""
        if os.path.exists(self.persist_directory) and any(os.scandir(self.persist_directory)):
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        else:
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )

    def add_documents(self, documents_path: str = "data/knowledge"):
        """Tambahkan dokumen ke vectorstore"""
        loader = DirectoryLoader(
            documents_path,
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        )
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=120
        )
        splits = text_splitter.split_documents(documents)

        if not splits:
            print("⚠️ Tidak ada dokumen ditemukan di folder data/knowledge")
            return

        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
        else:
            self.vectorstore.add_documents(splits)

        print(f"✅ Berhasil menambahkan {len(splits)} chunk ke knowledge base.")

    def retrieve(self, query: str, k: int = 4):
        """Retrieve dokumen relevan"""
        if not self.vectorstore:
            return []

        docs = self.vectorstore.similarity_search_with_score(query, k=k*2)
        
        # Filter hanya dokumen dengan skor bagus
        filtered = [doc for doc, score in docs if score < 0.8]
        return [doc.page_content for doc in filtered[:k]]