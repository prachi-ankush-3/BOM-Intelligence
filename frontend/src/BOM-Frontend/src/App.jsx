import { useState, useRef } from 'react'
import WindowTitleBar from './components/WindowTitleBar'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import ProjectInformation from './components/ProjectInformation'
import EngineeringDrawings from './components/EngineeringDrawings'
import Processing from './components/Processing'
import StatusBar from './components/StatusBar'

function App() {
  const [activePage, setActivePage] = useState('dashboard')

  const [projectInfo, setProjectInfo] = useState({
    name: 'Project 1',
    company: 'XYZ',
    engineer: 'Dr. Prashant Anerao',
    outputFolder: 'C:/Users/Dr.Prashant/Desktop/CAD2BOM_Pro/Output',
  })

  const [files, setFiles] = useState([])
  const [isProcessing, setIsProcessing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [completed, setCompleted] = useState(false)
  const [statusText, setStatusText] = useState('Ready')
  const timerRef = useRef(null)

  const handleProjectInfoChange = (field, value) => {
    setProjectInfo((prev) => ({ ...prev, [field]: value }))
  }

  const handleAddFiles = (newFiles) => {
    setFiles((prev) => [...prev, ...newFiles])
    setCompleted(false)
    setProgress(0)
    setStatusText('Ready')
  }

  const handleClear = () => {
    setFiles([])
    setCompleted(false)
    setProgress(0)
    setStatusText('Ready')
  }

  const handleBrowse = () => {
    // Browsers cannot expose arbitrary local filesystem paths for security
    // reasons. This is the best available browser-compatible fallback.
    window.alert(
      'For security reasons, browsers cannot set an arbitrary local folder path directly.\n' +
        'Please type the desired output path into the field, or use "Add Folder" to select a folder via the system picker.'
    )
  }

  const handleProcess = () => {
    if (files.length === 0 || isProcessing) return
    setIsProcessing(true)
    setCompleted(false)
    setProgress(0)
    setStatusText('Processing drawings...')

    let current = 0
    timerRef.current = setInterval(() => {
      current += Math.floor(Math.random() * 12) + 6
      if (current >= 100) {
        current = 100
        clearInterval(timerRef.current)
        setProgress(100)
        setIsProcessing(false)
        setCompleted(true)
        setStatusText('Extraction Completed Successfully.')
        return
      }
      setProgress(current)
    }, 250)
  }

  return (
    <div className="w-full h-screen flex flex-col bg-mainBg overflow-hidden">
      <WindowTitleBar />

      <div className="flex flex-1 min-h-0">
        <Sidebar activePage={activePage} onSelectPage={setActivePage} />

        <div className="flex-1 min-w-0 overflow-y-auto thin-scrollbar">
          {activePage === 'dashboard' ? (
            <div className="max-w-[880px] mx-auto px-6 pb-6">
              <Header />
              <ProjectInformation
                projectInfo={projectInfo}
                onChange={handleProjectInfoChange}
                onBrowse={handleBrowse}
              />
              <EngineeringDrawings
                files={files}
                onAddFiles={handleAddFiles}
                onClear={handleClear}
              />
              <Processing
                files={files}
                isProcessing={isProcessing}
                progress={progress}
                completed={completed}
                onProcess={handleProcess}
              />
            </div>
          ) : (
            <div className="h-full w-full flex items-center justify-center">
              <p className="text-textSecondary text-[14px] capitalize">
                {activePage} — coming soon
              </p>
            </div>
          )}
        </div>
      </div>

      <StatusBar text={statusText} />
    </div>
  )
}

export default App
