
# IDEF0 Diagrammer (v0.4.1)

Self‑contained HTML/CSS/JS app. No build, no server.

## Use
1. Open `index.html` in a browser.
2. Drag boxes; connect with handles.
3. Toolbar:
   - Router: Curvy vs Orthogonal
   - Corner Radius: soften orthogonal turns
   - Stub Length: default length for new stubs
   - Add Stub: Select a handle (I/C/M/O), then click Add Stub or press **S**
4. Save/Load uses browser localStorage.
5. Export JSON/SVG: downloads files locally.

## Notes
- Stubs stay orthogonal and maintain offset relative to the anchor handle when you move boxes.
- Output stubs: arrowhead at free end; I/C/M stubs: arrowhead at box.
- Connectors style by kind: Control dashed, Mechanism dot-dash.
