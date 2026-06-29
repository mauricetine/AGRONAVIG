from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.modules.diagnostic.service import create_diagnostic, get_diagnostics_by_user
from app.modules.diagnostic.schemas import DiagnosticResponse, DiagnosticListResponse
from app.modules.auth.router import get_current_user_dep
from fastapi import HTTPException

router = APIRouter()

@router.post("/analyser", response_model=DiagnosticResponse)
def analyser(
    culture: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_dep)
):
    # Validation simple de la culture
    valid_cultures = ["Apple", "Cherry", "Corn", "Grape", "Orange", "Peach", "Pepper", "Potato", "Squash", "Strawberry", "Tomato", "Soybean"]
    if culture not in valid_cultures:
        raise HTTPException(status_code=400, detail=f"La culture '{culture}' n'est pas supportée par notre IA.")
        
    return create_diagnostic(db, current_user.id, culture, file)

@router.get("/historique", response_model=DiagnosticListResponse)
def historique(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_dep)
):
    return get_diagnostics_by_user(db, current_user.id)

@router.get("/dernier", response_model=DiagnosticResponse)
def dernier_diagnostic(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_dep)
):
    from app.models.diagnostic import Diagnostic
    from fastapi import HTTPException
    diagnostic = db.query(Diagnostic)\
        .filter(Diagnostic.user_id == current_user.id)\
        .order_by(Diagnostic.created_at.desc())\
        .first()
    if not diagnostic:
        raise HTTPException(status_code=404, detail="Aucun diagnostic trouvé")
    return diagnostic