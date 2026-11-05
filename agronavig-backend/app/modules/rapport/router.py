from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.database.db import get_db
from app.modules.auth.router import get_current_user_dep
from app.models.diagnostic import Diagnostic
from datetime import datetime

router = APIRouter()

MOIS_FR = {
    1: "Jan",     2: "Fev", 3: "Mar", 4: "Avr",
    5: "Mai", 6: "Jun",     7: "Jul", 8: "Aou",
    9: "Sep", 10: "Oct", 11: "Nov",     12: "Dec"
}

@router.get("/")
def rapport(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_dep)
):
    diagnostics = db.query(Diagnostic)\
        .filter(Diagnostic.user_id == current_user.id)\
        .all()

    total   = len(diagnostics)
    traites = len([d for d in diagnostics if d.niveau == "faible"])

    # Repartition par maladie
    maladies = {}
    for d in diagnostics:
        maladies[d.maladie] = maladies.get(d.maladie, 0) + 1

    # Repartition par culture
    cultures = {}
    for d in diagnostics:
        cultures[d.culture] = cultures.get(d.culture, 0) + 1

    # Activite par mois - grouper les diagnostics par mois
    activite_raw = db.query(
        extract("month", Diagnostic.created_at).label("mois"),
        func.count(Diagnostic.id).label("total")
    ).filter(
        Diagnostic.user_id == current_user.id,
        extract("year", Diagnostic.created_at) == datetime.now().year
    ).group_by(
        extract("month", Diagnostic.created_at)
    ).order_by(
        extract("month", Diagnostic.created_at)
    ).all()

    # Construire tableau activité 12 mois
    activite_dict = {int(row.mois): row.total for row in activite_raw}
    activite = [
        {
            "mois":        MOIS_FR[m],
            "diagnostics": activite_dict.get(m, 0),
            "conseils":    0  # sera enrichi quand on aura la table conseils
        }
        for m in range(1, 13)
    ]

    return {
        "total_diagnostics":    total,
        "maladies_traitees":    traites,
        "repartition_maladies": maladies,
        "repartition_cultures": cultures,
        "activite_mensuelle":   activite,
        "derniers_diagnostics": [
            {
                "id":         d.id,
                "culture":    d.culture,
                "maladie":    d.maladie,
                "confiance":  d.confiance,
                "niveau":     d.niveau,
                "traitement": d.traitement,
                "created_at": str(d.created_at)
            }
            for d in sorted(diagnostics, key=lambda x: x.created_at, reverse=True)[:10]
        ]
    }