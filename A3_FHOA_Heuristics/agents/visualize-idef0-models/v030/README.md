# IDEF0 Diagrammer (split files)

This is a minimal, clean split of the HTML/CSS/JS so we can iterate fast:

- `index.html` – markup and toolbar
- `styles.css` – visuals for nodes, handles, connectors, layout
- `app.js` – dragging, handle-to-handle connections, save/load to `localStorage`

## Quick Start
Open `index.html` in a browser. Add boxes, connect via handles, drag to rearrange.
Use **Save** / **Load** to persist the layout in your browser's `localStorage`.

## Roadmap Ideas
- Snap-to-grid, box alignment guides
- Delete/move connectors, edge selection
- ICOM codes on boundary arrows; label editing on connectors
- Export to PNG/SVG/JSON
- Minimap and zoom/pan
- Enforce 3–6 boxes per non-context diagram, A-0 special casing
- Bundling/unbundling (fork/join) visuals
