import psycopg2

passwords = ["postgres", "admin", "root", "password", "agronavig", "123456", ""]

for pw in passwords:
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password=pw,
            host="127.0.0.1",
            port="5432",
            connect_timeout=2
        )
        print(f"SUCCESS with password: '{pw}'")
        conn.close()
        break
    except Exception as e:
        print(f"FAILED with password: '{pw}'")
