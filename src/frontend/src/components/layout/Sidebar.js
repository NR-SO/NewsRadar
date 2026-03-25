import { NavLink, useNavigate } from 'react-router-dom';
import { MdDashboard, MdOutlineSummarize, MdNotifications, MdPerson, MdLogout } from 'react-icons/md';
import { IoAlertCircleOutline } from 'react-icons/io5';
import { TbRss } from 'react-icons/tb';

const NAV_ITEMS = [
  { to: '/dashboard',      label: 'Dashboard',      Icon: MdDashboard },
  { to: '/resumen',        label: 'Resumen',         Icon: MdOutlineSummarize },
  { to: '/alertas',        label: 'Alertas',         Icon: IoAlertCircleOutline },
  { to: '/fuentes-rss',    label: 'Fuentes y RSS',   Icon: TbRss },
  { to: '/notificaciones', label: 'Notificaciones',  Icon: MdNotifications },
  { to: '/perfil',         label: 'Perfil',          Icon: MdPerson },
];

export default function Sidebar() {
  const navigate = useNavigate();

  return (
    <aside className="flex flex-col h-screen w-56 min-w-56 bg-[#161616] border-r border-[#2a2a2a]">
      {/* Logo */}
      <div className="flex items-center gap-2 px-5 py-5 border-b border-[#2a2a2a]">
        <span className="text-[#e63946] text-lg">◈</span>
        <span className="font-mono text-xs font-semibold tracking-widest text-white">NEWSRADAR</span>
      </div>

      {/* Nav */}
      <nav className="flex-1 flex flex-col gap-0.5 p-3">
        {NAV_ITEMS.map(({ to, label, Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-2.5 px-3 py-2 rounded text-sm font-medium transition-all duration-150
              ${isActive
                ? 'bg-[rgba(230,57,70,0.15)] text-white border-l-2 border-[#e63946]'
                : 'text-[#888] hover:bg-[#1f1f1f] hover:text-white'
              }`
            }
          >
            <Icon size={16} />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Logout */}
      <div className="p-3 border-t border-[#2a2a2a]">
        <button
          onClick={() => navigate('/login')}
          className="flex items-center gap-2.5 w-full px-3 py-2 rounded text-sm text-[#888] hover:bg-[#1f1f1f] hover:text-[#e63946] transition-all duration-150"
        >
          <MdLogout size={16} />
          <span>Cerrar sesión</span>
        </button>
      </div>
    </aside>
  );
}