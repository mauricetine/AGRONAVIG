from sqlalchemy.orm import Session
from app.models.user import User
from app.models.diagnostic import Diagnostic
from sqlalchemy import func

def get_global_stats(db: Session):
    total_users = db.query(User).count()
    total_diagnostics = db.query(Diagnostic).count()
    
    # Répartition par rôle
    roles = db.query(User.role, func.count(User.id)).group_by(User.role).all()
    roles_stats = {role: count for role, count in roles}
    
    # Maladies les plus fréquentes
    top_maladies = db.query(Diagnostic.maladie, func.count(Diagnostic.id))\
        .group_by(Diagnostic.maladie)\
        .order_by(func.count(Diagnostic.id).desc())\
        .limit(5).all()
    
    return {
        "total_users": total_users,
        "total_diagnostics": total_diagnostics,
        "roles_distribution": roles_stats,
        "top_maladies": [{"nom": m, "count": c} for m, c in top_maladies]
    }

def get_all_users(db: Session):
    return db.query(User).all()

def toggle_user_status(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.is_active = not user.is_active
        db.commit()
        db.refresh(user)
        return user
    return None

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        # Supprimer les diagnostics liés d'abord pour éviter l'erreur de clé étrangère
        db.query(Diagnostic).filter(Diagnostic.user_id == user_id).delete()
        db.delete(user)
        db.commit()
        return True
    return False
