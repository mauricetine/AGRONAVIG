import psycopg2
import sys

print(f"Python version: {sys.version}")
print(f"Encoding: {sys.getdefaultencoding()}")

try:
    print("Tentative de connexion pure...")
    conn = psycopg2.connect(
        dbname="agronavig",
        user="postgres",
        password="postgres",
        host="127.0.0.1",
        port="5432"
    )
    print("SUCCESS: Connexion etablie")
    conn.close()
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
