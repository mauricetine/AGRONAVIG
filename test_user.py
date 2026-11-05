import psycopg2
import os

user = os.getlogin()
print(f"Testing with Windows user: {user}")

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user=user,
        host="127.0.0.1",
        port="5432"
    )
    print(f"SUCCESS: Connected as {user}")
    conn.close()
except Exception as e:
    print(f"FAILED: {e}")
