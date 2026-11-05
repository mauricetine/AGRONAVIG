from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.sql import func
from app.database.db import Base

class Diagnostic(Base):
    __tablename__ = "diagnostics"

    id                      = Column(Integer, primary_key=True, index=True)
    user_id                 = Column(Integer, ForeignKey("users.id"), nullable=False)
    culture                 = Column(String, nullable=False)
    maladie                 = Column(String, nullable=False)
    confiance               = Column(Float, nullable=False)
    niveau                  = Column(String, nullable=False)
    traitement              = Column(String, nullable=True)
    image_path              = Column(String, nullable=True)
    
    # Nouveaux champs pour améliorations
    description             = Column(Text, nullable=True)  # Description détaillée
    top_predictions         = Column(JSON, nullable=True)  # Top 3 prédictions avec scores
    validated_by_user       = Column(Boolean, default=False)  # Validation utilisateur
    user_feedback           = Column(String, nullable=True)  # Feedback: 'correct', 'incorrect', 'partial'
    metadata_json           = Column(JSON, nullable=True)  # Données contextuelles (météo, saison, etc.)
    
    created_at              = Column(DateTime(timezone=True), server_default=func.now())
    updated_at              = Column(DateTime(timezone=True), onupdate=func.now())

    # Validation par un expert agronome
    agronome_validated      = Column(Boolean, default=False)
    agronome_comment        = Column(Text, nullable=True)
    validated_at            = Column(DateTime(timezone=True), nullable=True)
