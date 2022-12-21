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

    class Config:
        env_file = ".env"


config = Config()
