from langchain_community.document_loaders import WebBaseLoader,  GithubFileLoader, YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import settings
from urllib.parse import urlparse

def load_from_url(url: str):
    parsed_url = urlparse(url)
    
    if "github.com" in parsed_url.netloc:
        loader =  GithubFileLoader(clone_url=url, branch="main")
    elif "youtube.com" in parsed_url.netloc or "youtu.be" in parsed_url.netloc:
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
    else:
        loader = WebBaseLoader(url)
    
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap
    )
    split_docs = text_splitter.split_documents(documents)
    
    return split_docs