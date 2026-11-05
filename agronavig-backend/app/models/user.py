from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    nom        = Column(String, nullable=False)
    email      = Column(String, unique=True, index=True, nullable=False)
    password   = Column(String, nullable=False)
    role          = Column(String, default="producteur") # producteur, agriculteur, agronome, admin, etudiant
    telephone     = Column(String, nullable=True)
    localisation  = Column(String, nullable=True)
    cultures_interet = Column(String, default="tomate,oignon,mais") # Liste separee par virgules
    is_active  = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Coordonnées géographiques précises pour la météo et les prévisions locales
    latitude     = Column(Float, nullable=True)
    longitude    = Column(Float, nullable=True)
    region       = Column(String, nullable=True) # Ex. Thiès, Dakar, Saint-Louis, etc.
