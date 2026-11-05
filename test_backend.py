import sys
import os
# Ajouter le chemin du backend
backend_path = os.path.join(os.getcwd(), 'agronavig-backend')
sys.path.insert(0, backend_path)

print(f"Test de chargement depuis: {backend_path}")

try:
    from app.main import app
    print('SUCCESS: Backend charge avec succes')
except Exception as e:
    print(f'ERROR: Erreur lors du chargement: {e}')
    import traceback
    traceback.print_exc()
