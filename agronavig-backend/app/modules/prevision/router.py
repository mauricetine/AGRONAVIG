from fastapi import APIRouter, Depends
from app.modules.auth.router import get_current_user_dep
from app.modules.prevision.service import calculer_previsions

router = APIRouter()

@router.get("/recoltes")
def recoltes(surface: float = 1.0, current_user=Depends(get_current_user_dep)):
    # Utilise la logique de calcul réelle basée sur la météo (localisation profil) et les cultures de l'utilisateur
    loc = current_user.localisation or "Dakar"
    return calculer_previsions(user_cultures=current_user.cultures_interet, localisation=loc, surface_ha=surface)
