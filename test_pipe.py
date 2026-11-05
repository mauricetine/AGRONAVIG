import psycopg2

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres"
    )
    print("SUCCESS: Connected via pipe")
    conn.close()
except Exception as e:
    print(f"FAILED: {e}")
