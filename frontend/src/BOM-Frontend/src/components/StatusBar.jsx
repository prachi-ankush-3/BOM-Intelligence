function StatusBar({ text = 'Ready' }) {
  return (
    <div className="h-[22px] w-full bg-[#F0F1F3] border-t border-borderGray flex items-center px-3 select-none">
      <span className="text-[11.5px] text-textSecondary">{text}</span>
    </div>
  )
}

export default StatusBar
