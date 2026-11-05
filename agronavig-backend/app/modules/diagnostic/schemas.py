from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any

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
    
    # Nouveaux champs pour amélioration qualité et validation
    top_predictions: Optional[List[Dict[str, Any]]] = None
    validated_by_user: Optional[bool] = False
    user_feedback: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None
    
    # Champs calculés/attachés
    confidence_adjusted: Optional[float] = None
    seasonal_context: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class DiagnosticListResponse(BaseModel):
    total: int
    count: int = 0
    diagnostics: List[DiagnosticResponse]

class PaginatedDiagnosticResponse(BaseModel):
    total: int
    count: int
    limit: int
    offset: int
    diagnostics: List[DiagnosticResponse]

class ValidationRequest(BaseModel):
    status: str  # "correct", "incorrect", "partial"
    comment: Optional[str] = None
    correct_disease: Optional[str] = None

class ComparisonResult(BaseModel):
    diagnostic1: Dict[str, Any]
    diagnostic2: Dict[str, Any]
    evolution: Dict[str, Any]

class ProgressionResponse(BaseModel):
    culture: str
    total: int
    progression: List[Dict[str, Any]]

class StatsResponse(BaseModel):
    total_diagnostics: int
    validated_by_user: int
    confirmed_correct: int
    accuracy_rate: float
    cultures: List[str]
    unique_diseases: int
    avg_confidence: float
    last_diagnostic: Optional[str]