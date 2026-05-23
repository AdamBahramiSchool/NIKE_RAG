from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore


class vectorstore:
    def __init__(self, embedding_model, data_chunks: list[Document]):
        self.embedding_model = embedding_model
        self.data_chunks = data_chunks
        self.vector_store = self.initialize_in_mem_vector_store()

    def initialize_in_mem_vector_store(self) -> InMemoryVectorStore:
        store = InMemoryVectorStore(self.embedding_model)
        store.add_documents(self.data_chunks)
        return store
