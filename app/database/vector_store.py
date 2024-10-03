# from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_community.vectorstores import SupabaseVectorStore, FAISS, Chroma, Pinecone as PineconeVectorStore, Milvus
from supabase.client import create_client
# from langchain_milvus import Milvus
from langchain_elasticsearch import ElasticsearchStore
from app.config import settings
from app.embeddings.embeddings import get_embedding_model


def get_vector_store():
    embeddings = get_embedding_model()
    try:

        vector_store_config = {
            "pinecone":
            lambda: PineconeVectorStore(
                Pinecone(api_key=settings.vector_db_api_key).Index(
                    settings.vector_db_index_name), embeddings.embed_query,
                "text"),
            "qdrant":
            lambda: QdrantVectorStore(
                client=QdrantClient(url=settings.vector_db_url,
                                    api_key=settings.vector_db_api_key),
                collection_name=settings.vector_db_collection,
                embeddings=embeddings),
            "supabase":
            lambda: SupabaseVectorStore(create_client(
                settings.vector_db_url, settings.vector_db_api_key),
                                        embeddings,
                                        table_name=settings.vector_db_table),
            "milvus":
            lambda: Milvus(connection_args={
                "host": settings.vector_db_host,
                "port": settings.vector_db_port
            },
                           collection_name=settings.vector_db_collection,
                           embedding_function=embeddings),
            "elasticsearch":
            lambda: ElasticsearchStore(es_url=settings.vector_db_url,
                                       index_name=settings.
                                       vector_db_index_name,
                                       embedding=embeddings),
            "faiss":
            lambda: FAISS.from_documents([], embeddings),
            "chroma":
            lambda: Chroma(persist_directory=settings.
                           vector_db_persist_directory,
                           embedding_function=embeddings),
        }

        if settings.vector_db_provider not in vector_store_config:
            raise ValueError(
                f"مزود قاعدة البيانات المتجهية غير مدعوم: {settings.vector_db_provider}"
            )

        return vector_store_config[settings.vector_db_provider]()
    except KeyError:
        raise ValueError(
            f"مزود قاعدة البيانات المتجهية غير مدعوم: {settings.vector_db_provider}"
        )
    except Exception as e:
        raise ValueError(f"حدث خطأ أثناء إنشاء قاعدة البيانات المتجهية: {e}")


def add_to_vector_store(documents):
    vector_store = get_vector_store()
    vector_store.add_documents(documents)


def search_vector_store(query: str, k: int = 5):
    vector_store = get_vector_store()
    results = vector_store.similarity_search(query, k=k)
    return results
