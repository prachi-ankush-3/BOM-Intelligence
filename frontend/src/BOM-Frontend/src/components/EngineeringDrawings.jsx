import { useRef } from 'react'

function EngineeringDrawings({ files, onAddFiles, onClear }) {
  const fileInputRef = useRef(null)
  const folderInputRef = useRef(null)

  const handleFilesSelected = (e) => {
    const selected = Array.from(e.target.files || [])
    const dxfFiles = selected.filter((f) => f.name.toLowerCase().endsWith('.dxf'))
    onAddFiles(dxfFiles.length ? dxfFiles : selected)
    e.target.value = ''
  }

  const buttonClass =
    'flex-1 h-[38px] bg-primaryBlue hover:bg-primaryBlueDark text-white text-[13px] font-bold rounded-[3px] tracking-wide'

  return (
    <div className="group-box">
      <span className="group-box-title">Engineering Drawings</span>

      <div className="flex gap-3">
        <button className={buttonClass} onClick={() => fileInputRef.current?.click()}>
          Add DXF Files
        </button>
        <button className={buttonClass} onClick={() => folderInputRef.current?.click()}>
          Add Folder
        </button>
        <button className={buttonClass} onClick={onClear}>
          Clear
        </button>
      </div>

      {/* Hidden native file inputs */}
      <input
        ref={fileInputRef}
        type="file"
        accept=".dxf"
        multiple
        className="hidden"
        onChange={handleFilesSelected}
      />
      <input
        ref={folderInputRef}
        type="file"
        webkitdirectory=""
        directory=""
        multiple
        className="hidden"
        onChange={handleFilesSelected}
      />

      <div className="mt-3 h-[90px] bg-[#DCE6F0] border border-borderGray rounded-[2px] overflow-y-auto thin-scrollbar px-2 py-1.5">
        {files.length === 0 ? (
          <div className="text-[12px] text-textSecondary italic px-1 pt-1">
            No files added.
          </div>
        ) : (
          <ul>
            {files.map((f, idx) => (
              <li
                key={idx}
                className="text-[12.5px] text-textDark py-0.5 px-1 truncate"
              >
                {f.name}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

export default EngineeringDrawings
