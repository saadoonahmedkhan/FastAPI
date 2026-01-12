from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_hostname: str
    database_port: int
    database_name: str

    secret_key: str
    algorithm: str
    access_token_expire: int

    model_config = SettingsConfigDict(
        env_file=str(ROOT_DIR.parent / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False
    )

settings = Settings()
