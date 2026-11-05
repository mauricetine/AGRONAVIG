import os
import sys

for k, v in os.environ.items():
    try:
        k.encode('ascii')
        v.encode('ascii')
    except UnicodeEncodeError:
        print(f"NON-ASCII ENV: {k}={v.encode('utf-8')}")
