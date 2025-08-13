// === IDEF0 Diagrammer Script (v0.2.0) ===
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
    // control points (duplicate cubicPath math)
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

    // position label near midpoint (t=0.5)
    const mid = cubicPointAt(p0, c1, c2, p1, 0.5);
    if (conn.labelEl) {
      conn.labelEl.style.left = (mid.x + canvas.getBoundingClientRect().left + window.scrollX - canvas.getBoundingClientRect().left) - conn.labelEl.offsetWidth/2 + 'px';
      conn.labelEl.style.top  = (mid.y + canvas.getBoundingClientRect().top + window.scrollY - canvas.getBoundingClientRect().top) - conn.labelEl.offsetHeight/2 + 'px';
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
    path.setAttribute('id', id);
    connSvg.appendChild(path);
    const labelEl = createLabelEl(''); // empty label by default

    const conn = {
      id,
      a: { nodeId: source.closest('.function').id, handleSide: source.dataset.handle, role: source.dataset.role, handleEl: source },
      b: { nodeId: target.closest('.function').id, handleSide: target.dataset.handle, role: target.dataset.role, handleEl: target },
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

  // Dragging nodes with snap-to-grid (on mouseup)
  let drag = null;
  canvas.addEventListener('mousedown', (e) => {
    const node = e.target.closest('.function');
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
    // snap
    const left = parseFloat(drag.el.style.left || 0);
    const top  = parseFloat(drag.el.style.top  || 0);
    const snappedLeft = Math.round(left / GRID) * GRID;
    const snappedTop  = Math.round(top  / GRID) * GRID;
    drag.el.style.left = snappedLeft + 'px';
    drag.el.style.top  = snappedTop  + 'px';
    drag = null;
    refreshAllConnectors();
  });

  // Handle click-to-connect AND reattach endpoints if a connector is selected
  let pendingHandle = null;
  canvas.addEventListener('click', (e) => {
    const h = e.target.closest('.handle');
    if (!h) return;

    // Reattach if a connector is selected
    const selected = qp('.connector.selected', connSvg);
    if (selected) {
      const conn = connectors.find(c => c.pathEl === selected);
      if (conn) {
        if (e.altKey) {
          conn.a = { nodeId: h.closest('.function').id, handleSide: h.dataset.handle, role: h.dataset.role, handleEl: h };
          selected.setAttribute('data-kind', h.dataset.role);
        } else {
          conn.b = { nodeId: h.closest('.function').id, handleSide: h.dataset.handle, role: h.dataset.role, handleEl: h };
        }
        updateConnectorPath(conn);
        return;
      }
    }

    // Toggle selection for new connection
    if (pendingHandle === h) {
      h.classList.remove('active');
      pendingHandle = null;
      return;
    }
    if (!pendingHandle) {
      pendingHandle = h;
      h.classList.add('active');
    } else {
      if (pendingHandle.closest('.function') !== h.closest('.function')) {
        createConnector(pendingHandle, h);
      }
      pendingHandle.classList.remove('active');
      pendingHandle = null;
    }
    e.stopPropagation();
  });
  canvas.addEventListener('click', (e) => {
    if (e.target === canvas) {
      if (pendingHandle) pendingHandle.classList.remove('active');
      pendingHandle = null;
      qpa('.connector.selected', connSvg).forEach(p => p.classList.remove('selected'));
    }
  });

  // Keyboard delete for selected connector
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

  // Toolbar actions
  document.getElementById('clearEdges').addEventListener('click', () => {
    connectors.splice(0).forEach(c => { c.pathEl.remove(); if (c.labelEl) c.labelEl.remove(); });
  });
  document.getElementById('addBox').addEventListener('click', () => {
    const id = 'fn-' + Math.random().toString(36).slice(2,7);
    const node = document.createElement('div');
    node.className = 'function';
    node.id = id;
    node.style.left = Math.round(120 + Math.random()*360) + 'px';
    node.style.top  = Math.round(80 + Math.random()*280) + 'px';
    node.innerHTML = `
      <div class="handle handle-top"    data-role="control"   data-handle="top"></div>
      <div class="handle handle-left"   data-role="input"     data-handle="left"></div>
      <div class="handle handle-right"  data-role="output"    data-handle="right"></div>
      <div class="handle handle-bottom" data-role="mechanism" data-handle="bottom"></div>
      <div class="function-name" contenteditable="true">NEW FUNCTION</div>
      <div class="function-number">\${(Math.floor(Math.random()*6)+1)}</div>
    `;
    canvas.appendChild(node);
  });

  // Save/Load (localStorage)
  function serialize(){
    const nodes = qpa('.function', canvas).map(n => ({
      id: n.id,
      left: parseFloat(n.style.left || 0),
      top: parseFloat(n.style.top || 0),
      name: qp('.function-name', n)?.textContent?.trim() || '',
      number: qp('.function-number', n)?.textContent?.trim() || ''
    }));
    const edges = connectors.map(c => ({
      id: c.id,
      a: { nodeId: c.a.nodeId, handleSide: c.a.handleSide, role: c.a.role },
      b: { nodeId: c.b.nodeId, handleSide: c.b.handleSide, role: c.b.role },
      kind: c.pathEl.getAttribute('data-kind'),
      label: c.label || ''
    }));
    return { version: '0.2.0', nodes, edges };
  }
  function deserialize(data){
    // Clear existing
    qpa('.function', canvas).forEach(n => n.remove());
    qpa('.connector', connSvg).forEach(p => p.remove());
    qpa('.edge-label', canvas).forEach(l => l.remove());
    connectors.splice(0);

    // Nodes
    (data.nodes || []).forEach(n => {
      const node = document.createElement('div');
      node.className = 'function';
      node.id = n.id;
      node.style.left = n.left + 'px';
      node.style.top  = n.top  + 'px';
      node.innerHTML = `
        <div class="handle handle-top"    data-role="control"   data-handle="top"></div>
        <div class="handle handle-left"   data-role="input"     data-handle="left"></div>
        <div class="handle handle-right"  data-role="output"    data-handle="right"></div>
        <div class="handle handle-bottom" data-role="mechanism" data-handle="bottom"></div>
        <div class="function-name" contenteditable="true">${n.name || 'FUNCTION'}</div>
        <div class="function-number">${n.number || ''}</div>
      `;
      canvas.appendChild(node);
    });

    // Edges
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
        // selection click handler
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
    const data = serialize();
    localStorage.setItem('idef0-diagram', JSON.stringify(data));
    alert('Saved to localStorage.');
  });
  document.getElementById('load').addEventListener('click', () => {
    const raw = localStorage.getItem('idef0-diagram');
    if (!raw) { alert('No saved diagram found.'); return; }
    try { deserialize(JSON.parse(raw)); } catch (e) { alert('Load failed: ' + e.message); }
  });

  // Export JSON file
  document.getElementById('exportJson').addEventListener('click', () => {
    const data = serialize();
    const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'idef0-diagram.json';
    a.click();
    URL.revokeObjectURL(url);
  });

  // Export simple SVG (boxes + connectors)
  document.getElementById('exportSvg').addEventListener('click', () => {
    const cr = canvas.getBoundingClientRect();
    const data = serialize();
    // Build SVG content
    let svg = [];
    svg.push(`<svg xmlns="http://www.w3.org/2000/svg" width="${cr.width}" height="${cr.height}" viewBox="0 0 ${cr.width} ${cr.height}">`);
    svg.push(`<rect width="100%" height="100%" fill="#f8fbff" stroke="#cbd5e1" />`);

    // Draw boxes
    data.nodes.forEach(n => {
      const x = n.left, y = n.top, w = 220, h = 120;
      svg.push(`<g>`);
      svg.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#fff" stroke="#1f2937" stroke-width="2" rx="4" ry="4"/>`);
      svg.push(`<text x="${x + w/2}" y="${y + h/2}" font-family="Segoe UI, Arial" font-size="14" font-weight="700" text-anchor="middle" dominant-baseline="middle">${escapeXml(n.name || '')}</text>`);
      svg.push(`<text x="${x + w - 10}" y="${y + h - 8}" font-family="Segoe UI, Arial" font-size="12" text-anchor="end">${escapeXml(n.number || '')}</text>`);
      svg.push(`</g>`);
    });

    // For connectors, recompute points using current DOM (for accuracy)
    const liveConns = connectors.slice();
    liveConns.forEach(c => {
      const p0 = getCanvasPointFromPage(getHandlePoint(c.a.handleEl));
      const p1 = getCanvasPointFromPage(getHandlePoint(c.b.handleEl));
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
      svg.push(`<path d="${d}" fill="none" stroke="#111827" stroke-width="2"${dash}/>`);
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

  // Helpers
  function escapeXml(s){
    return (s || '').replace(/[&<>"']/g, ch => (
      ch === '&' ? '&amp;' : ch === '<' ? '&lt;' : ch === '>' ? '&gt;' : ch === '"' ? '&quot;' : '&#39;'
    ));
  }

  // Initial demo edge
  window.addEventListener('load', () => {
    const a = qp('#fn-1 .handle-right');
    const b = qp('#fn-2 .handle-left');
    if (a && b) {
      requestAnimationFrame(() => createConnector(a, b));
    }
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