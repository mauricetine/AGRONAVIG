import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";
import TopBar from "./TopBar";

import { useState } from "react";

const Layout = () => {
  const [isSidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#f6f8f6]">
      
      {/* Sidebar - Responsive */}
      <Sidebar isOpen={isSidebarOpen} setOpen={setSidebarOpen} />

      {/* Contenu principal */}
      <div className="lg:ml-64 transition-all duration-300">
        
        {/* TopBar - Responsive */}
        <TopBar setSidebarOpen={setSidebarOpen} />

        {/* Pages */}
        <main className="pt-16 min-h-screen">
          <div className="p-4 lg:p-6">
            <Outlet />
          </div>
        </main>

      </div>

      {/* Overlay pour mobile quand la sidebar est ouverte */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

    </div>
  );
};

export default Layout;