import { useState, useEffect } from "react";
import { Users, Microscope, TrendingUp, AlertTriangle, UserCheck, Shield, Activity, Settings, X } from "lucide-react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, PieChart, Pie, Cell,
} from "recharts";
import axios from "axios";

const COLORS = ["#13ec49", "#60a5fa", "#f97316", "#c084fc", "#ef4444"];

const Admin = () => {
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchData = () => {
    const token = localStorage.getItem("token");
    const config = { headers: { Authorization: `Bearer ${token}` } };
    
    Promise.all([
      axios.get("http://localhost:8000/api/admin/stats", config),
      axios.get("http://localhost:8000/api/admin/users", config)
    ])
    .then(([statsRes, usersRes]) => {
      setStats(statsRes.data);
      setUsers(usersRes.data);
    })
    .catch(err => console.error("Erreur admin:", err))
    .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleToggleStatus = async (userId) => {
    try {
      const token = localStorage.getItem("token");
      await axios.post(`http://localhost:8000/api/admin/users/${userId}/toggle`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchData(); // Rafraîchir
    } catch (err) {
      alert("Erreur lors de la modification du statut");
    }
  };

  const handleDeleteUser = async (userId) => {
    if (!window.confirm("Êtes-vous sûr de vouloir supprimer cet utilisateur ?")) return;
    try {
      const token = localStorage.getItem("token");
      await axios.delete(`http://localhost:8000/api/admin/users/${userId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchData(); // Rafraîchir
    } catch (err) {
      alert("Erreur lors de la suppression");
    }
  };

  if (loading) return (
    <div className="flex items-center justify-center h-screen">
      <div className="w-10 h-10 border-4 border-primary border-t-transparent rounded-full animate-spin" />
    </div>
  );

  const rolesData = Object.entries(stats?.roles_distribution || {}).map(([name, value]) => ({ name, value }));

  return (
    <div className="flex flex-col gap-8">
      
      {/* Header Admin */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-3">
            <Shield className="text-primary" /> Panneau d'Administration
          </h2>
          <p className="text-gray-400 text-sm mt-1">Surveillance globale de la plateforme AgroNavig</p>
        </div>
        <div className="flex items-center gap-2 bg-green-50 text-green-600 px-4 py-2 rounded-xl text-xs font-bold uppercase">
          <Activity size={14} /> Système Opérationnel
        </div>
      </div>

      {/* Cartes Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
          <Users className="text-blue-500 mb-3" size={24} />
          <p className="text-2xl font-bold text-gray-800">{stats?.total_users}</p>
          <p className="text-xs text-gray-400 uppercase font-bold tracking-wider">Utilisateurs</p>
        </div>
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
          <Microscope className="text-primary mb-3" size={24} />
          <p className="text-2xl font-bold text-gray-800">{stats?.total_diagnostics}</p>
          <p className="text-xs text-gray-400 uppercase font-bold tracking-wider">Diagnostics</p>
        </div>
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
          <TrendingUp className="text-purple-500 mb-3" size={24} />
          <p className="text-2xl font-bold text-gray-800">89%</p>
          <p className="text-xs text-gray-400 uppercase font-bold tracking-wider">Taux de Précision IA</p>
        </div>
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
          <AlertTriangle className="text-orange-500 mb-3" size={24} />
          <p className="text-2xl font-bold text-gray-800">12</p>
          <p className="text-xs text-gray-400 uppercase font-bold tracking-wider">Alertes Critiques</p>
        </div>
      </div>

      {/* Graphiques */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
          <h3 className="text-sm font-bold text-gray-700 mb-6 uppercase">Répartition des rôles</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={rolesData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                  {rolesData.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
          <h3 className="text-sm font-bold text-gray-700 mb-6 uppercase">Top Maladies Détectées</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats?.top_maladies}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
                <XAxis dataKey="nom" tick={{fontSize: 10}} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#13ec49" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Liste des Utilisateurs */}
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-gray-50 flex items-center justify-between">
          <h3 className="text-sm font-bold text-gray-700 uppercase">Gestion des Utilisateurs</h3>
          <button className="text-xs text-primary font-bold hover:underline">Tout voir</button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-gray-50 text-xs text-gray-400 uppercase font-bold">
              <tr>
                <th className="px-6 py-4">Utilisateur</th>
                <th className="px-6 py-4">Rôle</th>
                <th className="px-6 py-4">Email</th>
                <th className="px-6 py-4">Statut</th>
                <th className="px-6 py-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {users.map((u) => (
                <tr key={u.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center text-primary font-bold text-xs">
                        {u.nom[0]}
                      </div>
                      <span className="text-sm font-medium text-gray-700">{u.nom}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="px-2 py-1 bg-gray-100 text-gray-500 text-[10px] font-bold rounded uppercase">
                      {u.role}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-400">{u.email}</td>
                  <td className="px-6 py-4">
                    <span className={`flex items-center gap-1.5 text-xs font-medium ${u.is_active ? "text-green-500" : "text-red-400"}`}>
                      {u.is_active ? <UserCheck size={14} /> : <X size={14} />}
                      {u.is_active ? "Actif" : "Inactif"}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex items-center justify-end gap-3">
                      <button 
                        onClick={() => handleToggleStatus(u.id)} 
                        title={u.is_active ? "Désactiver" : "Activer"}
                        className={`p-2 rounded-lg transition-all ${u.is_active ? "text-orange-300 hover:text-orange-500 hover:bg-orange-50" : "text-green-300 hover:text-green-500 hover:bg-green-50"}`}
                      >
                        <Settings size={14} />
                      </button>
                      <button 
                        onClick={() => handleDeleteUser(u.id)} 
                        title="Supprimer"
                        className="p-2 text-gray-300 hover:text-red-500 hover:bg-red-50 rounded-lg transition-all"
                      >
                        <X size={14} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};

export default Admin;
