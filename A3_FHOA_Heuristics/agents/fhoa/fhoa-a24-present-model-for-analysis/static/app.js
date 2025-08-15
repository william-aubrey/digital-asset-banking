/* IDEF0 Diagrammer — simple, single-boot front-end
   - Populates Model/Context selects from window.MODELS
   - Draws the selected context into <svg id="svg">
   - Exposes window.importJSON(diagramOrText)
*/

(function () {
  // ---------- DOM helpers ----------
  const $ = (sel) => document.getElementById(sel);
  const svgNS = 'http://www.w3.org/2000/svg';

  function setOptions(selEl, items, getVal, getText) {
    selEl.innerHTML = items
      .map((it) => `<option value="${getVal(it)}">${getText(it)}</option>`)
      .join('');
  }

  function clearSVG(svg) {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
  }

  // ---------- Minimal renderer ----------
  function drawDiagram(diagram) {
    const data = typeof diagram === 'string' ? JSON.parse(diagram) : (diagram || {});
    const nodes = data.nodes || [];
    const edges = data.edges || [];
    const svg = $('svg'); // allow fallback id
    const svgEl = svg || $('canvas') || $('svgRoot') || document.getElementById('svg');
    const surface = $('svg') || document.getElementById('svg');

    const target = surface || svgEl;
    if (!target) {
      console.warn('No <svg id="svg"> element found; cannot draw.');
      return;
    }

    clearSVG(target);

    // index nodes
    const byId = {};
    nodes.forEach((n) => (byId[n.id] = n));

    // boxes
    nodes.forEach((n) => {
      const g = document.createElementNS(svgNS, 'g');

      const rect = document.createElementNS(svgNS, 'rect');
      rect.setAttribute('x', n.x);
      rect.setAttribute('y', n.y);
      rect.setAttribute('width', n.w);
      rect.setAttribute('height', n.h);
      rect.setAttribute('rx', 10);
      rect.setAttribute('ry', 10);
      rect.setAttribute('fill', 'white');
      rect.setAttribute('stroke', 'black');
      g.appendChild(rect);

      const title = document.createElementNS(svgNS, 'text');
      title.setAttribute('x', n.x + n.w / 2);
      title.setAttribute('y', n.y + 18);
      title.setAttribute('text-anchor', 'middle');
      title.setAttribute('font-size', '12');
      title.textContent = n.name || '';
      g.appendChild(title);

      const number = document.createElementNS(svgNS, 'text');
      number.setAttribute('x', n.x + n.w / 2);
      number.setAttribute('y', n.y + n.h - 6);
      number.setAttribute('text-anchor', 'middle');
      number.setAttribute('font-size', '10');
      number.textContent = n.number || '';
      g.appendChild(number);

      target.appendChild(g);
    });

    // lines (simple straight connectors: right->left)
    edges.forEach((e) => {
      const a = byId[e?.a?.nodeId];
      const b = byId[e?.b?.nodeId];
      if (!a || !b) return;

      const x1 = a.x + a.w;
      const y1 = a.y + a.h / 2;
      const x2 = b.x;
      const y2 = b.y + b.h / 2;

      const path = document.createElementNS(svgNS, 'path');
      path.setAttribute('d', `M ${x1} ${y1} L ${x2} ${y2}`);
      path.setAttribute('stroke', 'black');
      path.setAttribute('fill', 'none');
      target.appendChild(path);
    });
  }

  // Expose for other scripts/buttons
  window.importJSON = function (objOrString) {
    drawDiagram(objOrString);
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
      // ctx.diagram is already an object — but the renderer accepts either
      window.importJSON(ctx.diagram || { nodes: [], edges: [], stubs: [] });
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
        window.importJSON({ nodes: [], edges: [], stubs: [] });
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
      window.importJSON({ nodes: [], edges: [], stubs: [] });
    }
  }

  // ---------- Optional: hook a "Load" button in the footer ----------
  function wireOptionalLoadButton() {
    const btn = document.getElementById('btnLoad');
    if (!btn) return;
    btn.addEventListener('click', () => {
      const txt = window.prompt('Paste a diagram JSON (single context.diagram):');
      if (!txt) return;
      try { window.importJSON(txt); }
      catch (e) { alert('Invalid JSON'); }
    });
  }

  // ---------- Boot once ----------
  document.addEventListener('DOMContentLoaded', () => {
    try {
      applyModelsFromPayload();
      wireOptionalLoadButton();
    } catch (e) {
      console.error(e);
    }
  });
})();
