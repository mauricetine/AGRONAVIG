# 🧪 TEST GUIDE: Nouveaux Endpoints Diagnostic

## PRÉREQUIS

```bash
# 1. Backend running
cd agronavig-backend
pip install -r requirements.txt  # Install reportlab
python -m uvicorn app.main:app --reload

# 2. Redis running
redis-server

# 3. BD avec données de test
# Créer user et diagnostics dans BD (via /auth/register, /diagnostic/analyser)
```

---

## 📋 DONNÉES DE TEST

Supposons:
- User ID: 1 (connecté)
- Diagnostic 1: Tomato, Late Blight, confiance 92.4%, créé il y a 7 jours
- Diagnostic 2: Tomato, Early Blight, confiance 85%, créé aujourd'hui
- Diagnostic 3: Pepper, healthy, confiance 98%, créé il y a 1 jour

---

## 🔧 TESTS

### 1. TEST CACHE HIT/MISS
```bash
# Test 1a: Premier appel (CACHE MISS)
curl -X POST "http://localhost:8000/api/diagnostic/analyser" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "culture=Tomato" \
  -F "file=@/path/to/tomato_leaf.jpg"

# Response time: 3-5 secondes (TensorFlow model predict)
# Console log: "💾 Prediction cached: Tomato_abc123.jpg"

# Test 1b: Deuxième appel avec MÊME image (CACHE HIT)
curl -X POST "http://localhost:8000/api/diagnostic/analyser" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "culture=Tomato" \
  -F "file=@/path/to/tomato_leaf.jpg"

# Response time: 50ms (Redis retrieval)
# Console log: "✅ Cache hit: Tomato_abc123.jpg"

# ✅ EXPECTED: 2ème appel 60x+ plus rapide
```

### 2. TEST CONTEXTE SAISONNIER
```bash
# Supposons: Juin (Hivernage - rainy season)
# Maladies fongiques favorisées

curl -X GET "http://localhost:8000/api/diagnostic/dernier" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# RESPONSE:
{
  "id": 1,
  "maladie": "Tomato___Late_blight",
  "confiance": 92.4,
  "niveau": "élevé",
  "metadata": {
    "season": "hivernage",
    "confidence_adjusted": 97.4,           # +5% boost
    "seasonal_boost_penalty": 5.0,
    "seasonal_recommendations": [
      "Augmenter fréquence pulvérisations",
      "Favoriser circulation air",
      "Monitor humidity > 80%"
    ]
  },
  "seasonal_context": {
    "season": "hivernage",
    "boost": 5,
    "recommendations": [...]
  }
}

# ✅ EXPECTED: confidence_adjusted > confiance
# ✅ EXPECTED: season = hivernage
# ✅ EXPECTED: recommendations non-vides
```

### 3. TEST VALIDATION UTILISATEUR
```bash
# User confirme que diagnostic 1 est correct
curl -X POST "http://localhost:8000/api/diagnostic/validation/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "correct",
    "comment": "Confirmed late blight after inspection. Applied Metalaxyl treatment."
  }'

# RESPONSE:
{
  "success": true,
  "message": "Diagnostic validé",
  "diagnostic": {
    "id": 1,
    "validated_by_user": true,
    "user_feedback": {
      "status": "correct",
      "comment": "Confirmed...",
      "timestamp": "2024-..."
    }
  }
}

# ✅ EXPECTED: validated_by_user = true
# ✅ EXPECTED: user_feedback stocké
```

### 4. TEST CORRECTION DIAGNOSTIC
```bash
# User corrige diagnostic 2 (pensait Early Blight mais c'était autre chose)
curl -X POST "http://localhost:8000/api/diagnostic/validation/2" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "incorrect",
    "comment": "Rechecked with agronomist - actually Septoria",
    "correct_disease": "Tomato___Septoria"
  }'

# RESPONSE:
{
  "success": true,
  "diagnostic": {
    "id": 2,
    "validated_by_user": true,
    "user_feedback": {
      "status": "incorrect",
      "comment": "Rechecked...",
      "correct_disease": "Tomato___Septoria"
    }
  }
}

# ✅ EXPECTED: status = incorrect
# ✅ EXPECTED: correct_disease stocké
```

### 5. TEST COMPARAISON DIAGNOSTICS
```bash
# Comparer diagnostic 1 (7 jours ago) vs diagnostic 2 (aujourd'hui) - même culture
curl -X GET "http://localhost:8000/api/diagnostic/comparaison/1/2" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# RESPONSE:
{
  "diagnostic1": {
    "id": 1,
    "maladie": "Tomato___Late_blight",
    "confiance": 92.4,
    "niveau": "élevé",
    "culture": "Tomato",
    "created_at": "2024-01-15T10:30:00"
  },
  "diagnostic2": {
    "id": 2,
    "maladie": "Tomato___Early_blight",
    "confiance": 85,
    "niveau": "moyen",
    "culture": "Tomato",
    "created_at": "2024-01-22T14:15:00"
  },
  "evolution": {
    "maladie_changed": true,
    "confidence_change": -7.4,
    "level_improved": true,
    "days_apart": 7
  }
}

# ✅ EXPECTED: maladie_changed = true (Late vs Early)
# ✅ EXPECTED: confidence_change = -7.4
# ✅ EXPECTED: days_apart = 7
```

### 6. TEST PROGRESSION PAR CULTURE
```bash
# Voir toute l'historique Tomato pour cet user
curl -X GET "http://localhost:8000/api/diagnostic/progression/Tomato?limit=20" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# RESPONSE:
{
  "culture": "Tomato",
  "total": 2,
  "progression": [
    {
      "id": 2,
      "date": "2024-01-22",
      "maladie": "Tomato___Early_blight",
      "confiance": 85,
      "niveau": "moyen",
      "validated": true,
      "feedback": {
        "status": "incorrect",
        "correct_disease": "Tomato___Septoria"
      },
      "season": "transition",
      "confidence_adjusted": 84.5
    },
    {
      "id": 1,
      "date": "2024-01-15",
      "maladie": "Tomato___Late_blight",
      "confiance": 92.4,
      "niveau": "élevé",
      "validated": true,
      "feedback": {
        "status": "correct"
      },
      "season": "hivernage",
      "confidence_adjusted": 97.4
    }
  ]
}

# ✅ EXPECTED: Triage DESC by date
# ✅ EXPECTED: Feedback utilisateur présent
# ✅ EXPECTED: Saisons affichées
```

### 7. TEST STATISTIQUES UTILISATEUR
```bash
curl -X GET "http://localhost:8000/api/diagnostic/statistiques" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# RESPONSE:
{
  "total_diagnostics": 3,
  "validated_by_user": 2,
  "confirmed_correct": 1,
  "accuracy_rate": 50.0,                    # 1 correct / 2 validated
  "cultures": ["Tomato", "Pepper"],
  "unique_diseases": 2,
  "avg_confidence": 91.87,
  "last_diagnostic": "2024-01-22T14:15:00"
}

# ✅ EXPECTED: accuracy_rate = (confirmed_correct / validated_by_user) * 100
# ✅ EXPECTED: Récent diagnostic affiche last_diagnostic
```

### 8. TEST PAGINATION
```bash
# Récupérer historique avec pagination
curl -X GET "http://localhost:8000/api/diagnostic/historique?limit=1&offset=0" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# RESPONSE (Page 1):
{
  "total": 3,
  "count": 1,
  "diagnostics": [
    {
      "id": 2,
      "maladie": "Tomato___Early_blight",
      ...
    }
  ]
}

# Appel page 2
curl -X GET "http://localhost:8000/api/diagnostic/historique?limit=1&offset=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# RESPONSE (Page 2):
{
  "total": 3,
  "count": 1,
  "diagnostics": [
    {
      "id": 1,
      "maladie": "Tomato___Late_blight",
      ...
    }
  ]
}

# ✅ EXPECTED: count = 1 (limit)
# ✅ EXPECTED: total = 3 (total dans DB)
# ✅ EXPECTED: Pagination fonctionne (offset+1)
```

### 9. TEST EXPORT PDF SINGLE
```bash
# Exporter diagnostic 1 en PDF
curl -X GET "http://localhost:8000/api/diagnostic/export-pdf/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -o diagnostic_1.pdf

# ✅ EXPECTED: File diagnostic_1.pdf créé
# ✅ EXPECTED: PDF ouvrable (Format PDF valid)
# ✅ EXPECTED: Contient titre, résultats, top 3, traitements
```

### 10. TEST EXPORT PDF BATCH
```bash
# Exporter batch (limite 2)
curl -X POST "http://localhost:8000/api/diagnostic/export-batch-pdf?limit=2" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -o diagnostics_batch.pdf

# ✅ EXPECTED: File diagnostics_batch.pdf créé
# ✅ EXPECTED: PDF contient summary table avec 2 diagnostics
# ✅ EXPECTED: Statuts (accuracy, etc) présents
```

---

## 🔍 VÉRIFICATIONS

### A. Response Times
```
Cache Miss: 3-5 secondes (normal)
Cache Hit: 50-100ms (target)
Pagination: <500ms
Statistics: <200ms
PDF Single: 1-2 secondes
PDF Batch (100): 5-10 secondes
```

### B. Response Codes
```
✅ 200: Success
✅ 400: Invalid request
✅ 401: Unauthorized
✅ 404: Resource not found
✅ 500: Server error
```

### C. Response Format
```
✅ All JSON responses
✅ camelCase field names
✅ Proper HTTP headers
✅ Error messages informative
```

---

## 🐛 DEBUGGING

### Cache Not Working
```bash
# Check Redis
redis-cli PING
# Expected: PONG

redis-cli KEYS "Tomato_*"
# Expected: List of cache keys

redis-cli GET "Tomato_abc123"
# Expected: JSON prediction or (nil)
```

### DB Connection Issues
```bash
# Check PostgreSQL
psql -U postgres -d agronavig -c "SELECT COUNT(*) FROM diagnostic;"
# Expected: Number > 0
```

### PDF Export Errors
```bash
# Check reportlab installed
python -c "import reportlab; print(reportlab.__version__)"
# Expected: 4.0.0 or higher
```

---

## ✅ FULL TEST CHECKLIST

- [ ] Cache hit/miss works (90% speedup)
- [ ] Seasonal context applied (+/- confiance)
- [ ] Validation stored (validated_by_user = true)
- [ ] Comparison works (evolution calculated)
- [ ] Progression timeline correct
- [ ] Statistics accuracy rate calculated
- [ ] Pagination works (limit/offset)
- [ ] PDF single generated
- [ ] PDF batch generated
- [ ] All response codes correct
- [ ] No console errors
- [ ] Performance baseline met

---

## 📊 LOAD TEST (Optional)

```bash
# Generate 100 diagnostics and test batch export
for i in {1..100}; do
  curl -X POST "http://localhost:8000/api/diagnostic/analyser" \
    -H "Authorization: Bearer $TOKEN" \
    -F "culture=Tomato" \
    -F "file=@leaf.jpg" &
done
wait

# Export all 100 as PDF
time curl -X POST "http://localhost:8000/api/diagnostic/export-batch-pdf?limit=100" \
  -H "Authorization: Bearer $TOKEN" \
  -o batch_100.pdf

# Check performance
# Expected: < 10 seconds for PDF generation
# Expected: < 2s for batch statistics query
```

---

**Test Status**: Ready for manual QA
**Estimated Time**: 30 minutes full test suite
