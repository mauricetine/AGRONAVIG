import psycopg2

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        host="127.0.0.1"
    )
    print("SUCCESS")
    conn.close()
except Exception as e:
    print(f"FAILED: {e}")
