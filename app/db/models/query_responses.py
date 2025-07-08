from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float

from sqlalchemy.orm import relationship

from app.db.db import Base

class QueryResponse(Base):
    __tablename__ = "query_responses"

    id = Column(Integer, primary_key=True)
    query_id = Column(Integer, ForeignKey("queries.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    country = Column(String, nullable=True)
    url = Column(String, nullable=True)
    lat = Column(Float)
    lon = Column(Float)

    query = relationship("Query", backref="responses")
