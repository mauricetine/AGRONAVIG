from datetime import datetime, timezone
from types import SimpleNamespace
import sys
from pathlib import Path

backend = Path(__file__).parent / "agronavig-backend"
sys.path.insert(0, str(backend))

from app.modules.diagnostic.schemas import DiagnosticResponse
from app.core.cache import CacheService

obj = SimpleNamespace(
    id=1,
    culture="Tomato",
    maladie="Tomato___Late_blight",
    confiance=63.75,
    niveau="moyen",
    traitement=None,
    image_path=None,
    created_at=datetime.now(timezone.utc),
    description="Test",
    symptomes=[],
    prevention=[],
    traitements=[],
    top_predictions=[
        {"score": 63.75, "classe": "Tomato___Late_blight"},
        {"score": 23.62, "classe": "Tomato___Septoria_leaf_spot"},
    ],
    validated_by_user=False,
    user_feedback=None,
    metadata_json={"model": "MobileNetV2"},
    confidence_adjusted=None,
    seasonal_context=None,
)

result = DiagnosticResponse.model_validate(obj, from_attributes=True)
assert result.top_predictions[0]["classe"] == "Tomato___Late_blight"
assert result.metadata_json["model"] == "MobileNetV2"

cache = CacheService()
cache.set("test-key", {"ok": True})
assert cache.get("test-key") == {"ok": True}
cache.delete("test-key")
assert cache.get("test-key") is None

print("OK: contrat diagnostic et fallback cache valides")
