# -*- coding: utf-8 -*-
from datetime import datetime
from enum import Enum

class Saison(str, Enum):
    HIVERNAGE = "hivernage"
    SECHE = "seche"
    TRANSITION = "transition"

def get_current_season_senegal() -> Saison:
    """Detecte la saison actuelle au Senegal"""
    month = datetime.now().month
    if month in [6, 7, 8, 9]:
        return Saison.HIVERNAGE
    elif month in [12, 1, 2]:
        return Saison.SECHE
    else:
        return Saison.TRANSITION

def get_recommendations_by_season(culture: str, maladie: str, saison: Saison) -> list:
    """Recommandations contextuelles basees sur la saison"""
    recommendations = {
        ("Tomato", "Mildiou", Saison.HIVERNAGE): [
            "Tres haut risque en saison des pluies",
            "Augmentez la frequence des traitements fongicides",
            "Assurez une bonne ventilation et aeration",
            "Eliminez les feuilles infectees immediatement"
        ],
        ("Tomato", "TYLCV", Saison.SECHE): [
            "Risque modere en saison seche",
            "Renforcez la lutte contre les mouches blanches",
            "Utilisez des filets anti-insectes"
        ],
        ("Corn", "Cercosporiose", Saison.HIVERNAGE): [
            "Forte pression en saison humide",
            "Espacez les rangs pour meilleure circulation d'air",
            "Alternez les fongicides pour eviter resistance"
        ],
        ("Potato", "Mildiou", Saison.HIVERNAGE): [
            "URGENT : Mildiou tres agressif en saison des pluies",
            "Traitement obligatoire a titre preventif",
            "Verifiez les varietes resistantes pour prochaine saison"
        ],
    }
    
    key = (culture, maladie, saison)
    return recommendations.get(key, [
        f"Maladie detectee en saison {saison.value}",
        "Suivez le traitement recommande strictement",
        "Surveillez l'evolution de la culture"
    ])

WEATHER_CONTEXTS = {
    "high_humidity": {
        "icon": "H",
        "message": "Conditions humides detectees",
        "action": "Augmentez la frequence des traitements fongicides"
    },
    "dry_season": {
        "icon": "S",
        "message": "Periode seche",
        "action": "Optimisez l'irrigation et la lutte contre les acariens"
    },
    "rain_season": {
        "icon": "P",
        "message": "Saison des pluies - Risque eleve",
        "action": "Vigilance maximale contre les maladies fongiques"
    }
}
