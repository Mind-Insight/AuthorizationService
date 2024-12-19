from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn
from api import user_controller
from api.auth import router as auth_router
from db.database import create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    await delete_tables()


app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

app.include_router(user_controller.router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
