from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn

from api.user_controller import router
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

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
