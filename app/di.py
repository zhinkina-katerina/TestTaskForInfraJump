from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.db import AsyncSessionLocal
from app.db.repositories import QueryRepository
from app.services.pydantic_ai_service import LocationGenerator


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_query_repository(db: AsyncSession = Depends(get_db)):
    yield QueryRepository(db)


async def get_location_generator():
    yield LocationGenerator(api_key=settings.OPENAI_API_KEY)
