# 🔧 Corrections Authentification - AgroNavig

## Problèmes Identifiés et Corrigés

### ✅ Problème 1 : Attribut réservé SQLAlchemy
**Fichier** : `agronavig-backend/app/models/diagnostic.py`

**Erreur** : Le modèle `Diagnostic` utilisait `metadata` comme nom de colonne, mais c'est un attribut réservé par SQLAlchemy 2.0+

**Correction** : Renommage de `metadata` en `metadata_json` (ligne 22)

```python
# ❌ Avant
metadata = Column(JSON, nullable=True)

# ✅ Après
metadata_json = Column(JSON, nullable=True)
```

---

### ✅ Problème 2 : Configuration CORS incohérente
**Fichier** : `agronavig-backend/app/main.py`

**Erreur** : Le backend n'acceptait que `http://localhost:5173`, mais le frontend peut être ouvert depuis `http://127.0.0.1:5173`

**Correction** : Ajout de `http://127.0.0.1:5173` à la liste des origines autorisées (ligne 24)

```python
# ❌ Avant
allow_origins=["http://localhost:5173"]

# ✅ Après
allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"]
```

---

### ✅ Problème 3 : Port PostgreSQL incorrect
**Fichier** : `agronavig-backend/.env`

**Erreur** : Le `.env` configurait le port `5433`, mais PostgreSQL tourne sur le port standard `5432`

**Correction** : Mise à jour de l'URL de connexion à la base de données (ligne 3)

```env
# ❌ Avant
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/agronavig

# ✅ Après
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/agronavig
```

---

## 🚀 Instructions de Démarrage

### 1. Vérifier PostgreSQL
```bash
# Windows - vérifier que PostgreSQL tourne sur le port 5432
netstat -ano | findstr :5432

# Vous devriez voir une ligne LISTENING
```

### 2. Démarrer le Backend
```bash
cd agronavig-backend

# Activer l'environnement virtuel
.\venv\Scripts\activate

# Lancer le serveur FastAPI
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Le backend devrait être accessible sur `http://127.0.0.1:8000`

### 3. Démarrer le Frontend (dans un autre terminal)
```bash
cd agronavig-frontend

# Installer les dépendances (si nécessaire)
npm install

# Lancer le serveur Vite
npm run dev
```

Le frontend devrait être accessible sur `http://localhost:5173` ou `http://127.0.0.1:5173`

---

## ✅ Vérification

Une fois les serveurs lancés, testez les endpoints d'authentification :

### Créer un compte
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "role": "producteur",
    "telephone": "+221701234567",
    "localisation": "Dakar",
    "cultures_interet": "tomate,oignon"
  }'
```

### Se connecter
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

Vous devriez recevoir un `access_token` en réponse.

---

## 🔑 Compte Admin par défaut

Si vous avez besoin de réinitialiser la base de données :

```bash
cd agronavig-backend
.\venv\Scripts\python fix_db.py
```

Cela créera un compte admin :
- **Email** : `admin@agronavig.com`
- **Mot de passe** : `admin123`

---

## 📝 Notes importantes

1. **Base de données** : Assurez-vous que PostgreSQL est en cours d'exécution et que la base `agronavig` existe
2. **Dépendances** : Toutes les dépendances Python doivent être installées via `pip install -r requirements.txt`
3. **Variables d'environnement** : Le fichier `.env` doit être présent dans `agronavig-backend/`
4. **CORS** : Les deux origines (`localhost` et `127.0.0.1`) sont maintenant acceptées

---

## 🆘 Dépannage

### Erreur : "Connection refused" PostgreSQL
- Vérifiez que PostgreSQL est en cours d'exécution
- Vérifiez le port (5432 par défaut)
- Vérifiez les identifiants dans `.env`

### Erreur : "CORS policy: Cross-Origin Request Blocked"
- Assurez-vous que le frontend est ouvert depuis `http://localhost:5173` ou `http://127.0.0.1:5173`
- Vérifiez que le backend accepte cette origine dans `main.py`

### Erreur : "ModuleNotFoundError: No module named 'redis'"
- Réinstallez les dépendances : `pip install -r requirements.txt`

---

**Date des corrections** : 21 juillet 2026
