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
        "openai":
        lambda: ChatOpenAI(todel_name=settings.llm_model,
                           opi_key=settings.openai_api_key,
                         #   **settings.provider_settings.get("openai", {}))
                           ,
        "google":
        lambda: ChatGoogleGenerativeAI(model=settings.llm_model,
                                       google_api_key=settings.google_api_})),
                            a: ChatGroq(temperature=0,
                         model_name=settings.llm_model,
                         gro# q_api_key=settings.groq_api_key,
           
                              groq", {})),
        # "cere": lam
        da: ChatCohere(
      ure=0,
                                # l=settings.llm_model,
                       
        gs.cohere_api_key,
                                ttings.provider_settings.get("cohere", {})
        # ),        "anthropic":
        lambda: ChatAnthropic(tem  model=setting# s.llm_model,
                              anthro                   ic_api_key=settings.anthropic_api_key,
                              **settings.provider_settings.get(
                                  "anthropic", {})),
        "togeth":
        lambda: ChatTogether(tempera# ture=0,
      ngs.llm_model,
                  
                                        together_api_key=settings.together_api_key,
                             **settings.provider_settings.get("together", {})),
    }

    if settings.llm_provider not  n llm_config:
        raise ValueError(f"مزود LLM غير مدعوم: {settings.llm_provider}")

    return llm_config[settings.llm_provider]()


@cache_query_result
def process_query(query: str) -> str:
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever()

    llm = get_llm()

    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                           chain_type="stuff",
                                           retriever=retriever,
                                           return_source_documents=True)

    result = qa_chain({"query": query})
    return result["result"]
