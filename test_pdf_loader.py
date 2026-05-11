from collections import Counter

from app.rag.pdf_loader import load_and_split_pdfs


def main():
    split_docs = load_and_split_pdfs()

    print("생성된 chunk 개수:")
    print(len(split_docs))

    print("\nPDF별 chunk 개수:")
    source_counter = Counter(
        doc.metadata.get("source_file", "unknown")
        for doc in split_docs
    )

    for source_file, count in source_counter.items():
        print(f"{source_file}: {count}개")

    print("\n첫 번째 chunk 내용:")
    print(split_docs[0].page_content[:500])

    print("\n첫 번째 chunk metadata:")
    print(split_docs[0].metadata)


if __name__ == "__main__":
    main()