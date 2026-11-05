import subprocess

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode('cp1252')
    except Exception as e:
        return str(e)

# Utiliser psql avec l'utilisateur actuel si possible, ou tenter de voir si pg_lsclusters existe (non sur windows)
print(run('psql -U postgres -c "SELECT usename FROM pg_user;"'))
