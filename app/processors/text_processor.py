from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_cohere import ChatCohere
from langchain_anthropic import ChatAnthropic
from langchain_together import ChatTogether
from app.database.vector_store import get_vector_store
from app.config import settings
from app.utils.caching import cache_query_result


def get_llm():
    llm_config = {
        "openai": lambda: ChatOpenAI(
            temperature=0,
            model_name=settings.llm_model,
            openai_api_key=settings.openai_api_key,
            **settings.provider_settings.get("openai", {})
        ),
        "google": lambda: ChatGoogleGenerativeAI(
            model=settings.llm_model,
            google_api_key=settings.google_api_key,
            **settings.provider_settings.get("google", {})
        ),
        "groq": lambda: ChatGroq(
            temperature=0,
            model_name=settings.llm_model,
            groq_api_key=settings.groq_api_key,
            **settings.provider_settings.get("groq", {})
        ),
        "cohere": lambda: ChatCohere(
            temperature=0,
            model=settings.llm_model,
            cohere_api_key=settings.cohere_api_key,
            **settings.provider_settings.get("cohere", {})
        ),
        "anthropic": lambda: ChatAnthropic(
            temperature=0,
            model=settings.llm_model,
            anthropic_api_key=settings.anthropic_api_key,
            **settings.provider_settings.get("anthropic", {})
        ),
        "together": lambda: ChatTogether(
            temperature=0,
            model=settings.llm_model,
            together_api_key=settings.together_api_key,
            **settings.provider_settings.get("together", {})
        ),
    }
    
    if settings.llm_provider not in llm_config:
        raise ValueError(f"مزود LLM غير مدعوم: {settings.llm_provider}")
    
    return llm_config[settings.llm_provider]()


@cache_query_result
def process_query(query: str) -> str:
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever()
    
    llm = get_llm()
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    
    result = qa_chain({"query": query})
    return result["result"]