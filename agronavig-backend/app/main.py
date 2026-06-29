from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import Base, engine
from app.models import User, Diagnostic, Prevision
from app.modules.auth.router import router as auth_router
from app.modules.diagnostic.router import router as diagnostic_router
from app.modules.prevision.router import router as prevision_router
from app.modules.conseil.router import router as conseil_router
from app.modules.rapport.router import router as rapport_router
from app.modules.meteo.router import router as meteo_router
from app.modules.admin.router import router as admin_router

# Créer les tables automatiquement
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AgroNavig API",
    description="Plateforme agricole intelligente — ISI Dakar",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router,       prefix="/api/auth",       tags=["Auth"])
app.include_router(diagnostic_router, prefix="/api/diagnostic", tags=["Diagnostic"])
app.include_router(prevision_router,  prefix="/api/prevision",  tags=["Prévision"])
app.include_router(conseil_router,    prefix="/api/conseil",    tags=["Conseil IA"])
app.include_router(rapport_router,    prefix="/api/rapport",    tags=["Rapport"])
app.include_router(meteo_router,      prefix="/api/meteo",      tags=["Météo"])
app.include_router(admin_router,      prefix="/api/admin",      tags=["Admin"])

@app.get("/")
def root():
    return {"message": "AgroNavig API opérationnelle 🌱"}