import psycopg2

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        host="localhost"
    )
    print("SUCCESS")
    conn.close()
except Exception as e:
    print(f"FAILED: {e}")
