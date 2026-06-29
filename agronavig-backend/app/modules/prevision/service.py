# -*- coding: utf-8 -*-
from app.modules.meteo.service import get_meteo

RENDEMENTS_BASE = {
    "tomate":    {"tonnes_ha": 35, "prix_kg": 400, "eau_l_jour": 5, "cycle": 120},
    "oignon":    {"tonnes_ha": 30, "prix_kg": 350, "eau_l_jour": 4, "cycle": 150},
    "maïs":      {"tonnes_ha": 5,  "prix_kg": 250, "eau_l_jour": 3, "cycle": 90},
    "riz":       {"tonnes_ha": 7,  "prix_kg": 325, "eau_l_jour": 12, "cycle": 120},
    "pomme de terre": {"tonnes_ha": 25, "prix_kg": 450, "eau_l_jour": 4, "cycle": 110},
    "arachide":  {"tonnes_ha": 1.5, "prix_kg": 300, "eau_l_jour": 2, "cycle": 100},
}

def calculer_previsions(user_cultures: str = None, localisation: str = "Dakar", surface_ha: float = 1.0):
    meteo = get_meteo(localisation)
    temp  = meteo["temperature"]
    hum   = meteo["humidite"]
    
    # Déterminer les cultures à analyser
    cultures_to_check = RENDEMENTS_BASE.keys()
    if user_cultures:
        # Nettoyer et filtrer les cultures de l'utilisateur
        user_list = [c.strip().lower() for c in user_cultures.split(",")]
        cultures_to_check = [c for c in RENDEMENTS_BASE.keys() if c in user_list]
        # Si aucune culture reconnue, on remet tout par défaut
        if not cultures_to_check:
            cultures_to_check = RENDEMENTS_BASE.keys()

    resultats = []
    for culture in cultures_to_check:
        base = RENDEMENTS_BASE[culture]
        # Logique de calcul simplifiée pour le mémoire
        facteur = 1.0
        if temp > 32: facteur -= 0.10
        if hum > 80:  facteur -= 0.05
        
        rendement_estime = round(base["tonnes_ha"] * surface_ha * facteur, 2)
        chiffre_affaire = round(rendement_estime * 1000 * base["prix_kg"], 0)
        besoin_eau = round(base["eau_l_jour"] * surface_ha * 10000 * facteur, 0) # Litres par jour pour la surface
        
        resultats.append({
            "culture": culture.capitalize(),
            "surface": surface_ha,
            "rendement_estime": rendement_estime,
            "unite": "Tonnes",
            "chiffre_affaire_estime": chiffre_affaire,
            "besoin_eau_quotidien": besoin_eau,
            "cycle_jours": base["cycle"],
            "statut": "Optimal" if facteur > 0.9 else "Risque climatique",
            "conseil": "Conditions favorables" if facteur > 0.9 else "Attention au stress thermique",
            "risques": ["Sécheresse"] if hum < 40 else (["Inondation"] if hum > 85 else [])
        })
        
    return {
        "meteo_contexte": meteo,
        "previsions": resultats
    }
