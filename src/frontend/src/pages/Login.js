import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    // TODO: llamar a POST /api/v1/auth/login
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0d0d0d]">
      <div className="bg-[#161616] border border-[#2a2a2a] rounded-lg p-8 w-full max-w-sm">
        <div className="flex items-center gap-2 mb-8">
          <span className="text-[#e63946] text-xl">◈</span>
          <span className="font-mono text-sm font-semibold tracking-widest">NEWSRADAR</span>
        </div>
        <h2 className="text-lg font-semibold mb-1">Bienvenido</h2>
        <p className="text-[#888] text-xs mb-6">Accede a tu panel de control</p>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div>
            <label className="text-xs text-[#888] mb-1 block">Email</label>
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="email@ejemplo.com"
              className="w-full bg-[#1f1f1f] border border-[#2a2a2a] rounded px-3 py-2 text-sm text-white outline-none focus:border-[#e63946] transition-colors"
              required
            />
          </div>
          <div>
            <label className="text-xs text-[#888] mb-1 block">Contraseña</label>
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full bg-[#1f1f1f] border border-[#2a2a2a] rounded px-3 py-2 text-sm text-white outline-none focus:border-[#e63946] transition-colors"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-[#e63946] text-white text-sm font-semibold py-2 rounded hover:bg-[#c1121f] transition-colors mt-2"
          >
            Entrar al sistema →
          </button>
        </form>

        <p className="text-center text-xs text-[#888] mt-6">
          ¿No tienes cuenta?{' '}
          <Link to="/registro" className="text-[#e63946] hover:underline">Regístrate aquí</Link>
        </p>
      </div>
    </div>
  );
}