/* IDEF0 Diagrammer — simple, single-boot front-end
   - Populates Model/Context selects from window.MODELS
   - Draws the selected context into <svg id="svg">
   - Exposes window.drawDiagram(diagramOrText)
*/

(function () {
  "use strict";

  // ===================================================================
  // STATE & CONFIGURATION
  // ===================================================================
  const GRID = 10;
  const state = {
    nodes: [],
    edges: [],
    stubs: [],
    seq: 1,
    activeHandle: null,
  };

  function newid(p = "id") { return p + (state.seq++); }
  function snap(n) { return Math.round(n / GRID) * GRID; }
  const isHandle = el => !!(el && el.classList && el.classList.contains('handle'));

  // ===================================================================
  // DOM HELPERS
  // ===================================================================
  const $ = (sel) => document.getElementById(sel);
  const svgNS = 'http://www.w3.org/2000/svg';

  function createEl(tag, attrs = {}, textContent = '') {
    const el = document.createElementNS(svgNS, tag);
    for (const key in attrs) {
      el.setAttribute(key, attrs[key]);
    }
    if (textContent) {
      el.textContent = textContent;
    }
    return el;
  }

  function setOptions(selEl, items, getVal, getText) {
    selEl.innerHTML = items
      .map((it) => `<option value="${getVal(it)}">${getText(it)}</option>`)
      .join('');
  }

  function clearSVG(svgEl) {
    while (svgEl.firstChild) svgEl.removeChild(svgEl.firstChild);
  }

  // ===================================================================
  // POINT & ROUTING LOGIC
  // ===================================================================
  function handlePoints(node) {
    const cx = node.x + node.w / 2, cy = node.y + node.h / 2;
    return { left: { x: node.x, y: cy }, right: { x: node.x + node.w, y: cy }, top: { x: cx, y: node.y }, bottom: { x: cx, y: node.y + node.h } };
  }

  function route(p0, p1) {
    // Simple straight-line router for now.
    return `M ${p0.x} ${p0.y} L ${p1.x} ${p1.y}`;
  }

  // ---------- Model Manipulation (from stable_app.js) ----------
  const nodeById = id => state.nodes.find(n => n.id === id);

  function makeEdge(from, to) {
    if (!from || !to) return null;
    // Simplified validation: for this viewer, we assume any connection is valid.
    // A full implementation would check roles (I, C, O, M).
    if (from.nodeId === to.nodeId) return null; // Cannot connect to self

    const e = {
      id: newid('e'),
      type: 'normal',
      a: { nodeId: from.nodeId, side: from.side },
      b: { nodeId: to.nodeId, side: to.side },
      label: ''
    };
    state.edges.push(e);
    return e;
  }

  // ---------- Selection Management (from stable_app.js) ----------
  function setActiveHandle(h) {
    state.activeHandle = h;
    document.querySelectorAll('.handle').forEach(el => el.classList.remove('active'));
    if (!h) return;
    const sel = `.handle[data-node-id="${h.nodeId}"][data-side="${h.side}"]`;
    const el = $('svg').querySelector(sel);
    if (el) el.classList.add('active');
  }

  // ---------- SVG Rendering ----------
  function appendDefs(svgEl) {
    const defs = createEl('defs');
    const marker = createEl('marker', {
      id: 'arrow', viewBox: '0 0 10 10', refX: '10', refY: '5',
      markerWidth: '8', markerHeight: '8', orient: 'auto-start-reverse'
    });
    marker.appendChild(createEl('path', { d: 'M 0 0 L 10 5 L 0 10 z', class: 'arrowhead' }));
    defs.appendChild(marker);
    svgEl.appendChild(defs);
  }

  function drawNode(node) {
    const g = createEl('g', { class: 'g-node' });

    g.appendChild(createEl('rect', {
      x: node.x, y: node.y, width: node.w, height: node.h,
      class: 'node-box'
    }));
    g.appendChild(createEl('text', {
      x: node.x + node.w / 2, y: node.y + 20,
      'text-anchor': 'middle', class: 'node-name'
    }, node.name || ''));
    g.appendChild(createEl('text', {
      x: node.x + node.w / 2, y: node.y + node.h - 8,
      'text-anchor': 'middle', class: 'node-number'
    }, node.number || ''));

    // Add interactive handles (from stable_app.js)
    const hp = handlePoints(node);
    [{ side: 'left', ...hp.left }, { side: 'top', ...hp.top }, { side: 'right', ...hp.right }, { side: 'bottom', ...hp.bottom }]
      .forEach(h => {
        const c = createEl('circle', { class: 'handle', cx: h.x, cy: h.y, r: 6 });
        c.dataset.nodeId = node.id;
        c.dataset.side = h.side;
        g.appendChild(c);
      });

    return g;
  }

  function drawEdge(edge) {
    const a = nodeById(edge?.a?.nodeId);
    const b = nodeById(edge?.b?.nodeId);
    if (!a || !b) return null;

    const pA = handlePoints(a)[edge.a.side];
    const pB = handlePoints(b)[edge.b.side];
    const d = route(pA, pB);

    const g = createEl('g', { class: 'g-edge' });
    g.appendChild(createEl('path', { d, class: 'edge-path', 'marker-end': 'url(#arrow)' }));
    if (edge.label) {
      g.appendChild(createEl('text', {
        x: (pA.x + pB.x) / 2, y: (pA.y + pB.y) / 2 - 5,
        'text-anchor': 'middle', class: 'edge-label'
      }, edge.label));
    }

    return g;
  }

  function drawStub(stub) {
    const anchorNode = nodeById(stub?.anchor?.nodeId);
    if (!anchorNode) return null;

    const side = stub.anchor.side;
    const len = stub.length || 80;
    const dir = stub.dir || 1;

    let x1, y1, x2, y2, textAnchor, textOffset;

    if (side === 'left') {
      x1 = anchorNode.x; y1 = anchorNode.y + anchorNode.h / 2;
      x2 = x1 - len; y2 = y1;
      textAnchor = 'end'; textOffset = { x: -8, y: -4 };
    } else if (side === 'right') {
      x1 = anchorNode.x + anchorNode.w; y1 = anchorNode.y + anchorNode.h / 2;
      x2 = x1 + len; y2 = y1;
      textAnchor = 'start'; textOffset = { x: 8, y: -4 };
    } else if (side === 'top') {
      x1 = anchorNode.x + anchorNode.w / 2; y1 = anchorNode.y;
      x2 = x1; y2 = y1 - len;
      textAnchor = 'middle'; textOffset = { x: 0, y: -8 };
    } else { // bottom
      x1 = anchorNode.x + anchorNode.w / 2; y1 = anchorNode.y + anchorNode.h;
      x2 = x1; y2 = y1 + len;
      textAnchor = 'middle'; textOffset = { x: 0, y: 8 };
    }

    const g = createEl('g', { class: 'g-stub' });
    const isIncoming = (side === 'left' || side === 'top');
    const line = createEl('line', { x1, y1, x2, y2, class: 'stub' });
    // Set marker based on direction
    const marker = isIncoming ? 'marker-start' : 'marker-end';
    line.setAttribute(marker, 'url(#arrow)');
    g.appendChild(line);
    if (stub.label) {
      g.appendChild(createEl('text', {
        x: x2 + textOffset.x, y: y2 + textOffset.y,
        'text-anchor': textAnchor, class: 'stub-label'
      }, stub.label));
    }

    return g;
  }

  function render() {
    const svgEl = $('svg');
    clearSVG(svgEl);
    appendDefs(svgEl);

    state.stubs.forEach(stub => {
      const el = drawStub(stub);
      if (el) svgEl.appendChild(el);
    });
    state.edges.forEach(edge => {
      const el = drawEdge(edge);
      if (el) svgEl.appendChild(el);
    });
    state.nodes.forEach(node => {
      const el = drawNode(node);
      if (el) svgEl.appendChild(el);
    });

    // Restore selection highlight
    setActiveHandle(state.activeHandle);
  }

  // ---------- Main Orchestrator ----------
  window.drawDiagram = function (diagram) {
    const data = typeof diagram === 'string' ? JSON.parse(diagram) : (diagram || {});
    if (!$('svg')) {
      console.warn('No <svg id="svg"> element found; cannot draw diagram.');
      return;
    }

    // Load data into state and render
    state.nodes = data.nodes || [];
    state.edges = data.edges || [];
    state.stubs = data.stubs || [];
    state.activeHandle = null;
    render();
  };

  // ---------- Models / contexts ----------
  function applyModelsFromPayload() {
    const payload = (window.MODELS && Array.isArray(window.MODELS.models))
      ? window.MODELS
      : { models: [] };

    const models = payload.models || [];
    const modelSel = $('modelSelect');
    const ctxSel   = $('contextSelect');

    if (!modelSel || !ctxSel) {
      console.warn('modelSelect/contextSelect not found in DOM.');
      return;
    }

    // Fill model dropdown
    setOptions(modelSel, models, (m) => m.id, (m) => m.name || `Model ${m.id}`);

    function pickAndDrawContext(m, ctxId) {
      const ctx = (m.contexts || []).find((c) => String(c.id) === String(ctxId));
      if (!ctx) return;
      // ctx.diagram is already an object
      window.drawDiagram(ctx.diagram || { nodes: [], edges: [], stubs: [] });
    }

    function onModelChange() {
      const m = models.find((x) => String(x.id) === String(modelSel.value));
      if (!m) return;

      const contexts = m.contexts || [];
      setOptions(ctxSel, contexts, (c) => c.id, (c) => c.label || c.id);

      // Prefer A0 (decomposition). Fallback: A-0 (single box) → first available.
      const preferred =
        contexts.find((c) => c.id === 'A0') ||
        contexts.find((c) => c.id === 'A-0') ||
        contexts[0];

      if (preferred) {
        ctxSel.value = preferred.id;
        pickAndDrawContext(m, preferred.id);
      } else {
        // nothing to draw
        window.drawDiagram({ nodes: [], edges: [], stubs: [] });
      }
    }

    function onContextChange() {
      const m = models.find((x) => String(x.id) === String(modelSel.value));
      if (!m) return;
      pickAndDrawContext(m, ctxSel.value);
    }

    modelSel.onchange = onModelChange;
    ctxSel.onchange   = onContextChange;

    // Auto-select first model on load
    if (models[0]) {
      modelSel.value = models[0].id;
      onModelChange();
    } else {
      // No models — clear canvas
      window.drawDiagram({ nodes: [], edges: [], stubs: [] });
    }
  }

  // ---------- Two-click interactions (from stable_app.js) ----------
  function addInteractionListeners() {
    const svgEl = $('svg');
    if (!svgEl) return;

    svgEl.addEventListener('click', ev => {
      if (!isHandle(ev.target)) return;
      const clicked = { nodeId: ev.target.dataset.nodeId, side: ev.target.dataset.side };

      if (!state.activeHandle) {
        setActiveHandle(clicked);
      } else if (state.activeHandle.nodeId === clicked.nodeId && state.activeHandle.side === clicked.side) {
        setActiveHandle(null); // Deselect if clicking same handle
      } else {
        const edge = makeEdge(state.activeHandle, clicked);
        if (edge) { render(); }
        setActiveHandle(null);
      }
    });

    document.addEventListener('keydown', ev => {
      if (ev.key === 'Escape') {
        setActiveHandle(null);
      }
    });
  }

  // ---------- Optional: hook a "Load" button in the footer ----------
  function wireOptionalLoadButton() {
    const btn = document.getElementById('btnLoad');
    if (!btn) return;
    btn.addEventListener('click', () => {
      const txt = window.prompt('Paste a diagram JSON (single context.diagram):');
      if (!txt) return;
      try { window.drawDiagram(txt); }
      catch (e) { alert('Invalid JSON'); }
    });
  }

  // ---------- Boot once ----------
  document.addEventListener('DOMContentLoaded', () => {
    try {
      applyModelsFromPayload();
      wireOptionalLoadButton();
      addInteractionListeners();
    } catch (e) {
      console.error(e);
    }
  });
})();
