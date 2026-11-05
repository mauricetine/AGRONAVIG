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

    # Indicateurs climatiques et fourchette de rendement
    rendement_min      = Column(Float, nullable=True)
    rendement_max      = Column(Float, nullable=True)
    etp_estimee        = Column(Float, nullable=True)
    stress_hydrique    = Column(Float, nullable=True)
    confiance          = Column(Float, default=85.0)
