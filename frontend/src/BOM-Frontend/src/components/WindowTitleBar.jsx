function WindowTitleBar() {
  return (
    <div className="flex items-center justify-between h-8 bg-white border-b border-borderGray px-2 select-none">
      <div className="flex items-center gap-2">
        <span className="text-[13px] leading-none">🗔</span>
        <span className="text-[12.5px] text-textDark font-normal">
          BOMVision - Engineering BOM Intelligence Platform
        </span>
      </div>
      <div className="flex items-center">
        <div className="win-btn" title="Minimize">
          &#8211;
        </div>
        <div className="win-btn" title="Maximize">
          &#9633;
        </div>
        <div className="win-btn close-btn" title="Close">
          &#10005;
        </div>
      </div>
    </div>
  )
}

export default WindowTitleBar
