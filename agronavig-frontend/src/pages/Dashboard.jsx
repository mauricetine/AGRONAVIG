import { useEffect, useState } from "react";
import {
  Leaf, Microscope, TrendingUp, AlertTriangle,
  ArrowUpRight, ArrowDownRight, Clock, CheckCircle2, XCircle,
} from "lucide-react";
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer,
} from "recharts";
import { getRapport, getPrevisions } from "../services/api";

const COLORS_GRAPH = ["#13ec49", "#60a5fa", "#c084fc", "#fbbf24", "#f87171"];

// Données graphique par défaut
const previsionsDefaut = [
  { mois: "Jan", tomate: 420, oignon: 280, carotte: 190 },
  { mois: "Fév", tomate: 380, oignon: 310, carotte: 220 },
  { mois: "Mar", tomate: 510, oignon: 290, carotte: 240 },
  { mois: "Avr", tomate: 470, oignon: 340, carotte: 210 },
  { mois: "Mai", tomate: 590, oignon: 380, carotte: 270 },
  { mois: "Jun", tomate: 620, oignon: 410, carotte: 300 },
];

const StatCard = ({ icon: Icon, label, value, change, positive, color }) => (
  <div className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
    <div className="flex items-start justify-between">
      <div className={`w-11 h-11 rounded-xl flex items-center justify-center ${color}`}>
        <Icon size={20} className="text-white" />
      </div>
      <span className={`flex items-center gap-1 text-xs font-medium ${positive ? "text-green-500" : "text-red-400"}`}>
        {positive ? <ArrowUpRight size={13} /> : <ArrowDownRight size={13} />}
        {change}
      </span>
    </div>
    <div className="mt-4">
      <p className="text-2xl font-bold text-gray-800">{value}</p>
      <p className="text-sm text-gray-400 mt-0.5">{label}</p>
    </div>
  </div>
);

const StatutBadge = ({ statut }) => {
  const styles = {
    "traité":     "bg-green-50 text-green-600",
    "en cours":   "bg-yellow-50 text-yellow-600",
    "en attente": "bg-red-50 text-red-500",
    "faible":     "bg-green-50 text-green-600",
    "moyen":      "bg-yellow-50 text-yellow-600",
    "élevé":      "bg-red-50 text-red-500",
  };
  const icons = {
    "traité":     <CheckCircle2 size={12} />,
    "en cours":   <Clock size={12} />,
    "en attente": <XCircle size={12} />,
    "faible":     <CheckCircle2 size={12} />,
    "moyen":      <Clock size={12} />,
    "élevé":      <XCircle size={12} />,
  };
  return (
    <span className={`flex items-center gap-1 text-xs font-medium px-2.5 py-1 rounded-full ${styles[statut] || "bg-gray-50 text-gray-500"}`}>
      {icons[statut]} {statut}
    </span>
  );
};

const Dashboard = () => {
  const [rapport, setRapport]         = useState(null);
  const [previsions, setPrevisions]   = useState(previsionsDefaut);
  const [loading, setLoading]         = useState(true);

  const [rendementTotal, setRendementTotal] = useState(0);

  useEffect(() => {
    Promise.all([getRapport(), getPrevisions()])
      .then(([rapportRes, prevRes]) => {
        setRapport(rapportRes.data);
        if (prevRes.data?.previsions) {
          // Simulation de données mensuelles basées sur le calcul réel pour le graphique
          const months = ["Juil", "Août", "Sep", "Oct", "Nov", "Déc"];
          const simulatedMonthly = months.map((m) => {
            const entry = { mois: m };
            prevRes.data.previsions.forEach(p => {
              const cultureKey = p.culture.toLowerCase().replace(/ /g, "_");
              entry[cultureKey] = p.rendement_estime * (0.8 + Math.random() * 0.4);
            });
            return entry;
          });
          setPrevisions(simulatedMonthly);
          
          // Calcul du rendement total
          const total = prevRes.data.previsions.reduce((acc, curr) => acc + curr.rendement_estime, 0);
          setRendementTotal(Math.round(total * 1000)); // Convertir en kg
        }
      })
      .catch(() => console.log("Erreur chargement dashboard"))
      .finally(() => setLoading(false));
  }, []);

  const totalDiagnostics = rapport?.total_diagnostics || 0;
  const alertes          = rapport?.derniers_diagnostics?.filter(d => d.niveau === "élevé").length || 0;
  const derniers         = rapport?.derniers_diagnostics?.slice(0, 4) || [];

  return (
    <div className="flex flex-col gap-6">

      {/* Cartes statistiques */}
      <div className="grid grid-cols-4 gap-4">
        <StatCard
          icon={Leaf}
          label="Cultures suivies"
          value={Object.keys(rapport?.repartition_cultures || {}).length || 0}
          change="Total cultures"
          positive={true}
          color="bg-primary"
        />
        <StatCard
          icon={Microscope}
          label="Diagnostics effectués"
          value={totalDiagnostics}
          change="Total diagnostics"
          positive={true}
          color="bg-blue-500"
        />
        <StatCard
          icon={TrendingUp}
          label="Estimation IA (kg)"
          value={rendementTotal.toLocaleString()}
          change="+12% vs prévu"
          positive={true}
          color="bg-purple-500"
        />
        <StatCard
          icon={AlertTriangle}
          label="Niveau de risque"
          value={alertes > 0 ? "Élevé" : "Faible"}
          change={alertes > 0 ? `${alertes} alertes` : "Aucune alerte"}
          positive={alertes === 0}
          color={alertes > 0 ? "bg-red-500" : "bg-orange-400"}
        />
      </div>

      {/* Graphique + Diagnostics récents */}
      <div className="grid grid-cols-3 gap-4">

        {/* Graphique */}
        <div className="col-span-2 bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-gray-800 font-semibold text-base">Prévisions des récoltes</h3>
              <p className="text-gray-400 text-xs mt-0.5">Rendement estimé en kg</p>
            </div>
            <div className="flex flex-wrap items-center gap-4 text-xs text-gray-400">
              {previsions.length > 0 && Object.keys(previsions[0]).filter(k => k !== "mois").map((c, i) => (
                <span key={c} className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full inline-block" style={{ backgroundColor: COLORS_GRAPH[i % COLORS_GRAPH.length] }} />
                  {c.charAt(0).toUpperCase() + c.slice(1).replace(/_/g, " ")}
                </span>
              ))}
            </div>
          </div>
          <ResponsiveContainer width="100%" height={220}>
            <AreaChart data={previsions}>
              <defs>
                {COLORS_GRAPH.map((color, i) => (
                  <linearGradient key={i} id={`color-${i}`} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor={color} stopOpacity={0.2} />
                    <stop offset="95%" stopColor={color} stopOpacity={0} />
                  </linearGradient>
                ))}
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="mois" tick={{ fontSize: 12, fill: "#9ca3af" }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 12, fill: "#9ca3af" }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={{ borderRadius: "12px", border: "1px solid #f0f0f0", fontSize: "12px" }} />
              {previsions.length > 0 && Object.keys(previsions[0]).filter(k => k !== "mois").map((c, i) => (
                <Area key={c} type="monotone" dataKey={c} stroke={COLORS_GRAPH[i % COLORS_GRAPH.length]} strokeWidth={2} fill={`url(#color-${i})`} />
              ))}
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Derniers diagnostics */}
        <div className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-gray-800 font-semibold text-base">Derniers diagnostics</h3>
            <span className="text-xs text-primary font-medium cursor-pointer hover:underline">
              {totalDiagnostics} total
            </span>
          </div>

          {loading ? (
            <div className="flex items-center justify-center h-40">
              <div className="w-6 h-6 border-2 border-primary border-t-transparent rounded-full animate-spin" />
            </div>
          ) : derniers.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-40 gap-2">
              <Microscope size={32} className="text-gray-200" />
              <p className="text-gray-400 text-sm">Aucun diagnostic</p>
              <p className="text-gray-300 text-xs">Faites votre premier diagnostic</p>
            </div>
          ) : (
            <div className="flex flex-col gap-3">
              {derniers.map((d) => (
                <div key={d.id} className="flex flex-col gap-1.5 p-3 rounded-xl bg-gray-50 hover:bg-gray-100 transition-colors cursor-pointer">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700 capitalize">{d.culture}</span>
                    <StatutBadge statut={d.niveau} />
                  </div>
                  <p className="text-xs text-gray-400">{d.maladie}</p>
                  <p className="text-xs text-gray-300">
                    {new Date(d.created_at).toLocaleDateString("fr-FR")}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>

      </div>
    </div>
  );
};

export default Dashboard;