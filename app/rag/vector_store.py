from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from app.rag.pdf_loader import load_and_split_pdfs


VECTOR_DB_DIR = Path("data/vector_db/youth_housing_agent")
COLLECTION_NAME = "youth_housing_agent"


def build_vector_store():
    """
    PDF chunk를 OpenAI Embedding으로 변환한 뒤
    ChromaDB에 저장하는 함수입니다.
    """

    load_dotenv()

    split_docs = load_and_split_pdfs()

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vector_store = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=str(VECTOR_DB_DIR),
        collection_name=COLLECTION_NAME
    )

    return vector_store


def load_vector_store():
    """
    이미 저장된 ChromaDB를 다시 불러오는 함수입니다.
    """

    load_dotenv()

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vector_store = Chroma(
        persist_directory=str(VECTOR_DB_DIR),
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )

    return vector_store