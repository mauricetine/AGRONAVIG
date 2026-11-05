from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
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

# Synchroniser les colonnes ajoutées après la création initiale de la base.
# IF NOT EXISTS rend cette migration répétable et non destructive.
def _sync_schema():
    statements = (
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS latitude DOUBLE PRECISION",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS longitude DOUBLE PRECISION",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS region VARCHAR",
        "ALTER TABLE previsions ADD COLUMN IF NOT EXISTS rendement_min DOUBLE PRECISION",
        "ALTER TABLE previsions ADD COLUMN IF NOT EXISTS rendement_max DOUBLE PRECISION",
        "ALTER TABLE previsions ADD COLUMN IF NOT EXISTS etp_estimee DOUBLE PRECISION",
        "ALTER TABLE previsions ADD COLUMN IF NOT EXISTS stress_hydrique DOUBLE PRECISION",
        "ALTER TABLE previsions ADD COLUMN IF NOT EXISTS confiance DOUBLE PRECISION DEFAULT 85.0",
        "ALTER TABLE diagnostics ADD COLUMN IF NOT EXISTS description TEXT",
        "ALTER TABLE diagnostics ADD COLUMN IF NOT EXISTS top_predictions JSONB",
        "ALTER TABLE diagnostics ADD COLUMN IF NOT EXISTS validated_by_user BOOLEAN DEFAULT FALSE",
        "ALTER TABLE diagnostics ADD COLUMN IF NOT EXISTS user_feedback VARCHAR",
        "ALTER TABLE diagnostics ADD COLUMN IF NOT EXISTS metadata_json JSONB",
        "ALTER TABLE diagnostics ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE",
        "ALTER TABLE diagnostics ADD COLUMN IF NOT EXISTS agronome_validated BOOLEAN DEFAULT FALSE",
        "ALTER TABLE diagnostics ADD COLUMN IF NOT EXISTS agronome_comment TEXT",
        "ALTER TABLE diagnostics ADD COLUMN IF NOT EXISTS validated_at TIMESTAMP WITH TIME ZONE",
    )
    try:
        with engine.begin() as connection:
            for statement in statements:
                connection.execute(text(statement))
        print("SUCCESS: Schema utilisateurs synchronisé")
    except Exception as exc:
        print(f"WARNING: Synchronisation schema non effectuée: {exc}")


_sync_schema()

app = FastAPI(
    title="AgroNavig API",
    description="Plateforme agricole intelligente - ISI Dakar",
    version="1.0.0"
)

import os

origins_env = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
origins = [o.strip() for o in origins_env.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
    return {"message": "AgroNavig API operationnelle"}