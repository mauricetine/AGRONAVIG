# Déploiement d’AgroNavig

## Architecture

- `agronavig-frontend` : application React/Vite publiée sur Vercel.
- `agronavig-backend` : API FastAPI publiée sur Render avec le Dockerfile existant.
- PostgreSQL : base externe, par exemple Neon ou Supabase.

## 1. Base PostgreSQL

Créer une base PostgreSQL et conserver son URL privée au format `postgresql://...`. Ne jamais committer cette valeur dans GitHub.

## 2. Backend Render

Dans Render : **New > Blueprint**, sélectionner le dépôt `mauricetine/AGRONAVIG`, puis laisser Render utiliser `render.yaml`.

Ajouter les variables privées suivantes dans le service `agronavig-api` :

- `DATABASE_URL` : URL PostgreSQL.
- `SECRET_KEY` : valeur aléatoire longue.
- `CORS_ORIGINS` : URL Vercel du frontend, sans slash final.
- `OPENWEATHERMAP_API_KEY` : clé OpenWeather facultative.
- `GROQ_API_KEY` : clé Groq facultative si AgroBot utilise Groq.

L’URL de contrôle est : `https://URL-RENDER/`.

## 3. Frontend Vercel

Dans Vercel : **Add New > Project**, importer `mauricetine/AGRONAVIG` et régler **Root Directory** sur `agronavig-frontend`.

Paramètres de build :

- Framework : Vite.
- Build command : `npm run build`.
- Output directory : `dist`.
- Install command : `npm ci`.

Ajouter la variable d’environnement :

```text
VITE_API_URL=https://URL-RENDER/api
```

Après le premier déploiement Vercel, reporter son URL exacte dans `CORS_ORIGINS` sur Render, puis redéployer le backend.

## 4. Vérification

1. Ouvrir `https://URL-RENDER/` et vérifier la réponse JSON de l’API.
2. Ouvrir l’URL Vercel.
3. Créer un compte et se connecter.
4. Tester le diagnostic avec une image.
5. Vérifier l’onglet Network du navigateur si une requête échoue.

Le service Render Free peut se mettre en veille après une période d’inactivité. Le premier appel peut donc être lent après cette veille.
