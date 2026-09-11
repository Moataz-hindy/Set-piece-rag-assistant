from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class RetrievalService:
    def __init__(self):
        self.vectorstore = None
        self.retriever = None

    def initialize(self):
        """Load the vector store from disk."""
        logger.info(f"Loading vector store from {settings.VECTOR_STORE_PATH}")
        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = Chroma(
            persist_directory=settings.VECTOR_STORE_PATH,
            embedding_function=embedding_model
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})
        logger.info("Vector store loaded successfully.")

    def retrieve(self, query: str):
        """Retrieve relevant documents for the given query."""
        if not self.retriever:
            raise ValueError("Retriever is not initialized.")
        docs = self.retriever.invoke(query)
        return docs

retrieval_service = RetrievalService()
