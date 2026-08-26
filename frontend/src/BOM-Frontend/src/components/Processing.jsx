function Processing({ files, isProcessing, progress, completed, onProcess }) {
  const disabled = files.length === 0 || isProcessing

  let statusText = 'Waiting...'
  if (isProcessing) statusText = 'Processing...'
  if (completed) statusText = 'Extraction Completed Successfully.'

  return (
    <div className="group-box">
      <span className="group-box-title">Processing</span>

      <button
        onClick={onProcess}
        disabled={disabled}
        className={
          'w-full h-[42px] rounded-[3px] text-[13.5px] font-bold tracking-wider ' +
          (disabled
            ? 'bg-[#9AA3AD] text-[#EDEFF1] cursor-not-allowed'
            : 'bg-primaryBlue hover:bg-primaryBlueDark text-white')
        }
      >
        PROCESS DRAWINGS
      </button>

      <div className="mt-3 h-[18px] w-full bg-[#E3E6EA] border border-borderGray rounded-[2px] relative overflow-hidden">
        <div
          className="h-full bg-progressOrange transition-all duration-200"
          style={{ width: `${progress}%` }}
        />
        <div className="absolute inset-0 flex items-center justify-center text-[11px] font-semibold text-[#2a2a2a]">
          {progress}%
        </div>
      </div>

      <div className="mt-1.5 text-[12.5px] text-textSecondary">{statusText}</div>
    </div>
  )
}

export default Processing
