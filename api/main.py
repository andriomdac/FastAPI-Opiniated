from fastapi import FastAPI
from dotenv import load_dotenv
from config.database import Base, engine
from routes.users import user_router
from routes.token import token_router
from contextlib import asynccontextmanager
from models.users import User

# Environment Variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables when the server initiate
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(token_router)
