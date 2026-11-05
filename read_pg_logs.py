import os
import glob

log_dir = r"C:\Program Files\PostgreSQL\18\data\log"
logs = glob.glob(os.path.join(log_dir, "*.log"))
if logs:
    latest_log = max(logs, key=os.path.getmtime)
    print(f"Reading {latest_log}...")
    with open(latest_log, 'r', encoding='cp1252', errors='ignore') as f:
        lines = f.readlines()
        for line in lines[-50:]:
            print(line.strip())
else:
    print("No logs found")
