import os
import sys
from sqlalchemy import text
from dotenv import load_dotenv
load_dotenv()

# Configurer le chemin
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from app.database.db import SessionLocal, engine
from app.models.user import User
from app.models.diagnostic import Diagnostic

def check():
    print("--- Diagnostic Base de Données ---")
    try:
        # Test connexion simple
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("✅ Connexion au serveur PostgreSQL : OK")
        
        db = SessionLocal()
        try:
            user_count = db.query(User).count()
            diag_count = db.query(Diagnostic).count()
            print(f"✅ Table Users : {user_count} enregistrements")
            print(f"✅ Table Diagnostics : {diag_count} enregistrements")
            
            if user_count > 0:
                users = db.query(User).all()
                for u in users:
                    print(f"   - Utilisateur: {u.nom} ({u.email})")
            else:
                print("⚠️ Aucun utilisateur trouvé. C'est normal si vous ne vous êtes pas encore inscrit.")
                
        except Exception as e:
            print(f"❌ Erreur lors de la lecture des tables : {e}")
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")
        print("\nVérifiez que :")
        print("1. PostgreSQL est lancé")
        print("2. La base de données 'agronavig' existe")
        print("3. Les identifiants dans .env sont corrects (actuel: postgres:3218)")

if __name__ == "__main__":
    check()
