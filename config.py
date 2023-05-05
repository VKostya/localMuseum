from pydantic import BaseSettings


class Config(BaseSettings):
    HOST: str
    PORT: int
    DB_PROVIDER: str
    DB_NAME: str
    DEBUG: bool
    CLOUD_NAME: str
    API_KEY: str
    API_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    ALGORITHM: str

    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str

    class Config:
        env_file = ".env"


config = Config()
