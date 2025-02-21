from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.sessions import SessionMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import uvicorn

from api.user_controller import router
from api.social_auth_controller import social_router
from api.google_auth_controller import google_router
from db.database import create_tables, close_connection
from core.trace_config import configure_tracer, RequestIdMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    await close_connection()


app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

configure_tracer()

FastAPIInstrumentor.instrument_app(app)

app.add_middleware(RequestIdMiddleware)
app.add_middleware(
    SessionMiddleware,
    secret_key="secret",
    https_only=False,
    same_site="lax",
    session_cookie="session",
)

app.include_router(router)
app.include_router(social_router)
app.include_router(google_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
