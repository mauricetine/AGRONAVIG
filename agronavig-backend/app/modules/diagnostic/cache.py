# -*- coding: utf-8 -*-
import json
import hashlib
from datetime import datetime, timedelta
from app.core.cache import cache

CACHE_EXPIRY = 86400  # 24 heures

def get_image_cache_key(image_hash: str, culture: str) -> str:
    return f"diag:image:{image_hash}:{culture}"

def get_prediction_cache(image_path: str, culture: str) -> dict | None:
    """Récupère une prédiction en cache"""
    try:
        with open(image_path, "rb") as f:
            image_hash = hashlib.sha256(f.read()).hexdigest()
        cache_key = get_image_cache_key(image_hash, culture)
        cached = cache.get(cache_key)
        if cached:
            return cached
    except Exception:
        pass
    return None

def set_prediction_cache(image_path: str, culture: str, prediction: dict) -> None:
    """Stocke une prédiction en cache"""
    try:
        with open(image_path, "rb") as f:
            image_hash = hashlib.sha256(f.read()).hexdigest()
        cache_key = get_image_cache_key(image_hash, culture)
        cache.set(cache_key, prediction, expire=CACHE_EXPIRY)
    except Exception:
        pass

def invalidate_prediction_cache(image_path: str, culture: str) -> None:
    """Invalide le cache d'une prédiction"""
    try:
        with open(image_path, "rb") as f:
            image_hash = hashlib.sha256(f.read()).hexdigest()
        cache_key = get_image_cache_key(image_hash, culture)
        cache.delete(cache_key)
    except Exception:
        pass
