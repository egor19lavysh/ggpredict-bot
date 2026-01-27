from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TOKEN: str
    ADMIN_PASSWORD: str
    DB_URL: str = 'sqlite+aiosqlite:///data/db.sqlite3'
    REDIS_URL: str = 'redis://localhost:6379/0'
    

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )

settings = Settings()