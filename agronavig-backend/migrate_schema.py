"""Migration locale non destructive pour AgroNavig.

Ajoute uniquement les colonnes introduites après la création initiale des tables.
Le script peut être exécuté plusieurs fois grâce à IF NOT EXISTS.
"""
from sqlalchemy import text
from app.database.db import engine

STATEMENTS = (
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS latitude DOUBLE PRECISION",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS longitude DOUBLE PRECISION",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS region VARCHAR",
    "ALTER TABLE previsions ADD COLUMN IF NOT EXISTS rendement_min DOUBLE PRECISION",
    "ALTER TABLE previsions ADD COLUMN IF NOT EXISTS rendement_max DOUBLE PRECISION",
    "ALTER TABLE previsions ADD COLUMN IF NOT EXISTS etp_estimee DOUBLE PRECISION",
    "ALTER TABLE previsions ADD COLUMN IF NOT EXISTS stress_hydrique DOUBLE PRECISION",
    "ALTER TABLE previsions ADD COLUMN IF NOT EXISTS confiance DOUBLE PRECISION DEFAULT 85.0",
    "ALTER TABLE diagnostics ADD COLUMN IF NOT EXISTS description TEXT",
    "ALTER TABLE diagnostics ADD COLUMN IF NOT EXISTS top_predictions JSONB",
    "ALTER TABLE diagnostics ADD COLUMN IF NOT EXISTS validated_by_user BOOLEAN DEFAULT FALSE",
    "ALTER TABLE diagnostics ADD COLUMN IF NOT EXISTS user_feedback VARCHAR",
    "ALTER TABLE diagnostics ADD COLUMN IF NOT EXISTS metadata_json JSONB",
    "ALTER TABLE diagnostics ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE",
    "ALTER TABLE diagnostics ADD COLUMN IF NOT EXISTS agronome_validated BOOLEAN DEFAULT FALSE",
    "ALTER TABLE diagnostics ADD COLUMN IF NOT EXISTS agronome_comment TEXT",
    "ALTER TABLE diagnostics ADD COLUMN IF NOT EXISTS validated_at TIMESTAMP WITH TIME ZONE",
)


def main() -> None:
    with engine.begin() as connection:
        for statement in STATEMENTS:
            connection.execute(text(statement))
            print(f"OK: {statement}")
    print("Migration AgroNavig terminée.")


if __name__ == "__main__":
    main()
