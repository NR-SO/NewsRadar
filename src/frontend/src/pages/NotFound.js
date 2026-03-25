import { Link } from 'react-router-dom';

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#0d0d0d]">
      <span className="font-mono text-6xl font-bold text-[#2a2a2a] mb-4">404</span>
      <p className="text-[#888] text-sm mb-6">Página no encontrada</p>
      <Link to="/dashboard" className="text-[#e63946] text-sm hover:underline">← Volver al dashboard</Link>
    </div>
  );
}