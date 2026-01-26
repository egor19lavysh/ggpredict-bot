from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TOKEN: str
    DB_URL: str = 'sqlite+aiosqlite:///data/db.sqlite3'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )

settings = Settings()