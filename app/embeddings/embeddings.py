from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_cohere import CohereEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_together import TogetherEmbeddings
from langchain_voyageai import VoyageAIEmbeddings
from app.config import settings


def get_embedding_model():
    try:

        embedding_config = {
            "openai":
            lambda: OpenAIEmbeddings(openai_api_key=settings.openai_api_key,
                                     model=settings.embedding_model),
            "google":
            lambda: GoogleGenerativeAIEmbeddings(
                google_api_key=settings.google_api_key,
                model=settings.embedding_model),
            "cohere":
            lambda: CohereEmbeddings(cohere_api_key=settings.cohere_api_key,
                                     model=settings.embedding_model),
            # "huggingface": lambda: HuggingFaceEmbeddings(
            #     api_key=settings.huggingface_api_key,
            #     model_name=settings.embedding_model
            # ),
            "together":
            lambda: TogetherEmbeddings(together_api_key=settings.
                                       together_api_key,
                                       model=settings.embedding_model),
            "voyage":
            lambda: VoyageAIEmbeddings(voyage_api_key=settings.voyage_api_key,
                                       model=settings.embedding_model),
        }

        if settings.embedding_provider not in embedding_config:
            raise ValueError(
                f"مزود التضمين غير مدعوم: {settings.embedding_provider}")

        return embedding_config[settings.embedding_provider]()
    except KeyError:
        raise ValueError(
            f"مزود التضمين غير مدعوم: {settings.embedding_provider}")
    except Exception as e:
        raise ValueError(f"حدث خطأ أثناء إنشاء نموذج التضمين: {e}")
