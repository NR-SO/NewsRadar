import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

export default function Registro() {
  const [form, setForm] = useState({ nombre: '', apellidos: '', email: '', organizacion: '', password: '' });
  const navigate = useNavigate();

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    // TODO: llamar a POST /api/v1/auth/register
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0d0d0d]">
      <div className="bg-[#161616] border border-[#2a2a2a] rounded-lg p-8 w-full max-w-sm">
        <div className="flex items-center gap-2 mb-8">
          <span className="text-[#e63946] text-xl">◈</span>
          <span className="font-mono text-sm font-semibold tracking-widest">NEWSRADAR</span>
        </div>
        <h2 className="text-lg font-semibold mb-1">Únete a la red</h2>
        <p className="text-[#888] text-xs mb-6">Crea tu cuenta de analista</p>

        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          {[
            { name: 'nombre',       label: 'Nombre',       type: 'text',     placeholder: 'Juan' },
            { name: 'apellidos',    label: 'Apellidos',    type: 'text',     placeholder: 'Pérez' },
            { name: 'email',        label: 'Email',        type: 'email',    placeholder: 'email@ejemplo.com' },
            { name: 'organizacion', label: 'Organización', type: 'text',     placeholder: 'Empresa S.A.' },
            { name: 'password',     label: 'Contraseña',   type: 'password', placeholder: '••••••••' },
          ].map(({ name, label, type, placeholder }) => (
            <div key={name}>
              <label className="text-xs text-[#888] mb-1 block">{label}</label>
              <input
                type={type}
                name={name}
                value={form[name]}
                onChange={handleChange}
                placeholder={placeholder}
                className="w-full bg-[#1f1f1f] border border-[#2a2a2a] rounded px-3 py-2 text-sm text-white outline-none focus:border-[#e63946] transition-colors"
                required
              />
            </div>
          ))}
          <button
            type="submit"
            className="w-full bg-[#e63946] text-white text-sm font-semibold py-2 rounded hover:bg-[#c1121f] transition-colors mt-2"
          >
            Crear mi cuenta →
          </button>
        </form>

        <p className="text-center text-xs text-[#888] mt-6">
          ¿Ya tienes cuenta?{' '}
          <Link to="/login" className="text-[#e63946] hover:underline">Inicia sesión</Link>
        </p>
      </div>
    </div>
  );
}