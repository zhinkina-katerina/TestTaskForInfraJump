from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.models import Query, QueryExclude, QueryResponse


class QueryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(
        self,
        query: Query,
        excludes: list[str],
        responses: list[dict]
    ) -> Query:
        try:
            self.db.add(query)
            await self.db.flush()

            self.db.add_all([
                QueryExclude(query_id=query.id, name=name)
                for name in excludes
            ])

            self.db.add_all([
                QueryResponse(
                    query_id=query.id,
                    name=resp.get("name"),
                    description=resp.get("description"),
                    country=resp.get("country"),
                    url=resp.get("url"),
                    lat=resp["coordinates"]['lat'],
                    lon=resp["coordinates"]['lng']
                )
                for resp in responses
            ])

            await self.db.commit()
            result = await self.db.execute(
                select(Query)
                .options(
                    selectinload(Query.excludes),
                    selectinload(Query.responses)
                )
                .where(Query.id == query.id)
            )
            return result.scalar_one()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def get_all(self) -> list[Query]:
        result = await self.db.execute(
            select(Query)
            .options(
                selectinload(Query.excludes),
                selectinload(Query.responses)
            )
            .order_by(Query.created_at.desc())
        )
        return result.scalars().all()

