from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.modules.auth.schemas import UserCreate, UserLogin, TokenResponse, UserResponse
from app.modules.auth.service import register_user, login_user
from app.core.security import decode_token, create_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

def get_current_user_dep(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expire"
        )
    from app.models.user import User
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur introuvable"
        )
    return user

# Endpoint OAuth2 compatible Swagger (formulaire username/password)
@router.post("/token")
def token_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    from app.modules.auth.schemas import UserLogin
    data = UserLogin(email=form_data.username, password=form_data.password)
    result = login_user(db, data)
    return {
        "access_token": result["access_token"],
        "token_type": "bearer"
    }

# Endpoint login JSON (pour le frontend React)
@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, data)

# Endpoint register
@router.post("/register", response_model=TokenResponse)
def register(data: UserCreate, db: Session = Depends(get_db)):
    user = register_user(db, data)
    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": token, "token_type": "bearer", "user": user}

# Endpoint profil utilisateur connecte
@router.get("/me", response_model=UserResponse)
def me(current_user=Depends(get_current_user_dep)):
    return current_user