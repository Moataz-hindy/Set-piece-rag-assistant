import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Set-Piece Tactical Analyzer API"
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "phi3"
    VECTOR_STORE_PATH: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "vector_store")
    CORS_ORIGINS: list[str] = ["http://localhost:8501", "http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()
