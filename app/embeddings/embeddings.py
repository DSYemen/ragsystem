from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_cohere import CohereEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_together import TogetherEmbeddings
from langchain_voyageai import VoyageAIEmbeddings
from app.config import settings


def get_embedding_model():
    try:
        # تحقق من أن نموذج التضمين معرف في الإعدادات
        if not settings.embedding_model:
            raise ValueError(
                "نموذج التضمين (embedding model) غير محدد في الإعدادات. يرجى تحديد النموذج."
            )

        # تعريف التكوين لمقدمي التضمين
        embedding_config = {
            "openai":
            lambda: OpenAIEmbeddings(api_key=settings.openai_api_key,
                                     model=settings.embedding_model),
            "google":
            lambda: GoogleGenerativeAIEmbeddings(
                api_key=settings.google_api_key,
                model=settings.embedding_model),
            # "cohere":
            # lambda: CohereEmbeddings(api_key=settings.cohere_api_key,
            #                          model=settings.embedding_model),
            # # "huggingface": lambda: HuggingFaceEmbeddings(
            #     api_key=settings.huggingface_api_key,
            #     model_name=settings.embedding_model
            # ),
            "together":
            lambda: TogetherEmbeddings(api_key=settings.together_api_key,
                                       model=settings.embedding_model),
            "voyage":
            lambda: VoyageAIEmbeddings(api_key=settings.voyage_api_key,
                                       model=settings.embedding_model),
        }

        # تحقق من وجود مزود التضمين في التكوين
        if settings.embedding_provider not in embedding_config:
            raise ValueError(
                f"مزود التضمين غير مدعوم: {settings.embedding_provider}")

        # إرجاع نموذج التضمين المحدد
        return embedding_config[settings.embedding_provider]()

    except KeyError as e:
        raise ValueError(f"المفتاح المطلوب غير موجود في الإعدادات: {e}")
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise ValueError(f"حدث خطأ غير متوقع: {e}")
