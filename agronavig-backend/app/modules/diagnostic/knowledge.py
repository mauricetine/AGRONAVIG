# -*- coding: utf-8 -*-

KNOWLEDGE_BASE = {
    # POMMIER
    "Apple___Apple_scab": {
        "nom": "Tavelure du pommier",
        "description": "Maladie fongique causée par Venturia inaequalis, provoquant des taches noires sur feuilles et fruits.",
        "symptomes": ["Taches veloutées vert olive", "Déformation des fruits", "Chute prématurée des feuilles"],
        "prevention": ["Variétés résistantes", "Éliminer les feuilles mortes", "Élagage aéré"],
        "traitements": [{"type": "Fongicide", "produit": "Captane", "dose": "150g/100L", "frequence": "10-14 jours"}]
    },
    "Apple___Black_rot": {
        "nom": "Pourriture noire du pommier",
        "description": "Causée par Diplodia seriata, elle affecte les fruits, les feuilles et le bois.",
        "symptomes": ["Taches en œil de grenouille sur feuilles", "Pourriture noire du fruit", "Chancres sur le bois"],
        "prevention": ["Supprimer le bois mort", "Désinfecter les outils", "Éliminer les fruits momifiés"],
        "traitements": [{"type": "Fongicide", "produit": "Thiophanate-méthyl", "dose": "1kg/ha", "frequence": "Au débourrement"}]
    },
    "Apple___Cedar_apple_rust": {
        "nom": "Rouille du pommier",
        "description": "Maladie nécessitant deux hôtes (pommier et genévrier) pour son cycle.",
        "symptomes": ["Taches orange vif sur feuilles", "Points noirs au centre des taches", "Excroissances sous les feuilles"],
        "prevention": ["Éliminer les genévriers proches", "Variétés résistantes"],
        "traitements": [{"type": "Fongicide", "produit": "Myclobutanil", "dose": "0.3L/ha", "frequence": "7-10 jours"}]
    },
    "Apple___healthy": {
        "nom": "Pommier sain",
        "description": "Votre pommier est en bonne santé.",
        "symptomes": ["Feuillage bien vert", "Croissance vigoureuse"],
        "prevention": ["Taille annuelle", "Fertilisation équilibrée"],
        "traitements": [{"type": "Entretien", "produit": "Compost", "dose": "5kg/arbre", "frequence": "Printemps"}]
    },

    # MAÏS
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "nom": "Cercosporiose du maïs",
        "description": "Maladie fongique grave réduisant la photosynthèse.",
        "symptomes": ["Lésions rectangulaires grises", "Dessèchement des feuilles", "Affaiblissement de la tige"],
        "prevention": ["Rotation des cultures", "Enfouissement des résidus"],
        "traitements": [{"type": "Fongicide", "produit": "Azoxystrobine", "dose": "1L/ha", "frequence": "Stade 8-10 feuilles"}]
    },
    "Corn_(maize)___Common_rust_": {
        "nom": "Rouille commune du maïs",
        "description": "Pustules colorées apparaissant par temps frais et humide.",
        "symptomes": ["Pustules brunes sur les deux faces", "Jaunissement foliaire"],
        "prevention": ["Hybrides résistants", "Semis précoces"],
        "traitements": [{"type": "Fongicide", "produit": "Propiconazole", "dose": "0.5L/ha", "frequence": "Dès apparition"}]
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "nom": "Brûlure foliaire du nord",
        "description": "Grandes lésions en forme de cigare sur les feuilles.",
        "symptomes": ["Lésions allongées gris-vert", "Nécrose rapide du feuillage"],
        "prevention": ["Gestion des résidus", "Rotation 2 ans"],
        "traitements": [{"type": "Fongicide", "produit": "Triazole", "dose": "1L/ha", "frequence": "Stade floraison"}]
    },
    "Corn_(maize)___healthy": {
        "nom": "Maïs sain",
        "description": "Le maïs ne présente aucune pathologie.",
        "symptomes": ["Tiges robustes", "Feuilles larges et vertes"],
        "prevention": ["Irrigation régulière", "Apport en Azote"],
        "traitements": [{"type": "Entretien", "produit": "Urée", "dose": "100kg/ha", "frequence": "Au sarclage"}]
    },

    # POMME DE TERRE
    "Potato___Early_blight": {
        "nom": "Alternariose de la pomme de terre",
        "description": "Maladie fréquente affectant les feuilles âgées en premier.",
        "symptomes": ["Taches brunes à anneaux concentriques", "Jaunissement périphérique"],
        "prevention": ["Rotation longue", "Éviter le stress hydrique"],
        "traitements": [{"type": "Fongicide", "produit": "Mancozèbe", "dose": "2kg/ha", "frequence": "7-10 jours"}]
    },
    "Potato___Late_blight": {
        "nom": "Mildiou de la pomme de terre",
        "description": "Maladie la plus dangereuse pour la pomme de terre.",
        "symptomes": ["Taches brunes huileuses", "Duvet blanc sous les feuilles", "Pourriture des tubercules"],
        "prevention": ["Buttage haut", "Plants certifiés", "Pas d'arrosage nocturne"],
        "traitements": [{"type": "Fongicide", "produit": "Métalaxyl-M", "dose": "2.5kg/ha", "frequence": "7 jours"}]
    },
    "Potato___healthy": {
        "nom": "Pomme de terre saine",
        "description": "Culture saine et vigoureuse.",
        "symptomes": ["Tiges bien droites", "Feuillage dense"],
        "prevention": ["Surveillance pucerons", "Buttage régulier"],
        "traitements": [{"type": "Entretien", "produit": "Potasse", "dose": "200kg/ha", "frequence": "À la plantation"}]
    },

    # TOMATE
    "Tomato___Bacterial_spot": {
        "nom": "Taches bactériennes de la tomate",
        "description": "Maladie bactérienne favorisée par l'humidité.",
        "symptomes": ["Petites taches noires circulaires", "Croûtes sur les fruits", "Feuilles jaunies"],
        "prevention": ["Semences traitées", "Pas d'arrosage par aspersion"],
        "traitements": [{"type": "Bactéricide", "produit": "Hydroxyde de cuivre", "dose": "2kg/ha", "frequence": "7 jours"}]
    },
    "Tomato___Early_blight": {
        "nom": "Alternariose de la tomate",
        "description": "Champignon affectant feuilles et collet.",
        "symptomes": ["Taches en cible", "Tiges noires au sol", "Chute des feuilles"],
        "prevention": ["Paillage", "Rotation 3 ans", "Taille des gourmands"],
        "traitements": [{"type": "Fongicide", "produit": "Chlorothalonil", "dose": "1.5kg/ha", "frequence": "10 jours"}]
    },
    "Tomato___Late_blight": {
        "nom": "Mildiou de la tomate",
        "description": "Dévastateur en conditions humides et chaudes.",
        "symptomes": ["Grandes taches brunes", "Tiges noircies", "Fruits marbrés"],
        "prevention": ["Abri pluie", "Espacement large", "Effeuillage base"],
        "traitements": [{"type": "Fongicide", "produit": "Bouillie bordelaise", "dose": "20g/10L", "frequence": "Après pluie"}]
    },
    "Tomato___Leaf_Mold": {
        "nom": "Moisissure des feuilles",
        "description": "Fréquent sous serre avec forte humidité.",
        "symptomes": ["Taches jaunes face supérieure", "Feutrage gris face inférieure"],
        "prevention": ["Ventilation serres", "Réduire humidité"],
        "traitements": [{"type": "Fongicide", "produit": "Bacillus subtilis", "dose": "3L/ha", "frequence": "14 jours"}]
    },
    "Tomato___Septoria_leaf_spot": {
        "nom": "Septoriose de la tomate",
        "description": "Petites taches nombreuses sur les feuilles basses.",
        "symptomes": ["Taches grises à bord brun", "Points noirs dans les taches"],
        "prevention": ["Éliminer débris", "Paillage sol"],
        "traitements": [{"type": "Fongicide", "produit": "Mancozèbe", "dose": "2kg/ha", "frequence": "7 jours"}]
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "nom": "Araignées rouges (Acariens)",
        "description": "Minuscules acariens suçant la sève par temps sec.",
        "symptomes": ["Fines toiles", "Points blancs sur feuilles", "Bronzage du feuillage"],
        "prevention": ["Humidifier le feuillage", "Lâcher de prédateurs"],
        "traitements": [{"type": "Acaricide", "produit": "Abamectine", "dose": "0.75L/ha", "frequence": "Dès apparition"}]
    },
    "Tomato___Target_Spot": {
        "nom": "Tache cible",
        "description": "Lésions caractéristiques sur feuilles et fruits.",
        "symptomes": ["Taches circulaires foncées", "Zones concentriques nettes"],
        "prevention": ["Éviter blessures plants", "Bonne aération"],
        "traitements": [{"type": "Fongicide", "produit": "Difenoconazole", "dose": "0.5L/ha", "frequence": "12 jours"}]
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "nom": "Virus de l'enroulement jaune (TYLCV)",
        "description": "Transmis par la mouche blanche, très grave au Sénégal.",
        "symptomes": ["Feuilles enroulées", "Bords jaunes", "Croissance stoppée"],
        "prevention": ["Filets anti-insectes", "Pièges jaunes", "Variétés TY"],
        "traitements": [{"type": "Insecticide", "produit": "Imidaclopride", "dose": "0.5L/ha", "frequence": "Contre vecteur"}]
    },
    "Tomato___Tomato_mosaic_virus": {
        "nom": "Mosaïque de la tomate",
        "description": "Virus très résistant se transmettant par contact.",
        "symptomes": ["Marbrures vert clair/foncé", "Feuilles déformées (fougère)"],
        "prevention": ["Désinfecter mains/outils", "Pas de tabac près des plants"],
        "traitements": [{"type": "Sanitaire", "produit": "Arrachage", "dose": "Immédiat", "frequence": "Dès symptômes"}]
    },
    "Tomato___healthy": {
        "nom": "Tomate saine",
        "description": "Votre plant de tomate est en parfaite santé.",
        "symptomes": ["Feuillage vert sombre", "Fleurs bien formées"],
        "prevention": ["Arrosage régulier", "Tuteurage propre"],
        "traitements": [{"type": "Entretien", "produit": "Purin d'ortie", "dose": "10% dilution", "frequence": "15 jours"}]
    },

    # POIVRON
    "Pepper,_bell___Bacterial_spot": {
        "nom": "Taches bactériennes du poivron",
        "description": "Bactérie Xanthomonas affectant feuilles et fruits.",
        "symptomes": ["Lésions surélevées sur fruits", "Taches brunes irrégulières"],
        "prevention": ["Semences certifiées", "Rotation 3 ans"],
        "traitements": [{"type": "Bactéricide", "produit": "Cuivre", "dose": "2.5kg/ha", "frequence": "7-10 jours"}]
    },
    "Pepper,_bell___healthy": {
        "nom": "Poivron sain",
        "description": "Culture de poivron saine.",
        "symptomes": ["Feuilles lisses et vertes", "Fruits fermes"],
        "prevention": ["Gestion pucerons", "Irrigation goutte-à-goutte"],
        "traitements": [{"type": "Entretien", "produit": "NPK 15-15-15", "dose": "150kg/ha", "frequence": "Floraison"}]
    },

    # AUTRES (Fallback & Santé)
    "Grape___healthy": {"nom": "Vigne saine", "description": "Vigne en bonne santé.", "symptomes": ["Feuilles bien étalées"], "prevention": ["Taille courte"], "traitements": []},
    "Orange___Haunglongbing_(Citrus_greening)": {"nom": "Greening des agrumes", "description": "Maladie bactérienne mortelle transmise par psylle.", "symptomes": ["Feuilles marbrées", "Fruits amers et verts"], "prevention": ["Plants certifiés"], "traitements": [{"type": "Sanitaire", "produit": "Destruction", "dose": "Totale", "frequence": "Immédiat"}]},
    "Strawberry___healthy": {"nom": "Fraisier sain", "description": "Fraisier vigoureux.", "symptomes": ["Stolons sains"], "prevention": ["Paillage paille"], "traitements": []},
    "Peach___healthy": {"nom": "Pêcher sain", "description": "Pêcher en santé.", "symptomes": ["Feuillage dense"], "prevention": ["Taille hiver"], "traitements": []},
    "Soybean___healthy": {"nom": "Soja sain", "description": "Soja vigoureux.", "symptomes": ["Gousses bien formées"], "prevention": ["Inoculation"], "traitements": []},
    "Squash___Powdery_mildew": {"nom": "Oïdium de la courge", "description": "Feutrage blanc farineux sur les feuilles.", "symptomes": ["Poudre blanche", "Dessèchement"], "prevention": ["Variétés résistantes"], "traitements": [{"type": "Fongicide", "produit": "Soufre", "dose": "5g/L", "frequence": "7 jours"}]},
    
    "not_a_plant": {
        "nom": "Image non reconnue",
        "description": "L'IA ne reconnaît pas de plante ou de culture connue sur cette image.",
        "symptomes": ["Sujet non agricole détecté", "Image trop floue ou sombre"],
        "prevention": ["Prendre une photo nette de la feuille", "Bien éclairer le sujet", "Cadrer sur les symptômes"],
        "traitements": [{"type": "Action", "produit": "Nouvelle photo", "dose": "N/A", "frequence": "Maintenant"}]
    }
}

def get_disease_info(classe: str) -> dict:
    if classe in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[classe]
    
    # Fallback intelligent
    for key in KNOWLEDGE_BASE:
        if key in classe:
            return KNOWLEDGE_BASE[key]
            
    return KNOWLEDGE_BASE["not_a_plant"]
