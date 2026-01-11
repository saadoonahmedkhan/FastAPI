from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

# Get the root directory
ROOT_DIR = Path(__file__).parent.parent

class Settings(BaseSettings):
    database_username: str = os.getenv("DATABASE_USERNAME", "saadoon")
    database_password: str = os.getenv("DATABASE_PASSWORD", "s@@doon123")
    database_hostname: str = os.getenv("DATABASE_HOSTNAME", "localhost")
    database_port: int = int(os.getenv("DATABASE_PORT", "5432"))
    database_name: str = os.getenv("DATABASE_NAME", "fastAPI")
    secret_key: str = os.getenv("SECRET_KEY", "default-secret-key")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire: int = int(os.getenv("ACCESS_TOKEN_EXPIRE", "30"))

    model_config = SettingsConfigDict(
        env_file=str(ROOT_DIR.parent / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False
    )

settings = Settings()

print(f"Database URL: postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}")
