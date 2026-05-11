from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


PDF_DIR = Path("data/raw_pdfs")


def load_and_split_pdfs():
    """
    data/raw_pdfs 폴더의 PDF 파일을 읽고,
    검색하기 좋은 작은 chunk 단위로 나누는 함수입니다.
    """

    documents = []

    for pdf_path in PDF_DIR.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_path))
        loaded_docs = loader.load()

        for doc in loaded_docs:
            doc.metadata["source_file"] = pdf_path.name

        documents.extend(loaded_docs)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    split_docs = text_splitter.split_documents(documents)

    return split_docs