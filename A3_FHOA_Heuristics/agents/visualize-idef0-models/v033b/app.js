/* IDEF0 Diagrammer — v0.3.3b (hotfix-2)
   - Two-click: select source handle, then click target OR press S for stub
   - ESC cancels selection
   - Stub arrowheads via markers (no distortion)
*/
const GRID = 10;

const state = {
  settings: { router: 'ortho', cornerRadius: 12, grid: GRID },
  nodes: [], // {id, kind:'function'|'offpage', x,y,w,h, name, number}
  edges: [], // {id,type:'normal', a:{nodeId,side,role}, b:{nodeId,side,role}, label}
  stubs: [], // {id,type:'stub', role, anchor:{nodeId,side,role}, axis:'x'|'y', offset, length, dir:1|-1, label}
  seq: 1,
  activeHandle: null,
  entities: ['Capital','Contracts','Revenue','Orders','Products','Financing','Government Regulation','People & Roles']
};

function newid(p="id"){ return p + (state.seq++); }
function snap(n){ return Math.round(n/GRID)*GRID; }

const svg = document.getElementById('svg');
function make(tag, attrs={}){ const el = document.createElementNS('http://www.w3.org/2000/svg', tag); for (const k in attrs) el.setAttribute(k, attrs[k]); return el; }
const isHandle = el => !!(el && el.classList && el.classList.contains('handle'));

function handlePoints(node){
  if (node.kind === 'offpage') {
    const cx = node.x + 28, cy = node.y + 28;
    return {
      left:   {x: cx-28, y: cy},
      right:  {x: cx+28, y: cy},
      top:    {x: cx,    y: cy-28},
      bottom: {x: cx,    y: cy+28}
    };
  }
  const cx = node.x + node.w/2;
  const cy = node.y + node.h/2;
  return {
    left:   {x: node.x,        y: cy},
    right:  {x: node.x+node.w, y: cy},
    top:    {x: cx,            y: node.y},
    bottom: {x: cx,            y: node.y+node.h}
  };
}

// ---------- Routers ----------
function routeOrtho(p0, p1, side0, side1, r=12){
  const K = 20;
  const lead = (p, side) => side==='left' ? {x:p.x-K,y:p.y}
                     : side==='right' ? {x:p.x+K,y:p.y}
                     : side==='top' ? {x:p.x,y:p.y-K}
                     : {x:p.x,y:p.y+K};
  const pA = lead(p0, side0), pB = lead(p1, side1);
  const mid = {x:(pA.x+pB.x)/2, y:(pA.y+pB.y)/2};
  const pts = [p0, pA, {x:mid.x,y:pA.y}, {x:mid.x,y:pB.y}, pB, p1]
    .map(p=>({x:snap(p.x), y:snap(p.y)}));
  let d = `M ${pts[0].x} ${pts[0].y}`;
  for (let i=1;i<pts.length;i++){
    const a=pts[i-1], b=pts[i], c=pts[i+1];
    if (c && ((a.x===b.x && b.y!==c.y) || (a.y===b.y && b.x!==c.x))){
      let p1={x:b.x,y:b.y}, p2={x:b.x,y:b.y};
      if (a.x===b.x){ p1.y=b.y-Math.sign(b.y-a.y)*r; p2.x=b.x+Math.sign(c.x-b.x)*r; }
      else          { p1.x=b.x-Math.sign(b.x-a.x)*r; p2.y=b.y+Math.sign(c.y-b.y)*r; }
      d += ` L ${p1.x} ${p1.y} Q ${b.x} ${b.y} ${p2.x} ${p2.y}`;
    } else d += ` L ${b.x} ${b.y}`;
  }
  return d;
}
function routeCurvy(p0,p1){ const m=(p0.x+p1.x)/2; return `M ${p0.x} ${p0.y} C ${m} ${p0.y}, ${m} ${p1.y}, ${p1.x} ${p1.y}`; }
function route(p0,p1,s0,s1){ return (document.getElementById('routerSelect').value==='ortho') ? routeOrtho(p0,p1,s0,s1,12) : routeCurvy(p0,p1); }

// ---------- Model ops ----------
function addFunction(x,y){
  state.nodes.push({ id:newid('n'), kind:'function', x:snap(x), y:snap(y), w:220, h:120, name:'Function', number:'A1' });
  render();
}
function addOffpage(x,y){
  state.nodes.push({ id:newid('o'), kind:'offpage', x:snap(x), y:snap(y), w:56, h:56, name:'OFF-PAGE', number:'' });
  render();
}
const nodeById = id => state.nodes.find(n=>n.id===id);

function makeEdge(from, to){
  if (!from || !to) return null;
  if (from.role!=='O' || to.role==='O') return null; // O → I/C/M
  const e = { id:newid('e'), type:'normal',
    a:{nodeId:from.nodeId, side:from.side, role:'O'},
    b:{nodeId:to.nodeId,   side:to.side,   role:to.role},
    label:'' };
  state.edges.push(e);
  return e;
}
function makeStub(handle){
  const role = handle.role;
  const axis = (role==='I'||role==='O')?'x':'y';
  const dir  = (role==='I'||role==='C')?-1:1; // I/C into box, O/M away
  const s = { id:newid('s'), type:'stub', role,
    anchor:{nodeId:handle.nodeId, side:handle.side, role},
    axis, offset:0, length:80, dir, label:'' };
  state.stubs.push(s);
  return s;
}

// ---------- Rendering ----------
function clearSvg(){ while(svg.firstChild) svg.removeChild(svg.firstChild); }
function appendDefs(){
  const defs = make('defs');
  const m = make('marker',{id:'arrow',viewBox:'0 0 10 10',refX:'10',refY:'5',markerWidth:'8',markerHeight:'8',orient:'auto-start-reverse'});
  m.appendChild(make('path',{d:'M 0 0 L 10 5 L 0 10 z',class:'arrowhead'}));
  defs.appendChild(m);
  svg.appendChild(defs);
}

function drawNode(n){
  const g = make('g', {'data-id':n.id, class:'g-node'});

  if (n.kind==='offpage'){
    const cx = n.x + 28, cy = n.y + 28, r = 28;
    g.appendChild(make('circle', {cx, cy, r, fill:'#fff', stroke:'#64748b', 'stroke-width':2, 'stroke-dasharray':'4 4'}));
    const t = make('text', {x:cx, y:cy, 'text-anchor':'middle', 'dominant-baseline':'middle', 'font-size':10, fill:'#334155'});
    t.textContent = 'OFF-PAGE'; g.appendChild(t);
  } else {
    g.appendChild(make('rect', {class:'node-box', x:n.x, y:n.y, width:n.w, height:n.h}));
    const name = make('text', {class:'node-name', x:n.x+n.w/2, y:n.y+n.h/2, 'text-anchor':'middle'}); name.textContent = n.name; g.appendChild(name);
    const num  = make('text', {class:'node-number', x:n.x+n.w-8, y:n.y+n.h-6, 'text-anchor':'end'}); num.textContent = n.number||''; g.appendChild(num);
  }

  // handles
  const hp = handlePoints(n);
  [
    {side:'left', role:'I', ...hp.left},
    {side:'top', role:'C', ...hp.top},
    {side:'right', role:'O', ...hp.right},
    {side:'bottom', role:'M', ...hp.bottom},
  ].forEach(h=>{
    const c = make('circle',{class:'handle', cx:h.x, cy:h.y, r:6});
    c.dataset.nodeId=n.id; c.dataset.side=h.side; c.dataset.role=h.role;
    g.appendChild(c);
  });

  // drag (ignores clicks on handles)
  let dragging=false, dx=0, dy=0;
  g.addEventListener('pointerdown', (ev)=>{
    if (isHandle(ev.target)) return;
    dragging=true; dx=ev.clientX-n.x; dy=ev.clientY-n.y;
    window.addEventListener('pointermove', onMove);
    window.addEventListener('pointerup', onUp, {once:true});
  });
  function onMove(ev){ if(!dragging) return; n.x=snap(ev.clientX-dx); n.y=snap(ev.clientY-dy); render(); }
  function onUp(){ dragging=false; window.removeEventListener('pointermove', onMove); }

  svg.appendChild(g);
}

function drawEdge(e){
  const A=nodeById(e.a.nodeId), B=nodeById(e.b.nodeId); if(!A||!B) return;
  const pA=handlePoints(A)[e.a.side], pB=handlePoints(B)[e.b.side];
  const d=route(pA,pB,e.a.side,e.b.side);
  const path=make('path',{d, class:'edge-path','marker-end':'url(#arrow)'}); svg.appendChild(path);
  const lbl=make('text',{class:'edge-label', x:(pA.x+pB.x)/2, y:(pA.y+pB.y)/2, 'text-anchor':'middle'}); lbl.textContent=e.label||''; svg.appendChild(lbl);
}

function drawStub(s){
  const N=nodeById(s.anchor.nodeId); if(!N) return;
  const p=handlePoints(N)[s.anchor.side]; const free={x:p.x,y:p.y};
  if(s.axis==='x') free.x += s.dir*s.length; else free.y += s.dir*s.length;

  let x1,y1,x2,y2;
  if (s.role==='O'){ // outward → arrow at free end
    x1=p.x; y1=p.y; x2=free.x; y2=free.y;
  } else {          // I/C/M → arrow at box end
    x1=free.x; y1=free.y; x2=p.x; y2=p.y;
  }
  const line = make('line', {x1:snap(x1), y1:snap(y1), x2:snap(x2), y2:snap(y2), class:'stub'});
  line.setAttribute('marker-end','url(#arrow)');
  svg.appendChild(line);

  const lx = s.axis==='x' ? free.x + (s.dir>0?20:-20) : free.x;
  const ly = s.axis==='y' ? free.y + (s.dir>0?16:-16) : free.y;
  const lbl=make('text',{class:'stub-label', x:lx, y:ly, 'text-anchor': s.axis==='x' ? (s.dir>0?'start':'end') : 'middle'}); lbl.textContent=s.label||''; svg.appendChild(lbl);
}

function render(){
  clearSvg(); appendDefs();
  state.edges.forEach(drawEdge);
  state.stubs.forEach(drawStub);
  state.nodes.forEach(drawNode);
}

// ---------- Two-click handle interactions ----------
svg.addEventListener('click', (ev)=>{
  if (!isHandle(ev.target)) return;
  const clicked = { nodeId: ev.target.dataset.nodeId, side: ev.target.dataset.side, role: ev.target.dataset.role };

  // If nothing active → activate this one
  if (!state.activeHandle) {
    document.querySelectorAll('.handle').forEach(h=>h.classList.remove('active'));
    ev.target.classList.add('active');
    state.activeHandle = clicked;
    return;
  }

  // Clicking the same handle toggles off
  if (state.activeHandle.nodeId===clicked.nodeId && state.activeHandle.side===clicked.side) {
    ev.target.classList.remove('active');
    state.activeHandle = null;
    return;
  }

  // Otherwise, attempt to connect (O → I/C/M)
  const e = makeEdge(state.activeHandle, clicked);
  if (e) {
    state.activeHandle = null;
    document.querySelectorAll('.handle').forEach(h=>h.classList.remove('active'));
    render();
  } else {
    // keep selection; user can press S to stub or click a different target
  }
});

// S = stub from active handle; ESC = cancel
document.addEventListener('keydown', (ev)=>{
  const k = ev.key.toLowerCase();
  if (k==='s' && state.activeHandle) { makeStub(state.activeHandle); render(); }
  if (k==='escape') {
    state.activeHandle = null;
    document.querySelectorAll('.handle').forEach(h=>h.classList.remove('active'));
  }
});

// ---------- Top bar ----------
document.getElementById('btnAddBox').onclick = ()=> addFunction(160+Math.random()*360, 160+Math.random()*200);
document.getElementById('btnOffPage').onclick= ()=> addOffpage(80+Math.random()*120, 80+Math.random()*120);
document.getElementById('btnClear').onclick   = ()=>{ state.nodes=[]; state.edges=[]; state.stubs=[]; render(); };
document.getElementById('btnExportJson').onclick = ()=>{ const data={settings:state.settings,nodes:state.nodes,edges:state.edges,stubs:state.stubs}; const a=document.createElement('a'); a.href='data:application/json;charset=utf-8,'+encodeURIComponent(JSON.stringify(data,null,2)); a.download='diagram.json'; a.click(); };
document.getElementById('btnExportSvg').onclick  = ()=>{ const clone=svg.cloneNode(true); clone.removeAttribute('style'); const a=document.createElement('a'); a.href='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(new XMLSerializer().serializeToString(clone)); a.download='diagram.svg'; a.click(); };
document.getElementById('btnSave').onclick = ()=> localStorage.setItem('idef0_v033b', JSON.stringify({settings:state.settings,nodes:state.nodes,edges:state.edges,stubs:state.stubs}));
document.getElementById('btnLoad').onclick = ()=>{ const v=localStorage.getItem('idef0_v033b'); if(v){ const d=JSON.parse(v); Object.assign(state.settings,d.settings||{}); state.nodes=d.nodes||[]; state.edges=d.edges||[]; state.stubs=d.stubs||[]; render(); } };
document.getElementById('routerSelect').onchange = ()=> render();

// ---------- Seed ----------
(function init(){
  addFunction(200,180);
  addFunction(520,180);
  const n1=state.nodes[0], n2=state.nodes[1];
  makeEdge({nodeId:n1.id,side:'right',role:'O'},{nodeId:n2.id,side:'left',role:'I'});
  state.stubs.push({id:newid('s'), type:'stub', role:'C', anchor:{nodeId:n1.id, side:'top', role:'C'}, axis:'y', offset:0, length:80, dir:-1, label:'Regulation'});
  state.stubs.push({id:newid('s'), type:'stub', role:'M', anchor:{nodeId:n2.id, side:'bottom', role:'M'}, axis:'y', offset:0, length:80, dir:1,  label:'People'});
  render();
})();
