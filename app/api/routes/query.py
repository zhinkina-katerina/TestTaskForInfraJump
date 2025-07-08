import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.db.models import Query
from app.db.repositories import QueryRepository
from app.di import get_query_repository, get_location_generator
from app.schemas.query import QueryCreate, QueryOut
from app.services.pydantic_ai_service import LocationGenerator

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/generate", response_model=QueryOut)
async def generate(data: QueryCreate,
                   query_repository: QueryRepository = Depends(get_query_repository),
                   location_generator: LocationGenerator = Depends(get_location_generator)):
    logger.info(
    f"Received generate request: city={data.city}, text={data.text}, num_places={data.num_places}, exclude={data.exclude}")
    result = await location_generator.generate(
        city=data.city,
        text=data.text,
        exclude=data.exclude or [],
        num_places=data.num_places
    )
    logger.info(f"AI returned {len(result)} locations for city '{data.city}'")

    responses = [r.model_dump() for r in result]

    query = Query(
        city=data.city,
        text=data.text,
        num_places=data.num_places,
    )

    saved_query = await query_repository.save(query, excludes=data.exclude or [], responses=responses)
    logger.info(f"Query saved to database with id={saved_query.id}")

    return QueryOut.from_model(saved_query)



@router.get("/history", response_model=list[QueryOut])
async def history(query_repository: QueryRepository = Depends(get_query_repository)):
    logger.info("Fetching query history from database")
    queries = await query_repository.get_all()
    logger.info(f"Fetched {len(queries)} historical queries")
    return [QueryOut.from_model(q) for q in queries]
