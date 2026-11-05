import os

paths = [
    r"C:\Program Files\PostgreSQL\18\bin\psql.exe",
    r"C:\Program Files\PostgreSQL\17\bin\psql.exe",
    r"C:\Program Files\PostgreSQL\16\bin\psql.exe",
    r"C:\Program Files\PostgreSQL\15\bin\psql.exe"
]

for p in paths:
    if os.path.exists(p):
        print(f"FOUND: {p}")
