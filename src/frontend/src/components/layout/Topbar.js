import { MdSearch } from 'react-icons/md';

export default function Topbar({ user }) {
  const initials = user ? `${user.nombre?.[0] ?? ''}${user.apellidos?.[0] ?? ''}` : 'JP';

  return (
    <header className="h-14 min-h-14 flex items-center justify-between px-6 bg-[#161616] border-b border-[#2a2a2a]">
      {/* Search */}
      <div className="flex items-center gap-2 bg-[#1f1f1f] border border-[#2a2a2a] rounded px-3 py-1.5 w-80">
        <MdSearch size={16} className="text-[#888]" />
        <input
          type="text"
          placeholder="Buscar noticias..."
          className="bg-transparent outline-none text-sm text-white placeholder-[#888] w-full"
        />
      </div>

      {/* Right side */}
      <div className="flex items-center gap-3">
        <button className="font-mono text-xs font-semibold text-[#888] border border-[#2a2a2a] rounded px-2 py-1 hover:text-white transition-colors">
          ES
        </button>
        <div className="w-8 h-8 rounded-full bg-[#e63946] text-white text-xs font-semibold flex items-center justify-center font-mono cursor-pointer">
          {initials}
        </div>
      </div>
    </header>
  );
}