import os
from functools import lru_cache
from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    """Provides application configuration loaded from environment settings. 
    It stores the credentials and model name required by the application.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",
    )
    # --- Existing Settings ---
    GROQ_API_KEY: SecretStr
    GROQ_MODEL_NAME: str
    TAVILY_API_KEY: SecretStr
    # --- LangSmith Settings ---
    LANGSMITH_TRACING: str = Field(default="true")
    LANGSMITH_API_KEY: SecretStr
    LANGSMITH_PROJECT: str = Field(default="default-langgraph-project")
@lru_cache
def get_settings() -> Settings:
    """Loads and caches the application settings. 
    It returns the same configuration instance for the lifetime of the process.
    """
    settings = Settings()
    # Push the LangSmith variables directly into the system environment 
    # so that LangGraph can automatically read them
    os.environ["LANGSMITH_TRACING"] = settings.LANGSMITH_TRACING
    os.environ["LANGSMITH_API_KEY"] = settings.LANGSMITH_API_KEY.get_secret_value()
    os.environ["LANGSMITH_PROJECT"] = settings.LANGSMITH_PROJECT
    return settings
