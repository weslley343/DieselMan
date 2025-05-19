from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.infrastructure.db.models.user_model import Base
# from app.infrastructure.db.models.vehicle_model import Base
from dotenv import load_dotenv
import os
load_dotenv()
# Altere aqui:
database_url = os.getenv("DATABASE_URL")

engine = create_async_engine(database_url, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
