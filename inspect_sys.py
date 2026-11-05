import os
import subprocess

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode('cp1252')
    except Exception as e:
        return str(e)

print("--- REGISTRY PG ---")
print(run('reg query "HKLM\\SOFTWARE\\PostgreSQL" /s'))

print("--- SERVICES ---")
print(run('sc query postgresql-x64-16')) # Ajuster la version si besoin
