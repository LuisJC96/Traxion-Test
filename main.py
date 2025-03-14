from uvicorn import Server
from uvicorn.config import Config
from fastapi import FastAPI
from app.v1.router import app as app_v1
from contextlib import asynccontextmanager
from tools.mongodb_singleton import MongoDBSingleton


@asynccontextmanager
async def lifespan(app: FastAPI):
    MongoDBSingleton.get_client()
    yield
    MongoDBSingleton.close_client()


app = FastAPI(lifespan=lifespan)
app.mount("/v1", app_v1)

if __name__ == "__main__":
    conf = Config(
        app="main:app",
        port=5000,
        host="0.0.0.0",
        reload=True
    )
    server = Server(conf)
    server.run()