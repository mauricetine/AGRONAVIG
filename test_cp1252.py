import psycopg2
import sys

try:
    conn = psycopg2.connect(
        dbname="agronavig",
        user="postgres",
        password="postgres",
        host="127.0.0.1",
        port="5432"
    )
    # Tenter de changer l'encodage apres connexion
    conn.set_client_encoding('UTF8')
    print("SUCCESS")
    conn.close()
except UnicodeDecodeError as e:
    print(f"DECODE ERROR: {e}")
    print(f"Byte at error: {e.object[e.start:e.end]}")
    # Tenter de decoder avec cp1252 pour voir le message
    try:
        msg = e.object.decode('cp1252')
        print(f"Decoded with CP1252: {msg}")
    except:
        pass
except Exception as e:
    print(f"OTHER ERROR: {e}")
