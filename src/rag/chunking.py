from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.schemas.document import Document
from src.schemas.chunk import Chunk


def split_text_into_chunks(documents: list[Document], chunk_size=1000, chunk_overlap=200) -> list[Chunk]:
    """
    Split the input text into chunks of specified size with overlap.
    """

    all_chunks: list[Chunk] = []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )

    for doc in documents:
        chunks = text_splitter.split_text(doc.content)
        for i, chunk_content in enumerate(chunks):
            chunk = Chunk(
                source_document=doc.title,
                content=chunk_content,
                metadata={
                    'chunk_index': i,
                    **doc.metatdata
                }
            )

            all_chunks.append(chunk)
    print(f"Splitted {len(documents)} documents into {len(all_chunks)} chunks.")
    return all_chunks

if __name__ == "__main__":
    from src.rag.ingest import load_documents_from_directory

    directory_path = "/Users/bachng/Coding/Multi-Agent-Customer-Support-System/docs"  # Update this path to your documents directory
    documents = load_documents_from_directory(directory_path)
    chunks = split_text_into_chunks(documents)
