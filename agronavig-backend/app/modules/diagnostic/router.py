from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.modules.diagnostic.service import (
    create_diagnostic,
    get_diagnostics_by_user,
    validate_diagnostic,
    compare_diagnostics,
    get_disease_progression,
    get_user_diagnostic_stats
)
from app.modules.diagnostic.schemas import DiagnosticResponse, DiagnosticListResponse
from app.modules.diagnostic.export import generate_diagnostic_pdf, generate_batch_diagnostics_pdf
from app.modules.auth.router import get_current_user_dep
from app.models.diagnostic import Diagnostic
import json
from fastapi.responses import FileResponse

router = APIRouter()

@router.post("/analyser", response_model=DiagnosticResponse)
def analyser(
    culture: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_dep)
):
    """Analyse une image de feuille et retourne un diagnostic complet"""
    valid_cultures = ["Apple", "Cherry", "Corn", "Grape", "Orange", "Peach", "Pepper", "Potato", "Squash", "Strawberry", "Tomato", "Soybean"]
    if culture not in valid_cultures:
        raise HTTPException(status_code=400, detail=f"La culture '{culture}' n'est pas supportee par notre IA.")
        
    return create_diagnostic(db, current_user.id, culture, file)

@router.get("/historique", response_model=DiagnosticListResponse)
def historique(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_dep)
):
    """Recupere l'historique des diagnostiques avec pagination"""
    return get_diagnostics_by_user(db, current_user.id, limit=limit, offset=offset)

@router.get("/dernier", response_model=DiagnosticResponse)
def dernier_diagnostic(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_dep)
):
    """Recupere le dernier diagnostic effectue"""
    diagnostic = db.query(Diagnostic)\
        .filter(Diagnostic.user_id == current_user.id)\
        .order_by(Diagnostic.created_at.desc())\
        .first()
    if not diagnostic:
        raise HTTPException(status_code=404, detail="Aucun diagnostic trouve")
    return diagnostic

@router.post("/validation/{diagnostic_id}")
def valider_diagnostic(
    diagnostic_id: int,
    validation: dict,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_dep)
):
    """
    Valide ou corrige un diagnostic existant
    """
    diagnostic = db.query(Diagnostic).filter(
        Diagnostic.id == diagnostic_id,
        Diagnostic.user_id == current_user.id
    ).first()
    
    if not diagnostic:
        raise HTTPException(status_code=404, detail="Diagnostic not found")
    
    updated = validate_diagnostic(db, diagnostic_id, validation)
    return {
        "success": True,
        "message": "Diagnostic valide",
        "diagnostic": updated
    }

@router.get("/comparaison/{id1}/{id2}")
def comparer_diagnostiques(
    id1: int,
    id2: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_dep)
):
    """Compare deux diagnostiques pour suivre l'evolution (ex: avant/apres traitement)"""
    d1 = db.query(Diagnostic).filter(Diagnostic.id == id1, Diagnostic.user_id == current_user.id).first()
    d2 = db.query(Diagnostic).filter(Diagnostic.id == id2, Diagnostic.user_id == current_user.id).first()
    
    if not d1 or not d2:
        raise HTTPException(status_code=404, detail="Un ou plusieurs diagnostics non trouves")
    
    return compare_diagnostics(db, id1, id2)

@router.get("/progression/{culture}")
def progression_maladie(
    culture: str,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_dep)
):
    """Affiche la progression d'une maladie pour une culture donnee"""
    return get_disease_progression(db, current_user.id, culture, limit=limit)

@router.get("/statistiques")
def statistiques_utilisateur(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_dep)
):
    """Retourne les statistiques de diagnostic de l'utilisateur"""
    return get_user_diagnostic_stats(db, current_user.id)

@router.get("/export-pdf/{diagnostic_id}")
def exporter_pdf(
    diagnostic_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_dep)
):
    """Exporte un diagnostic au format PDF"""
    diagnostic = db.query(Diagnostic).filter(
        Diagnostic.id == diagnostic_id,
        Diagnostic.user_id == current_user.id
    ).first()
    
    if not diagnostic:
        raise HTTPException(status_code=404, detail="Diagnostic not found")
    
    try:
        pdf_path = generate_diagnostic_pdf(diagnostic)
        return FileResponse(pdf_path, media_type="application/pdf", filename=f"diagnostic_{diagnostic_id}.pdf")
    except ImportError as e:
        raise HTTPException(status_code=500, detail=f"PDF export not available: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")

@router.post("/export-batch-pdf")
def exporter_batch_pdf(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_dep)
):
    """Exporte un batch de diagnostiques en PDF"""
    diagnostics = db.query(Diagnostic)\
        .filter(Diagnostic.user_id == current_user.id)\
        .order_by(Diagnostic.created_at.desc())\
        .limit(limit)\
        .all()
    
    if not diagnostics:
        raise HTTPException(status_code=404, detail="No diagnostics found")
    
    try:
        pdf_path = generate_batch_diagnostics_pdf(diagnostics)
        return FileResponse(pdf_path, media_type="application/pdf", filename="diagnostics_batch.pdf")
    except ImportError as e:
        raise HTTPException(status_code=500, detail=f"PDF export not available: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
