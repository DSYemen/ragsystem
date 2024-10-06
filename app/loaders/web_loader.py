from langchain_community.document_loaders import WebBaseLoader, YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import config
from app.config import settings
from urllib.parse import urlparse
from app.utils.github_fun import GithubFileLoader_folder, GithubFileLoader_singleFile, GithubFileLoader_listFiles

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)


def load_from_url(url: str):
    parsed_url = urlparse(url)

    if "github.com" in parsed_url.netloc:
        loader = GithubFileLoader_singleFile(url).load_and_split(text_splitter)
    elif "youtube.com" in parsed_url.netloc or "youtu.be" in parsed_url.netloc:
        loader = YoutubeLoader.from_youtube_url(
            url, add_video_info=True).load_and_split(text_splitter)
    else:
        loader = WebBaseLoader(url).load_and_split(text_splitter)

    documents = loader

    return documents
