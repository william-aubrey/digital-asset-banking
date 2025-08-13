// === IDEF0 Diagrammer Script (v0.3.0) ===
(function(){
  const canvas = document.getElementById('canvas');
  const connSvg = document.getElementById('connSvg');
  const connectors = []; // {id, a:{handleEl,nodeId,handleSide,role}, b:{...}, pathEl, labelEl, label}
  const GRID = 10; // px snap

  const qp = (sel, root=document)=>root.querySelector(sel);
  const qpa = (sel, root=document)=>Array.from(root.querySelectorAll(sel));

  function getHandlePoint(handleEl) {
    const r = handleEl.getBoundingClientRect();
    return { x: r.left + r.width/2 + window.scrollX, y: r.top + r.height/2 + window.scrollY };
  }
  function getCanvasPointFromPage(p) {
    const cr = canvas.getBoundingClientRect();
    return { x: p.x - cr.left - window.scrollX, y: p.y - cr.top - window.scrollY };
  }
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
    return `M ${p0.x},${p0.y} C ${c1.x},${c1.y} ${c2.x},${c2.y} ${p1.x},${p1.y}`;
  }
  function cubicPointAt(p0, c1, c2, p1, t){
    const mt = 1 - t;
    const x = mt*mt*mt*p0.x + 3*mt*mt*t*c1.x + 3*mt*t*t*c2.x + t*t*t*p1.x;
    const y = mt*mt*mt*p0.y + 3*mt*mt*t*c1.y + 3*mt*t*t*c2.y + t*t*t*p1.y;
    return {x,y};
  }
  function makeConnectorId(){ return 'edge-' + Math.random().toString(36).slice(2,9); }

  function updateConnectorPath(conn) {
    const p0 = getCanvasPointFromPage(getHandlePoint(conn.a.handleEl));
    const p1 = getCanvasPointFromPage(getHandlePoint(conn.b.handleEl));
    // control points
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

    // position label near midpoint
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
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.classList.add('connector');
    path.setAttribute('data-kind', kind);
    path.setAttribute('marker-end', `url(#arrow-${kind || 'generic'})`);
    path.setAttribute('id', id);
    connSvg.appendChild(path);
    const labelEl = createLabelEl('');

    const conn = {
      id,
      a: { nodeId: source.closest('.node')?.id || source.closest('.function, .offpage').id, handleSide: source.dataset.handle, role: source.dataset.role, handleEl: source },
      b: { nodeId: target.closest('.node')?.id || target.closest('.function, .offpage').id, handleSide: target.dataset.handle, role: target.dataset.role, handleEl: target },
      pathEl: path,
      labelEl,
      label: ''
    };
    connectors.push(conn);
    updateConnectorPath(conn);

    // selection
    path.addEventListener('click', (e) => {
      qpa('.connector.selected', connSvg).forEach(p => p.classList.remove('selected'));
      path.classList.add('selected');
      e.stopPropagation();
    });
  }

  // Dragging nodes (function + offpage) with snap-to-grid
  let drag = null;
  canvas.addEventListener('mousedown', (e) => {
    const node = e.target.closest('.function, .offpage');
    if (!node) return;
    if (e.target.classList.contains('handle') || e.target.isContentEditable) return;
    drag = {
      el: node,
      startX: e.clientX,
      startY: e.clientY,
      origLeft: parseFloat(node.style.left || 0),
      origTop: parseFloat(node.style.top || 0)
    };
    e.preventDefault();
  });
  window.addEventListener('mousemove', (e) => {
    if (!drag) return;
    const dx = e.clientX - drag.startX;
    const dy = e.clientY - drag.startY;
    drag.el.style.left = (drag.origLeft + dx) + 'px';
    drag.el.style.top  = (drag.origTop  + dy) + 'px';
    refreshAllConnectors();
  });
  window.addEventListener('mouseup', () => {
    if (!drag) return;
    const left = parseFloat(drag.el.style.left || 0);
    const top  = parseFloat(drag.el.style.top  || 0);
    drag.el.style.left = (Math.round(left / GRID) * GRID) + 'px';
    drag.el.style.top  = (Math.round(top  / GRID) * GRID) + 'px';
    drag = null;
    refreshAllConnectors();
  });

  // Handle click-to-connect, reattach, and spawn-new-box-from-output
  let pendingHandle = null;
  canvas.addEventListener('click', (e) => {
    const h = e.target.closest('.handle');
    if (!h) return;

    // If a connector is selected, reattach
    const selected = qp('.connector.selected', connSvg);
    if (selected) {
      const conn = connectors.find(c => c.pathEl === selected);
      if (conn) {
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

    // Normal two-click connect
    if (pendingHandle === h) {
      h.classList.remove('active');
      pendingHandle = null;
      return;
    }
    if (!pendingHandle) {
      pendingHandle = h;
      h.classList.add('active');
    } else {
      if (pendingHandle.closest('.function, .offpage') !== h.closest('.function, .offpage')) {
        createConnector(pendingHandle, h);
      }
      pendingHandle.classList.remove('active');
      pendingHandle = null;
    }
    e.stopPropagation();
  });

  // Spawn a new function by clicking empty canvas after selecting an OUTPUT handle
  canvas.addEventListener('click', (e) => {
    if (e.target !== canvas) return;
    if (!pendingHandle) return;
    const role = pendingHandle.dataset.role;
    const side = pendingHandle.dataset.handle;
    if (role === 'output') {
      // Create a new function near the click and connect output->input
      const id = 'fn-' + Math.random().toString(36).slice(2,7);
      const node = document.createElement('div');
      node.className = 'function';
      node.id = id;
      const cr = canvas.getBoundingClientRect();
      const x = e.clientX - cr.left - 110; // center new box on click
      const y = e.clientY - cr.top  - 60;
      node.style.left = (Math.round(x / GRID)*GRID) + 'px';
      node.style.top  = (Math.round(y / GRID)*GRID) + 'px';
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
      // clicking canvas cancels pending if it's not output
      pendingHandle.classList.remove('active');
      pendingHandle = null;
    }
  });

  // Deselect on empty canvas click
  canvas.addEventListener('click', (e) => {
    if (e.target === canvas) {
      qpa('.connector.selected', connSvg).forEach(p => p.classList.remove('selected'));
    }
  });

  // Keyboard delete
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Delete' || e.key === 'Backspace') {
      const sel = qp('.connector.selected', connSvg);
      if (sel) {
        const idx = connectors.findIndex(c => c.pathEl === sel);
        if (idx >= 0) {
          const c = connectors[idx];
          c.pathEl.remove();
          if (c.labelEl) c.labelEl.remove();
          connectors.splice(idx,1);
        }
      }
    }
  });

  // Toolbar
  document.getElementById('clearEdges').addEventListener('click', () => {
    connectors.splice(0).forEach(c => { c.pathEl.remove(); if (c.labelEl) c.labelEl.remove(); });
  });
  document.getElementById('addBox').addEventListener('click', () => {
    addFunctionAt(160 + Math.random()*320, 120 + Math.random()*240);
  });
  document.getElementById('addOffpage').addEventListener('click', () => {
    addOffpageAt(40 + Math.random()*60, 40 + Math.random()*60);
  });

  function addFunctionAt(x,y){
    const id = 'fn-' + Math.random().toString(36).slice(2,7);
    const node = document.createElement('div');
    node.className = 'function';
    node.id = id;
    node.style.left = (Math.round(x/10)*10) + 'px';
    node.style.top  = (Math.round(y/10)*10) + 'px';
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
    node.style.left = (Math.round(x/10)*10) + 'px';
    node.style.top  = (Math.round(y/10)*10) + 'px';
    node.innerHTML = `
      <div class="handle handle-top"    data-role="control"   data-handle="top"><span class="icom">C</span></div>
      <div class="handle handle-left"   data-role="input"     data-handle="left"><span class="icom">I</span></div>
      <div class="handle handle-right"  data-role="output"    data-handle="right"><span class="icom">O</span></div>
      <div class="handle handle-bottom" data-role="mechanism" data-handle="bottom"><span class="icom">M</span></div>
      <div class="label">OFF‑PAGE</div>
    `;
    canvas.appendChild(node);
  }

  // Save/Load
  function serialize(){
    const nodes = qpa('.function, .offpage', canvas).map(n => ({
      id: n.id,
      type: n.classList.contains('offpage') ? 'offpage' : 'function',
      left: parseFloat(n.style.left || 0),
      top: parseFloat(n.style.top || 0),
      name: n.classList.contains('function') ? (qp('.function-name', n)?.textContent?.trim() || '') : 'OFF-PAGE',
      number: n.classList.contains('function') ? (qp('.function-number', n)?.textContent?.trim() || '') : ''
    }));
    const edges = connectors.map(c => ({
      id: c.id,
      a: { nodeId: c.a.nodeId, handleSide: c.a.handleSide, role: c.a.role },
      b: { nodeId: c.b.nodeId, handleSide: c.b.handleSide, role: c.b.role },
      kind: c.pathEl.getAttribute('data-kind'),
      label: c.label || ''
    }));
    return { version: '0.3.0', nodes, edges };
  }
  function deserialize(data){
    qpa('.function, .offpage', canvas).forEach(n => n.remove());
    qpa('.connector', connSvg).forEach(p => p.remove());
    qpa('.edge-label', canvas).forEach(l => l.remove());
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
      const aSel = `#${e.a.nodeId} .handle-${e.a.handleSide}`;
      const bSel = `#${e.b.nodeId} .handle-${e.b.handleSide}`;
      const aHandle = qp(aSel, canvas);
      const bHandle = qp(bSel, canvas);
      if (aHandle && bHandle) {
        const id = e.id || makeConnectorId();
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.classList.add('connector');
        path.setAttribute('data-kind', e.kind || e.a.role);
        path.setAttribute('marker-end', `url(#arrow-${e.kind || e.a.role || 'generic'})`);
        path.setAttribute('id', id);
        connSvg.appendChild(path);
        const labelEl = createLabelEl(e.label || '');
        const conn = {
          id,
          a: { nodeId: e.a.nodeId, handleSide: e.a.handleSide, role: e.a.role, handleEl: aHandle },
          b: { nodeId: e.b.nodeId, handleSide: e.b.handleSide, role: e.b.role, handleEl: bHandle },
          pathEl: path,
          labelEl,
          label: e.label || ''
        };
        connectors.push(conn);
        path.addEventListener('click', (ev) => {
          qpa('.connector.selected', connSvg).forEach(p => p.classList.remove('selected'));
          path.classList.add('selected');
          ev.stopPropagation();
        });
        updateConnectorPath(conn);
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

  // Export SVG
  document.getElementById('exportSvg').addEventListener('click', () => {
    const cr = canvas.getBoundingClientRect();
    const data = serialize();
    let svg = [];
    svg.push(`<svg xmlns="http://www.w3.org/2000/svg" width="${cr.width}" height="${cr.height}" viewBox="0 0 ${cr.width} ${cr.height}">`);
    svg.push(`<rect width="100%" height="100%" fill="#f8fbff" stroke="#cbd5e1" />`);

    // Boxes and off-page
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

    // Connectors from live DOM geometry
    const liveConns = connectors.slice();
    liveConns.forEach(c => {
      function getPts(handle){
        const p = getCanvasPointFromPage(getHandlePoint(handle.handleEl));
        return p;
      }
      const p0 = getPts(c.a);
      const p1 = getPts(c.b);
      const dx = Math.max(40, Math.abs(p0.x - p1.x) / 2);
      const dy = Math.max(40, Math.abs(p0.y - p1.y) / 2);
      let c1 = {x: p0.x, y: p0.y};
      let c2 = {x: p1.x, y: p1.y};
      if (c.a.handleSide === 'right') c1.x += dx;
      if (c.a.handleSide === 'left')  c1.x -= dx;
      if (c.a.handleSide === 'top')   c1.y -= dy;
      if (c.a.handleSide === 'bottom')c1.y += dy;
      if (c.b.handleSide === 'right') c2.x += dx;
      if (c.b.handleSide === 'left')  c2.x -= dx;
      if (c.b.handleSide === 'top')   c2.y -= dy;
      if (c.b.handleSide === 'bottom')c2.y += dy;
      const d = `M ${p0.x},${p0.y} C ${c1.x},${c1.y} ${c2.x},${c2.y} ${p1.x},${p1.y}`;
      const dash = c.pathEl.getAttribute('data-kind') === 'control' ? ' stroke-dasharray="6 4"' :
                   c.pathEl.getAttribute('data-kind') === 'mechanism' ? ' stroke-dasharray="2 4"' : '';
      svg.push(`<path d="${d}" fill="none" stroke="#111827" stroke-width="2"${dash} marker-end="url(#arrow)"/>`);
      if (c.label && c.label.trim()) {
        const mid = cubicPointAt(p0, c1, c2, p1, 0.5);
        svg.push(`<text x="${mid.x}" y="${mid.y}" font-family="Segoe UI, Arial" font-size="12" text-anchor="middle" dominant-baseline="central" fill="#111827">${escapeXml(c.label)}</text>`);
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

  function escapeXml(s){
    return (s || '').replace(/[&<>"']/g, ch => (
      ch === '&' ? '&amp;' : ch === '<' ? '&lt;' : ch === '>' ? '&gt;' : ch === '"' ? '&quot;' : '&#39;'
    ));
  }

  // Initial demo edge
  window.addEventListener('load', () => {
    const a = qp('#fn-1 .handle-right');
    const b = qp('#fn-2 .handle-left');
    if (a && b) requestAnimationFrame(() => createConnector(a, b));
  });

  // Keep SVG sized to canvas
  const connSvgEl = document.getElementById('connSvg');
  function sizeSvgToCanvas() {
    const cr = canvas.getBoundingClientRect();
    connSvgEl.setAttribute('width', cr.width);
    connSvgEl.setAttribute('height', cr.height);
  }
  new ResizeObserver(() => { sizeSvgToCanvas(); refreshAllConnectors(); }).observe(canvas);
  sizeSvgToCanvas();
})();