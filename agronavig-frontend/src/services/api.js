import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

// Ajouter le token JWT automatiquement à chaque requête
API.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth
export const register = (data) => API.post("/auth/register", data);
export const login    = (data) => API.post("/auth/login", data);
export const getMe    = ()     => API.get("/auth/me");

// Diagnostic
export const analyserImage  = (formData) => API.post("/diagnostic/analyser", formData);
export const getHistorique  = ()          => API.get("/diagnostic/historique");
export const getDernier     = ()          => API.get("/diagnostic/dernier");

// Météo
export const getMeteo       = (ville = "Dakar") => API.get(`/meteo/?ville=${ville}`);

// Prévision
export const getPrevisions  = () => API.get("/prevision/recoltes");

// Rapport
export const getRapport     = () => API.get("/rapport/");

// Conseil
export const envoyerMessage = (data) => API.post("/conseil/message", data);

export default API;