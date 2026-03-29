from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader, UnstructuredMarkdownLoader
from pathlib import Path

from src.schemas.document import Document

def load_documents_from_directory(directory_path: str) -> list[Document]:
    """
    Load documents from a specified directory.
    """

    loader_mapping = {
        "**/*.txt": (TextLoader, {'encoding': 'utf-8'}),
        "**/*.md": (UnstructuredMarkdownLoader, {}),
        "**/*.pdf": (PyPDFLoader, {}),
    }

    all_documents: list[Document] = []

    for glob_pattern, (loader_cls, loader_kwargs) in loader_mapping.items():
        try:
            loader = DirectoryLoader(
                directory_path,
                glob=glob_pattern,
                loader_cls=loader_cls,
                loader_kwargs=loader_kwargs,
                show_progress=True
            )

            lc_documents = loader.load()

            for doc in lc_documents:
                source = doc.metadata.get('source', 'Unknown')

                extracted_title = Path(source).stem if source != 'Unknown' else 'Untitled'

                document = Document(
                    title=extracted_title,
                    content=doc.page_content,
                    metadata=doc.metadata
                )
                all_documents.append(document)
                print(f"Loaded file: {document.title}.")

        except Exception as e:
            print(f"Loading Errors: {glob_pattern}: {e}")

    print(f"Loaded {len(all_documents)} documents from {directory_path}.")
    return all_documents

if __name__ == "__main__":
    directory_path = "/Users/bachng/Coding/Multi-Agent-Customer-Support-System/docs"  # Update this path to your documents directory
    documents = load_documents_from_directory(directory_path)