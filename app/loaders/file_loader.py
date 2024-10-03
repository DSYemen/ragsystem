from langchain_unstructured import UnstructuredLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import settings
import tempfile
import os

def load_and_process_file(content: bytes, filename: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    try:
        loader = UnstructuredLoader(temp_file_path)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        split_docs = text_splitter.split_documents(documents)
        
        return split_docs
    finally:
        os.unlink(temp_file_path)

def is_supported_file(filename: str) -> bool:
    supported_extensions = ['.txt', '.md', '.pdf', '.docx', '.html']
    return any(filename.lower().endswith(ext) for ext in supported_extensions)