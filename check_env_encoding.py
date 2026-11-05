import os

def check_file(path):
    if not os.path.exists(path): return
    try:
        with open(path, 'rb') as f:
            content = f.read()
            content.decode('utf-8')
        print(f"UTF8 OK: {path}")
    except UnicodeDecodeError as e:
        print(f"NON-UTF8: {path} - {e}")

check_file('.env')
check_file('agronavig-backend/.env')
