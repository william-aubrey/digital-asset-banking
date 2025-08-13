/* IDEF0 Diagrammer — v0.3.3b
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
