from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "ComicCraft"
    debug: bool = True

    gemini_api_key: str = ""
    gemini_outline_model: str = "gemini-3.5-flash-lite"
    gemini_story_model: str = "gemini-3.5-flash-lite"
    gemini_image_model: str = "gemini-2.5-flash-image"

    image_provider: str = "none"

    default_panels: int = 5

    hf_token: str = ""
    hf_image_model: str = ""
    local_image_model: str = "runwayml/stable-diffusion-v1-5"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
PANELS_DIR = STATIC_DIR / "panels"
EXPORTS_DIR = STATIC_DIR / "exports"

PANELS_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)