from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from core.config import settings


config = Config(".env")

oauth_yandex = OAuth(config)
oauth_yandex.register(
    name="yandex",
    client_id=settings.YANDEX_CLIENT_ID,
    client_secret=settings.YANDEX_CLIENT_SECRET,
    authorize_state="secret",
    userinfo_endpoint="https://login.yandex.ru/info",
    access_token_url="https://oauth.yandex.ru/token",
    authorize_url="https://oauth.yandex.ru/authorize",
    client_kwargs={"scope": "login:email login:info"},
)


google_oauth = OAuth(config)
google_oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_state="secret",
    client_kwargs={
        "scope": "openid email profile",
    },
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
)
