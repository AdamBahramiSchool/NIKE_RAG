from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class chunker:
    def __init__(self, docs: list[Document]):
        self.docs = docs
        self.chunked_data: list[Document] = []
        self.chunk_documents()

    def chunk_documents(self) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
        )
        self.chunked_data = text_splitter.split_documents(self.docs)
        return self.chunked_data
