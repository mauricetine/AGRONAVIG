import { useState, useEffect } from "react";
import { User, Mail, Phone, MapPin, Leaf, Shield, Settings, Save } from "lucide-react";

const Profil = () => {
  const [user, setUser] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [form, setForm] = useState({
    nom: "", email: "", telephone: "", localisation: "", cultures_interet: ""
  });

  useEffect(() => {
    const savedUser = JSON.parse(localStorage.getItem("user"));
    if (savedUser) {
      setUser(savedUser);
      setForm({
        nom: savedUser.nom || "",
        email: savedUser.email || "",
        telephone: savedUser.telephone || "",
        localisation: savedUser.localisation || "",
        cultures_interet: savedUser.cultures_interet || ""
      });
    }
  }, []);

  const handleSave = async () => {
    try {
      // Dans un cas réel, on appellerait l'API ici
      // res = await updateProfile(form);
      const updatedUser = { ...user, ...form };
      localStorage.setItem("user", JSON.stringify(updatedUser));
      setUser(updatedUser);
      setIsEditing(false);
      alert("Profil mis à jour avec succès !");
      window.location.reload(); // Recharger pour mettre à jour les prévisions partout
    } catch (err) {
      alert("Erreur lors de la mise à jour");
    }
  };

  const toggleCulture = (culture) => {
    let cultures = form.cultures_interet ? form.cultures_interet.split(",") : [];
    if (cultures.includes(culture)) {
      cultures = cultures.filter(c => c !== culture);
    } else {
      cultures.push(culture);
    }
    const newVal = cultures.join(",");
    setForm({ ...form, cultures_interet: newVal });
    // Sauvegarde immédiate pour les cultures
    const updatedUser = { ...user, cultures_interet: newVal };
    localStorage.setItem("user", JSON.stringify(updatedUser));
    setUser(updatedUser);
  };

  const culturesDisponibles = ["tomate", "oignon", "maïs", "riz", "pomme de terre", "arachide"];

  if (!user) return null;

  return (
    <div className="max-w-4xl mx-auto flex flex-col gap-6">
      
      {/* Header Profil */}
      <div className="bg-white rounded-3xl p-8 border border-gray-100 shadow-sm flex flex-col md:flex-row items-center gap-8">
        <div className="w-32 h-32 bg-primary/10 rounded-full flex items-center justify-center border-4 border-white shadow-lg">
          <User size={64} className="text-primary" />
        </div>
        <div className="flex-1 text-center md:text-left">
          <div className="flex items-center justify-center md:justify-start gap-3">
            <h2 className="text-2xl font-bold text-gray-800">{user.nom}</h2>
            <span className="px-3 py-1 bg-primary/20 text-primary text-xs font-bold rounded-full uppercase tracking-wider">
              {user.role}
            </span>
          </div>
          <p className="text-gray-400 mt-1">{user.email}</p>
          <div className="flex flex-wrap justify-center md:justify-start gap-4 mt-4">
            <div className="flex items-center gap-2 text-sm text-gray-500 bg-gray-50 px-3 py-1.5 rounded-lg">
              <MapPin size={14} /> {user.localisation || "Sénégal"}
            </div>
            <div className="flex items-center gap-2 text-sm text-gray-500 bg-gray-50 px-3 py-1.5 rounded-lg">
              <Phone size={14} /> {user.telephone || "Non renseigné"}
            </div>
          </div>
        </div>
        <button 
          onClick={() => setIsEditing(!isEditing)}
          className="px-6 py-2.5 bg-gray-800 text-white rounded-xl text-sm font-medium hover:bg-gray-700 transition-colors flex items-center gap-2"
        >
          {isEditing ? "Annuler" : <><Settings size={16} /> Modifier</>}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Colonne Gauche - Infos */}
        <div className="md:col-span-2 flex flex-col gap-6">
          <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-sm">
            <h3 className="text-lg font-bold text-gray-800 mb-6 flex items-center gap-2">
              <Shield size={18} className="text-primary" /> Informations personnelles
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-bold text-gray-400 uppercase">Nom complet</label>
                {isEditing ? (
                  <input 
                    className="bg-gray-50 border border-gray-100 rounded-xl px-4 py-3 text-sm outline-none focus:border-primary"
                    value={form.nom}
                    onChange={(e) => setForm({...form, nom: e.target.value})}
                  />
                ) : (
                  <p className="text-gray-700 font-medium">{user.nom}</p>
                )}
              </div>
              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-bold text-gray-400 uppercase">Email</label>
                <p className="text-gray-700 font-medium">{user.email}</p>
              </div>
              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-bold text-gray-400 uppercase">Téléphone</label>
                {isEditing ? (
                  <input 
                    className="bg-gray-50 border border-gray-100 rounded-xl px-4 py-3 text-sm outline-none focus:border-primary"
                    value={form.telephone}
                    onChange={(e) => setForm({...form, telephone: e.target.value})}
                  />
                ) : (
                  <p className="text-gray-700 font-medium">{user.telephone || "N/A"}</p>
                )}
              </div>
              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-bold text-gray-400 uppercase">Localisation</label>
                {isEditing ? (
                  <input 
                    className="bg-gray-50 border border-gray-100 rounded-xl px-4 py-3 text-sm outline-none focus:border-primary"
                    value={form.localisation}
                    onChange={(e) => setForm({...form, localisation: e.target.value})}
                  />
                ) : (
                  <p className="text-gray-700 font-medium">{user.localisation || "Sénégal"}</p>
                )}
              </div>
            </div>

            {isEditing && (
              <button 
                onClick={handleSave}
                className="mt-8 w-full py-3 bg-primary text-[#102215] font-bold rounded-xl flex items-center justify-center gap-2 hover:opacity-90 transition-opacity"
              >
                <Save size={18} /> Enregistrer les modifications
              </button>
            )}
          </div>
        </div>

        {/* Colonne Droite - Cultures */}
        <div className="flex flex-col gap-6">
          <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-sm">
            <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
              <Leaf size={18} className="text-primary" /> Mes cultures
            </h3>
            <p className="text-xs text-gray-400 mb-4">Cultures prioritaires pour vos prévisions IA</p>
            
            <div className="flex flex-wrap gap-2">
              {culturesDisponibles.map(c => (
                <button 
                  key={c} 
                  onClick={() => toggleCulture(c)}
                  className={`px-4 py-2 border text-sm font-medium rounded-xl capitalize transition-all ${
                    (user.cultures_interet || "").split(",").includes(c)
                    ? "bg-primary/10 border-primary text-primary"
                    : "bg-gray-50 border-gray-100 text-gray-400 hover:border-gray-200"
                  }`}
                >
                  {c}
                </button>
              ))}
            </div>
            
            <p className="mt-4 text-[10px] text-gray-300 italic">Cliquez sur une culture pour l'ajouter ou la retirer de votre suivi.</p>
          </div>
        </div>

      </div>
    </div>
  );
};

export default Profil;
