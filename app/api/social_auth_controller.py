import aiohttp
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
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
        ex=settings.jwt.yandex_access_token_expire_seconds,
    )
    await redis.set(
        f"{user_email}:refresh_token",
        token.get("refresh_token"),
        ex=settings.jwt.yandex_refresh_token_expire_second,
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
async def refresh_token(request: Request, redis: Redis = Depends(get_redis)):
    user_email = request.session.get("user_email")
    if not user_email:
        raise HTTPException(status_code=401, detail="Not authenticated")

    refresh_token = await redis.get(f"{user_email}:refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token not found",
        )

    async with aiohttp.ClientSession() as session:
        async with session.post(
            settings.yandex_token_url,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": settings.YANDEX_CLIENT_ID,
                "client_secret": settings.YANDEX_CLIENT_SECRET,
            },
        ) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=response.status,
                    detail="Failed to refresh token",
                )
            new_token = await response.json()

    await redis.set(
        f"{user_email}:access_token",
        new_token["access_token"],
        ex=settings.jwt.yandex_access_token_expire_seconds,
    )
    await redis.set(
        f"{user_email}:refresh_token",
        new_token["refresh_token"],
        ex=settings.jwt.yandex_refresh_token_expire_second,
    )

    return {
        "message": "Token refreshed successfully",
        "access_token": new_token["access_token"],
    }


@social_router.get("/auth/logout")
async def logout_user(request: Request, redis: Redis = Depends(get_redis)):
    user_email = request.session.get("user_email")
    if not user_email:
        raise HTTPException(status_code=401, detail="Not authenticated")

    await redis.delete(f"{user_email}:access_token")
    await redis.delete(f"{user_email}:refresh_token")
    request.session.clear()
    return {"message": "Successfully logged out"}
