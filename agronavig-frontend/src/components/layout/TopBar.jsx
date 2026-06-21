import { Bell, Search, User, Menu, AlertTriangle, X } from "lucide-react";
import { useLocation, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { getPrevisions } from "../../services/api";

const pageTitles = {
  "/dashboard":          { title: "Dashboard",             subtitle: "Vue générale" },
  "/diagnostic":         { title: "Diagnostic",            subtitle: "Analyse IA" },
  "/diagnostic/resultat":{ title: "Résultats",             subtitle: "Recommandations" },
  "/prevision":          { title: "Prévisions",            subtitle: "Météo & Récoltes" },
  "/conseil":            { title: "Conseil IA",            subtitle: "Assistant personnel" },
  "/rapport":            { title: "Rapports",              subtitle: "Historique" },
  "/profil":             { title: "Mon Profil",            subtitle: "Paramètres personnels" },
  "/admin":              { title: "Administration",        subtitle: "Gestion système" },
};

const TopBar = ({ setSidebarOpen }) => {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const [userName, setUserName] = useState("Producteur");
  const [showNotifs, setShowNotifs] = useState(false);
  const [alertes, setAlertes] = useState([]);
  const current = pageTitles[pathname] || { title: "AgroNavig", subtitle: "" };

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("user"));
    if (user && user.nom) setUserName(user.nom);

    // Charger les alertes basées sur les prévisions
    getPrevisions().then(res => {
      const risks = [];
      res.data.previsions?.forEach(p => {
        if (p.risques && p.risques.length > 0) {
          risks.push({
            id: Date.now() + Math.random(),
            msg: `Alerte ${p.risques[0]} pour votre culture de ${p.culture}.`,
            type: "danger"
          });
        }
      });
      setAlertes(risks);
    }).catch(() => {});
  }, []);

  return (
    <header className="h-16 bg-white border-b border-gray-100 flex items-center justify-between px-4 lg:px-6 fixed top-0 right-0 left-0 lg:left-64 z-40">
      
      {/* Titre & Menu Mobile */}
      <div className="flex items-center gap-3">
        <button 
          onClick={() => setSidebarOpen(true)}
          className="lg:hidden w-9 h-9 flex items-center justify-center text-gray-500 hover:bg-gray-50 rounded-lg"
        >
          <Menu size={20} />
        </button>
        <div className="pl-4 border-l-2 border-gray-100">
          <h2 className="text-gray-800 font-bold text-lg lg:text-xl leading-none tracking-tight">
            {current.title}
          </h2>
          <p className="hidden sm:block text-gray-400 text-[10px] lg:text-xs mt-1.5 font-medium uppercase tracking-wider">{current.subtitle}</p>
        </div>
      </div>

      {/* Actions droite */}
      <div className="flex items-center gap-2 lg:gap-3">

        {/* Barre de recherche - Masquée sur mobile petit */}
        <div className="hidden md:flex items-center gap-2 bg-gray-50 border border-gray-200 rounded-xl px-4 py-2 w-40 lg:w-56 transition-all focus-within:w-64">
          <Search size={15} className="text-gray-400" />
          <input
            type="text"
            placeholder="Rechercher..."
            className="bg-transparent text-sm text-gray-600 outline-none w-full placeholder:text-gray-400"
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                navigate(`/rapport?q=${e.target.value}`);
              }
            }}
          />
        </div>

        {/* Notifications */}
        <div className="relative">
          <button 
            onClick={() => setShowNotifs(!showNotifs)}
            className="relative w-9 h-9 bg-gray-50 border border-gray-200 rounded-xl flex items-center justify-center hover:bg-gray-100 transition-colors"
          >
            <Bell size={16} className="text-gray-500" />
            {alertes.length > 0 && (
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
            )}
          </button>

          {showNotifs && (
            <div className="absolute right-0 mt-4 w-72 bg-white border border-gray-100 shadow-2xl rounded-2xl p-4 animate-in fade-in slide-in-from-top-2 duration-200">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-bold text-xs text-gray-800">Alertes & Notifications</h4>
                <button onClick={() => setShowNotifs(false)} className="text-gray-400"><X size={14} /></button>
              </div>
              <div className="flex flex-col gap-2 max-h-60 overflow-y-auto">
                {alertes.length === 0 ? (
                  <p className="text-center py-6 text-[10px] text-gray-400">Aucune alerte</p>
                ) : (
                  alertes.map(a => (
                    <div key={a.id} className="p-2.5 bg-red-50 rounded-xl flex gap-2 border border-red-100">
                      <AlertTriangle size={14} className="text-red-500 shrink-0 mt-0.5" />
                      <p className="text-[10px] text-red-700 leading-tight">{a.msg}</p>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>

        {/* Avatar utilisateur */}
        <button 
          onClick={() => navigate("/profil")}
          className="flex items-center gap-2 bg-gray-50 border border-gray-200 rounded-xl px-2 lg:px-3 py-2 hover:bg-gray-100 transition-colors"
        >
          <div className="w-6 h-6 bg-primary/20 rounded-lg flex items-center justify-center">
            <User size={13} className="text-primary" />
          </div>
          <span className="hidden sm:block text-sm font-medium text-gray-700">{userName}</span>
        </button>

      </div>
    </header>
  );
};

export default TopBar;