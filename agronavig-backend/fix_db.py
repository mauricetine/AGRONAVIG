import os
import sys
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import text
from app.database.db import engine, SessionLocal
from app.models.user import User
from app.core.security import hash_password

def fix():
    with engine.connect() as conn:
        print("Mise a jour de la table users...")
        # Ajouter les colonnes si elles n'existent pas
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR DEFAULT 'producteur'"))
            conn.execute(text("ALTER TABLE users ADD COLUMN telephone VARCHAR"))
            conn.execute(text("ALTER TABLE users ADD COLUMN localisation VARCHAR"))
            conn.execute(text("ALTER TABLE users ADD COLUMN cultures_interet VARCHAR"))
            conn.commit()
            print("Colonnes ajoutees avec succes.")
        except Exception as e:
            print(f"Note: {e}")

    db = SessionLocal()
    try:
        # Créer l'admin par défaut
        admin_email = "admin@agronavig.com"
        existing = db.query(User).filter(User.email == admin_email).first()
        if not existing:
            admin = User(
                nom="Administrateur AgroNavig",
                email=admin_email,
                password=hash_password("admin123"),
                role="admin",
                telephone="770000000",
                localisation="Dakar, Senegal",
                cultures_interet="toutes"
            )
            db.add(admin)
            db.commit()
            print(f"Compte Administrateur cree : {admin_email} / admin123")
        else:
            print("Le compte admin existe deja.")
    finally:
        db.close()

if __name__ == "__main__":
    fix()
