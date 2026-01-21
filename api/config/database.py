from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base


DB_URL = "sqlite+aiosqlite:///./database.db"
engine = create_async_engine(url=DB_URL)
Session = async_sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)
Base = declarative_base()


async def get_db():
    async with Session() as db:
        yield db
