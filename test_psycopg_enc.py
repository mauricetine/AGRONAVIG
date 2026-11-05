import psycopg2
import sys

print(f"Default encoding: {sys.getdefaultencoding()}")
print(f"FileSystem encoding: {sys.getfilesystemencoding()}")

try:
    # Tenter de forcer l'encodage au niveau de la connexion
    conn = psycopg2.connect(
        dbname="agronavig",
        user="postgres",
        password="postgres",
        host="127.0.0.1",
        port="5432",
        client_encoding="utf-8"
    )
    print("SUCCESS with client_encoding=utf-8")
    conn.close()
except Exception as e:
    print(f"ERROR UTF-8: {e}")

try:
    conn = psycopg2.connect(
        dbname="agronavig",
        user="postgres",
        password="postgres",
        host="127.0.0.1",
        port="5432",
        client_encoding="latin1"
    )
    print("SUCCESS with client_encoding=latin1")
    conn.close()
except Exception as e:
    print(f"ERROR Latin1: {e}")
