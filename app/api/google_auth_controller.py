import aiohttp
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from redis.asyncio import Redis

from db.database import get_redis
from core.social_auth_config import google_oauth as oauth
from core.config import settings

google_router = APIRouter(prefix="/social", tags=["google"])


@google_router.get("/login/google")
async def login_with_google(request: Request):
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)


@google_router.get("/callback/google")
async def callback_from_google(
    request: Request, redis: Redis = Depends(get_redis)
):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.userinfo(token=token)
    user_email = user_info.get("email")

    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found or credentials invalid",
        )

    request.session["user_email"] = user_email
    await redis.set(
        f"{user_email}:access_token",
        token.get("access_token"),
        ex=3600,
    )
    if refreh_token := token.get("refresh_token"):
        await redis.set(
            f"{user_email}:refresh_token",
            refreh_token,
            ex=2592000,
        )
    return RedirectResponse("http://127.0.0.1:8000/social/auth/me/")


@google_router.get("/auth/me")
async def get_current_user(
    request: Request, redis: Redis = Depends(get_redis)
):
    email = request.session.get("user_email")
    if not email:
        raise HTTPException(status_code=401, detail="Not authenticated")

    access_token = await redis.get(f"{email}:access_token")
    return {"email": email, "token": access_token}


@google_router.get("/auth/refresh/google")
async def refresh_google_token(
    request: Request, redis: Redis = Depends(get_redis)
):
    user_email = request.session.get("user_email")
    if not user_email:
        raise HTTPException(status_code=401, detail="Not authenticated")

    refresh_token = await redis.get(f"{user_email}:refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token not found")

    async with aiohttp.ClientSession() as session:
        async with session.post(
            settings.GOOGLE_TOKEN_URL,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
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
        ex=3600,
    )
    return {
        "message": "Token refreshed successfully",
        "access_token": new_token["access_token"],
    }


@google_router.get("/auth/logout/google")
async def logout_google_user(
    request: Request, redis: Redis = Depends(get_redis)
):
    user_email = request.session.get("user_email")
    if not user_email:
        raise HTTPException(status_code=401, detail="Not authenticated")

    await redis.delete(f"{user_email}:access_token")
    await redis.delete(f"{user_email}:refresh_token")
    request.session.clear()
    return {"message": "Successfully logged out from Google"}
