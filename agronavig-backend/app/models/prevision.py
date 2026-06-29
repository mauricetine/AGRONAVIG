from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.db import Base

class Prevision(Base):
    __tablename__ = "previsions"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False)
    culture      = Column(String, nullable=False)
    mois         = Column(String, nullable=False)
    rendement    = Column(Float, nullable=False)
    objectif     = Column(Float, nullable=False)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())