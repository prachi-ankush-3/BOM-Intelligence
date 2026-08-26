# CAD2BOM Pro — Frontend

A pixel-accurate React + Vite + Tailwind recreation of the CAD2BOM Pro desktop application UI.

## Run it

```bash
npm install
npm run dev
```

Then open the URL Vite prints (usually http://localhost:5173).

## Build

```bash
npm run build
npm run preview
```

## Structure

```
src/
  App.jsx                     # top-level layout + state (project info, files, processing sim)
  index.css                   # Tailwind + custom desktop-GUI styles (group boxes, scrollbars, title bar)
  components/
    WindowTitleBar.jsx        # top window chrome (title, minimize/maximize/close)
    Sidebar.jsx                # left navigation (Dashboard/Drawings/Reports/Weight/Settings/About)
    Header.jsx                 # centered "CAD2BOM PRO" header + institute info
    ProjectInformation.jsx     # Project Name / Company / Engineer / Output Folder group box
    EngineeringDrawings.jsx    # Add DXF Files / Add Folder / Clear + file list
    Processing.jsx             # Process button, progress bar, status message
    StatusBar.jsx               # bottom "Ready" status strip
```

## Notes on functionality

- **Add DXF Files** opens a native file picker filtered to `.dxf`.
- **Add Folder** uses the `webkitdirectory` attribute for browser-supported folder selection.
- **Clear** empties the file list.
- **Browse** cannot set an arbitrary absolute local path from the browser (this is a browser security restriction, not a bug) — it shows a note explaining that, matching what's realistically possible client-side.
- **Process Drawings** is disabled until at least one file is added, then simulates progress from 0% → 100% with an orange progress bar and a completion message, matching the app's described behavior.
