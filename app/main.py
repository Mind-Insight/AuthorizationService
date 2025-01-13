from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

from api.user_controller import router
from api.social_auth_controller import social_router
from db.database import create_tables, close_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    await close_connection()


app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)
app.add_middleware(
    SessionMiddleware,
    secret_key="secret",
    https_only=False,
    same_site="lax",
    session_cookie="session",
)


app.include_router(router)
app.include_router(social_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
