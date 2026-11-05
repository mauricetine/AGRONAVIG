import psycopg2
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), 'agronavig-backend', '.env'))
url = os.getenv('DATABASE_URL')
print(f"Tentative de connexion a: {url}")

try:
    # Extraire les composants manuellement pour eviter les problemes d'encodage de la chaine DSN
    # postgresql://postgres:postgres@localhost:5432/agronavig
    conn = psycopg2.connect(
        dbname="agronavig",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    print("SUCCESS: Connexion etablie")
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
