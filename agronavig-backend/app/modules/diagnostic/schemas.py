from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DiagnosticResponse(BaseModel):
    id: int
    culture: str
    maladie: str
    confiance: float
    niveau: str
    traitement: Optional[str]
    image_path: Optional[str]
    created_at: datetime
    
    # Champs étendus pour les détails de la maladie
    description: str = ""
    symptomes: list[str] = []
    prevention: list[str] = []
    traitements: list[dict] = []

    class Config:
        from_attributes = True

class DiagnosticListResponse(BaseModel):
    total: int
    diagnostics: list[DiagnosticResponse]