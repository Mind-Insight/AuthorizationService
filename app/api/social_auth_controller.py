from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuthError
from redis.asyncio import Redis

from db.database import get_redis
from core.social_auth_config import oauth
from core.config import settings


social_router = APIRouter(prefix="/social", tags=["social"])


@social_router.get("/login/yandex")
async def login_with_yandex(request: Request):
    redirect_uri = settings.yandex_redirect_uri
    return await oauth.yandex.authorize_redirect(request, redirect_uri)


@social_router.get("/callback/yandex")
async def callback_from_yandex(
    request: Request,
    redis: Redis = Depends(get_redis),
):
    token = await oauth.yandex.authorize_access_token(request)
    user_info = await oauth.yandex.userinfo(token=token)
    user_email = user_info.get("default_email")
    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found of credentials invalid",
        )

    request.session["user_email"] = user_email
    await redis.set(
        f"{user_email}:access_token",
        token.get("access_token"),
        ex=settings.jwt.yandex_token_expire_seconds,
    )
    await redis.set(
        f"{user_email}:refresh_token",
        token.get("refresh_token"),
        ex=settings.jwt.yandex_token_expire_seconds,
    )
    return RedirectResponse("http://127.0.0.1:8000/social/auth/me/")


@social_router.get("/auth/me")
async def get_current_user(
    request: Request,
    redis: Redis = Depends(get_redis),
):
    email = request.session.get("user_email")
    if not email:
        raise HTTPException(status_code=401, detail="Not authenticated")

    access_token = await redis.get(f"{email}:access_token")
    return {"email": email, "token": access_token}


@social_router.get("/auth/refresh")
async def refresh_tokens(
    request: Request,
    redis: Redis = Depends(get_redis),
):
    email = request.session.get("user_email")
    if not email:
        raise HTTPException(status_code=401, detail="Not authenticated")

    refresh_token = await redis.get(f"{email}:refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token not found")

    try:
        token = await oauth.yandex.refresh_token(
            url="https://oauth.yandex.ru/token",
            refresh_token=refresh_token.decode("utf-8"),
        )
    except OAuthError as e:
        raise HTTPException(
            status_code=400, detail=f"Token refresh failed: {str(e)}"
        )

    await redis.set(
        f"{email}:access_token",
        token.get("access_token"),
        ex=settings.jwt.yandex_token_expire_seconds,
    )
    if "refresh_token" in token:
        await redis.set(
            f"{email}:refresh_token",
            token.get("refresh_token"),
            ex=settings.jwt.yandex_token_expire_seconds,
        )

    return {"access_token": token.get("access_token")}
