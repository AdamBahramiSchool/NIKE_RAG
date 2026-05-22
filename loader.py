from langchain_core.documents import Document
import pypdf


class loader:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.documents: list[Document] = []
        self.load_pdf_pages()

    def load_pdf_pages(self) -> list[Document]:
        reader = pypdf.PdfReader(self.pdf_path)
        self.documents = [
            Document(
                page_content=page.extract_text() or "",
                metadata={"source": self.pdf_path, "page": i},
            )
            for i, page in enumerate(reader.pages)
        ]
        self.length_of_documents()
        return self.documents

    def length_of_documents(self) -> None:
        print("# of docs:", len(self.documents))
