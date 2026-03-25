import { Routes, Route, Navigate } from 'react-router-dom';
import AppLayout      from './components/layout/AppLayout';
import Dashboard      from './pages/Dashboard';
import Alertas        from './pages/Alertas';
import FuentesRSS     from './pages/FuentesRSS';
import Notificaciones from './pages/Notificaciones';
import Perfil         from './pages/Perfil';
import Login          from './pages/Login';
import Registro       from './pages/Registro';
import NotFound       from './pages/NotFound';
import './assets/global.css';

export default function App() {
  return (
    <Routes>
      {/* Auth */}
      <Route path="/login"    element={<Login />} />
      <Route path="/registro" element={<Registro />} />

      {/* App con sidebar */}
      <Route element={<AppLayout />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard"      element={<Dashboard />} />
        <Route path="/alertas"        element={<Alertas />} />
        <Route path="/fuentes-rss"    element={<FuentesRSS />} />
        <Route path="/notificaciones" element={<Notificaciones />} />
        <Route path="/perfil"         element={<Perfil />} />
      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}