import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_db
from app.db.models import Query
from app.db.repositories import QueryRepository
from app.schemas.query import QueryCreate, QueryOut
from app.services.pydantic_ai_service import location_generator

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate", response_model=QueryOut)
async def generate(data: QueryCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Received generate request: city={data.city}, text={data.text}, num_places={data.num_places}, exclude={data.exclude}")
    try:
        result = await location_generator.generate(
            city=data.city,
            text=data.text,
            exclude=data.exclude or [],
            num_places=data.num_places or 3
        )
        logger.info(f"AI returned {len(result)} locations for city '{data.city}'")

        responses = [r.model_dump() for r in result]

        query = Query(
            city=data.city,
            text=data.text,
            num_places=data.num_places or 3,
        )

        repo = QueryRepository(db)
        saved_query = await repo.save(query, excludes=data.exclude or [], responses=responses)
        logger.info(f"Query saved to database with id={saved_query.id}")

        return QueryOut.from_model(saved_query)

    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.exception(f"Unexpected error during generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=list[QueryOut])
async def history(db: AsyncSession = Depends(get_db)):
    logger.info("Fetching query history from database")
    try:
        repo = QueryRepository(db)
        queries = await repo.get_all()
        logger.info(f"Fetched {len(queries)} historical queries")
        return [QueryOut.from_model(q) for q in queries]
    except SQLAlchemyError as e:
        logger.error(f"Database error when fetching history: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")
