# -*- coding: utf-8 -*-
import random

# Base de connaissances pour l'assistant
EXPERT_KNOWLEDGE = {
    "tomate": [
        "Pour la tomate au Sénégal, surveillez le TYLCV transmis par la mouche blanche. Utilisez des filets anti-insectes.",
        "L'arrosage doit être régulier au pied du plant. Évitez de mouiller les feuilles pour prévenir le mildiou.",
        "Un apport en potasse lors de la floraison garantit des fruits fermes et savoureux."
    ],
    "oignon": [
        "Le repiquage de l'oignon se fait généralement 45 à 60 jours après le semis en pépinière.",
        "Surveillez les thrips, ils peuvent réduire considérablement votre rendement.",
        "L'arrêt de l'arrosage 15 jours avant la récolte améliore la conservation des bulbes."
    ],
    "maïs": [
        "Le maïs a besoin de beaucoup d'azote. Fractionnez vos apports en deux : au sarclage et à la floraison.",
        "Contre la chenille légionnaire d'automne, inspectez le cornet des jeunes plants régulièrement.",
        "Une bonne densité de semis est de 50 000 à 60 000 pieds par hectare pour un rendement optimal."
    ],
    "pomme de terre": [
        "Le buttage est essentiel pour protéger les tubercules de la lumière et du mildiou.",
        "Utilisez des semences certifiées pour éviter les virus et la gale commune.",
        "La récolte se fait quand le feuillage commence à jaunir et à se dessécher."
    ],
    "riz": [
        "Au Sénégal, la culture du riz en Casamance ou dans la Vallée du Fleuve nécessite une bonne maîtrise de l'eau. Assurez-vous d'un nivellement parfait de vos casiers.",
        "Surveillez la pyriculariose, surtout en période de forte humidité.",
        "L'apport de fumure organique en fond de cuve améliore considérablement le tallage du riz."
    ],
    "arachide": [
        "L'arachide est une culture clé au Sénégal. Semez dès les premières pluies utiles (environ 20mm).",
        "Évitez les sols trop argileux qui rendent la récolte difficile et favorisent l'aflatoxine.",
        "Un traitement fongicide des semences est indispensable pour garantir une bonne levée."
    ],
    "general": [
        "Une rotation des cultures sur 3 ou 4 ans est la meilleure défense contre les maladies du sol.",
        "L'apport de matière organique (compost) améliore la structure du sol et sa capacité de rétention d'eau.",
        "Observez vos cultures quotidiennement : une détection précoce permet souvent un traitement biologique simple.",
        "Utilisez toujours des semences certifiées provenant de l'ISRA ou de distributeurs agréés.",
        "L'irrigation goutte-à-goutte est la solution la plus économe en eau pour les zones sèches du Sénégal."
    ]
}

OFF_TOPIC_KEYWORDS = [
    "foot", "ballon", "match", "politique", "élection", "musique", "film", "cinéma", "jeu", "gaming",
    "cuisine", "recette", "sport", "météo", "bourse", "crypto", "amour", "relation"
]

def generer_conseil(message: str, culture: str = None) -> str:
    msg_lower = message.lower()
    
    # 1. Vérification Hors-Sujet
    if any(word in msg_lower for word in OFF_TOPIC_KEYWORDS):
        return "Désolé, je suis un assistant spécialisé exclusivement dans l'agriculture et la santé des cultures. Je ne peux pas vous répondre sur ce sujet hors de mon domaine d'expertise."

    # 2. Détection de la culture
    detected_culture = culture.lower() if culture else None
    if not detected_culture:
        for c in EXPERT_KNOWLEDGE.keys():
            if c in msg_lower:
                detected_culture = c
                break
            
    # 3. Réponse experte ou générale
    if detected_culture and detected_culture in EXPERT_KNOWLEDGE:
        conseils = EXPERT_KNOWLEDGE[detected_culture]
        return f"En ce qui concerne la culture de {detected_culture} : " + random.choice(conseils)
    
    # 4. Réponses contextuelles
    if "bonjour" in msg_lower or "salut" in msg_lower:
        return "Bonjour ! Je suis l'assistant AgroNavig. Comment puis-je vous aider dans votre exploitation aujourd'hui ?"
    
    if "maladie" in msg_lower or "problème" in msg_lower:
        return "En cas de suspicion de maladie, je vous recommande d'utiliser notre module de 'Diagnostic IA' pour analyser une photo de votre plante."
        
    return random.choice(EXPERT_KNOWLEDGE["general"])
