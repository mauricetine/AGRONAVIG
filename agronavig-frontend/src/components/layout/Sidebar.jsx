import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  Microscope,
  TrendingUp,
  MessageSquareText,
  BarChart3,
  Leaf,
  LogOut,
  ShieldCheck
} from "lucide-react";

const navItems = [
  { path: "/dashboard", icon: LayoutDashboard,  label: "Dashboard",   userOnly: true },
  { path: "/diagnostic",icon: Microscope,        label: "Diagnostic",  userOnly: true },
  { path: "/prevision", icon: TrendingUp,        label: "Prévisions",  userOnly: true },
  { path: "/conseil",   icon: MessageSquareText, label: "Conseil IA",  userOnly: true },
  { path: "/rapport",   icon: BarChart3,         label: "Rapports"    },
  { path: "/admin",     icon: ShieldCheck,       label: "Administration", adminOnly: true },
];

import { X } from "lucide-react";

const Sidebar = ({ isOpen, setOpen }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    localStorage.removeItem("dernierDiagnostic");
    navigate("/auth");
  };

  return (
    <aside className={`fixed top-0 left-0 h-screen w-64 bg-[#102215] flex flex-col z-50 transition-transform duration-300 lg:translate-x-0 ${isOpen ? "translate-x-0" : "-translate-x-full"}`}>
      
      {/* Bouton fermer sur mobile */}
      <button 
        onClick={() => setOpen(false)}
        className="lg:hidden absolute top-4 right-4 text-white/60 hover:text-white"
      >
        <X size={20} />
      </button>

      {/* Logo */}
      <div className="flex items-center gap-2 px-6 py-6 border-b border-white/10">
        <img src="/images/logo.png" alt="AgroNavig Logo" className="w-25 h-25 object-contain rounded-lg" />
        
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 flex flex-col gap-1">
        {navItems.filter(item => {
          const user = JSON.parse(localStorage.getItem("user") || "{}");
          const userRole = (user.role || "").toLowerCase();
          if (item.adminOnly && userRole !== "admin") return false;
          if (item.userOnly && userRole === "admin") return false;
          return true;
        }).map(({ path, icon: Icon, label }) => (
          <NavLink
            key={path}
            to={path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 ${
                isActive
                  ? "bg-primary text-[#102215] font-semibold"
                  : "text-white/60 hover:text-white hover:bg-white/10"
              }`
            }
          >
            <Icon size={18} />
            {label}
          </NavLink>
        ))}
      </nav>

      {/* Déconnexion */}
      <div className="px-4 py-6 border-t border-white/10">
        <button
          onClick={handleLogout}
          className="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-white/60 hover:text-white hover:bg-white/10 transition-all duration-200 w-full"
        >
          <LogOut size={18} />
          Déconnexion
        </button>
      </div>

    </aside>
  );
};

export default Sidebar;