from authlib.integrations.starlette_client import OAuth
from starlette.config import Config


config = Config(".env")

oauth = OAuth(config)
oauth.register(
    name="yandex",
    client_id="4770242b6c2c40e9a5f985257b884a8e",
    client_secret="68495c1254f3415c9746c3c238c8cda4",
    authorize_state="secret",
    userinfo_endpoint="https://login.yandex.ru/info",
    access_token_url="https://oauth.yandex.ru/token",
    authorize_url="https://oauth.yandex.ru/authorize",
    client_kwargs={"scope": "login:email login:info"},
)
