from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Index

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

    __table_args__ = (
        Index("ix_queryresponse_query_id_name", "query_id", "name"),
    )