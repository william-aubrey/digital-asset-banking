// === IDEF0 Diagrammer Script (v0.3.3) ===
(function(){
  const canvas = document.getElementById('canvas');
  const connSvg = document.getElementById('connSvg');
  const connectors = []; // includes normal and stub connectors
  const GRID = 10;

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
  function cubicPointAt(p0, c1, c2, p1, t){
    const mt = 1 - t;
    const x = mt*mt*mt*p0.x + 3*mt*mt*t*c1.x + 3*mt*t*t*c2.x + t*t*t*p1.x;
    const y = mt*mt*mt*p0.y + 3*mt*mt*t*c1.y + 3*mt*t*t*c2.y + t*t*t*p1.y;
    return {x,y};
  }
  function makeConnectorId(){ return 'edge-' + Math.random().toString(36).slice(2,9); }

  function updateConnectorPath(conn) {
    if (conn.type === 'stub') {
      const head = getCanvasPointFromPage(getHandlePoint(conn.anchor.handleEl));
      // Compute tail from offset unless actively dragging
      let tailX = head.x, tailY = head.y;
      if (conn.axis === 'x') {
        if (conn.draggingTail) { conn.offset = grid(conn.free.x) - head.x; }
        tailX = head.x + conn.offset;
        tailY = head.y; // stay orthogonal
      } else { // axis 'y'
        if (conn.draggingTail) { conn.offset = grid(conn.free.y) - head.y; }
        tailX = head.x;
        tailY = head.y + conn.offset;
      }
      // persist computed free for UI elements
      conn.free.x = tailX; conn.free.y = tailY;

      // Direction: output = head->tail (arrow at free end); others tail->head (arrow at box)
      const d = (conn.role === 'output')
        ? `M ${head.x},${head.y} L ${tailX},${tailY}`
        : `M ${tailX},${tailY} L ${head.x},${head.y}`;
      conn.pathEl.setAttribute('d', d);

      if (conn.labelEl) {
        conn.labelEl.style.left = (tailX - conn.labelEl.offsetWidth/2) + 'px';
        conn.labelEl.style.top  = (tailY - conn.labelEl.offsetHeight/2) + 'px';
      }
      if (conn.knobEl) {
        conn.knobEl.style.left = (tailX - 6) + 'px';
        conn.knobEl.style.top  = (tailY - 6) + 'px';
      }
      return;
    }

    // Normal connector
    const p0 = getCanvasPointFromPage(getHandlePoint(conn.a.handleEl));
    const p1 = getCanvasPointFromPage(getHandlePoint(conn.b.handleEl));
    const dx = Math.max(40, Math.abs(p0.x - p1.x) / 2);
    const dy = Math.max(40, Math.abs(p0.y - p1.y) / 2);
    let c1 = {x: p0.x, y: p0.y};
    let c2 = {x: p1.x, y: p1.y};
    if (conn.a.handleSide === 'right') c1.x += dx;
    if (conn.a.handleSide === 'left')  c1.x -= dx;
    if (conn.a.handleSide === 'top')   c1.y -= dy;
    if (conn.a.handleSide === 'bottom')c1.y += dy;
    if (conn.b.handleSide === 'right') c2.x += dx;
    if (conn.b.handleSide === 'left')  c2.x -= dx;
    if (conn.b.handleSide === 'top')   c2.y -= dy;
    if (conn.b.handleSide === 'bottom')c2.y += dy;

    const d = `M ${p0.x},${p0.y} C ${c1.x},${c1.y} ${c2.x},${c2.y} ${p1.x},${p1.y}`;
    conn.pathEl.setAttribute('d', d);

    const mid = cubicPointAt(p0, c1, c2, p1, 0.5);
    if (conn.labelEl) {
      conn.labelEl.style.left = (mid.x - conn.labelEl.offsetWidth/2) + 'px';
      conn.labelEl.style.top  = (mid.y - conn.labelEl.offsetHeight/2) + 'px';
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

  function getStubLength(){
    const len = parseFloat(qp('#stubLen')?.value || '120');
    return isFinite(len) ? Math.max(20, Math.min(400, len)) : 120;
  }

  // === Stub arrows (Inputs/Control/Mechanism + Output outward) with sticky orthogonal offset ===
  function createStubFromHandle(handleEl){
    const role = handleEl.dataset.role;   // input | control | mechanism | output
    const side = handleEl.dataset.handle; // left | top | bottom | right
    if (!['input','control','mechanism','output'].includes(role)) {
      alert('Select a handle (I/C/M or O) to create a stub arrow.');
      return;
    }
    const head = getCanvasPointFromPage(getHandlePoint(handleEl));
    const L = getStubLength();
    // axis + default offset
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
      axis,            // 'x' or 'y'
      offset,          // signed amount from head along axis
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

    // Drag tail via knob or label (updates offset relative to live head)
    function startTailDrag(e){
      conn.draggingTail = true;
      conn.dragStart = { x: e.clientX, y: e.clientY, freeX: conn.free.x, freeY: conn.free.y };
      e.preventDefault();
    }
    function moveTailDrag(e){
      if (!conn.draggingTail) return;
      const dx = e.clientX - conn.dragStart.x;
      const dy = e.clientY - conn.dragStart.y;
      if (conn.axis === 'x') conn.free.x = grid(conn.dragStart.freeX + dx);
      if (conn.axis === 'y') conn.free.y = grid(conn.dragStart.freeY + dy);
      updateConnectorPath(conn); // recomputes offset live
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
    dragNode = {
      el: node, startX: e.clientX, startY: e.clientY,
      origLeft: parseFloat(node.style.left || 0),
      origTop: parseFloat(node.style.top || 0)
    };
    e.preventDefault();
  });
  window.addEventListener('mousemove', (e) => {
    if (!dragNode) return;
    const dx = e.clientX - dragNode.startX;
    const dy = e.clientY - dragNode.startY;
    dragNode.el.style.left = (dragNode.origLeft + dx) + 'px';
    dragNode.el.style.top  = (dragNode.origTop  + dy) + 'px';
    refreshAllConnectors(); // stubs will recompute tail from offset
  });
  window.addEventListener('mouseup', () => {
    if (!dragNode) return;
    const left = parseFloat(dragNode.el.style.left || 0);
    const top  = parseFloat(dragNode.el.style.top  || 0);
    dragNode.el.style.left = grid(left) + 'px';
    dragNode.el.style.top  = grid(top) + 'px';
    dragNode = null;
    refreshAllConnectors();
  });

  // Handle connect/reattach/spawn
  let pendingHandle = null;
  canvas.addEventListener('click', (e) => {
    const h = e.target.closest('.handle');
    if (!h) return;

    // reattach if a connector is selected (normal only)
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

    // pending select to connect or stub
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
  canvas.addEventListener('click', (e) => {
    if (e.target === canvas) {
      qpa('.connector.selected', connSvg).forEach(p => p.classList.remove('selected'));
    }
  });

  // Keyboard delete + 'S' hotkey to add stub from selected handle
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

  // Save/Load (persist stubs with axis + offset; backward compatible with prior versions)
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
          free: { x: c.free.x, y: c.free.y }, // for compatibility/debug
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
    return { version: '0.3.3', nodes, edges };
  }
  function deserialize(data){
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
          // backward compatibility: infer axis/offset if missing
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

  // Export SVG (compute tails from offset so diagrams export in "sticky" state)
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

    // Edges
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
        const d = `M ${a.x},${a.y} C ${c1.x},${c1.y} ${c2.x},${c2.y} ${b.x},${b.y}`;
        const dash = e.kind === 'control' ? ' stroke-dasharray="6 4"' :
                     e.kind === 'mechanism' ? ' stroke-dasharray="2 4"' : '';
        const marker = e.kind ? ` marker-end="url(#arrow-${e.kind})"` : ' marker-end="url(#arrow-generic)"';
        svg.push(`<path d="${d}" fill="none" stroke="#111827" stroke-width="2"${dash}${marker}/>`);
        if (e.label && e.label.trim()) {
          const midx = (a.x + c1.x + c2.x + b.x) / 4;
          const midy = (a.y + c1.y + c2.y + b.y) / 4;
          svg.push(`<text x="${midx}" y="${midy}" font-family="Segoe UI, Arial" font-size="12" text-anchor="middle" dominant-baseline="central" fill="#111827">${e.label}</text>`);
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
})();