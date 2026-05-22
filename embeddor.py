import os

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings


load_dotenv("./.env")


class embeddor:
    def __init__(self, data_chunks: list[Document], model: str = "text-embedding-3-small"):
        self.data_chunks = data_chunks
        self.embeddings_model = self.initialize_model(model)

    def initialize_model(self, model: str) -> OpenAIEmbeddings:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing. Add it to .env")
        return OpenAIEmbeddings(model=model, api_key=api_key)

    def embed_query(self, query: str) -> list[float]:
        return self.embeddings_model.embed_query(query)
