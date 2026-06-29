import requests
from app.core.config import settings
from app.core.cache import cache

JOURS_FR = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

def get_meteo(ville: str = "Dakar") -> dict:
    # 1. Tenter de récupérer depuis le cache Redis
    cache_key = f"meteo_{ville.lower()}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    if not settings.OPENWEATHERMAP_API_KEY:
        return _meteo_simulee(ville)

    try:
        # Météo actuelle
        url_current = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q":     ville,
            "appid": settings.OPENWEATHERMAP_API_KEY,
            "units": "metric",
            "lang":  "fr"
        }
        res = requests.get(url_current, params=params, timeout=5)
        data = res.json()

        if res.status_code != 200:
            return _meteo_simulee(ville)

        # Prévisions 7 jours
        url_forecast = "https://api.openweathermap.org/data/2.5/forecast"
        res_f = requests.get(url_forecast, params=params, timeout=5)
        forecast_data = res_f.json()

        # Extraire 7 jours (1 entrée par jour à midi)
        previsions = []
        jours_vus  = set()
        for item in forecast_data.get("list", []):
            from datetime import datetime
            dt   = datetime.fromtimestamp(item["dt"])
            jour = dt.strftime("%Y-%m-%d")
            if jour not in jours_vus and len(previsions) < 7:
                jours_vus.add(jour)
                previsions.append({
                    "jour": JOURS_FR[dt.weekday()],
                    "temp": round(item["main"]["temp"]),
                    "icon": _icon_emoji(item["weather"][0]["icon"]),
                })

        result = {
            "ville":       f"{data['name']}, Sénégal",
            "temperature": round(data["main"]["temp"]),
            "ressenti":    round(data["main"]["feels_like"]),
            "humidite":    data["main"]["humidity"],
            "vent":        round(data["wind"]["speed"] * 3.6),
            "condition":   data["weather"][0]["description"].capitalize(),
            "icon":        _icon_emoji(data["weather"][0]["icon"]),
            "previsions":  previsions,
        }

        # 2. Mettre en cache pour 30 minutes (1800 secondes)
        cache.set(cache_key, result, expire=1800)
        return result

    except Exception as e:
        print(f"Erreur météo : {e}")
        return _meteo_simulee(ville)


def _icon_emoji(icon_code: str) -> str:
    mapping = {
        "01d": "☀️",  "01n": "🌙",
        "02d": "⛅",  "02n": "⛅",
        "03d": "☁️",  "03n": "☁️",
        "04d": "☁️",  "04n": "☁️",
        "09d": "🌧️", "09n": "🌧️",
        "10d": "🌦️", "10n": "🌧️",
        "11d": "⛈️", "11n": "⛈️",
        "13d": "❄️",  "13n": "❄️",
        "50d": "🌫️", "50n": "🌫️",
    }
    return mapping.get(icon_code, "⛅")


def _meteo_simulee(ville: str) -> dict:
    return {
        "ville":       f"{ville}, Sénégal",
        "temperature": 28,
        "ressenti":    31,
        "humidite":    74,
        "vent":        18,
        "condition":   "Partiellement nuageux",
        "icon":        "⛅",
        "previsions": [
            {"jour": "Lun", "temp": 28, "icon": "☀️"},
            {"jour": "Mar", "temp": 29, "icon": "⛅"},
            {"jour": "Mer", "temp": 27, "icon": "🌧️"},
            {"jour": "Jeu", "temp": 26, "icon": "🌧️"},
            {"jour": "Ven", "temp": 28, "icon": "⛅"},
            {"jour": "Sam", "temp": 30, "icon": "☀️"},
            {"jour": "Dim", "temp": 31, "icon": "☀️"},
        ]
    }