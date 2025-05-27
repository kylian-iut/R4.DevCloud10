from pydantic import BaseSettings

class Settings(BaseSettings):
    MASTERCARD_API_KEY: str
    MASTERCARD_PRIVATE_KEY_PATH: str

    class Config:
        env_file = ".env"

settings = Settings()
