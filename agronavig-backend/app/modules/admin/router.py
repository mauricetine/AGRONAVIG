from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.modules.auth.router import get_current_user_dep
from app.modules.admin.service import get_global_stats, get_all_users

router = APIRouter()

def check_admin(current_user = Depends(get_current_user_dep)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acces reserve aux administrateurs")
    return current_user

@router.get("/stats")
def stats(db: Session = Depends(get_db), admin = Depends(check_admin)):
    return get_global_stats(db)

@router.get("/users")
def users(db: Session = Depends(get_db), admin = Depends(check_admin)):
    return get_all_users(db)

@router.post("/users/{user_id}/toggle")
def toggle_user(user_id: int, db: Session = Depends(get_db), admin = Depends(check_admin)):
    from app.modules.admin.service import toggle_user_status
    return toggle_user_status(db, user_id)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin = Depends(check_admin)):
    from app.modules.admin.service import delete_user as du
    return du(db, user_id)
