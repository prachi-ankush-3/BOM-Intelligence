import { useEffect, useRef } from 'react'

function Row({ label, children }) {
  return (
    <div className="flex items-center mb-2 last:mb-0">
      <label className="w-[100px] shrink-0 text-[13px] text-textDark">{label}</label>
      {children}
    </div>
  )
}

function ProjectInformation({ projectInfo, onChange, onBrowse }) {
  const nameInputRef = useRef(null)

  // Match screenshot: Project Name field starts selected/highlighted
  useEffect(() => {
    if (nameInputRef.current) {
      nameInputRef.current.focus()
      nameInputRef.current.select()
    }
  }, [])

  const inputBase =
    'flex-1 h-[27px] px-2 text-[13px] bg-inputBg border rounded-[2px] text-textDark focus:outline-none'

  return (
    <div className="group-box">
      <span className="group-box-title">Project Information</span>

      <Row label="Project Name">
        <input
          ref={nameInputRef}
          type="text"
          value={projectInfo.name}
          onChange={(e) => onChange('name', e.target.value)}
          className={inputBase + ' border-primaryBlue ring-1 ring-primaryBlue'}
        />
      </Row>

      <Row label="Company">
        <input
          type="text"
          value={projectInfo.company}
          onChange={(e) => onChange('company', e.target.value)}
          placeholder=""
          className={inputBase + ' border-borderGray'}
        />
      </Row>

      <Row label="Engineer">
        <input
          type="text"
          value={projectInfo.engineer}
          onChange={(e) => onChange('engineer', e.target.value)}
          className={inputBase + ' border-borderGray text-textSecondary'}
        />
      </Row>

      <Row label="Output Folder">
        <input
          type="text"
          value={projectInfo.outputFolder}
          onChange={(e) => onChange('outputFolder', e.target.value)}
          className={inputBase + ' border-borderGray'}
        />
        <button
          onClick={onBrowse}
          className="ml-2 h-[27px] px-4 bg-primaryBlue hover:bg-primaryBlueDark text-white text-[12.5px] font-semibold rounded-[2px] shrink-0"
        >
          Browse
        </button>
      </Row>
    </div>
  )
}

export default ProjectInformation
