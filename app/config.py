from pydantic import BaseModel
import os
from dotenv import load_dotenv
from typing import Optional, Dict
from functools import lru_cache

load_dotenv()


class Settings(BaseModel):
    # API Keys
    openai_api_key: Optional[str] = os.getenv('OPENAI_API_KEY')
    google_api_key: Optional[str] = os.getenv('GEMINI_API_KEY')
    groq_api_key: Optional[str] = os.getenv('GROQ_API_KEY')
    cohere_api_key: Optional[str] = os.getenv('COHERE_API_KEY')
    anthropic_api_key: Optional[str] = os.getenv('ANTHROPIC_API_KEY')
    together_api_key: Optional[str] = os.getenv('TOGETHER_API_KEY')
    huggingface_api_key: Optional[str] = os.getenv('HUGGINGFACE_API_KEY')
    voyage_api_key: Optional[str] = os.getenv('VOYAGE_API_KEY')

    # Vector DB Settings
    vector_db_provider: str = os.getenv('VECTOR_STORE_TYPE')
    vector_db_api_key: str = os.getenv('QDRANT_API_KEY')
    vector_db_url: Optional[str] = os.getenv('QDRANT_URL')
    vector_db_collection: Optional[str] = os.getenv('QDRANT_COLLECTION')
    vector_db_index_name: Optional[str] = os.getenv('PINECONE_INDEX')
    vector_db_host: Optional[str] = os.getenv('PINECONE_HOST')
    vector_db_table: Optional[str] = os.getenv('SUPABASE_TABEL')
    vector_db_port: Optional[int] = int(os.getenv('VECTOR_DB_PORT', 6333))
    vector_db_persist_directory: Optional[str] = os.getenv(
        'VECTOR_DB_PERSIST_DIRECTORY')

    # Embedding Settings
    embedding_provider: str = os.getenv('EMBEDDING_TYPE')
    embedding_model: str = os.getenv('TOGETHER_EMBED_MODEL')

    # GITHUB Setting
    github_token: Optional[str] = os.getenv('GITHUB_ACCESS_TOKEN')

    # LLM Settings
    llm_provider: str = os.getenv('LLM_TYPE')
    llm_model: str = os.getenv('GEMINI_LLM_MODEL')  # Default value provided

    # Additional Settings
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # إعدادات السجل
    log_file: str = "app.log"
    log_level: str = "INFO"

    # إعدادات محدد معدل الطلبات
    rate_limit_calls: int = 100
    rate_limit_period: int = 60  # بالثواني

    # Provider-specific settings
    provider_settings: Dict[str, Dict[str, str]] = {
        "openai": {
            "api_base": "https://api.openai.com/v1"
        },
        "google": {
            "project": "your-project-id"
        },
        "anthropic": {
            "api_base": "https://api.anthropic.com"
        },
        # Add other provider-specific settings here
    }


# class Config:
#     env_file = ".env"
#     env_file_encoding = 'utf-8'


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
