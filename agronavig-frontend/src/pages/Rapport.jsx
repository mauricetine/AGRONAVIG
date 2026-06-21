import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import {
  BarChart3, Microscope, CheckCircle2, TrendingUp,
  Download, Filter, Calendar,
} from "lucide-react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, PieChart, Pie, Cell,
} from "recharts";
import { getRapport } from "../services/api";

const COLORS = ["#13ec49", "#60a5fa", "#f97316", "#c084fc", "#94a3b8"];

const StatutBadge = ({ niveau }) => {
  const styles = {
    "élevé":  "bg-red-50 text-red-500",
    "moyen":  "bg-yellow-50 text-yellow-600",
    "faible": "bg-green-50 text-green-600",
  };
  return (
    <span className={`text-xs font-medium px-2.5 py-1 rounded-full ${styles[niveau] || "bg-gray-50 text-gray-500"}`}>
      {niveau}
    </span>
  );
};

const StatCard = ({ icon: Icon, label, value, sub, color }) => (
  <div className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
    <div className={`w-11 h-11 rounded-xl flex items-center justify-center ${color} mb-4`}>
      <Icon size={20} className="text-white" />
    </div>
    <p className="text-2xl font-bold text-gray-800">{value}</p>
    <p className="text-sm text-gray-500 mt-0.5">{label}</p>
    <p className="text-xs text-gray-300 mt-1">{sub}</p>
  </div>
);

const Rapport = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const searchQuery = queryParams.get("q") || "";

  const [data, setData]         = useState(null);
  const [activite, setActivite] = useState([]);
  const [loading, setLoading]   = useState(true);
  const [filter, setFilter]     = useState(""); // Filtre par culture
  const [sortOrder, setSortOrder] = useState("desc"); // Tri par date

  useEffect(() => {
    getRapport()
      .then(res => {
        setData(res.data);
        if (res.data?.activite_mensuelle) {
          setActivite(res.data.activite_mensuelle);
        }
      })
      .catch(() => console.log("Erreur chargement rapport"))
      .finally(() => setLoading(false));
  }, []);

  // Préparer données camembert
  const maladiesPie = data?.repartition_maladies
    ? Object.entries(data.repartition_maladies).map(([name, value], i) => ({
        name, value, color: COLORS[i % COLORS.length]
      }))
    : [{ name: "Aucune donnée", value: 1, color: "#e5e7eb" }];

  const total      = data?.total_diagnostics || 0;
  const traites    = data?.maladies_traitees  || 0;
  const tauxSucces = total > 0 ? Math.round((traites / total) * 100) : 0;
  
  // Appliquer filtres et tri sur l'historique
  const historiqueRaw = data?.derniers_diagnostics || [];
  const historique = historiqueRaw
    .filter(d => {
      const matchFilter = filter === "" || d.culture.toLowerCase() === filter.toLowerCase();
      const matchSearch = searchQuery === "" || 
                          d.culture.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          d.maladie.toLowerCase().includes(searchQuery.toLowerCase());
      return matchFilter && matchSearch;
    })
    .sort((a, b) => {
      const dateA = new Date(a.created_at);
      const dateB = new Date(b.created_at);
      return sortOrder === "desc" ? dateB - dateA : dateA - dateB;
    });

  const culturesDisponibles = data?.repartition_cultures 
    ? Object.keys(data.repartition_cultures) 
    : [];

  return (
    <div className="flex flex-col gap-6">

      {/* Cartes stats */}
      <div className="grid grid-cols-4 gap-4">
        <StatCard
          icon={Microscope}
          label="Diagnostics effectués"
          value={total}
          sub="Total depuis le début"
          color="bg-[#13ec49]"
        />
        <StatCard
          icon={CheckCircle2}
          label="Maladies traitées"
          value={traites}
          sub={`${tauxSucces}% de taux de succès`}
          color="bg-blue-400"
        />
        <StatCard
          icon={TrendingUp}
          label="Cultures diagnostiquées"
          value={Object.keys(data?.repartition_cultures || {}).length}
          sub="Types de cultures"
          color="bg-purple-400"
        />
        <StatCard
          icon={BarChart3}
          label="Maladies identifiées"
          value={Object.keys(data?.repartition_maladies || {}).length}
          sub="Types de maladies"
          color="bg-orange-400"
        />
      </div>

      {/* Graphiques */}
      <div className="grid grid-cols-3 gap-6">

        {/* Activité mensuelle — données réelles */}
        <div className="col-span-2 bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
          <div className="flex items-center gap-2 mb-6">
            <Calendar size={17} className="text-primary" />
            <div>
              <h3 className="text-gray-800 font-semibold text-sm">Activité mensuelle</h3>
              <p className="text-gray-400 text-xs">
                Diagnostics réels — {new Date().getFullYear()}
              </p>
            </div>
          </div>
          {loading ? (
            <div className="flex items-center justify-center h-52">
              <div className="w-6 h-6 border-2 border-primary border-t-transparent rounded-full animate-spin" />
            </div>
          ) : (
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={activite} barSize={16}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis
                  dataKey="mois"
                  tick={{ fontSize: 12, fill: "#9ca3af" }}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis
                  tick={{ fontSize: 12, fill: "#9ca3af" }}
                  axisLine={false}
                  tickLine={false}
                  allowDecimals={false}
                />
                <Tooltip
                  contentStyle={{
                    borderRadius: "12px",
                    border: "1px solid #f0f0f0",
                    fontSize: "12px"
                  }}
                />
                <Bar
                  dataKey="diagnostics"
                  fill="#13ec49"
                  radius={[4, 4, 0, 0]}
                  name="Diagnostics"
                />
                <Bar
                  dataKey="conseils"
                  fill="#60a5fa"
                  radius={[4, 4, 0, 0]}
                  name="Conseils IA"
                />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* Répartition maladies */}
        <div className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <BarChart3 size={17} className="text-primary" />
            <h3 className="text-gray-700 font-semibold text-sm">Maladies détectées</h3>
          </div>
          <ResponsiveContainer width="100%" height={180}>
            <PieChart>
              <Pie
                data={maladiesPie}
                cx="50%"
                cy="50%"
                innerRadius={50}
                outerRadius={75}
                paddingAngle={3}
                dataKey="value"
              >
                {maladiesPie.map((entry, index) => (
                  <Cell key={index} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  borderRadius: "12px",
                  border: "1px solid #f0f0f0",
                  fontSize: "12px"
                }}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="flex flex-col gap-1.5 mt-2">
            {maladiesPie.map((m) => (
              <div key={m.name} className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <span
                    className="w-2.5 h-2.5 rounded-full shrink-0"
                    style={{ backgroundColor: m.color }}
                  />
                  <span className="text-gray-500 truncate max-w-[120px]">{m.name}</span>
                </div>
                <span className="font-medium text-gray-700">{m.value}</span>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Tableau historique */}
      <div className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Microscope size={17} className="text-primary" />
            <h3 className="text-gray-800 font-semibold text-sm">
              Historique des diagnostics
            </h3>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 bg-gray-50 border border-gray-200 rounded-xl px-3 py-1.5">
              <Filter size={13} className="text-gray-400" />
              <select 
                className="bg-transparent text-xs text-gray-600 outline-none cursor-pointer"
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
              >
                <option value="">Toutes les cultures</option>
                {culturesDisponibles.map(c => (
                  <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>
                ))}
              </select>
            </div>
            <button 
              onClick={() => setSortOrder(sortOrder === "desc" ? "asc" : "desc")}
              className="flex items-center gap-2 px-3 py-2 rounded-xl border border-gray-200 text-gray-500 text-xs hover:bg-gray-50 transition-colors"
            >
              <Calendar size={13} /> {sortOrder === "desc" ? "Plus récents" : "Plus anciens"}
            </button>
          </div>
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-32">
            <div className="w-6 h-6 border-2 border-primary border-t-transparent rounded-full animate-spin" />
          </div>
        ) : historique.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-32 gap-2">
            <Microscope size={32} className="text-gray-200" />
            <p className="text-gray-400 text-sm">Aucun diagnostic pour l'instant</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-100">
                  {["Date", "Culture", "Maladie détectée", "Confiance IA", "Traitement", "Niveau"].map(h => (
                    <th
                      key={h}
                      className="text-left text-xs font-semibold text-gray-400 pb-3 pr-4"
                    >
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {historique.map((row) => (
                  <tr
                    key={row.id}
                    className="border-b border-gray-50 hover:bg-gray-50 transition-colors"
                  >
                    <td className="py-3 pr-4 text-xs text-gray-400">
                      {new Date(row.created_at).toLocaleDateString("fr-FR")}
                    </td>
                    <td className="py-3 pr-4 text-sm font-medium text-gray-700 capitalize">
                      {row.culture}
                    </td>
                    <td className="py-3 pr-4 text-sm text-gray-600">{row.maladie}</td>
                    <td className="py-3 pr-4">
                      <div className="flex items-center gap-2">
                        <div className="w-16 bg-gray-100 rounded-full h-1.5">
                          <div
                            className="h-1.5 rounded-full bg-primary"
                            style={{ width: `${row.confiance}%` }}
                          />
                        </div>
                        <span className="text-xs font-medium text-gray-600">
                          {row.confiance}%
                        </span>
                      </div>
                    </td>
                    <td className="py-3 pr-4 text-xs text-gray-500">{row.traitement}</td>
                    <td className="py-3"><StatutBadge niveau={row.niveau} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

    </div>
  );
};

export default Rapport;