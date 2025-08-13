import os, json, zipfile, pathlib

PROJECT = "idef0_v033b_split"
root = os.path.join(os.path.dirname(__file__), PROJECT)
os.makedirs(root, exist_ok=True)

index_html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>IDEF0 Diagrammer — v0.3.3b</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <!-- Top metadata & controls -->
  <header class="topbar">
    <div class="left">
      <div class="field">
        <label>Author</label>
        <input id="author" placeholder="Your name" />
      </div>
      <div class="field">
        <label>Date</label>
        <input id="date" />
      </div>
      <div class="field">
        <label>Project</label>
        <input id="project" placeholder="Project name" />
      </div>
      <div class="field">
        <label>Status</label>
        <select id="status">
          <option>WORKING</option>
          <option>DRAFT</option>
          <option>REC.</option>
          <option>PUB.</option>
        </select>
      </div>
    </div>
    <div class="right">
      <div class="field">
        <label>Model</label>
        <select id="modelSelect"></select>
      </div>
      <div class="field">
        <label>Router</label>
        <select id="routerSelect">
          <option value="ortho">Orthogonal</option>
          <option value="curvy">Curvy (non-FIPS)</option>
        </select>
      </div>
      <div class="buttons">
        <button id="btnAddBox">+ Function</button>
        <button id="btnOffPage">+ Off-page</button>
        <button id="btnExportJson">Export JSON</button>
        <button id="btnExportSvg">Export SVG</button>
        <button id="btnSave">Save</button>
        <button id="btnLoad">Load</button>
        <button id="btnClear">Clear</button>
      </div>
    </div>
  </header>

  <!-- Canvas -->
  <main class="canvas-wrap">
    <div class="grid"></div>
    <svg id="svg" class="canvas" xmlns="http://www.w3.org/2000/svg"></svg>
  </main>

  <!-- Bottom identification fields -->
  <footer class="bottombar">
    <div class="field"><label>Used At</label><input id="usedAt"/></div>
    <div class="field node"><label>Node</label><input id="node" placeholder="A0 / A1 / A12 ..."/></div>
    <div class="field title"><label>Title</label><input id="title" placeholder="Diagram title"/></div>
    <div class="field number">
      <div class="sub">
        <label>C-Number</label><input id="cnum" />
      </div>
      <div class="sub">
        <label>Page</label><input id="page" />
      </div>
    </div>
  </footer>

  <!-- Floating mini palette for labels -->
  <div class="label-editor" id="labelEditor">
    <input id="labelInput" />
    <div class="label-row">
      <select id="entityList"></select>
      <button id="btnLabelApply">Apply</button>
    </div>
  </div>

  <script src="app.js"></script>
</body>
</html>
"""

styles_css = """/* Reset-ish */
* { box-sizing: border-box; }
html, body { height: 100%; margin: 0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial; }

:root {
  --grid: 10px;
  --border: #111;
  --muted: #9ca3af;
  --handle: #cbd5e1;
  --handle-hover: #111;
  --handle-active: #fb923c; /* orange fill when active */
  --function-bg: #fff;
}

/* Top metadata bar */
.topbar, .bottombar {
  display: flex;
  justify-content: space-between;
  gap: .75rem;
  padding: .5rem .75rem;
  border-bottom: 2px solid #111;
  background: #fafafa;
}
.bottombar { border-top: 2px solid #111; border-bottom: none; }

.topbar .left, .topbar .right { display: flex; align-items: end; gap: .5rem; flex-wrap: wrap; }
.field { display: grid; gap: .25rem; }
.field label { font-size: .75rem; color: #374151; text-transform: uppercase; }
.field input, .field select { padding: .3rem .4rem; border: 1px solid #9ca3af; border-radius: .25rem; min-width: 8rem; }

.buttons { display: flex; gap: .4rem; }
button { border: 1px solid #111; background: #fff; padding: .35rem .6rem; border-radius: .35rem; cursor: pointer; }
button:active { transform: translateY(1px); }

/* Canvas */
.canvas-wrap { position: relative; height: calc(100vh - 164px);  /* rough: bars + paddings */ }
.grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(to right, #eee 1px, transparent 1px),
    linear-gradient(to bottom, #eee 1px, transparent 1px);
  background-size: var(--grid) var(--grid);
  pointer-events: none;
}
.canvas { position: absolute; inset: 0; width: 100%; height: 100%; }

/* Function Box */
.g-node { cursor: move; }
.node-box {
  fill: var(--function-bg); stroke: var(--border); stroke-width: 2px; rx: 0; ry: 0;
}
.node-name { font-weight: 700; font-size: 14px; }
.node-number { font-size: 12px; }
.handle {
  r: 6; fill: #fff; stroke: var(--handle); stroke-width: 2;
}
.handle:hover { stroke: var(--handle-hover); }
.handle.active { fill: var(--handle-active); stroke: var(--handle-hover); }

/* Edge and stub styling */
.edge-path { fill: none; stroke: #111; stroke-width: 2; }
.arrowhead { fill: #111; }
.stub { stroke: #111; stroke-width: 2; }
.stub-arrowhead { fill: #111; }

.edge-label, .stub-label { font-size: 12px; dominant-baseline: middle; user-select: none; }

/* Selection hints */
.selected .node-box { stroke-dasharray: 4 3; }

/* Label editor */
.label-editor {
  position: absolute; display: none; gap: .25rem;
  background: #fff; border: 1px solid #111; padding: .25rem; border-radius: .35rem;
  box-shadow: 0 6px 16px rgba(0,0,0,.15); z-index: 1000;
}
.label-editor .label-row { display: flex; gap: .25rem; }
"""

app_js = r"""/* IDEF0 Diagrammer — v0.3.3b
   - Orthogonal (FIPS-friendly) default routing with rounded 90° corners
   - Sticky stubs with axis-locked tails
   - Center handles I/C/O/M with hover/active states
   - Export/Import JSON and SVG
   - Simple off-page connector primitive
*/
const GRID = 10;

const state = {
  settings: { router: 'ortho', cornerRadius: 12, grid: GRID },
  nodes: [], // {id, kind:'function'|'offpage', x,y,w,h, name, number}
  edges: [], // normal edges {id,type:'normal', a:{nodeId,side,role}, b:{nodeId,side,role}, label}
  stubs: [], // stub edges {id,type:'stub', role, anchor:{nodeId,side,role}, axis:'x'|'y', offset, length, dir:1|-1, label}
  seq: 1,
  selection: null,
  activeHandle: null,
  entities: ['Capital','Contracts','Revenue','Orders','Products','Financing','Government Regulation','People & Roles']
};

function id() { return 'id'+(state.seq++); }

const svg = document.getElementById('svg');

function make(tag, attrs={}) {
  const el = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const k in attrs) el.setAttribute(k, attrs[k]);
  return el;
}

function snap(n) { return Math.round(n / GRID) * GRID; }

function handlePoints(node) {
  const cx = node.x + node.w/2;
  const cy = node.y + node.h/2;
  return {
    left: {x: node.x, y: cy},
    right:{x: node.x + node.w, y: cy},
    top:  {x: cx, y: node.y},
    bottom:{x: cx, y: node.y + node.h}
  };
}

// Routers
function routeOrtho(p0, p1, side0, side1, r=12) {
  const K = 20;
  const a = p0, b = p1;
  function lead(p, side) {
    if (side==='left')  return {x: p.x - K, y: p.y};
    if (side==='right') return {x: p.x + K, y: p.y};
    if (side==='top')   return {x: p.x, y: p.y - K};
    if (side==='bottom')return {x: p.x, y: p.y + K};
  }
  const pA = lead(a, side0); const pB = lead(b, side1);
  const mid = { x: (pA.x + pB.x)/2, y: (pA.y + pB.y)/2 };
  const seq = [a, pA, {x: mid.x, y: pA.y}, {x: mid.x, y: pB.y}, pB, b];
  for (let i=0;i<seq.length;i++){ seq[i].x=snap(seq[i].x); seq[i].y=snap(seq[i].y); }
  let d = `M ${seq[0].x} ${seq[0].y}`;
  for (let i=1;i<seq.length;i++) {
    const prev = seq[i-1], cur = seq[i], next = seq[i+1];
    if (next && ((prev.x===cur.x && cur.y!==next.y) || (prev.y===cur.y && cur.x!==next.x))) {
      let p1={x:cur.x,y:cur.y}, p2={x:cur.x,y:cur.y};
      if (prev.x===cur.x) { p1.y = cur.y - Math.sign(cur.y-prev.y)*r; p2.x = cur.x + Math.sign(next.x-cur.x)*r; }
      else { p1.x = cur.x - Math.sign(cur.x-prev.x)*r; p2.y = cur.y + Math.sign(next.y-cur.y)*r; }
      d += ` L ${p1.x} ${p1.y} Q ${cur.x} ${cur.y} ${p2.x} ${p2.y}`;
    } else {
      d += ` L ${cur.x} ${cur.y}`;
    }
  }
  return { svgPath: d };
}

function routeCurvy(p0, p1) {
  const m = (p0.x + p1.x)/2;
  const d = `M ${p0.x} ${p0.y} C ${m} ${p0.y}, ${m} ${p1.y}, ${p1.x} ${p1.y}`;
  return { svgPath: d };
}

function router(p0, p1, side0, side1) {
  return (document.getElementById('routerSelect').value === 'ortho')
    ? routeOrtho(p0, p1, side0, side1, state.settings.cornerRadius)
    : routeCurvy(p0, p1);
}

// Model ops
function addFunction(x, y) {
  const n = { id: id(), kind:'function', x:snap(x), y:snap(y), w:220, h:120, name:'Function', number:'A1' };
  state.nodes.push(n); render();
}
function addOffpage(x,y) {
  const n = { id: id(), kind:'offpage', x:snap(x), y:snap(y), w:40, h:40, name:'A#', number:'' };
  state.nodes.push(n); render();
}

function findNode(id){ return state.nodes.find(n=>n.id===id);}

function edgeFrom(handleA, handleBOrNull) {
  if (!handleBOrNull) return null;
  const {nodeId:aId, side:side0, role:role0} = handleA;
  const {nodeId:bId, side:side1, role:role1} = handleBOrNull;
  if (role0!=='O') return null;
  if (role1==='O') return null;
  const e = { id:id(), type:'normal',
    a:{nodeId:aId, side:side0, role:'O'},
    b:{nodeId:bId, side:side1, role:role1},
    label:''
  };
  state.edges.push(e);
  return e;
}

function stubFrom(handle, role) {
  const axis = (role==='I' || role==='O') ? 'x' : 'y';
  const dir = (role==='I' || role==='C') ? -1 : 1;
  const s = { id:id(), type:'stub', role:role, anchor:{nodeId:handle.nodeId, side:handle.side, role:role},
              axis, offset:0, length:80, dir, label:'' };
  state.stubs.push(s);
  return s;
}

// Rendering
const svgEl = document.getElementById('svg');
function clearSvg(){ while(svgEl.firstChild) svgEl.removeChild(svgEl.firstChild); }

function render() {
  clearSvg();
  const defs = make('defs');
  const ah = make('marker', {id:'arrow', viewBox:'0 0 10 10', refX:'10', refY:'5', markerWidth:'8', markerHeight:'8', orient:'auto-start-reverse'});
  ah.appendChild(make('path', {d:'M 0 0 L 10 5 L 0 10 z', class:'arrowhead'}));
  defs.appendChild(ah);
  svgEl.appendChild(defs);

  state.edges.forEach(e => drawEdge(e));
  state.stubs.forEach(s => drawStub(s));
  state.nodes.forEach(n => drawNode(n));
}

function drawNode(n) {
  const g = make('g', {class:'g-node', 'data-id':n.id});
  const rect = make('rect', {class:'node-box', x:n.x, y:n.y, width:n.w, height:n.h});
  g.appendChild(rect);

  const name = make('text', {class:'node-name', x:n.x + n.w/2, y:n.y + n.h/2, 'text-anchor':'middle'});
  name.textContent = n.name;
  g.appendChild(name);

  const num = make('text', {class:'node-number', x:n.x + n.w - 8, y:n.y + n.h - 6, 'text-anchor':'end'});
  num.textContent = n.number||'';
  g.appendChild(num);

  // Handles
  const hp = handlePoints(n);
  [
    {side:'left', role:'I', ...hp.left},
    {side:'top', role:'C', ...hp.top},
    {side:'right', role:'O', ...hp.right},
    {side:'bottom', role:'M', ...hp.bottom},
  ].forEach(h => {
    const c = make('circle', {class:'handle', cx:h.x, cy:h.y, r:6});
    c.dataset.nodeId = n.id; c.dataset.side = h.side; c.dataset.role = h.role;
    g.appendChild(c);
  });

  // Dragging
  let dragging = false, dx=0, dy=0;
  g.addEventListener('pointerdown', (ev)=>{
    if (ev.target.tagName==='circle') return;
    dragging = true; g.setPointerCapture(ev.pointerId);
    dx = ev.clientX - n.x; dy = ev.clientY - n.y;
  });
  g.addEventListener('pointermove', (ev)=>{
    if (!dragging) return;
    n.x = snap(ev.clientX - dx); n.y = snap(ev.clientY - dy);
    render();
  });
  g.addEventListener('pointerup', ()=> dragging=false);

  svgEl.appendChild(g);
}

function drawEdge(e) {
  const nA = findNode(e.a.nodeId), nB = findNode(e.b.nodeId);
  const pA = handlePoints(nA)[e.a.side];
  const pB = handlePoints(nB)[e.b.side];
  const {svgPath} = router(pA, pB, e.a.side, e.b.side);
  const path = make('path', {d:svgPath, class:'edge-path', 'marker-end':'url(#arrow)'});
  path.addEventListener('dblclick', (ev) => openLabelEditor(ev.clientX, ev.clientY, e));
  svgEl.appendChild(path);
  const lb = make('text', {class:'edge-label', x:(pA.x+pB.x)/2, y:(pA.y+pB.y)/2, 'text-anchor':'middle'});
  lb.textContent = e.label||'';
  svgEl.appendChild(lb);
}

function drawStub(s) {
  const node = findNode(s.anchor.nodeId);
  const p = handlePoints(node)[s.anchor.side];
  const free = {x:p.x, y:p.y};
  if (s.axis==='x') free.x += s.dir * s.length;
  else free.y += s.dir * s.length;

  const p1 = {x: snap(p.x), y: snap(p.y)};
  const p2 = {x: snap(free.x + (s.axis==='x' ? -6*s.dir : 0)), y: snap(free.y + (s.axis==='y' ? -6*s.dir : 0))};

  const line = make('line', {x1:p1.x, y1:p1.y, x2:p2.x, y2:p2.y, class:'stub'});
  svgEl.appendChild(line);

  let ahx, ahy, rot;
  if (s.role==='O') { 
    ahx = free.x; ahy = free.y; rot = (s.axis==='x' ? (s.dir>0?0:180) : (s.dir>0?90:270));
  } else {
    ahx = p.x; ahy = p.y; rot = (s.axis==='x' ? (s.dir>0?180:0) : (s.dir>0?270:90));
  }
  const ah = make('path', {d:'M 0 0 L 10 5 L 0 10 z', class:'stub-arrowhead',
    transform:`translate(${ahx} ${ahy}) rotate(${rot}) scale(0.8)`});
  svgEl.appendChild(ah);

  const lx = s.axis==='x' ? free.x + (s.dir>0?20:-20) : free.x;
  const ly = s.axis==='y' ? free.y + (s.dir>0?16:-16) : free.y;
  const lbl = make('text', {class:'stub-label', x: lx, y: ly, 'text-anchor': s.axis==='x' ? (s.dir>0?'start':'end') : 'middle'});
  lbl.textContent = s.label||'';
  lbl.addEventListener('dblclick', (ev)=> openLabelEditor(ev.clientX, ev.clientY, s));
  svgEl.appendChild(lbl);
}

// Handle interactions
svgEl.addEventListener('pointerdown', (ev) => {
  const t = ev.target;
  if (t.classList.contains('handle')) {
    document.querySelectorAll('.handle').forEach(h => h.classList.remove('active'));
    t.classList.add('active');
    state.activeHandle = { nodeId: t.dataset.nodeId, side: t.dataset.side, role: t.dataset.role };
  }
});

svgEl.addEventListener('pointerup', (ev) => {
  const t = ev.target;
  if (state.activeHandle && t.classList.contains('handle')) {
    const from = state.activeHandle;
    const to = { nodeId: t.dataset.nodeId, side: t.dataset.side, role: t.dataset.role };
    const e = edgeFrom(from, to);
    if (e) render();
    state.activeHandle = null;
    document.querySelectorAll('.handle').forEach(h => h.classList.remove('active'));
  }
});

document.addEventListener('keydown', (ev) => {
  if (ev.key.toLowerCase()==='s' && state.activeHandle) {
    stubFrom(state.activeHandle, state.activeHandle.role);
    render();
  }
});

// Labels
const labelEditor = document.getElementById('labelEditor');
const labelInput = document.getElementById('labelInput');
const entityList = document.getElementById('entityList');
const btnApply = document.getElementById('btnLabelApply');
let editingTarget = null;

function openLabelEditor(x, y, target) {
  editingTarget = target;
  labelInput.value = target.label || '';
  labelEditor.style.left = (x+8)+'px';
  labelEditor.style.top  = (y+8)+'px';
  labelEditor.style.display = 'grid';
  labelInput.focus();
}
btnApply.addEventListener('click', ()=>{
  const v = labelInput.value || entityList.value || '';
  if (editingTarget) editingTarget.label = v;
  labelEditor.style.display='none';
  render();
});
function refreshEntityList() {
  entityList.innerHTML = '<option value="">(choose)</option>' + state.entities.map(e => `<option>${e}</option>`).join('');
}

// Save/Load/Export
function exportJSON() {
  const data = { settings: state.settings, nodes: state.nodes, edges: state.edges, stubs: state.stubs };
  const str = JSON.stringify(data, null, 2);
  download('diagram.json', str, 'application/json');
}
function importJSON(str) {
  try {
    const d = JSON.parse(str);
    Object.assign(state.settings, d.settings||{});
    state.nodes = d.nodes||[]; state.edges=d.edges||[]; state.stubs=d.stubs||[];
    render();
  } catch(e) { alert('Invalid JSON'); }
}
function exportSVG() {
  const clone = svgEl.cloneNode(true);
  clone.removeAttribute('style');
  const xml = new XMLSerializer().serializeToString(clone);
  download('diagram.svg', xml, 'image/svg+xml');
}
function download(filename, data, mime) {
  const a = document.createElement('a');
  a.href = 'data:'+mime+';charset=utf-8,' + encodeURIComponent(data);
  a.download = filename;
  a.click();
}
document.getElementById('btnExportJson').onclick = exportJSON;
document.getElementById('btnExportSvg').onclick = exportSVG;
document.getElementById('btnSave').onclick = ()=>{
  localStorage.setItem('idef0_v033b', JSON.stringify({settings:state.settings,nodes:state.nodes,edges:state.edges,stubs:state.stubs}));
};
document.getElementById('btnLoad').onclick = ()=>{
  const v = localStorage.getItem('idef0_v033b'); if (!v) return;
  importJSON(v);
};
document.getElementById('btnClear').onclick = ()=>{ state.nodes=[]; state.edges=[]; state.stubs=[]; render(); };
document.getElementById('btnAddBox').onclick = ()=> addFunction(120,120);
document.getElementById('btnOffPage').onclick= ()=> addOffpage(80,80);
document.getElementById('routerSelect').onchange = ()=> render();

// Model dropdown sample loader
async function loadModels() {
  try {
    const res = await fetch('sample_models.json');
    const data = await res.json();
    const sel = document.getElementById('modelSelect');
    sel.innerHTML = data.models.map(m=>`<option value="${m.id}">${m.name}</option>`).join('');
    sel.onchange = ()=> {
      const found = data.models.find(x=>x.id===sel.value);
      if (found && found.diagram) importJSON(JSON.stringify(found.diagram));
    };
    if (data.models[0]) sel.value = data.models[0].id, sel.onchange();
  } catch(e) {
    console.warn('Failed to load sample models', e);
  }
}

// Init
(function init(){
  document.getElementById('date').valueAsDate = new Date();
  refreshEntityList();
  // Seed
  addFunction(200, 180);
  addFunction(520, 180);
  const n1 = state.nodes[0], n2 = state.nodes[1];
  edgeFrom({nodeId:n1.id, side:'right', role:'O'}, {nodeId:n2.id, side:'left', role:'I'});
  state.stubs.push({id:id(), type:'stub', role:'C', anchor:{nodeId:n1.id, side:'top', role:'C'}, axis:'y', offset:0, length:80, dir:-1, label:'Regulation'});
  state.stubs.push({id:id(), type:'stub', role:'M', anchor:{nodeId:n2.id, side:'bottom', role:'M'}, axis:'y', offset:0, length:80, dir:1, label:'People'});
  render();
  loadModels();
})();
"""

sample_models = {
  "models":[
    {"id":"demo1","name":"Demo: Two-Box","diagram":{
      "settings":{"router":"ortho","cornerRadius":12,"grid":10},
      "nodes":[
        {"id":"id1","kind":"function","x":200,"y":180,"w":220,"h":120,"name":"Governance","number":"A1"},
        {"id":"id2","kind":"function","x":520,"y":180,"w":220,"h":120,"name":"Production","number":"A2"}
      ],
      "edges":[
        {"id":"e1","type":"normal","a":{"nodeId":"id1","side":"right","role":"O"},"b":{"nodeId":"id2","side":"left","role":"I"},"label":"Orders"}
      ],
      "stubs":[
        {"id":"s1","type":"stub","role":"C","anchor":{"nodeId":"id1","side":"top","role":"C"},"axis":"y","offset":0,"length":80,"dir":-1,"label":"Govt Regulation"},
        {"id":"s2","type":"stub","role":"M","anchor":{"nodeId":"id2","side":"bottom","role":"M"},"axis":"y","offset":0,"length":80,"dir":1,"label":"People"}
      ]
    }}
  ]
}

schema_patch_sql = """-- Snowflake patch to align with the UI data model
CREATE OR REPLACE TABLE IF NOT EXISTS DIAGRAMS (
  DIAGRAM_ID NUMBER(38,0) PRIMARY KEY,
  MODEL_ID NUMBER(38,0) NOT NULL,
  NODE VARCHAR(32) NOT NULL,
  TITLE VARCHAR(255),
  AUTHOR VARCHAR(255),
  STATUS VARCHAR(32),
  CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
  UPDATED_AT TIMESTAMP_NTZ
);

ALTER TABLE IF EXISTS FUNCTIONS ADD COLUMN IF NOT EXISTS X NUMBER(10,0);
ALTER TABLE IF EXISTS FUNCTIONS ADD COLUMN IF NOT EXISTS Y NUMBER(10,0);
ALTER TABLE IF EXISTS FUNCTIONS ADD COLUMN IF NOT EXISTS W NUMBER(10,0);
ALTER TABLE IF EXISTS FUNCTIONS ADD COLUMN IF NOT EXISTS H NUMBER(10,0);
ALTER TABLE IF EXISTS FUNCTIONS ADD COLUMN IF NOT EXISTS BOX_NUMBER VARCHAR(8);
ALTER TABLE IF EXISTS FUNCTIONS ADD COLUMN IF NOT EXISTS KIND VARCHAR(20) DEFAULT 'FUNCTION';

CREATE OR REPLACE TABLE IF NOT EXISTS CONNECTORS (
  CONNECTOR_ID NUMBER(38,0) PRIMARY KEY,
  MODEL_ID NUMBER(38,0) NOT NULL,
  A_FUNCTION_ID NUMBER(38,0) NOT NULL,
  A_SIDE VARCHAR(10) NOT NULL,
  A_ROLE VARCHAR(2) NOT NULL,
  B_FUNCTION_ID NUMBER(38,0) NOT NULL,
  B_SIDE VARCHAR(10) NOT NULL,
  B_ROLE VARCHAR(2) NOT NULL,
  LABEL VARCHAR(255)
);

CREATE OR REPLACE TABLE IF NOT EXISTS STUBS (
  STUB_ID NUMBER(38,0) PRIMARY KEY,
  MODEL_ID NUMBER(38,0) NOT NULL,
  FUNCTION_ID NUMBER(38,0) NOT NULL,
  SIDE VARCHAR(10) NOT NULL,
  ROLE VARCHAR(2) NOT NULL,
  AXIS VARCHAR(1) NOT NULL,
  OFFSET NUMBER(10,0) DEFAULT 0,
  LENGTH NUMBER(10,0) DEFAULT 80,
  DIR NUMBER(2,0) DEFAULT 1,
  LABEL VARCHAR(255),
  TUNNEL_STATUS VARCHAR(50) DEFAULT 'NONE',
  ICOM_CODE VARCHAR(8)
);

CREATE OR REPLACE TABLE IF NOT EXISTS ENTITY_CATALOG (
  ENTITY_ID NUMBER(38,0) PRIMARY KEY,
  ENTITY_NAME VARCHAR(255) NOT NULL UNIQUE
);
"""

readme_md = """# IDEF0 Diagrammer — v0.3.3b

Baseline rollback with hard orthogonal routing and sticky stubs.

- Open `index.html` in a browser.
- Click a handle, press **S** to add a stub.
- Double-click a connector/stub label to edit (or pick from the dropdown).
- Save/Load uses localStorage. Export JSON & SVG are built-in.

Files: `index.html`, `styles.css`, `app.js`, `sample_models.json`, `schema_patch.sql`, `streamlit_idef0_page.py`.
"""

streamlit_py = """import streamlit as st
st.set_page_config(layout='wide', page_title='IDEF0 Diagrammer v0.3.3b')
st.title('IDEF0 Diagrammer v0.3.3b')

def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

html = read('index.html').replace('href="styles.css"', '<style>'+read('styles.css')+'</style>') \
                         .replace('<script src="app.js"></script>', '<script>'+read('app.js')+'</script>')
st.components.v1.html(html, height=800, scrolling=True)
"""

# write files
open(os.path.join(root,"index.html"),"w",encoding="utf-8").write(index_html)
open(os.path.join(root,"styles.css"),"w",encoding="utf-8").write(styles_css)
open(os.path.join(root,"app.js"),"w",encoding="utf-8").write(app_js)
open(os.path.join(root,"sample_models.json"),"w",encoding="utf-8").write(json.dumps(sample_models, indent=2))
open(os.path.join(root,"schema_patch.sql"),"w",encoding="utf-8").write(schema_patch_sql)
open(os.path.join(root,"README.md"),"w",encoding="utf-8").write(readme_md)
open(os.path.join(root,"streamlit_idef0_page.py"),"w",encoding="utf-8").write(streamlit_py)

# zip it for convenience
zip_path = os.path.join(os.path.dirname(__file__), PROJECT + ".zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for p in pathlib.Path(root).rglob("*"):
        z.write(str(p), arcname=str(p.relative_to(root)))

print("Wrote:", root)
print("Zip:", zip_path)
