from fastapi import APIRouter, Query, Depends
from app.modules.meteo.service import get_meteo
from app.modules.auth.router import get_current_user_dep

router = APIRouter()

@router.get("/")
def meteo(ville: str = None, current_user = Depends(get_current_user_dep)):
    loc = ville or current_user.localisation or "Dakar"
    return get_meteo(loc)