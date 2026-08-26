const NAV_ITEMS = [
  { key: 'dashboard', label: 'Dashboard', icon: '🏠' },
  { key: 'drawings', label: 'Drawings', icon: '📁' },
  { key: 'reports', label: 'Reports', icon: '📊' },
  { key: 'weight', label: 'Weight', icon: '⚖️' },
  { key: 'settings', label: 'Settings', icon: '⚙️' },
  { key: 'about', label: 'About', icon: 'ℹ️' },
]

function Sidebar({ activePage, onSelectPage }) {
  return (
    <div className="w-[197px] shrink-0 bg-sidebarBg h-full flex flex-col items-center pt-6 gap-2">
      {NAV_ITEMS.map((item) => {
        const isActive = activePage === item.key
        return (
          <button
            key={item.key}
            onClick={() => onSelectPage(item.key)}
            className={
              'w-[164px] h-[42px] flex items-center gap-3 px-4 rounded-md text-[13.5px] transition-colors ' +
              (isActive
                ? 'bg-primaryBlue text-white font-semibold shadow-sm'
                : 'bg-transparent text-[#3a3f47] font-normal hover:bg-[#dde2ee]')
            }
          >
            <span className="text-[15px] leading-none">{item.icon}</span>
            <span>{item.label}</span>
          </button>
        )
      })}
    </div>
  )
}

export default Sidebar
