import sys
import os

# Ajouter le chemin du backend
sys.path.insert(0, os.path.join(os.getcwd(), 'agronavig-backend'))

from app.modules.conseil.service import generer_conseil

try:
    print("Appel de generer_conseil...")
    reponse = generer_conseil("Comment traiter le mildiou de la tomate ?", culture="tomate")
    print("SUCCESS: Reponse du service conseil recue")
    print(f"Conseil: {reponse[:200]}...")
except Exception as e:
    print(f"ERROR: {e}")
