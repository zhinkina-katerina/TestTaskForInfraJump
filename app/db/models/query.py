from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.db import Base


class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=True)
    text = Column(String, nullable=False)
    num_places = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)