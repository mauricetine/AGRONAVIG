import { useState } from "react";
import { 
  Leaf, Eye, EyeOff, LogIn, UserPlus, Mail, Lock, User, 
  Phone, MapPin, ChevronRight, ChevronLeft, CheckCircle2, Sprout
} from "lucide-react";
import { register, login } from "../services/api";

const Auth = () => {
  const [mode, setMode]           = useState("login"); // "login" | "register"
  const [step, setStep]           = useState(1);       // 1, 2, 3 pour register
  const [showPass, setShowPass]   = useState(false);
  const [loading, setLoading]     = useState(false);
  const [form, setForm]           = useState({
    nom: "", email: "", password: "", confirm: "",
    role: "producteur", telephone: "", localisation: "", cultures_interet: []
  });

  const culturesDisponibles = [
    { id: "tomate", label: "Tomate", icon: "🍅" },
    { id: "oignon", label: "Oignon", icon: "🧅" },
    { id: "maïs",   label: "Maïs",   icon: "🌽" },
    { id: "riz",    label: "Riz",    icon: "🌾" },
    { id: "pomme_de_terre", label: "Pomme de terre", icon: "🥔" },
    { id: "arachide", label: "Arachide", icon: "🥜" },
  ];

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const toggleCulture = (id) => {
    const current = [...form.cultures_interet];
    if (current.includes(id)) {
      setForm({ ...form, cultures_interet: current.filter(c => c !== id) });
    } else {
      setForm({ ...form, cultures_interet: [...current, id] });
    }
  };

  const isLogin = mode === "login";

  const nextStep = () => setStep(s => s + 1);
  const prevStep = () => setStep(s => s - 1);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      let res;
      if (isLogin) {
        res = await login({ email: form.email, password: form.password });
      } else {
        res = await register({ 
          nom: form.nom, 
          email: form.email, 
          password: form.password,
          role: form.role,
          telephone: form.telephone,
          localisation: form.localisation,
          cultures_interet: form.cultures_interet.join(",")
        });
      }
      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem("user", JSON.stringify(res.data.user));
      window.location.href = "/dashboard";
    } catch (err) {
      const status = err.response?.status;
      const detail = err.response?.data?.detail;
      const msg = !err.response
        ? "Le serveur AgroNavig est inaccessible. Vérifiez que le backend FastAPI est démarré sur http://127.0.0.1:8000."
        : detail || (status === 422 ? "Les informations saisies sont invalides." : "Erreur lors de l'authentification.");
      alert(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#f6f8f6] flex font-sans">
      
      {/* Panneau gauche — visuel (caché sur mobile) */}
      <div className="hidden lg:flex w-1/2 bg-[#102215] flex-col justify-between p-12 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-primary/10 rounded-full -mr-32 -mt-32 blur-3xl"></div>
        
        <div className="flex items-center gap-3 relative z-10">
          <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center">
            <Leaf size={22} className="text-[#102215]" />
          </div>
          <div>
            <h1 className="text-white font-bold text-xl leading-none">AgroNavig</h1>
            <p className="text-white/40 text-xs mt-0.5">Plateforme IA agricole</p>
          </div>
        </div>

        <div className="flex flex-col gap-6 relative z-10">
          <h2 className="text-white font-bold text-5xl leading-tight">
            L'agriculture de demain,<br />
            <span className="text-primary italic">aujourd'hui.</span>
          </h2>
          <p className="text-white/50 text-lg leading-relaxed max-w-md">
            Une plateforme intelligente conçue pour les agriculteurs sénégalais. 
            Précision, conseil et prévision à portée de main.
          </p>
        </div>

        <p className="text-white/20 text-xs relative z-10">
          © 2026 AgroNavig — Maurice Raphael TINE
        </p>
      </div>

      {/* Panneau droit — Formulaire */}
      <div className="flex-1 flex items-center justify-center p-6 md:p-12">
        <div className="w-full max-w-md">
          
          {/* Header */}
          <div className="mb-8">
            <h2 className="text-gray-800 font-bold text-3xl">
              {isLogin ? "Heureux de vous revoir" : "Commencez l'aventure"}
            </h2>
            <p className="text-gray-400 text-sm mt-2">
              {isLogin ? "Connectez-vous pour gérer votre exploitation" : "Créez votre profil agronomique en quelques étapes"}
            </p>
          </div>

          {/* LOGIN MODE */}
          {isLogin ? (
            <div className="flex flex-col gap-5">
              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-bold text-gray-500 uppercase">Adresse email</label>
                <div className="flex items-center gap-3 bg-white border border-gray-200 rounded-2xl px-4 py-4 focus-within:border-primary transition-all shadow-sm">
                  <Mail size={18} className="text-gray-300" />
                  <input 
                    type="email" name="email" value={form.email} onChange={handleChange}
                    placeholder="votre@email.com" className="flex-1 text-sm outline-none bg-transparent" 
                  />
                </div>
              </div>
              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-bold text-gray-500 uppercase">Mot de passe</label>
                <div className="flex items-center gap-3 bg-white border border-gray-200 rounded-2xl px-4 py-4 focus-within:border-primary transition-all shadow-sm">
                  <Lock size={18} className="text-gray-300" />
                  <input 
                    type={showPass ? "text" : "password"} name="password" value={form.password} onChange={handleChange}
                    placeholder="••••••••" className="flex-1 text-sm outline-none bg-transparent" 
                  />
                  <button onClick={() => setShowPass(!showPass)} className="text-gray-300 hover:text-gray-500">
                    {showPass ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
              </div>
              <button 
                onClick={handleSubmit} disabled={loading}
                className="w-full py-4 bg-primary text-[#102215] font-bold rounded-2xl flex items-center justify-center gap-2 hover:opacity-90 transition-all shadow-lg shadow-primary/20 mt-2"
              >
                {loading ? <div className="w-5 h-5 border-2 border-[#102215]/30 border-t-[#102215] rounded-full animate-spin" /> : <><LogIn size={18} /> Se connecter</>}
              </button>
            </div>
          ) : (
            /* REGISTER MODE — MULTI-STEP */
            <div className="flex flex-col gap-6">
              
              {/* Indicateur d'étape */}
              <div className="flex items-center gap-2 mb-2">
                {[1, 2, 3].map(i => (
                  <div key={i} className={`h-1.5 flex-1 rounded-full transition-all ${step >= i ? "bg-primary" : "bg-gray-200"}`}></div>
                ))}
              </div>

              {/* ÉTAPE 1 : Identifiants */}
              {step === 1 && (
                <div className="flex flex-col gap-4 animate-in fade-in slide-in-from-right-4 duration-300">
                  <div className="flex flex-col gap-1.5">
                    <label className="text-xs font-bold text-gray-500 uppercase">Nom complet</label>
                    <div className="flex items-center gap-3 bg-white border border-gray-200 rounded-2xl px-4 py-4 focus-within:border-primary transition-all shadow-sm">
                      <User size={18} className="text-gray-300" />
                      <input type="text" name="nom" value={form.nom} onChange={handleChange} placeholder="Mamadou Diallo" className="flex-1 text-sm outline-none bg-transparent" />
                    </div>
                  </div>
                  <div className="flex flex-col gap-1.5">
                    <label className="text-xs font-bold text-gray-500 uppercase">Email</label>
                    <div className="flex items-center gap-3 bg-white border border-gray-200 rounded-2xl px-4 py-4 focus-within:border-primary transition-all shadow-sm">
                      <Mail size={18} className="text-gray-300" />
                      <input type="email" name="email" value={form.email} onChange={handleChange} placeholder="votre@email.com" className="flex-1 text-sm outline-none bg-transparent" />
                    </div>
                  </div>
                  <div className="flex flex-col gap-1.5">
                    <label className="text-xs font-bold text-gray-500 uppercase">Mot de passe</label>
                    <div className="flex items-center gap-3 bg-white border border-gray-200 rounded-2xl px-4 py-4 focus-within:border-primary transition-all shadow-sm">
                      <Lock size={18} className="text-gray-300" />
                      <input type="password" name="password" value={form.password} onChange={handleChange} placeholder="••••••••" className="flex-1 text-sm outline-none bg-transparent" />
                    </div>
                  </div>
                  <button onClick={nextStep} className="w-full py-4 bg-gray-800 text-white font-bold rounded-2xl flex items-center justify-center gap-2 hover:bg-gray-700 transition-all mt-2">
                    Continuer <ChevronRight size={18} />
                  </button>
                </div>
              )}

              {/* ÉTAPE 2 : Profil Métier */}
              {step === 2 && (
                <div className="flex flex-col gap-4 animate-in fade-in slide-in-from-right-4 duration-300">
                  <div className="flex flex-col gap-1.5">
                    <label className="text-xs font-bold text-gray-500 uppercase">Votre profil</label>
                    <div className="grid grid-cols-1 gap-2">
                      {["producteur", "agronome", "etudiant"].map(r => (
                        <button 
                          key={r} onClick={() => setForm({...form, role: r})}
                          className={`p-4 rounded-2xl border-2 text-left transition-all flex items-center justify-between ${form.role === r ? "border-primary bg-primary/5" : "border-gray-100 bg-white hover:border-gray-200"}`}
                        >
                          <span className="capitalize font-medium text-gray-700">{r}</span>
                          {form.role === r && <CheckCircle2 size={18} className="text-primary" />}
                        </button>
                      ))}
                    </div>
                  </div>
                  <div className="flex flex-col gap-1.5">
                    <label className="text-xs font-bold text-gray-500 uppercase">Téléphone</label>
                    <div className="flex items-center gap-3 bg-white border border-gray-200 rounded-2xl px-4 py-4 focus-within:border-primary transition-all shadow-sm">
                      <Phone size={18} className="text-gray-300" />
                      <input type="text" name="telephone" value={form.telephone} onChange={handleChange} placeholder="+221 77..." className="flex-1 text-sm outline-none bg-transparent" />
                    </div>
                  </div>
                  <div className="flex flex-col gap-1.5">
                    <label className="text-xs font-bold text-gray-500 uppercase">Localisation</label>
                    <div className="flex items-center gap-3 bg-white border border-gray-200 rounded-2xl px-4 py-4 focus-within:border-primary transition-all shadow-sm">
                      <MapPin size={18} className="text-gray-300" />
                      <input type="text" name="localisation" value={form.localisation} onChange={handleChange} placeholder="Dakar, Thiès, Saint-Louis..." className="flex-1 text-sm outline-none bg-transparent" />
                    </div>
                  </div>
                  <div className="flex gap-3 mt-2">
                    <button onClick={prevStep} className="flex-1 py-4 bg-gray-100 text-gray-600 font-bold rounded-2xl hover:bg-gray-200 transition-all flex items-center justify-center gap-2">
                      <ChevronLeft size={18} /> Retour
                    </button>
                    <button onClick={nextStep} className="flex-[2] py-4 bg-gray-800 text-white font-bold rounded-2xl hover:bg-gray-700 transition-all flex items-center justify-center gap-2">
                      Suivant <ChevronRight size={18} />
                    </button>
                  </div>
                </div>
              )}

              {/* ÉTAPE 3 : Enquête Cultures */}
              {step === 3 && (
                <div className="flex flex-col gap-4 animate-in fade-in slide-in-from-right-4 duration-300">
                  <div className="mb-2">
                    <label className="text-xs font-bold text-gray-500 uppercase">Quelles cultures pratiquez-vous ?</label>
                    <p className="text-xs text-gray-400 mt-1">L'IA personnalisera vos prévisions en fonction de ce choix.</p>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    {culturesDisponibles.map(c => (
                      <button 
                        key={c.id} onClick={() => toggleCulture(c.id)}
                        className={`p-4 rounded-2xl border-2 transition-all flex flex-col items-center gap-2 ${form.cultures_interet.includes(c.id) ? "border-primary bg-primary/5" : "border-gray-100 bg-white hover:border-gray-200"}`}
                      >
                        <span className="text-2xl">{c.icon}</span>
                        <span className="text-xs font-bold text-gray-700">{c.label}</span>
                      </button>
                    ))}
                  </div>
                  <div className="flex gap-3 mt-4">
                    <button onClick={prevStep} className="flex-1 py-4 bg-gray-100 text-gray-600 font-bold rounded-2xl hover:bg-gray-200 transition-all flex items-center justify-center gap-2">
                      <ChevronLeft size={18} /> Retour
                    </button>
                    <button 
                      onClick={handleSubmit} disabled={loading || form.cultures_interet.length === 0}
                      className="flex-[2] py-4 bg-primary text-[#102215] font-bold rounded-2xl hover:opacity-90 transition-all flex items-center justify-center gap-2 shadow-lg shadow-primary/20"
                    >
                      {loading ? <div className="w-5 h-5 border-2 border-[#102215]/30 border-t-[#102215] rounded-full animate-spin" /> : <><Sprout size={18} /> Terminer l'inscription</>}
                    </button>
                  </div>
                </div>
              )}

            </div>
          )}

          {/* Footer toggle */}
          <div className="mt-8 text-center">
            <p className="text-sm text-gray-400">
              {isLogin ? "Nouveau sur la plateforme ?" : "Vous avez déjà un compte ?"}
              {" "}
              <button 
                onClick={() => { setMode(isLogin ? "register" : "login"); setStep(1); }}
                className="text-primary font-bold hover:underline ml-1"
              >
                {isLogin ? "Créer un compte" : "Se connecter"}
              </button>
            </p>
          </div>

        </div>
      </div>
    </div>
  );
};

export default Auth;
