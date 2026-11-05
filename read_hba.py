import os

hba_path = r"C:\Program Files\PostgreSQL\18\data\pg_hba.conf"
if os.path.exists(hba_path):
    print(f"Reading {hba_path}...")
    with open(hba_path, 'r') as f:
        for line in f:
            if not line.startswith('#') and line.strip():
                print(line.strip())
else:
    print("pg_hba.conf not found")
