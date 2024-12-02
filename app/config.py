from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "My FastAPI Application"
    verify_message: str = "AAAAA"

    class Config:
        env_file = ".env"


settings = Settings()
