import psycopg2

try:
    # On tente une connexion minimale sans host pour voir si ça change quelque chose (via socket/pipe local)
    conn = psycopg2.connect(
        dbname="agronavig",
        user="postgres",
        password="postgres"
    )
    print("SUCCESS: Connected via local pipe")
    conn.close()
except Exception as e:
    print(f"ERROR Local: {e}")
