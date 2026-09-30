from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str = Field(default="", validation_alias="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-2.5-flash", validation_alias="GEMINI_MODEL")
    demo_mode: bool = Field(default=False, validation_alias="DEMO_MODE")
    backend_url: str = Field(default="http://127.0.0.1:8000", validation_alias="BACKEND_URL")
    cors_origins: str = Field(
        default="http://localhost:8501,http://127.0.0.1:8501",
        validation_alias="CORS_ORIGINS",
    )
    max_input_chars: int = 12000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
