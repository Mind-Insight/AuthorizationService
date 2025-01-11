import secrets

from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.responses import RedirectResponse
from redis.asyncio import Redis

from api.dependencies import oauth2_scheme
from db import database
from core.social_auth_config import oauth


social_router = APIRouter(prefix="/social", tags=["social"])


import logging

logger = logging.getLogger("uvicorn")


@social_router.get("/login/yandex")
async def login_with_yandex(
    request: Request, redis: Redis = Depends(database.get_redis)
):
    redirect_uri = "http://localhost:8000/social/callback/yandex"
    # key = list(request.session.keys())[0]
    # state = key.split("_")[-1]
    # print(request)
    return await oauth.yandex.authorize_redirect(request, redirect_uri)

@social_router.get("/callback/yandex")
async def callback_from_yandex(
    request: Request, redis: Redis = Depends(database.get_redis)
):
    # state_from_query = request.query_params.get("state")
    # logger.error(f"State from query: {state_from_query}")
    token = await oauth.yandex.authorize_access_token(request)
    request.session["token"] = token
    return RedirectResponse(url="/social/auth/me")


@social_router.get("/auth/me")
async def get_current_user(request: Request):
    token = request.session.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"token": token}
