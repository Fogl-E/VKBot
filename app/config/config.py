from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    Token: str
    Admin_id: int
    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" 
    )


config = Settings()