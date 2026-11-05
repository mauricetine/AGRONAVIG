from sqlalchemy import create_engine
import sys

url = "postgresql://postgres:postgres@127.0.0.1:5432/agronavig"
print(f"Testing SQLAlchemy with {url}")

try:
    engine = create_engine(url)
    with engine.connect() as conn:
        print("SUCCESS: SQLAlchemy connected")
except Exception as e:
    print(f"ERROR: {e}")
