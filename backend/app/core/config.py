import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "CloneStudio PT-BR"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Base paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    CLONES_DIR: Path = DATA_DIR / "clones"
    UPLOADS_DIR: Path = DATA_DIR / "uploads"
    OUTPUTS_DIR: Path = DATA_DIR / "outputs"
    EXPORTS_DIR: Path = DATA_DIR / "exports"
    ASSETS_DIR: Path = BASE_DIR / "app" / "assets"
    TEMPLATES_DIR: Path = BASE_DIR / "app" / "templates"
    
    # LLM Defaults
    DEFAULT_LLM_PROVIDER: str = "deepseek"
    
    MARITACA_API_KEY: str = os.getenv("MARITACA_API_KEY", "")
    MARITACA_API_URL: str = "https://chat.maritaca.ai/api"
    MARITACA_MODEL: str = "sabia-3"
    
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_URL: str = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL: str = "deepseek-chat"
    
    OLLAMA_API_URL: str = os.getenv("OLLAMA_API_URL", "http://localhost:11434/v1")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
    
    CUSTOM_API_KEY: str = os.getenv("CUSTOM_API_KEY", "")
    CUSTOM_API_URL: str = os.getenv("CUSTOM_API_URL", "")
    CUSTOM_MODEL: str = os.getenv("CUSTOM_MODEL", "")
    
    # Worker Settings
    DEFAULT_WORKER_URL: str = os.getenv("WORKER_URL", "")
    DEFAULT_WORKER_TOKEN: str = os.getenv("WORKER_TOKEN", "")

    def ensure_directories(self):
        for path in [self.DATA_DIR, self.CLONES_DIR, self.UPLOADS_DIR, self.OUTPUTS_DIR, self.EXPORTS_DIR, self.ASSETS_DIR, self.TEMPLATES_DIR]:
            path.mkdir(parents=True, exist_ok=True)

settings = Settings()
settings.ensure_directories()
