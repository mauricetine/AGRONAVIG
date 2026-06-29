from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.modules.auth.router import get_current_user_dep
from app.modules.conseil.service import generer_conseil

router = APIRouter()

class MessageRequest(BaseModel):
    message: str
    culture: str = ""

@router.post("/message")
def message(
    req: MessageRequest,
    current_user=Depends(get_current_user_dep)
):
    reponse = generer_conseil(req.message, req.culture)
    return {
        "reponse": reponse,
        "culture": req.culture or "générale",
        "user":    current_user.nom
    }