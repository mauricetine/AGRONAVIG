import { useEffect, useState } from "react";
import { Cloud, Wind, Droplets, Thermometer, TrendingUp, Calendar, Leaf } from "lucide-react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, LineChart, Line, Legend,
} from "recharts";
import { getPrevisions } from "../services/api";

// Données par défaut si API indisponible
const meteoDefaut = {
  ville: "Dakar, Sénégal", temperature: 28, ressenti: 31,
  humidite: 74, vent: 18, condition: "Partiellement nuageux",
  previsions: [
    { jour: "Lun", temp: 28, icon: "☀️" },
    { jour: "Mar", temp: 29, icon: "⛅" },
    { jour: "Mer", temp: 27, icon: "🌧️" },
    { jour: "Jeu", temp: 26, icon: "🌧️" },
    { jour: "Ven", temp: 28, icon: "⛅" },
    { jour: "Sam", temp: 30, icon: "☀️" },
    { jour: "Dim", temp: 31, icon: "☀️" },
  ],
};

const previsionsDefaut = [
  { mois: "Juil", tomate: 580, oignon: 420, carotte: 310, laitue: 190 },
  { mois: "Août", tomate: 620, oignon: 390, carotte: 340, laitue: 210 },
  { mois: "Sep",  tomate: 540, oignon: 450, carotte: 290, laitue: 240 },
  { mois: "Oct",  tomate: 680, oignon: 480, carotte: 370, laitue: 260 },
  { mois: "Nov",  tomate: 720, oignon: 510, carotte: 400, laitue: 280 },
  { mois: "Déc",  tomate: 690, oignon: 470, carotte: 380, laitue: 250 },
];

const culturesDefaut = [
  { culture: "Tomate",  rendement: 720, objectif: 800, progression: 90, emoji: "🍅", color: "#13ec49" },
  { culture: "Oignon",  rendement: 510, objectif: 600, progression: 85, emoji: "🧅", color: "#60a5fa" },
  { culture: "Carotte", rendement: 400, objectif: 450, progression: 89, emoji: "🥕", color: "#f97316" },
  { culture: "Laitue",  rendement: 280, objectif: 300, progression: 93, emoji: "🥬", color: "#c084fc" },
];

const MeteoStat = ({ icon: Icon, label, value, color }) => (
  <div className="flex items-center gap-3 bg-white/10 rounded-xl px-4 py-3">
    <Icon size={18} className={color} />
    <div>
      <p className="text-white/50 text-xs">{label}</p>
      <p className="text-white font-semibold text-sm">{value}</p>
    </div>
  </div>
);

const Prevision = () => {
  const [meteo, setMeteo]               = useState(meteoDefaut);
  const [previsionsData, setPrevisions] = useState([]);
  const [cultures, setCultures]         = useState([]);
  const [loading, setLoading]           = useState(true);

  const COLORS_GRAPH = ["#13ec49", "#60a5fa", "#f97316", "#c084fc", "#f87171", "#fbbf24"];

  useEffect(() => {
    getPrevisions()
      .then(res => {
        const data = res.data;
        if (data.meteo_contexte) setMeteo({ ...meteoDefaut, ...data.meteo_contexte });
        if (data.previsions && data.previsions.length > 0) {
          const mappedCultures = data.previsions.map((p, i) => ({
            culture: p.culture,
            rendement: p.rendement_estime,
            revenu: p.chiffre_affaire_estime,
            eau: p.besoin_eau_quotidien,
            risques: p.risques,
            objectif: p.rendement_estime * 1.2,
            progression: 85,
            emoji: culturesDefaut.find(c => c.culture.toLowerCase() === p.culture.toLowerCase())?.emoji || "🌱",
            color: COLORS_GRAPH[i % COLORS_GRAPH.length]
          }));
          setCultures(mappedCultures);
          
          const months = ["Juil", "Août", "Sep", "Oct", "Nov", "Déc"];
          const simulatedMonthly = months.map((m) => {
            const entry = { mois: m };
            data.previsions.forEach(p => {
              entry[p.culture.toLowerCase()] = p.rendement_estime * (0.8 + Math.random() * 0.4);
            });
            return entry;
          });
          setPrevisions(simulatedMonthly);
        } else {
          setPrevisions(previsionsDefaut);
          setCultures(culturesDefaut);
        }
      })
      .catch(() => {
        setPrevisions(previsionsDefaut);
        setCultures(culturesDefaut);
      })
      .finally(() => setLoading(false));
  }, []);

  const iconsMeteo = { "☀️": "☀️", "01d": "☀️", "02d": "⛅", "04d": "⛅", "10d": "🌧️" };

  return (
    <div className="flex flex-col gap-6">

      {/* Bloc météo */}
      <div className="bg-gradient-to-br from-[#102215] to-[#1a3a24] rounded-2xl p-6 shadow-md">
        <div className="flex items-start justify-between">
          <div className="flex items-start gap-4">
            <span className="text-6xl">⛅</span>
            <div>
              <p className="text-white/50 text-sm">{meteo.ville || "Dakar, Sénégal"}</p>
              <p className="text-white font-bold text-5xl mt-1">{meteo.temperature}°C</p>
              <p className="text-white/40 text-sm mt-1">
                Ressenti {meteo.ressenti}°C · {meteo.condition}
              </p>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <MeteoStat icon={Droplets}    label="Humidité"  value={`${meteo.humidite}%`}  color="text-blue-300" />
            <MeteoStat icon={Wind}        label="Vent"      value={`${meteo.vent} km/h`}   color="text-gray-300" />
            <MeteoStat icon={Thermometer} label="Ressenti"  value={`${meteo.ressenti}°C`}  color="text-orange-300" />
            <MeteoStat icon={Cloud}       label="Condition" value="Nuageux"                color="text-white/60" />
          </div>
        </div>

        {/* Prévisions 7 jours */}
        <div className="mt-6 pt-4 border-t border-white/10">
          <p className="text-white/40 text-xs mb-3 uppercase tracking-wide">Prévisions 7 jours</p>
          <div className="grid grid-cols-7 gap-2">
            {meteo.previsions.map((p, i) => (
              <div key={i} className="flex flex-col items-center gap-1.5 bg-white/5 rounded-xl py-3">
                <span className="text-white/40 text-xs">{p.jour}</span>
                <span className="text-xl">{iconsMeteo[p.icon] || p.icon || "⛅"}</span>
                <span className="text-white font-medium text-sm">{p.temp}°</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Graphique + tableau */}
      <div className="grid grid-cols-3 gap-6">

        {/* Graphique linéaire */}
        <div className="col-span-2 bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
          <div className="flex items-center gap-2 mb-6">
            <TrendingUp size={17} className="text-primary" />
            <div>
              <h3 className="text-gray-800 font-semibold text-sm">Prévisions des rendements</h3>
              <p className="text-gray-400 text-xs">Estimation en kg — 6 prochains mois</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={previsionsData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="mois" tick={{ fontSize: 12, fill: "#9ca3af" }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 12, fill: "#9ca3af" }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={{ borderRadius: "12px", border: "1px solid #f0f0f0", fontSize: "12px" }} />
              <Legend wrapperStyle={{ fontSize: "12px" }} />
              {previsionsData.length > 0 && Object.keys(previsionsData[0]).filter(k => k !== "mois").map((c, i) => (
                <Line key={c} type="monotone" dataKey={c} stroke={COLORS_GRAPH[i % COLORS_GRAPH.length]} strokeWidth={2} dot={{ r: 4 }} name={c.charAt(0).toUpperCase() + c.slice(1)} />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Objectifs par culture */}
        <div className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <Leaf size={17} className="text-primary" />
            <h3 className="text-gray-700 font-semibold text-sm">Objectifs par culture</h3>
          </div>
          <div className="flex flex-col gap-4 overflow-y-auto max-h-[240px] pr-2">
            {cultures.map((c) => (
              <div key={c.culture} className="flex flex-col gap-2 p-3 bg-gray-50 rounded-xl">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span>{c.emoji}</span>
                    <span className="text-sm font-bold text-gray-700">{c.culture}</span>
                  </div>
                  <span className="text-[10px] font-bold text-primary">{c.rendement} Tonnes</span>
                </div>
                <div className="flex justify-between text-[10px] text-gray-400">
                  <span>Revenu: <b className="text-gray-600">{c.revenu?.toLocaleString()} F</b></span>
                  <span>Eau: <b className="text-blue-400">{c.eau?.toLocaleString()} L/j</b></span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-1.5 mt-1">
                  <div className="h-1.5 rounded-full transition-all" style={{ width: `${c.progression}%`, backgroundColor: c.color }} />
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Graphique barres */}
      <div className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
        <div className="flex items-center gap-2 mb-6">
          <Calendar size={17} className="text-primary" />
          <div>
            <h3 className="text-gray-800 font-semibold text-sm">Comparaison des rendements par culture</h3>
            <p className="text-gray-400 text-xs">Vue mensuelle comparative en kg</p>
          </div>
        </div>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={previsionsData} barSize={16}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="mois" tick={{ fontSize: 12, fill: "#9ca3af" }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fontSize: 12, fill: "#9ca3af" }} axisLine={false} tickLine={false} />
            <Tooltip contentStyle={{ borderRadius: "12px", border: "1px solid #f0f0f0", fontSize: "12px" }} />
            <Legend wrapperStyle={{ fontSize: "12px" }} />
            {previsionsData.length > 0 && Object.keys(previsionsData[0]).filter(k => k !== "mois").map((c, i) => (
              <Bar key={c} dataKey={c} fill={COLORS_GRAPH[i % COLORS_GRAPH.length]} radius={[4, 4, 0, 0]} name={c.charAt(0).toUpperCase() + c.slice(1)} />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>

    </div>
  );
};

export default Prevision;