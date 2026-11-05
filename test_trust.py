import psycopg2

try:
    # Si pg_hba.conf est en 'trust' pour 127.0.0.1, le mot de passe n'est pas requis
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        host="127.0.0.1",
        port="5432"
    )
    print("SUCCESS: Connected without password (trust)")
    conn.close()
except Exception as e:
    print(f"FAILED: {e}")
