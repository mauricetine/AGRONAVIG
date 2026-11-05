# -*- coding: utf-8 -*-

KNOWLEDGE_BASE = {
    # POMMIER
    "Apple___Apple_scab": {
        "nom": "Tavelure du pommier",
        "description": "Maladie fongique causee par Venturia inaequalis, provoquant des taches noires sur feuilles et fruits.",
        "symptomes": ["Taches veloutees vert olive", "Deformation des fruits", "Chute prematuree des feuilles"],
        "prevention": ["Varietes resistantes", "Eliminer les feuilles mortes", "Elagage aere"],
        "traitements": [{"type": "Fongicide", "produit": "Captane", "dose": "150g/100L", "frequence": "10-14 jours"}]
    },
    "Apple___Black_rot": {
        "nom": "Pourriture noire du pommier",
        "description": "Causee par Diplodia seriata, elle affecte les fruits, les feuilles et le bois.",
        "symptomes": ["Taches en oeil de grenouille sur feuilles", "Pourriture noire du fruit", "Chancres sur le bois"],
        "prevention": ["Supprimer le bois mort", "Desinfecter les outils", "Eliminer les fruits momifies"],
        "traitements": [{"type": "Fongicide", "produit": "Thiophanate-methyl", "dose": "1kg/ha", "frequence": "Au debourrement"}]
    },
    "Apple___Cedar_apple_rust": {
        "nom": "Rouille du pommier",
        "description": "Maladie necessitant deux hotes (pommier et genevrier) pour son cycle.",
        "symptomes": ["Taches orange vif sur feuilles", "Points noirs au centre des taches", "Excroissances sous les feuilles"],
        "prevention": ["Eliminer les genevriers proches", "Varietes resistantes"],
        "traitements": [{"type": "Fongicide", "produit": "Myclobutanil", "dose": "0.3L/ha", "frequence": "7-10 jours"}]
    },
    "Apple___healthy": {
        "nom": "Pommier sain",
        "description": "Votre pommier est en bonne sante.",
        "symptomes": ["Feuillage bien vert", "Croissance vigoureuse"],
        "prevention": ["Taille annuelle", "Fertilisation equilibree"],
        "traitements": [{"type": "Entretien", "produit": "Compost", "dose": "5kg/arbre", "frequence": "Printemps"}]
    },

    # MAIS
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "nom": "Cercosporiose du mais",
        "description": "Maladie fongique grave reduisant la photosynthese.",
        "symptomes": ["Lesions rectangulaires grises", "Dessechement des feuilles", "Affaiblissement de la tige"],
        "prevention": ["Rotation des cultures", "Enfouissement des residus"],
        "traitements": [{"type": "Fongicide", "produit": "Azoxystrobine", "dose": "1L/ha", "frequence": "Stade 8-10 feuilles"}]
    },
    "Corn_(maize)___Common_rust_": {
        "nom": "Rouille commune du mais",
        "description": "Pustules colorees apparaissant par temps frais et humide.",
        "symptomes": ["Pustules brunes sur les deux faces", "Jaunissement foliaire"],
        "prevention": ["Hybrides resistants", "Semis precoces"],
        "traitements": [{"type": "Fongicide", "produit": "Propiconazole", "dose": "0.5L/ha", "frequence": "Des apparition"}]
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "nom": "Brulure foliaire du nord",
        "description": "Grandes lesions en forme de cigare sur les feuilles.",
        "symptomes": ["Lesions allongees gris-vert", "Necrose rapide du feuillage"],
        "prevention": ["Gestion des residus", "Rotation 2 ans"],
        "traitements": [{"type": "Fongicide", "produit": "Triazole", "dose": "1L/ha", "frequence": "Stade floraison"}]
    },
    "Corn_(maize)___healthy": {
        "nom": "Mais sain",
        "description": "Le mais ne presente aucune pathologie.",
        "symptomes": ["Tiges robustes", "Feuilles larges et vertes"],
        "prevention": ["Irrigation reguliere", "Apport en Azote"],
        "traitements": [{"type": "Entretien", "produit": "Uree", "dose": "100kg/ha", "frequence": "Au sarclage"}]
    },

    # POMME DE TERRE
    "Potato___Early_blight": {
        "nom": "Alternariose de la pomme de terre",
        "description": "Maladie frequente affectant les feuilles agees en premier.",
        "symptomes": ["Taches brunes a anneaux concentriques", "Jaunissement peripherique"],
        "prevention": ["Rotation longue", "Eviter le stress hydrique"],
        "traitements": [{"type": "Fongicide", "produit": "Mancozebe", "dose": "2kg/ha", "frequence": "7-10 jours"}]
    },
    "Potato___Late_blight": {
        "nom": "Mildiou de la pomme de terre",
        "description": "Maladie la plus dangereuse pour la pomme de terre.",
        "symptomes": ["Taches brunes huileuses", "Duvet blanc sous les feuilles", "Pourriture des tubercules"],
        "prevention": ["Buttage haut", "Plants certifies", "Pas d'arrosage nocturne"],
        "traitements": [{"type": "Fongicide", "produit": "Metalaxyl-M", "dose": "2.5kg/ha", "frequence": "7 jours"}]
    },
    "Potato___healthy": {
        "nom": "Pomme de terre saine",
        "description": "Culture saine et vigoureuse.",
        "symptomes": ["Tiges bien droites", "Feuillage dense"],
        "prevention": ["Surveillance pucerons", "Buttage regulier"],
        "traitements": [{"type": "Entretien", "produit": "Potasse", "dose": "200kg/ha", "frequence": "A la plantation"}]
    },

    # TOMATE
    "Tomato___Bacterial_spot": {
        "nom": "Taches bacteriennes de la tomate",
        "description": "Maladie bacterienne favorisee par l'humidite.",
        "symptomes": ["Petites taches noires circulaires", "Croutes sur les fruits", "Feuilles jaunies"],
        "prevention": ["Semences traitees", "Pas d'arrosage par aspersion"],
        "traitements": [{"type": "Bactericide", "produit": "Hydroxyde de cuivre", "dose": "2kg/ha", "frequence": "7 jours"}]
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
        "description": "Devastateur en conditions humides et chaudes.",
        "symptomes": ["Grandes taches brunes", "Tiges noircies", "Fruits marbres"],
        "prevention": ["Abri pluie", "Espacement large", "Effeuillage base"],
        "traitements": [{"type": "Fongicide", "produit": "Bouillie bordelaise", "dose": "20g/10L", "frequence": "Apres pluie"}]
    },
    "Tomato___Leaf_Mold": {
        "nom": "Moisissure des feuilles",
        "description": "Frequent sous serre avec forte humidite.",
        "symptomes": ["Taches jaunes face superieure", "Feutrage gris face inferieure"],
        "prevention": ["Ventilation serres", "Reduire humidite"],
        "traitements": [{"type": "Fongicide", "produit": "Bacillus subtilis", "dose": "3L/ha", "frequence": "14 jours"}]
    },
    "Tomato___Septoria_leaf_spot": {
        "nom": "Septoriose de la tomate",
        "description": "Petites taches nombreuses sur les feuilles basses.",
        "symptomes": ["Taches grises a bord brun", "Points noirs dans les taches"],
        "prevention": ["Eliminer debris", "Paillage sol"],
        "traitements": [{"type": "Fongicide", "produit": "Mancozebe", "dose": "2kg/ha", "frequence": "7 jours"}]
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "nom": "Araignees rouges (Acariens)",
        "description": "Minuscules acariens sucant la seve par temps sec.",
        "symptomes": ["Fines toiles", "Points blancs sur feuilles", "Bronzage du feuillage"],
        "prevention": ["Humidifier le feuillage", "Lacher de predateurs"],
        "traitements": [{"type": "Acaricide", "produit": "Abamectine", "dose": "0.75L/ha", "frequence": "Des apparition"}]
    },
    "Tomato___Target_Spot": {
        "nom": "Tache cible",
        "description": "Lesions caracteristiques sur feuilles et fruits.",
        "symptomes": ["Taches circulaires foncees", "Zones concentriques nettes"],
        "prevention": ["Eviter blessures plants", "Bonne aeration"],
        "traitements": [{"type": "Fongicide", "produit": "Difenoconazole", "dose": "0.5L/ha", "frequence": "12 jours"}]
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "nom": "Virus de l'enroulement jaune (TYLCV)",
        "description": "Transmis par la mouche blanche, tres grave au Senegal.",
        "symptomes": ["Feuilles enroulees", "Bords jaunes", "Croissance stoppee"],
        "prevention": ["Filets anti-insectes", "Pieges jaunes", "Varietes TY"],
        "traitements": [{"type": "Insecticide", "produit": "Imidaclopride", "dose": "0.5L/ha", "frequence": "Contre vecteur"}]
    },
    "Tomato___Tomato_mosaic_virus": {
        "nom": "Mosaique de la tomate",
        "description": "Virus tres resistant se transmettant par contact.",
        "symptomes": ["Marbrures vert clair/fonce", "Feuilles deformees (fougere)"],
        "prevention": ["Desinfecter mains/outils", "Pas de tabac pres des plants"],
        "traitements": [{"type": "Sanitaire", "produit": "Arrachage", "dose": "Immediat", "frequence": "Des symptomes"}]
    },
    "Tomato___healthy": {
        "nom": "Tomate saine",
        "description": "Votre plant de tomate est en parfaite sante.",
        "symptomes": ["Feuillage vert sombre", "Fleurs bien formees"],
        "prevention": ["Arrosage regulier", "Tuteurage propre"],
        "traitements": [{"type": "Entretien", "produit": "Purin d'ortie", "dose": "10% dilution", "frequence": "15 jours"}]
    },

    # POIVRON
    "Pepper,_bell___Bacterial_spot": {
        "nom": "Taches bacteriennes du poivron",
        "description": "Bacterie Xanthomonas affectant feuilles et fruits.",
        "symptomes": ["Lesions surelevees sur fruits", "Taches brunes irregulieres"],
        "prevention": ["Semences certifiees", "Rotation 3 ans"],
        "traitements": [{"type": "Bactericide", "produit": "Cuivre", "dose": "2.5kg/ha", "frequence": "7-10 jours"}]
    },
    "Pepper,_bell___healthy": {
        "nom": "Poivron sain",
        "description": "Culture de poivron saine.",
        "symptomes": ["Feuilles lisses et vertes", "Fruits fermes"],
        "prevention": ["Gestion pucerons", "Irrigation goutte-a-goutte"],
        "traitements": [{"type": "Entretien", "produit": "NPK 15-15-15", "dose": "150kg/ha", "frequence": "Floraison"}]
    },

    # AUTRES (Fallback & Sante)
    "Grape___healthy": {"nom": "Vigne saine", "description": "Vigne en bonne sante.", "symptomes": ["Feuilles bien etalees"], "prevention": ["Taille courte"], "traitements": []},
    "Orange___Haunglongbing_(Citrus_greening)": {"nom": "Greening des agrumes", "description": "Maladie bacterienne mortelle transmise par psylle.", "symptomes": ["Feuilles marbrees", "Fruits amers et verts"], "prevention": ["Plants certifies"], "traitements": [{"type": "Sanitaire", "produit": "Destruction", "dose": "Totale", "frequence": "Immediat"}]},
    "Strawberry___healthy": {"nom": "Fraisier sain", "description": "Fraisier vigoureux.", "symptomes": ["Stolons sains"], "prevention": ["Paillage paille"], "traitements": []},
    "Peach___healthy": {"nom": "Pecher sain", "description": "Pecher en sante.", "symptomes": ["Feuillage dense"], "prevention": ["Taille hiver"], "traitements": []},
    "Soybean___healthy": {"nom": "Soja sain", "description": "Soja vigoureux.", "symptomes": ["Gousses bien formees"], "prevention": ["Inoculation"], "traitements": []},
    "Squash___Powdery_mildew": {"nom": "Oidium de la courge", "description": "Feutrage blanc farineux sur les feuilles.", "symptomes": ["Poudre blanche", "Dessechement"], "prevention": ["Varietes resistantes"], "traitements": [{"type": "Fongicide", "produit": "Soufre", "dose": "5g/L", "frequence": "7 jours"}]},
    
    "not_a_plant": {
        "nom": "Image non reconnue",
        "description": "L'IA ne reconnait pas de plante ou de culture connue sur cette image.",
        "symptomes": ["Sujet non agricole detecte", "Image trop floue ou sombre"],
        "prevention": ["Prendre une photo nette de la feuille", "Bien eclairer le sujet", "Cadrer sur les symptomes"],
        "traitements": [{"type": "Action", "produit": "Nouvelle photo", "dose": "N/A", "frequence": "Maintenant"}]
    },
    "Tomato___Whitefly_Damage": {
        "nom": "Attaque de mouches blanches (Vecteur TYLCV)",
        "description": "Ravageur majeur dans la zone des Niayes provoquant la chlorose et la transmission de viroses.",
        "symptomes": ["Présence de petits insectes blancs au dos des feuilles", "Miellat et fumagine", "Enroulement foliaire"],
        "prevention": ["Filets anti-insectes", "Pièges jaunes englués", "Élimination des adventices hôtes"],
        "traitements": [
            {"type": "Biologique", "produit": "Huile de Neem ou Savon noir", "dose": "10ml/L", "frequence": "Tous les 5 jours"},
            {"type": "Chimique homologué", "produit": "Imidaclopride ou Acetamipride", "dose": "Selon l'étiquette du produit autorisé", "frequence": "Selon seuil de capture"}
        ]
    }
}

def get_disease_info(classe: str) -> dict:
    if classe in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[classe]
    
    for key in KNOWLEDGE_BASE:
        if key in classe:
            return KNOWLEDGE_BASE[key]
            
    return KNOWLEDGE_BASE["not_a_plant"]




def get_enriched_disease_info(key: str) -> dict:
    base = KNOWLEDGE_BASE.get(key, {
        "nom": key,
        "description": "Pathologie ou état non répertorié précisément dans la base locale.",
        "symptomes": ["Observer les feuilles et tiges"],
        "prevention": ["Rotation des cultures", "Surveillance régulière"],
        "traitements": [{"type": "Conseil", "produit": "Consulter un agronome", "dose": "-", "frequence": "-"}]
    })

    # Enrichissement avec des blocs normalisés pour l'interface et le rapport
    base["traitement_biologique"] = [
        {"produit": "Purin de neem / décoction d'ail", "action": "Répulsif naturel et fongicide de contact", "frequence": "Tous les 5 à 7 jours en préventif"},
        {"produit": "Bouillie bordelaise (si homologué)", "action": "Protection cuprique contre les champignons", "frequence": "Après la pluie"}
    ]
    base["precautions_emploi"] = [
        "Porter des équipements de protection individuelle (gants, masque, combinaison) lors de l'application des produits chimiques.",
        "Respecter scrupuleusement le délai avant récolte (DAR) indiqué sur l'étiquette du produit homologué.",
        "Éviter de traiter aux heures chaudes de la journée pour ne pas brûler le feuillage."
    ]
    return base
