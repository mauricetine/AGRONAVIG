import psycopg2

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="HP",
        password="HP",
        host="127.0.0.1",
        port="5432"
    )
    print("SUCCESS: Connected as HP")
    conn.close()
except Exception as e:
    print(f"FAILED: {e}")
