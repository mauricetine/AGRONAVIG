import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/layout/Layout";
import Dashboard from "./pages/Dashboard";
import Diagnostic from "./pages/Diagnostic";
import ResultatDiagnostic from "./pages/ResultatDiagnostic";
import Prevision from "./pages/Prevision";
import ConseilIA from "./pages/ConseilIA";
import Rapport from "./pages/Rapport";
import Auth from "./pages/Auth";
import Admin from "./pages/Admin";
import Profil from "./pages/Profil";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Page publique — pas besoin d'être connecté */}
        <Route path="/auth" element={<Auth />} />

        {/* Pages protégées — redirect vers /auth si pas connecté */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard"          element={<Dashboard />} />
          <Route path="diagnostic"         element={<Diagnostic />} />
          <Route path="diagnostic/resultat"element={<ResultatDiagnostic />} />
          <Route path="prevision"          element={<Prevision />} />
          <Route path="conseil"            element={<ConseilIA />} />
          <Route path="rapport"            element={<Rapport />} />
          <Route path="profil"             element={<Profil />} />
          <Route 
            path="admin"              
            element={
              <ProtectedRoute adminOnly={true}>
                <Admin />
              </ProtectedRoute>
            } 
          />
        </Route>

        {/* Route inconnue → redirect dashboard */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;