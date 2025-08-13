# Implement v0.4.0: global toggle between Curvy (cubic) and Orthogonal (Manhattan) connectors with soft rounded corners.
# Adds Corner Radius control; orthogonal router computes H/V waypoints and renders with rounded 'Q' joints.
import os, zipfile, textwrap, json, re

base = "/mnt/data/idef0_split"

index_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>IDEF0 Diagrammer · v0.4.0</title>
  <link rel="stylesheet" href="styles.css"/>
</head>
<body>
  <div class="page">
    <header>
      <div class="toolbar">
        <button id="addBox">Add Function</button>
        <button id="addOffpage">Add Off‑Page Connector</button>
        <button id="addStub">Add Stub Arrow</button>
        <label class="group">
          <span>Router</span>
          <select id="routerMode">
            <option value="curvy">Curvy</option>
            <option value="ortho" selected>Orthogonal</option>
          </select>
        </label>
        <label class="group">
          <span>Corner Radius</span>
          <input id="cornerRadius" type="number" min="0" max="60" step="2" value="30">
        </label>
        <label class="group">
          <span>Stub Length</span>
          <input id="stubLen" type="number" min="20" max="400" step="10" value="120">
        </label>
        <button id="clearEdges">Clear Connectors</button>
        <button id="save">Save</button>
        <button id="load">Load</button>
        <button id="exportJson">Export JSON</button>
        <button id="exportSvg">Export SVG</button>
        <span class="hint">Switch between Curvy and Orthogonal connectors. Orthogonal uses soft rounded corners (default ~3 grids).</span>
      </div>
    </header>

    <main class="canvas grid-bg" id="canvas" aria-label="IDEF0 canvas">
      <svg class="connections" id="connSvg" aria-hidden="true">
        <defs>
          <marker id="arrow-output" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#111827"></path>
          </marker>
          <marker id="arrow-control" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#111827"></path>
          </marker>
          <marker id="arrow-mechanism" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#111827"></path>
          </marker>
          <marker id="arrow-generic" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#111827"></path>
          </marker>
        </defs>
      </svg>

      <!-- Starter nodes -->
      <div class="function" id="fn-1" style="left: 120px; top: 120px;">
        <div class="handle handle-top"    data-role="control"   data-handle="top"><span class="icom">C</span></div>
        <div class="handle handle-left"   data-role="input"     data-handle="left"><span class="icom">I</span></div>
        <div class="handle handle-right"  data-role="output"    data-handle="right"><span class="icom">O</span></div>
        <div class="handle handle-bottom" data-role="mechanism" data-handle="bottom"><span class="icom">M</span></div>
        <div class="function-name" contenteditable="true">PLAN NEW INFORMATION PROGRAM</div>
        <div class="function-number">1</div>
      </div>

      <div class="function" id="fn-2" style="left: 480px; top: 260px;">
        <div class="handle handle-top"    data-role="control"   data-handle="top"><span class="icom">C</span></div>
        <div class="handle handle-left"   data-role="input"     data-handle="left"><span class="icom">I</span></div>
        <div class="handle handle-right"  data-role="output"    data-handle="right"><span class="icom">O</span></div>
        <div class="handle handle-bottom" data-role="mechanism" data-handle="bottom"><span class="icom">M</span></div>
        <div class="function-name" contenteditable="true">DELIVER PRODUCTS</div>
        <div class="function-number">2</div>
      </div>
    </main>

    <footer>
      Node: FHOA/A0 · Title: Evolve System · Status: WORKING
    </footer>
  </div>

  <script src="app.js"></script>
</body>
</html>
"""

# Update styles to style toolbar group
styles_path = os.path.join(base, "styles.css")
styles = open(styles_path, "r", encoding="utf-8").read()
if ".toolbar .group" not in styles:
    styles += """

/* Toolbar groups */
.toolbar .group {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 1px solid #cbd5e1;
  padding: 4px 6px;
  border-radius: 6px;
  background: #fff;
}
.toolbar .group input[type="number"], .toolbar .group select {
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  padding: 2px 6px;
  height: 26px;
}
"""
    with open(styles_path, "w", encoding="utf-8") as f:
        f.write(styles)

app_js = r"""// === IDEF0 Diagrammer Script (v0.4.0) ===
(function(){
  const canvas = document.getElementById('canvas');
  const connSvg = document.getElementById('connSvg');
  const connectors = []; // includes normal and stub connectors
  const GRID = 10;

  const routerSelect = document.getElementById('routerMode');
  const cornerInput = document.getElementById('cornerRadius');

  const qp = (sel, root=document)=>root.querySelector(sel);
  const qpa = (sel, root=document)=>Array.from(root.querySelectorAll(sel));

  function grid(n){ return Math.round(n/GRID)*GRID; }

  function getHandlePoint(handleEl) {
    const r = handleEl.getBoundingClientRect();
    return { x: r.left + r.width/2 + window.scrollX, y: r.top + r.height/2 + window.scrollY };
  }
  function getCanvasPointFromPage(p) {
    const cr = canvas.getBoundingClientRect();
    return { x: p.x - cr.left - window.scrollX, y: p.y - cr.top - window.scrollY };
  }

  // --- Curvy cubic helper (existing) ---
  function cubicPath(p0, p1, side0, side1) {
    const dx = Math.max(40, Math.abs(p0.x - p1.x) / 2);
    const dy = Math.max(40, Math.abs(p0.y - p1.y) / 2);
    let c1 = {x: p0.x, y: p0.y};
    let c2 = {x: p1.x, y: p1.y};
    if (side0 === 'right') c1.x += dx;
    if (side0 === 'left')  c1.x -= dx;
    if (side0 === 'top')   c1.y -= dy;
    if (side0 === 'bottom')c1.y += dy;
    if (side1 === 'right') c2.x += dx;
    if (side1 === 'left')  c2.x -= dx;
    if (side1 === 'top')   c2.y -= dy;
    if (side1 === 'bottom')c2.y += dy;
    return {d: `M ${p0.x},${p0.y} C ${c1.x},${c1.y} ${c2.x},${c2.y} ${p1.x},${p1.y}`, labelAt: {x:(p0.x+c1.x+c2.x+p1.x)/4, y:(p0.y+c1.y+c2.y+p1.y)/4}};
  }

  // --- Orthogonal router with soft corners ---
  function orthoPoints(p0, p1, side0, side1){
    // Extend out of each handle by a small elbow (2*GRID) to leave the node boundary
    const ELBOW = 2*GRID;
    const a = {x:p0.x, y:p0.y}, b = {x:p1.x, y:p1.y};
    let pA = {x:a.x, y:a.y};
    if (side0 === 'right') pA.x += ELBOW;
    if (side0 === 'left')  pA.x -= ELBOW;
    if (side0 === 'top')   pA.y -= ELBOW;
    if (side0 === 'bottom')pA.y += ELBOW;

    let pB = {x:b.x, y:b.y};
    if (side1 === 'right') pB.x += ELBOW;
    if (side1 === 'left')  pB.x -= ELBOW;
    if (side1 === 'top')   pB.y -= ELBOW;
    if (side1 === 'bottom')pB.y += ELBOW;

    pA.x = grid(pA.x); pA.y = grid(pA.y);
    pB.x = grid(pB.x); pB.y = grid(pB.y);

    const pts = [{x:a.x,y:a.y}, pA];

    // Simple dog-leg logic
    if (pA.x === pB.x || pA.y === pB.y) {
      // Already aligned
      pts.push(pB);
    } else {
      // Choose an L route via mid-corner; prefer horizontal-then-vertical if leaving right/left
      const via1 = {x:pB.x, y:pA.y};
      const via2 = {x:pA.x, y:pB.y};

      // Heuristic: pick the via that doesn't backtrack into the node based on sides
      let choose = via1;
      if ((side0 === 'top' || side0 === 'bottom') && (side1 === 'top' || side1 === 'bottom')) choose = via2;
      pts.push(choose);
      pts.push(pB);
    }
    pts.push({x:b.x,y:b.y});
    return pts;
  }

  function roundedPathFromPoints(pts, r){
    if (pts.length < 2) return {d:'', labelAt: pts[0] || {x:0,y:0}};
    const rr = Math.max(0, Math.min(r, 60)); // clamp
    if (rr === 0) {
      const d0 = pts.map((p,i)=> (i===0?`M ${p.x},${p.y}`:`L ${p.x},${p.y}`)).join(' ');
      const mid = pts[Math.floor(pts.length/2)];
      return {d:d0, labelAt: mid};
    }
    let d = `M ${pts[0].x},${pts[0].y}`;
    for (let i=1;i<pts.length-1;i++){
      const p0 = pts[i-1], p1 = pts[i], p2 = pts[i+1];
      const v1 = {x: p1.x - p0.x, y: p1.y - p0.y};
      const v2 = {x: p2.x - p1.x, y: p2.y - p1.y};
      const len1 = Math.max(1, Math.abs(v1.x) + Math.abs(v1.y));
      const len2 = Math.max(1, Math.abs(v2.x) + Math.abs(v2.y));
      const r1 = Math.min(rr, Math.floor(len1/2));
      const r2 = Math.min(rr, Math.floor(len2/2));
      const cut = Math.min(r1, r2);
      // points before and after corner
      const pA = {x: p1.x - Math.sign(v1.x)*cut, y: p1.y - Math.sign(v1.y)*cut};
      const pB = {x: p1.x + Math.sign(v2.x)*cut, y: p1.y + Math.sign(v2.y)*cut};
      d += ` L ${pA.x},${pA.y} Q ${p1.x},${p1.y} ${pB.x},${pB.y}`;
    }
    const last = pts[pts.length-1];
    d += ` L ${last.x},${last.y}`;
    // crude label point: midpoint of the middle segment (good enough)
    const midIdx = Math.floor((pts.length-1)/2);
    const a = pts[midIdx], b = pts[midIdx+1] || pts[midIdx];
    const mid = {x:(a.x+b.x)/2, y:(a.y+b.y)/2};
    return {d, labelAt: mid};
  }

  function updateConnectorPath(conn) {
    if (conn.type === 'stub') {
      // identical to v0.3.3 behavior
      const head = getCanvasPointFromPage(getHandlePoint(conn.anchor.handleEl));
      let tailX = head.x, tailY = head.y;
      if (conn.axis === 'x') {
        if (conn.draggingTail) { conn.offset = grid(conn.free.x) - head.x; }
        tailX = head.x + conn.offset;
        tailY = head.y;
      } else {
        if (conn.draggingTail) { conn.offset = grid(conn.free.y) - head.y; }
        tailX = head.x;
        tailY = head.y + conn.offset;
      }
      conn.free.x = tailX; conn.free.y = tailY;
      const d = (conn.role === 'output')
        ? `M ${head.x},${head.y} L ${tailX},${tailY}`
        : `M ${tailX},${tailY} L ${head.x},${head.y}`;
      conn.pathEl.setAttribute('d', d);
      if (conn.labelEl) { conn.labelEl.style.left = (tailX - conn.labelEl.offsetWidth/2) + 'px'; conn.labelEl.style.top  = (tailY - conn.labelEl.offsetHeight/2) + 'px'; }
      if (conn.knobEl)  { conn.knobEl .style.left = (tailX - 6) + 'px';                    conn.knobEl .style.top  = (tailY - 6) + 'px'; }
      return;
    }

    // Normal connector: route based on router mode
    const a = getCanvasPointFromPage(getHandlePoint(conn.a.handleEl));
    const b = getCanvasPointFromPage(getHandlePoint(conn.b.handleEl));

    if ((routerSelect?.value || 'ortho') === 'ortho') {
      const pts = orthoPoints(a, b, conn.a.handleSide, conn.b.handleSide);
      const {d, labelAt} = roundedPathFromPoints(pts, parseFloat(cornerInput?.value || 30));
      conn.pathEl.setAttribute('d', d);
      if (conn.labelEl) { conn.labelEl.style.left = (labelAt.x - conn.labelEl.offsetWidth/2) + 'px'; conn.labelEl.style.top  = (labelAt.y - conn.labelEl.offsetHeight/2) + 'px'; }
    } else {
      const {d, labelAt} = cubicPath(a, b, conn.a.handleSide, conn.b.handleSide);
      conn.pathEl.setAttribute('d', d);
      if (conn.labelEl) { conn.labelEl.style.left = (labelAt.x - conn.labelEl.offsetWidth/2) + 'px'; conn.labelEl.style.top  = (labelAt.y - conn.labelEl.offsetHeight/2) + 'px'; }
    }
  }
  function refreshAllConnectors(){ connectors.forEach(updateConnectorPath); }

  function createLabelEl(text){
    const el = document.createElement('div');
    el.className = 'edge-label';
    el.contentEditable = true;
    el.textContent = text || '';
    canvas.appendChild(el);
    el.addEventListener('input', () => {
      const conn = connectors.find(c => c.labelEl === el);
      if (conn) conn.label = el.textContent.trim();
    });
    return el;
  }
  function createKnobEl(){
    const el = document.createElement('div');
    el.className = 'stub-knob';
    canvas.appendChild(el);
    return el;
  }
  function makePath(kind){
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.classList.add('connector');
    path.setAttribute('data-kind', kind);
    path.setAttribute('marker-end', `url(#arrow-${kind || 'generic'})`);
    connSvg.appendChild(path);
    path.addEventListener('click', (e) => {
      qpa('.connector.selected', connSvg).forEach(p => p.classList.remove('selected'));
      path.classList.add('selected');
      e.stopPropagation();
    });
    return path;
  }

  function createConnector(aHandle, bHandle) {
    const aRole = aHandle.dataset.role;
    const bRole = bHandle.dataset.role;
    const valid =
      (aRole === 'output'   && (bRole === 'input' || bRole === 'control' || bRole === 'mechanism')) ||
      (aRole === 'control'  && bRole === 'input') ||
      (aRole === 'input'    && bRole === 'output') ||
      (aRole === 'mechanism'&& bRole === 'input');
    let source = aHandle, target = bHandle;
    if (!(aRole === 'output' || aRole === 'control' || aRole === 'mechanism')) {
      [source, target] = [bHandle, aHandle];
    }
    const kind = source.dataset.role;
    if (!valid) { console.warn('Incompatible handle roles'); return; }
    const id = makeConnectorId();
    const path = makePath(kind);
    path.setAttribute('id', id);
    const labelEl = createLabelEl('');

    const conn = {
      id,
      type: 'normal',
      a: { nodeId: source.closest('.function, .offpage').id, handleSide: source.dataset.handle, role: source.dataset.role, handleEl: source },
      b: { nodeId: target.closest('.function, .offpage').id, handleSide: target.dataset.handle, role: target.dataset.role, handleEl: target },
      pathEl: path,
      labelEl,
      label: ''
    };
    connectors.push(conn);
    updateConnectorPath(conn);
  }

  // Stub helpers (from v0.3.3)
  function getStubLength(){
    const len = parseFloat(qp('#stubLen')?.value || '120');
    return isFinite(len) ? Math.max(20, Math.min(400, len)) : 120;
  }
  function createStubFromHandle(handleEl){
    const role = handleEl.dataset.role;
    const side = handleEl.dataset.handle;
    if (!['input','control','mechanism','output'].includes(role)) {
      alert('Select a handle (I/C/M or O) to create a stub arrow.');
      return;
    }
    const head = getCanvasPointFromPage(getHandlePoint(handleEl));
    const L = getStubLength();
    const axis = (role === 'input' || role === 'output' || side === 'left' || side === 'right') ? 'x' : 'y';
    const offset = (role === 'output' || side === 'right') ? +L :
                   (role === 'input'  || side === 'left')  ? -L :
                   (role === 'mechanism'|| side === 'bottom') ? +L : -L;
    const id = makeConnectorId();
    const path = makePath(role);
    path.setAttribute('id', id);
    const labelEl = createLabelEl('');
    const knobEl = createKnobEl();

    const conn = {
      id,
      type: 'stub',
      role,
      axis, offset,
      anchor: { nodeId: handleEl.closest('.function, .offpage').id, handleSide: side, role, handleEl },
      free: { x: head.x + (axis==='x'?offset:0), y: head.y + (axis==='y'?offset:0) },
      pathEl: path,
      labelEl,
      knobEl,
      label: '',
      draggingTail: false
    };
    connectors.push(conn);
    updateConnectorPath(conn);

    function startTailDrag(e){ conn.draggingTail = true; conn.dragStart = { x: e.clientX, y: e.clientY, freeX: conn.free.x, freeY: conn.free.y }; e.preventDefault(); }
    function moveTailDrag(e){
      if (!conn.draggingTail) return;
      const dx = e.clientX - conn.dragStart.x;
      const dy = e.clientY - conn.dragStart.y;
      if (conn.axis === 'x') conn.free.x = grid(conn.dragStart.freeX + dx);
      if (conn.axis === 'y') conn.free.y = grid(conn.dragStart.freeY + dy);
      updateConnectorPath(conn);
    }
    function endTailDrag(){ conn.draggingTail = false; }

    conn.knobEl.addEventListener('mousedown', startTailDrag);
    conn.labelEl.addEventListener('mousedown', startTailDrag);
    window.addEventListener('mousemove', moveTailDrag);
    window.addEventListener('mouseup', endTailDrag);
  }

  // Node dragging with snap
  let dragNode = null;
  canvas.addEventListener('mousedown', (e) => {
    const node = e.target.closest('.function, .offpage');
    if (!node) return;
    if (e.target.classList.contains('handle') || e.target.isContentEditable) return;
    dragNode = { el: node, startX: e.clientX, startY: e.clientY, origLeft: parseFloat(node.style.left || 0), origTop: parseFloat(node.style.top || 0) };
    e.preventDefault();
  });
  window.addEventListener('mousemove', (e) => {
    if (!dragNode) return;
    const dx = e.clientX - dragNode.startX;
    const dy = e.clientY - dragNode.startY;
    dragNode.el.style.left = (dragNode.origLeft + dx) + 'px';
    dragNode.el.style.top  = (dragNode.origTop  + dy) + 'px';
    refreshAllConnectors();
  });
  window.addEventListener('mouseup', () => {
    if (!dragNode) return;
    dragNode.el.style.left = grid(parseFloat(dragNode.el.style.left || 0)) + 'px';
    dragNode.el.style.top  = grid(parseFloat(dragNode.el.style.top  || 0)) + 'px';
    dragNode = null;
    refreshAllConnectors();
  });

  // Handle connect/reattach/spawn
  let pendingHandle = null;
  canvas.addEventListener('click', (e) => {
    const h = e.target.closest('.handle');
    if (!h) return;

    // reattach if selected (normal only)
    const selected = qp('.connector.selected', connSvg);
    if (selected) {
      const conn = connectors.find(c => c.pathEl === selected);
      if (conn && conn.type === 'normal') {
        if (e.altKey) {
          conn.a = { nodeId: h.closest('.function, .offpage').id, handleSide: h.dataset.handle, role: h.dataset.role, handleEl: h };
          selected.setAttribute('data-kind', h.dataset.role);
          selected.setAttribute('marker-end', `url(#arrow-${h.dataset.role || 'generic'})`);
        } else {
          conn.b = { nodeId: h.closest('.function, .offpage').id, handleSide: h.dataset.handle, role: h.dataset.role, handleEl: h };
        }
        updateConnectorPath(conn);
        return;
      }
    }

    if (pendingHandle === h) { h.classList.remove('active'); pendingHandle = null; return; }
    if (!pendingHandle) { pendingHandle = h; h.classList.add('active'); }
    else {
      if (pendingHandle.closest('.function, .offpage') !== h.closest('.function, .offpage')) {
        createConnector(pendingHandle, h);
      }
      pendingHandle.classList.remove('active');
      pendingHandle = null;
    }
    e.stopPropagation();
  });

  // Spawn function from output on empty area
  canvas.addEventListener('click', (e) => {
    if (e.target !== canvas) return;
    if (!pendingHandle) return;
    const role = pendingHandle.dataset.role;
    if (role === 'output') {
      const id = 'fn-' + Math.random().toString(36).slice(2,7);
      const node = document.createElement('div');
      node.className = 'function';
      node.id = id;
      const cr = canvas.getBoundingClientRect();
      const x = e.clientX - cr.left - 110;
      const y = e.clientY - cr.top  - 60;
      node.style.left = grid(x) + 'px';
      node.style.top  = grid(y) + 'px';
      node.innerHTML = `
        <div class="handle handle-top"    data-role="control"   data-handle="top"><span class="icom">C</span></div>
        <div class="handle handle-left"   data-role="input"     data-handle="left"><span class="icom">I</span></div>
        <div class="handle handle-right"  data-role="output"    data-handle="right"><span class="icom">O</span></div>
        <div class="handle handle-bottom" data-role="mechanism" data-handle="bottom"><span class="icom">M</span></div>
        <div class="function-name" contenteditable="true">NEW FUNCTION</div>
        <div class="function-number">1</div>
      `;
      canvas.appendChild(node);
      const inputHandle = qp(`#${id} .handle-left`, canvas);
      createConnector(pendingHandle, inputHandle);
      pendingHandle.classList.remove('active');
      pendingHandle = null;
    } else {
      pendingHandle.classList.remove('active');
      pendingHandle = null;
    }
  });

  // Deselect on empty canvas
  canvas.addEventListener('click', (e) => { if (e.target === canvas) { qpa('.connector.selected', connSvg).forEach(p => p.classList.remove('selected')); } });

  // Keyboard delete + 'S' hotkey
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Delete' || e.key === 'Backspace') {
      const sel = qp('.connector.selected', connSvg);
      if (sel) {
        const idx = connectors.findIndex(c => c.pathEl === sel);
        if (idx >= 0) {
          const c = connectors[idx];
          c.pathEl.remove();
          if (c.labelEl) c.labelEl.remove();
          if (c.knobEl) c.knobEl.remove();
          connectors.splice(idx,1);
        }
      }
    }
    if (e.key.toLowerCase() === 's') {
      if (!pendingHandle) { alert('Click a handle, then press S to add a stub arrow.'); return; }
      createStubFromHandle(pendingHandle);
      pendingHandle.classList.remove('active');
      pendingHandle = null;
    }
  });

  // Toolbar
  document.getElementById('clearEdges').addEventListener('click', () => {
    connectors.splice(0).forEach(c => { c.pathEl.remove(); if (c.labelEl) c.labelEl.remove(); if (c.knobEl) c.knobEl.remove(); });
  });
  document.getElementById('addBox').addEventListener('click', () => {
    addFunctionAt(160 + Math.random()*320, 120 + Math.random()*240);
  });
  document.getElementById('addOffpage').addEventListener('click', () => {
    addOffpageAt(40 + Math.random()*60, 40 + Math.random()*60);
  });
  document.getElementById('addStub').addEventListener('click', () => {
    if (!pendingHandle) { alert('Click a handle first (I/C/M or O).'); return; }
    createStubFromHandle(pendingHandle);
    pendingHandle.classList.remove('active');
    pendingHandle = null;
  });
  routerSelect.addEventListener('change', refreshAllConnectors);
  cornerInput.addEventListener('change', refreshAllConnectors);

  function addFunctionAt(x,y){
    const id = 'fn-' + Math.random().toString(36).slice(2,7);
    const node = document.createElement('div');
    node.className = 'function';
    node.id = id;
    node.style.left = grid(x) + 'px';
    node.style.top  = grid(y) + 'px';
    node.innerHTML = `
      <div class="handle handle-top"    data-role="control"   data-handle="top"><span class="icom">C</span></div>
      <div class="handle handle-left"   data-role="input"     data-handle="left"><span class="icom">I</span></div>
      <div class="handle handle-right"  data-role="output"    data-handle="right"><span class="icom">O</span></div>
      <div class="handle handle-bottom" data-role="mechanism" data-handle="bottom"><span class="icom">M</span></div>
      <div class="function-name" contenteditable="true">NEW FUNCTION</div>
      <div class="function-number">1</div>
    `;
    canvas.appendChild(node);
  }
  function addOffpageAt(x,y){
    const id = 'op-' + Math.random().toString(36).slice(2,7);
    const node = document.createElement('div');
    node.className = 'offpage';
    node.id = id;
    node.style.left = grid(x) + 'px';
    node.style.top  = grid(y) + 'px';
    node.innerHTML = `
      <div class="handle handle-top"    data-role="control"   data-handle="top"><span class="icom">C</span></div>
      <div class="handle handle-left"   data-role="input"     data-handle="left"><span class="icom">I</span></div>
      <div class="handle handle-right"  data-role="output"    data-handle="right"><span class="icom">O</span></div>
      <div class="handle handle-bottom" data-role="mechanism" data-handle="bottom"><span class="icom">M</span></div>
      <div class="label">OFF‑PAGE</div>
    `;
    canvas.appendChild(node);
  }

  // Save/Load (persist router mode as a doc-level setting for convenience)
  function serialize(){
    const nodes = qpa('.function, .offpage', canvas).map(n => ({
      id: n.id,
      type: n.classList.contains('offpage') ? 'offpage' : 'function',
      left: parseFloat(n.style.left || 0),
      top: parseFloat(n.style.top  || 0),
      name: n.classList.contains('function') ? (qp('.function-name', n)?.textContent?.trim() || '') : 'OFF-PAGE',
      number: n.classList.contains('function') ? (qp('.function-number', n)?.textContent?.trim() || '') : ''
    }));
    const edges = connectors.map(c => {
      if (c.type === 'stub') {
        return {
          id: c.id,
          type: 'stub',
          role: c.role,
          axis: c.axis,
          offset: c.offset,
          anchor: { nodeId: c.anchor.nodeId, handleSide: c.anchor.handleSide, role: c.anchor.role },
          free: { x: c.free.x, y: c.free.y },
          kind: c.pathEl.getAttribute('data-kind'),
          label: c.label || ''
        };
      }
      return {
        id: c.id,
        type: 'normal',
        a: { nodeId: c.a.nodeId, handleSide: c.a.handleSide, role: c.a.role },
        b: { nodeId: c.b.nodeId, handleSide: c.b.handleSide, role: c.b.role },
        kind: c.pathEl.getAttribute('data-kind'),
        label: c.label || ''
      };
    });
    return {
      version: '0.4.0',
      settings: {
        routerMode: routerSelect?.value || 'ortho',
        cornerRadius: parseFloat(cornerInput?.value || 30)
      },
      nodes, edges
    };
  }
  function deserialize(data){
    routerSelect.value = data?.settings?.routerMode || 'ortho';
    cornerInput.value  = (data?.settings?.cornerRadius ?? 30);

    qpa('.function, .offpage', canvas).forEach(n => n.remove());
    qpa('.connector', connSvg).forEach(p => p.remove());
    qpa('.edge-label', canvas).forEach(l => l.remove());
    qpa('.stub-knob', canvas).forEach(k => k.remove());
    connectors.splice(0);

    (data.nodes || []).forEach(n => {
      if (n.type === 'offpage') addOffpageAt(n.left, n.top);
      else {
        addFunctionAt(n.left, n.top);
        const el = document.getElementById(n.id) || qp('.function:last-child', canvas);
        if (el) {
          el.id = n.id;
          const nameEl = qp('.function-name', el);
          const numEl  = qp('.function-number', el);
          if (nameEl) nameEl.textContent = n.name || 'FUNCTION';
          if (numEl)  numEl.textContent  = n.number || '';
        }
      }
    });

    (data.edges || []).forEach(e => {
      if (e.type === 'stub') {
        const hSel = `#${e.anchor.nodeId} .handle-${e.anchor.handleSide}`;
        const h = qp(hSel, canvas);
        if (h) {
          const path = makePath(e.kind || e.anchor.role);
          path.setAttribute('id', e.id || makeConnectorId());
          const labelEl = createLabelEl(e.label || '');
          const knobEl = createKnobEl();
          const head = getCanvasPointFromPage(getHandlePoint(h));
          const axis = e.axis || ((e.anchor.role === 'input' || e.anchor.role === 'output' || e.anchor.handleSide === 'left' || e.anchor.handleSide === 'right') ? 'x' : 'y');
          let offset = e.offset;
          if (offset === undefined || offset === null) {
            offset = axis === 'x' ? (e.free?.x || head.x) - head.x : (e.free?.y || head.y) - head.y;
            offset = grid(offset);
          }
          const conn = {
            id: e.id || makeConnectorId(),
            type: 'stub',
            role: e.role || e.anchor.role,
            axis,
            offset,
            anchor: { nodeId: e.anchor.nodeId, handleSide: e.anchor.handleSide, role: e.anchor.role, handleEl: h },
            free: { x: head.x + (axis==='x'?offset:0), y: head.y + (axis==='y'?offset:0) },
            pathEl: path,
            labelEl,
            knobEl,
            label: e.label || '',
            draggingTail: false
          };
          connectors.push(conn);
          updateConnectorPath(conn);
        }
      } else {
        const aSel = `#${e.a.nodeId} .handle-${e.a.handleSide}`;
        const bSel = `#${e.b.nodeId} .handle-${e.b.handleSide}`;
        const aHandle = qp(aSel, canvas);
        const bHandle = qp(bSel, canvas);
        if (aHandle && bHandle) {
          const path = makePath(e.kind || e.a.role);
          path.setAttribute('id', e.id || makeConnectorId());
          const labelEl = createLabelEl(e.label || '');
          const conn = {
            id: e.id || makeConnectorId(),
            type: 'normal',
            a: { nodeId: e.a.nodeId, handleSide: e.a.handleSide, role: e.a.role, handleEl: aHandle },
            b: { nodeId: e.b.nodeId, handleSide: e.b.handleSide, role: e.b.role, handleEl: bHandle },
            pathEl: path,
            labelEl,
            label: e.label || ''
          };
          connectors.push(conn);
          updateConnectorPath(conn);
        }
      }
    });
    refreshAllConnectors();
  }

  document.getElementById('save').addEventListener('click', () => {
    localStorage.setItem('idef0-diagram', JSON.stringify(serialize()));
    alert('Saved to localStorage.');
  });
  document.getElementById('load').addEventListener('click', () => {
    const raw = localStorage.getItem('idef0-diagram');
    if (!raw) { alert('No saved diagram found.'); return; }
    try { deserialize(JSON.parse(raw)); } catch (e) { alert('Load failed: ' + e.message); }
  });

  // Export JSON
  document.getElementById('exportJson').addEventListener('click', () => {
    const blob = new Blob([JSON.stringify(serialize(), null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'idef0-diagram.json';
    a.click();
    URL.revokeObjectURL(url);
  });

  // Export SVG uses live router setting
  document.getElementById('exportSvg').addEventListener('click', () => {
    const cr = canvas.getBoundingClientRect();
    const data = serialize();
    let svg = [];
    svg.push(`<svg xmlns="http://www.w3.org/2000/svg" width="${cr.width}" height="${cr.height}" viewBox="0 0 ${cr.width} ${cr.height}">`);
    svg.push(`<defs>
      <marker id="arrow-output" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="#111827"></path>
      </marker>
      <marker id="arrow-control" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="#111827"></path>
      </marker>
      <marker id="arrow-mechanism" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="#111827"></path>
      </marker>
      <marker id="arrow-generic" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="#111827"></path>
      </marker>
    </defs>`);
    svg.push(`<rect width="100%" height="100%" fill="#f8fbff" stroke="#cbd5e1" />`);

    function escapeXml(s){
      return (s || '').replace(/[&<>"']/g, ch => (
        ch === '&' ? '&amp;' : ch === '<' ? '&lt;' : ch === '>' ? '&gt;' : ch === '"' ? '&quot;' : '&#39;'
      ));
    }
    function liveHandlePoint(nodeId, side){
      const el = qp(`#${nodeId} .handle-${side}`, canvas);
      if (!el) return null;
      const p = getCanvasPointFromPage(getHandlePoint(el));
      return p;
    }

    // Nodes
    data.nodes.forEach(n => {
      if (n.type === 'offpage') {
        const x = n.left, y = n.top, r = 28;
        svg.push(`<g>`);
        svg.push(`<circle cx="${x+r}" cy="${y+r}" r="${r}" fill="#fff" stroke="#64748b" stroke-dasharray="4 4" stroke-width="2"/>`);
        svg.push(`<text x="${x+r}" y="${y+r}" font-family="Segoe UI, Arial" font-size="10" text-anchor="middle" dominant-baseline="central" fill="#334155">OFF-PAGE</text>`);
        svg.push(`</g>`);
      } else {
        const x = n.left, y = n.top, w = 220, h = 120;
        svg.push(`<g>`);
        svg.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#fff" stroke="#1f2937" stroke-width="2" rx="4" ry="4"/>`);
        svg.push(`<text x="${x + w/2}" y="${y + h/2}" font-family="Segoe UI, Arial" font-size="14" font-weight="700" text-anchor="middle" dominant-baseline="middle">${escapeXml(n.name || '')}</text>`);
        svg.push(`<text x="${x + w - 10}" y="${y + h - 8}" font-family="Segoe UI, Arial" font-size="12" text-anchor="end">${escapeXml(n.number || '')}</text>`);
        svg.push(`</g>`);
      }
    });

    const mode = (routerSelect?.value || 'ortho');
    const cornerR = parseFloat(cornerInput?.value || 30);

    (data.edges || []).forEach(e => {
      if (e.type === 'stub') {
        const head = liveHandlePoint(e.anchor.nodeId, e.anchor.handleSide);
        if (!head) return;
        const axis = e.axis || ((e.anchor.role === 'input' || e.anchor.role === 'output' || e.anchor.handleSide === 'left' || e.anchor.handleSide === 'right') ? 'x' : 'y');
        const tailX = axis === 'x' ? head.x + (e.offset || 0) : head.x;
        const tailY = axis === 'y' ? head.y + (e.offset || 0) : head.y;
        const dash = e.kind === 'control' ? ' stroke-dasharray="6 4"' :
                     e.kind === 'mechanism' ? ' stroke-dasharray="2 4"' : '';
        if ((e.role || e.anchor.role) === 'output') {
          svg.push(`<path d="M ${head.x},${head.y} L ${tailX},${tailY}" fill="none" stroke="#111827" stroke-width="2"${dash} marker-end="url(#arrow-output)"/>`);
        } else {
          svg.push(`<path d="M ${tailX},${tailY} L ${head.x},${head.y}" fill="none" stroke="#111827" stroke-width="2"${dash} marker-end="url(#arrow-${e.kind || 'generic'})"/>`);
        }
        if (e.label && e.label.trim()) {
          svg.push(`<text x="${tailX}" y="${tailY}" font-family="Segoe UI, Arial" font-size="12" text-anchor="middle" dominant-baseline="central" fill="#111827">${escapeXml(e.label)}</text>`);
        }
      } else {
        const a = liveHandlePoint(e.a.nodeId, e.a.handleSide);
        const b = liveHandlePoint(e.b.nodeId, e.b.handleSide);
        if (!a || !b) return;
        let pathD = '';
        let label = {x:(a.x+b.x)/2, y:(a.y+b.y)/2};
        if (mode === 'curvy') {
          // cubic
          const dx = Math.max(40, Math.abs(a.x - b.x) / 2);
          const dy = Math.max(40, Math.abs(a.y - b.y) / 2);
          let c1 = {x: a.x, y: a.y};
          let c2 = {x: b.x, y: b.y};
          if (e.a.handleSide === 'right') c1.x += dx;
          if (e.a.handleSide === 'left')  c1.x -= dx;
          if (e.a.handleSide === 'top')   c1.y -= dy;
          if (e.a.handleSide === 'bottom')c1.y += dy;
          if (e.b.handleSide === 'right') c2.x += dx;
          if (e.b.handleSide === 'left')  c2.x -= dx;
          if (e.b.handleSide === 'top')   c2.y -= dy;
          if (e.b.handleSide === 'bottom')c2.y += dy;
          pathD = `M ${a.x},${a.y} C ${c1.x},${c1.y} ${c2.x},${c2.y} ${b.x},${b.y}`;
          label = {x:(a.x+c1.x+c2.x+b.x)/4, y:(a.y+c1.y+c2.y+b.y)/4};
        } else {
          // orthogonal rounded
          function grid(n){ return Math.round(n/10)*10; }
          const ELBOW = 20;
          let pA = {x:a.x, y:a.y};
          if (e.a.handleSide === 'right') pA.x += ELBOW;
          if (e.a.handleSide === 'left')  pA.x -= ELBOW;
          if (e.a.handleSide === 'top')   pA.y -= ELBOW;
          if (e.a.handleSide === 'bottom')pA.y += ELBOW;
          let pB = {x:b.x, y:b.y};
          if (e.b.handleSide === 'right') pB.x += ELBOW;
          if (e.b.handleSide === 'left')  pB.x -= ELBOW;
          if (e.b.handleSide === 'top')   pB.y -= ELBOW;
          if (e.b.handleSide === 'bottom')pB.y += ELBOW;
          pA.x=grid(pA.x); pA.y=grid(pA.y); pB.x=grid(pB.x); pB.y=grid(pB.y);
          const pts = [{x:a.x,y:a.y}, pA];
          if (pA.x===pB.x || pA.y===pB.y) { pts.push(pB); }
          else {
            const via1 = {x:pB.x, y:pA.y};
            const via2 = {x:pA.x, y:pB.y};
            let choose = via1;
            if ((e.a.handleSide==='top'||e.a.handleSide==='bottom') && (e.b.handleSide==='top'||e.b.handleSide==='bottom')) choose = via2;
            pts.push(choose); pts.push(pB);
          }
          pts.push({x:b.x,y:b.y});
          // rounded with quadratic corners
          if (cornerR <= 0) {
            pathD = pts.map((p,i)=> (i===0?`M ${p.x},${p.y}`:`L ${p.x},${p.y}`)).join(' ');
          } else {
            let d = `M ${pts[0].x},${pts[0].y}`;
            for (let i=1;i<pts.length-1;i++){
              const p0 = pts[i-1], p1 = pts[i], p2 = pts[i+1];
              const v1 = {x: p1.x - p0.x, y: p1.y - p0.y};
              const v2 = {x: p2.x - p1.x, y: p2.y - p1.y};
              const len1 = Math.max(1, Math.abs(v1.x) + Math.abs(v1.y));
              const len2 = Math.max(1, Math.abs(v2.x) + Math.abs(v2.y));
              const r1 = Math.min(cornerR, Math.floor(len1/2));
              const r2 = Math.min(cornerR, Math.floor(len2/2));
              const cut = Math.min(r1, r2);
              const pA2 = {x: p1.x - Math.sign(v1.x)*cut, y: p1.y - Math.sign(v1.y)*cut};
              const pB2 = {x: p1.x + Math.sign(v2.x)*cut, y: p1.y + Math.sign(v2.y)*cut};
              d += ` L ${pA2.x},${pA2.y} Q ${p1.x},${p1.y} ${pB2.x},${pB2.y}`;
            }
            const last = pts[pts.length-1];
            d += ` L ${last.x},${last.y}`;
            pathD = d;
          }
          const midIdx = Math.floor((pts.length-1)/2);
          const mA = pts[midIdx], mB = pts[midIdx+1] || pts[midIdx];
          label = {x:(mA.x+mB.x)/2, y:(mA.y+mB.y)/2};
        }
        const dash = e.kind === 'control' ? ' stroke-dasharray="6 4"' :
                     e.kind === 'mechanism' ? ' stroke-dasharray="2 4"' : '';
        const marker = e.kind ? ` marker-end="url(#arrow-${e.kind})"` : ' marker-end="url(#arrow-generic)"';
        svg.push(`<path d="${pathD}" fill="none" stroke="#111827" stroke-width="2"${dash}${marker}/>`);
        if (e.label && e.label.trim()) {
          svg.push(`<text x="${label.x}" y="${label.y}" font-family="Segoe UI, Arial" font-size="12" text-anchor="middle" dominant-baseline="central" fill="#111827">${escapeXml(e.label)}</text>`);
        }
      }
    });

    svg.push(`</svg>`);
    const blob = new Blob([svg.join('')], {type: 'image/svg+xml'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'idef0-diagram.svg';
    a.click();
    URL.revokeObjectURL(url);
  });

  // Demo edge
  window.addEventListener('load', () => {
    const a = qp('#fn-1 .handle-right');
    const b = qp('#fn-2 .handle-left');
    if (a && b) requestAnimationFrame(() => createConnector(a, b));
  });

  // Keep SVG sized
  const connSvgEl = document.getElementById('connSvg');
  function sizeSvgToCanvas() {
    const cr = canvas.getBoundingClientRect();
    connSvgEl.setAttribute('width', cr.width);
    connSvgEl.setAttribute('height', cr.height);
  }
  new ResizeObserver(() => { sizeSvgToCanvas(); refreshAllConnectors(); }).observe(canvas);
  sizeSvgToCanvas();
})();"""

with open(os.path.join(base, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)
with open(os.path.join(base, "app.js"), "w", encoding="utf-8") as f:
    f.write(app_js)

# Zip new version
zip_path = "/mnt/data/idef0_split_project_v040.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for p in ["index.html", "styles.css", "app.js", "README.md"]:
        z.write(os.path.join(base, p), arcname=p)

{"dir": base, "zip": zip_path}
