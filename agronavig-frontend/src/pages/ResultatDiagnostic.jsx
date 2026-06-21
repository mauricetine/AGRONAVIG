import { useEffect, useState } from "react";
import {
  AlertTriangle,
  CheckCircle2,
  ArrowLeft,
  Microscope,
  Pill,
  ShieldAlert,
  Leaf,
  ChevronRight,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

// Données de fallback si pas de diagnostic en localStorage
const resultatDefaut = {
  culture:     "Tomate",
  maladie:     "Mildiou (Phytophthora infestans)",
  confiance:   92,
  niveau:      "élevé",
  description: "Le mildiou est une maladie fongique très répandue qui affecte principalement les tomates. Elle se développe rapidement dans des conditions humides et fraîches.",
  symptomes: [
    "Taches brun-jaunâtres sur les feuilles",
    "Duvet blanc-grisâtre sous les feuilles",
    "Noircissement et pourriture des tiges",
    "Fruits présentant des taches brunes et fermes",
  ],
  traitements: [
    { type: "Traitement chimique",    produit: "Bouillie bordelaise",      dose: "20g / 10L d'eau",  frequence: "Tous les 7-10 jours", icon: "💊" },
    { type: "Traitement biologique",  produit: "Trichoderma harzianum",    dose: "5g / L d'eau",     frequence: "Tous les 14 jours",   icon: "🌿" },
  ],
  prevention: [
    "Éviter l'arrosage par aspersion le soir",
    "Assurer une bonne aération entre les plants",
    "Retirer et brûler les parties infectées",
    "Pratiquer la rotation des cultures",
  ],
};

// Badge niveau
const NiveauBadge = ({ niveau }) => {
  const styles = {
    "élevé":  { bg: "bg-red-50",    text: "text-red-500",    icon: <AlertTriangle size={13} /> },
    "moyen":  { bg: "bg-orange-50", text: "text-orange-500", icon: <AlertTriangle size={13} /> },
    "faible": { bg: "bg-green-50",  text: "text-green-600",  icon: <CheckCircle2  size={13} /> },
  };
  const s = styles[niveau] || styles["moyen"];
  return (
    <span className={`flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-full ${s.bg} ${s.text}`}>
      {s.icon} Gravité {niveau}
    </span>
  );
};

const ResultatDiagnostic = () => {
  const navigate = useNavigate();
  const [resultat, setResultat] = useState(null);

  useEffect(() => {
    const data = localStorage.getItem("dernierDiagnostic");
    if (data) {
      const parsed = JSON.parse(data);
      
      // Si on a les nouveaux champs détaillés de l'API
      if (parsed.description && parsed.symptomes) {
        setResultat({
          culture:    parsed.culture,
          maladie:    parsed.maladie,
          confiance:  parsed.confiance,
          niveau:     parsed.niveau,
          description: parsed.description,
          symptomes:   parsed.symptomes,
          prevention:  parsed.prevention,
          traitements: parsed.traitements.map(t => ({ ...t, icon: t.type.includes("Bio") ? "🌿" : "💊" })),
        });
      } else {
        // Fallback pour les anciens diagnostics ou données incomplètes
        setResultat({
          ...resultatDefaut,
          culture:    parsed.culture    || resultatDefaut.culture,
          maladie:    parsed.maladie    || resultatDefaut.maladie,
          confiance:  parsed.confiance  || resultatDefaut.confiance,
          niveau:     parsed.niveau     || resultatDefaut.niveau,
        });
      }
    } else {
      setResultat(resultatDefaut);
    }
  }, []);

  if (!resultat) return (
    <div className="flex items-center justify-center h-64">
      <div className="w-6 h-6 border-2 border-primary border-t-transparent rounded-full animate-spin" />
    </div>
  );

  return (
    <div className="flex flex-col gap-6 max-w-4xl mx-auto">

      {/* En-tête */}
      <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={() => navigate("/diagnostic")}
              className="w-9 h-9 bg-gray-50 rounded-xl flex items-center justify-center hover:bg-gray-100 transition-colors border border-gray-200"
            >
              <ArrowLeft size={16} className="text-gray-500" />
            </button>
            <div>
              <h2 className="text-gray-800 font-semibold text-lg">Résultats du diagnostic</h2>
              <p className="text-gray-400 text-sm">Analyse IA complétée avec succès</p>
            </div>
          </div>
          <div className="flex items-center gap-2 bg-green-50 border border-green-100 px-4 py-2 rounded-xl">
            <CheckCircle2 size={15} className="text-green-500" />
            <span className="text-sm font-medium text-green-600">Analyse terminée</span>
          </div>
        </div>
      </div>

      {/* Résultat principal */}
      <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-4">
            <div className="w-14 h-14 bg-red-50 rounded-2xl flex items-center justify-center">
              <Microscope size={26} className="text-red-400" />
            </div>
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs font-medium text-gray-400 uppercase tracking-wide">Culture analysée</span>
                <span className="flex items-center gap-1 text-xs font-medium text-primary bg-primary/10 px-2 py-0.5 rounded-full">
                  <Leaf size={11} /> {resultat.culture}
                </span>
              </div>
              <h3 className="text-gray-800 font-bold text-xl">{resultat.maladie}</h3>
              <p className="text-gray-400 text-sm mt-1 max-w-lg">{resultat.description}</p>
            </div>
          </div>
          <NiveauBadge niveau={resultat.niveau} />
        </div>

        {/* Barre de confiance */}
        <div className="mt-6 bg-gray-50 rounded-xl p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-600">Niveau de confiance IA</span>
            <span className="text-lg font-bold text-primary">{resultat.confiance}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div
              className="bg-primary h-2.5 rounded-full transition-all duration-700"
              style={{ width: `${resultat.confiance}%` }}
            />
          </div>
          <p className="text-xs text-gray-400 mt-2">Le modèle est très confiant dans ce diagnostic.</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">

        {/* Symptômes */}
        <div className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <ShieldAlert size={17} className="text-orange-400" />
            <h3 className="text-gray-700 font-semibold text-sm">Symptômes identifiés</h3>
          </div>
          <div className="flex flex-col gap-2">
            {resultat.symptomes.map((s, i) => (
              <div key={i} className="flex items-start gap-2.5 p-3 bg-orange-50 rounded-xl">
                <ChevronRight size={14} className="text-orange-400 mt-0.5 shrink-0" />
                <span className="text-sm text-gray-600">{s}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Prévention */}
        <div className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <Leaf size={17} className="text-primary" />
            <h3 className="text-gray-700 font-semibold text-sm">Mesures préventives</h3>
          </div>
          <div className="flex flex-col gap-2">
            {resultat.prevention.map((p, i) => (
              <div key={i} className="flex items-start gap-2.5 p-3 bg-green-50 rounded-xl">
                <CheckCircle2 size={14} className="text-green-500 mt-0.5 shrink-0" />
                <span className="text-sm text-gray-600">{p}</span>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Traitements */}
      <div className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
        <div className="flex items-center gap-2 mb-4">
          <Pill size={17} className="text-blue-400" />
          <h3 className="text-gray-700 font-semibold text-sm">Traitements recommandés</h3>
        </div>
        <div className="grid grid-cols-2 gap-4">
          {resultat.traitements.map((t, i) => (
            <div key={i} className="border border-gray-100 rounded-xl p-4 hover:border-primary/30 hover:bg-primary/5 transition-all">
              <div className="flex items-center gap-2 mb-3">
                <span className="text-2xl">{t.icon}</span>
                <span className="text-sm font-semibold text-gray-700">{t.type}</span>
              </div>
              <div className="flex flex-col gap-2">
                <div className="flex justify-between text-xs">
                  <span className="text-gray-400">Produit</span>
                  <span className="font-medium text-gray-700">{t.produit}</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-gray-400">Dose</span>
                  <span className="font-medium text-gray-700">{t.dose}</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-gray-400">Fréquence</span>
                  <span className="font-medium text-gray-700">{t.frequence}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-3">
        <button
          onClick={() => navigate("/diagnostic")}
          className="flex-1 py-3.5 rounded-2xl border border-gray-200 text-gray-600 font-medium text-sm hover:bg-gray-50 transition-colors"
        >
          Nouveau diagnostic
        </button>
        <button
          onClick={() => navigate("/conseil")}
          className="flex-1 py-3.5 rounded-2xl bg-primary text-[#102215] font-semibold text-sm hover:opacity-90 transition-opacity shadow-md"
        >
          Obtenir des conseils personnalisés →
        </button>
      </div>

    </div>
  );
};

export default ResultatDiagnostic;