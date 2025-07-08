from sqlalchemy import Column, Integer, String, DateTime, Index
from datetime import datetime

from app.db.db import Base


class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=True)
    text = Column(String, nullable=False)
    num_places = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_query_city_text", "city", "text"),
    )