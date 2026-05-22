from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-3.5-flash"

# Optimasi Token & Cost
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 1024          # Turunkan agar lebih hemat
    MAX_HISTORY_TURNS: int = 15     # Batasi panjang history
    
    # RAG Settings
    RAG_K: int = 3
    RAG_SCORE_THRESHOLD: float = 0.78
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
settings = Settings()