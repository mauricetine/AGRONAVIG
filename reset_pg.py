import subprocess
import os

psql = r"C:\Program Files\PostgreSQL\18\bin\psql.exe"
# Tenter de se connecter via l'utilisateur systeme si trust est active pour local
cmd = f'"{psql}" -U postgres -d postgres -c "ALTER USER postgres PASSWORD \'postgres\';"'

try:
    out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    print("SUCCESS: Password reset to 'postgres'")
except Exception as e:
    print(f"FAILED: {e}")
