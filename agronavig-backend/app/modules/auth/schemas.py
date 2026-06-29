from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    nom: str
    email: EmailStr
    password: str
    role: str = "producteur"
    telephone: str = None
    localisation: str = None
    cultures_interet: str = "tomate,oignon,maïs"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    nom: str
    email: str
    role: str
    telephone: str = None
    localisation: str = None
    cultures_interet: str = None
    is_active: bool

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse