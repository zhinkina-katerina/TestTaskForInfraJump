from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.orm import relationship

from app.db.db import Base


class QueryExclude(Base):
    __tablename__ = "query_excludes"

    id = Column(Integer, primary_key=True)
    query_id = Column(Integer, ForeignKey("queries.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)

    query = relationship("Query", backref="excludes")
