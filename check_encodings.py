import os

def check_file(path):
    try:
        with open(path, 'rb') as f:
            content = f.read()
            content.decode('utf-8')
        return True, None
    except UnicodeDecodeError as e:
        return False, str(e)

root = 'agronavig-backend/app'
for r, d, files in os.walk(root):
    for f in files:
        if f.endswith('.py'):
            full_path = os.path.join(r, f)
            ok, err = check_file(full_path)
            if not ok:
                print(f"NON-UTF8: {full_path} - {err}")
