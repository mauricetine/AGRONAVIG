from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.modules.auth.schemas import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token

def register_user(db: Session, data: UserCreate):
    # Vérifier si email déjà utilisé
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet email est déjà utilisé"
        )
    # Créer l'utilisateur
    # Forcer admin si l'email est admin@agronavig.com
    user_role = data.role
    if data.email == "admin@agronavig.com":
        user_role = "admin"
        
    user = User(
        nom=data.nom,
        email=data.email,
        password=hash_password(data.password),
        role=user_role,
        telephone=data.telephone,
        localisation=data.localisation,
        cultures_interet=data.cultures_interet
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(db: Session, data: UserLogin):
    # Vérifier email
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )
    # Vérifier mot de passe
    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )
    # Générer token JWT
    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": token, "token_type": "bearer", "user": user}

def get_current_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable"
        )
    return user