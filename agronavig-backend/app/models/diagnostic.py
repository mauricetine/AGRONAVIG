from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.db import Base

class Diagnostic(Base):
    __tablename__ = "diagnostics"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False)
    culture      = Column(String, nullable=False)
    maladie      = Column(String, nullable=False)
    confiance    = Column(Float, nullable=False)
    niveau       = Column(String, nullable=False)
    traitement   = Column(String, nullable=True)
    image_path   = Column(String, nullable=True)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())