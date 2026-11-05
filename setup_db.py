import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def setup():
    try:
        # Connexion à la base 'postgres' par défaut pour créer la nouvelle base
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="3218",
            host="127.0.0.1",
            port="5432"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Vérifier si la base existe
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'agronavig'")
        exists = cur.fetchone()
        
        if not exists:
            print("Création de la base de données 'agronavig'...")
            cur.execute("CREATE DATABASE agronavig")
            print("Base de données créée avec succès.")
        else:
            print("La base de données 'agronavig' existe déjà.")
            
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Erreur lors de la configuration de la base de données : {e}")
        return False

if __name__ == "__main__":
    setup()
