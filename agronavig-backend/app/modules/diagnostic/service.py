import os
import uuid
import shutil
import json
import numpy as np
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import UploadFile
from app.models.diagnostic import Diagnostic
from app.modules.diagnostic.knowledge import get_disease_info
from app.modules.diagnostic.cache import get_prediction_cache, set_prediction_cache, invalidate_prediction_cache
from app.modules.diagnostic.context import get_current_season_senegal, get_recommendations_by_season

# Dossier d'upload persistant (adapte pour local Windows)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "diagnostics")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Chargement du modele IA
MODEL_PATH   = os.path.join(BASE_DIR, "models", "agronavig_model.h5")
CLASSES_PATH = os.path.join(BASE_DIR, "models", "classes.json")

model         = None
classes       = None

def load_model():
    global model, classes
    if model is None:
        try:
            import tensorflow as tf
            if os.path.exists(MODEL_PATH):
                model = tf.keras.models.load_model(MODEL_PATH)
                with open(CLASSES_PATH, "r") as f:
                    classes = json.load(f)
                print(f"SUCCESS: Modele IA charge - {len(classes)} classes")
            else:
                print(f"WARNING: Modele non trouve a {MODEL_PATH}")
        except Exception as e:
            print(f"WARNING: Erreur chargement modele : {e}")
            model   = None
            classes = None

# Charger au demarrage
load_model()

def get_niveau(confiance: float, classe: str) -> str:
    if "healthy" in classe:
        return "sain"
    if confiance >= 85:
        return "eleve"
    elif confiance >= 60:
        return "moyen"
    return "faible"

def save_image(file: UploadFile) -> str:
    ext      = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    path     = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return path

def predict_image_with_confidence(image_path: str) -> dict:
    """Prediction amelioree avec top 3 + reajustement de confiance"""
    if model is None or classes is None:
        return {
            "classe":        "Analyse non concluante (Modèle CNN absent)",
            "confiance":     0.0,
            "niveau":        "indéterminé",
            "top_3":         [
                {"classe": "Modèle non chargé", "score": 0.0}
            ]
        }
    try:
        import tensorflow as tf
        img = tf.keras.preprocessing.image.load_img(
            image_path,
            target_size=(224, 224)
        )
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        predictions  = model.predict(img_array, verbose=0)
        
        top_indices = np.argsort(predictions[0])[-3:][::-1]
        top_classes = [
            {
                "classe": classes.get(str(idx), "Unknown"),
                "score": float(predictions[0][idx]) * 100
            }
            for idx in top_indices
        ]
        
        best_classe = top_classes[0]["classe"]
        best_confiance = top_classes[0]["score"]
        
        for item in top_classes:
            if "healthy" in item["classe"].lower() and item["score"] > 15 and best_confiance < 60:
                best_classe = item["classe"]
                best_confiance = item["score"]
                break

        if best_confiance < 30:
            return {
                "classe":    "not_a_plant",
                "confiance": round(best_confiance, 2),
                "niveau":    "inconnu",
                "top_3":     top_classes,
            }

        return {
            "classe":    best_classe,
            "confiance": round(best_confiance, 2),
            "niveau":    get_niveau(best_confiance, best_classe),
            "top_3":     top_classes,
        }
    except Exception as e:
        print(f"Erreur prediction : {e}")
        return {
            "classe":    "Analyse non concluante (erreur du modèle CNN)",
            "confiance": 0.0,
            "niveau":    "indéterminé",
            "top_3":     [],
        }

def create_diagnostic(
    db: Session,
    user_id: int,
    culture: str,
    file: UploadFile
) -> Diagnostic:
    """Diagnostic complet avec cache, contexte saisonnier et validation"""
    image_path = save_image(file)

    # Verifier le cache avant prediction
    cache_key = f"{culture}_{os.path.basename(image_path)}"
    cached_prediction = get_prediction_cache(image_path, culture) # Utilise la signature correcte du cache
    
    if cached_prediction:
        prediction = cached_prediction
    else:
        prediction = predict_image_with_confidence(image_path)
        set_prediction_cache(image_path, culture, prediction)
    
    classe     = prediction["classe"]
    top_3      = prediction.get("top_3", [])
    
    warning = ""
    if culture.lower() not in classe.lower() and "healthy" not in classe.lower():
        warning = f"Attention : Vous avez selectionne '{culture}', mais l'IA detecte une pathologie typique du '{classe.split('___')[0]}'."

    info = get_disease_info(classe)
    current_season = get_current_season_senegal()
    seasonal_recommendations = get_recommendations_by_season(culture, classe, current_season)
    # Le module context renvoie une liste ; le diagnostic expose un contrat stable.
    seasonal_context = {
        "recommendations": seasonal_recommendations,
        "boost": 0,
        "penalty": 0,
        "season": current_season.value,
    }
    
    confidence_adjusted = prediction["confiance"]
    if seasonal_context and seasonal_context.get("boost"):
        confidence_adjusted = min(100, confidence_adjusted + seasonal_context["boost"])
    elif seasonal_context and seasonal_context.get("penalty"):
        confidence_adjusted = max(0, confidence_adjusted - seasonal_context["penalty"])

    diagnostic = Diagnostic(
        user_id=user_id,
        culture=culture,
        maladie=info["nom"],
        confiance=prediction["confiance"],
        niveau=prediction["niveau"],
        traitement=json.dumps(info["traitements"]),
        image_path=image_path,
        description=warning + "\n\n" + info["description"] if warning else info["description"],
        top_predictions=top_3, # Le modele est JSON
        validated_by_user=False,
        user_feedback=None,
        metadata_json={ # Renomme metadata -> metadata_json
            "season": current_season,
            "confidence_adjusted": round(confidence_adjusted, 2),
            "seasonal_boost_penalty": seasonal_context.get("boost") or -seasonal_context.get("penalty", 0) if seasonal_context else 0,
            "seasonal_recommendations": seasonal_context.get("recommendations", []) if seasonal_context else []
        }
    )
    
    db.add(diagnostic)
    db.commit()
    db.refresh(diagnostic)
    
    diagnostic.symptomes   = info["symptomes"]
    diagnostic.prevention  = info["prevention"]
    diagnostic.traitements = info["traitements"]
    diagnostic.confidence_adjusted = round(confidence_adjusted, 2)
    diagnostic.seasonal_context = seasonal_context
    
    return diagnostic

def get_diagnostics_by_user(db: Session, user_id: int, limit: int = 50, offset: int = 0) -> dict:
    diagnostics = db.query(Diagnostic)\
        .filter(Diagnostic.user_id == user_id)\
        .order_by(desc(Diagnostic.created_at))\
        .limit(limit)\
        .offset(offset)\
        .all()
    
    total = db.query(Diagnostic)\
        .filter(Diagnostic.user_id == user_id)\
        .count()
    
    return {
        "total": total,
        "count": len(diagnostics),
        "diagnostics": diagnostics
    }

def validate_diagnostic(db: Session, diagnostic_id: int, user_feedback: dict) -> Diagnostic:
    diagnostic = db.query(Diagnostic).filter(Diagnostic.id == diagnostic_id).first()
    if not diagnostic:
        return None
    
    diagnostic.validated_by_user = True
    diagnostic.user_feedback = user_feedback.get("status")
    
    db.commit()
    db.refresh(diagnostic)
    return diagnostic

def compare_diagnostics(db: Session, id1: int, id2: int) -> dict:
    d1 = db.query(Diagnostic).filter(Diagnostic.id == id1).first()
    d2 = db.query(Diagnostic).filter(Diagnostic.id == id2).first()
    
    if not d1 or not d2:
        return {"error": "Diagnostics non trouves"}
        
    return {
        "diag1": d1,
        "diag2": d2,
        "evolution": "Amelioration" if d2.confiance < d1.confiance and "healthy" in d2.maladie.lower() else "Stable"
    }

def get_disease_progression(db: Session, user_id: int, culture: str, limit: int = 10) -> list:
    return db.query(Diagnostic)\
        .filter(Diagnostic.user_id == user_id, Diagnostic.culture == culture)\
        .order_by(Diagnostic.created_at.asc())\
        .limit(limit)\
        .all()

def get_user_diagnostic_stats(db: Session, user_id: int) -> dict:
    diagnostics = db.query(Diagnostic).filter(Diagnostic.user_id == user_id).all()
    stats = {
        "total": len(diagnostics),
        "cultures": {},
        "maladies": {}
    }
    for d in diagnostics:
        stats["cultures"][d.culture] = stats["cultures"].get(d.culture, 0) + 1
        stats["maladies"][d.maladie] = stats["maladies"].get(d.maladie, 0) + 1
    return stats
