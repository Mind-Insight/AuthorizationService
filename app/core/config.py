import os
from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 30
    yandex_access_token_expire_seconds: int = 3600
    yandex_refresh_token_expire_second: int = 2592000


class Settings(BaseSettings):
    DB_HOST: str = Field(..., env="DB_HOST")
    DB_PORT: str = Field(..., env="DB_PORT")
    DB_NAME: str = Field(..., env="DB_NAME")
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")

    REDIS_HOST: str = Field(..., env="REDIS_HOST")
    REDIS_PORT: str = Field(..., env="REDIS_PORT")

    YANDEX_CLIENT_ID: str = Field(..., env="CLIENT_ID")
    YANDEX_CLIENT_SECRET: str = Field(..., env="CLIENT_SECRET")
    yandex_token_url: str = "https://oauth.yandex.ru/token"
    yandex_redirect_uri: str = "http://127.0.0.1:8000/social/callback/yandex"

    db_schema: str = "auth"

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")

    jwt: AuthJWT = AuthJWT()

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.pg_dsn = self.get_db_url()

    def get_db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
