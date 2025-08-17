/* IDEF0 Diagrammer — v0.3.3b (hotfix-3)
   - Solid two-click workflow
   - Selection resets after stub/edge
   - Invalid connect switches selection to the clicked handle
   - Esc clears selection
   - Highlight persists across re-renders
*/
const GRID = 10;

const state = {
  settings: { router: 'ortho', cornerRadius: 12, grid: GRID },
  nodes: [],
  edges: [],
  stubs: [],
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
    return { left:{x:cx-28,y:cy}, right:{x:cx+28,y:cy}, top:{x:cx,y:cy-28}, bottom:{x:cx,y:cy+28} };
  }
  const cx = node.x + node.w/2, cy = node.y + node.h/2;
  return { left:{x:node.x,y:cy}, right:{x:node.x+node.w,y:cy}, top:{x:cx,y:node.y}, bottom:{x:cx,y:node.y+node.h} };
}

// ---------- Router ----------
function routeOrtho(p0,p1,side0,side1,r=12){
  const K=20, lead=(p,s)=>s==='left'?{x:p.x-K,y:p.y}:s==='right'?{x:p.x+K,y:p.y}:s==='top'?{x:p.x,y:p.y-K}:{x:p.x,y:p.y+K};
  const pA=lead(p0,side0), pB=lead(p1,side1), mid={x:(pA.x+pB.x)/2, y:(pA.y+pB.y)/2};
  const pts=[p0,pA,{x:mid.x,y:pA.y},{x:mid.x,y:pB.y},pB,p1].map(p=>({x:snap(p.x),y:snap(p.y)}));
  let d=`M ${pts[0].x} ${pts[0].y}`;
  for(let i=1;i<pts.length;i++){const a=pts[i-1],b=pts[i],c=pts[i+1];
    if(c&&((a.x===b.x&&b.y!==c.y)||(a.y===b.y&&b.x!==c.x))){
      let p1={x:b.x,y:b.y},p2={x:b.x,y:b.y};
      if(a.x===b.x){p1.y=b.y-Math.sign(b.y-a.y)*r; p2.x=b.x+Math.sign(c.x-b.x)*r;}
      else{p1.x=b.x-Math.sign(b.x-a.x)*r; p2.y=b.y+Math.sign(c.y-b.y)*r;}
      d+=` L ${p1.x} ${p1.y} Q ${b.x} ${b.y} ${p2.x} ${p2.y}`;
    } else d+=` L ${b.x} ${b.y}`;
  }
  return d;
}
function routeCurvy(p0,p1){ const m=(p0.x+p1.x)/2; return `M ${p0.x} ${p0.y} C ${m} ${p0.y}, ${m} ${p1.y}, ${p1.x} ${p1.y}`; }
function route(p0,p1,s0,s1){ return (document.getElementById('routerSelect').value==='ortho') ? routeOrtho(p0,p1,s0,s1,12) : routeCurvy(p0,p1); }

// ---------- Model ----------
function addFunction(x,y){ state.nodes.push({ id:newid('n'), kind:'function', x:snap(x), y:snap(y), w:220, h:120, name:'Function', number:'A1' }); render(); }
function addOffpage(x,y){ state.nodes.push({ id:newid('o'), kind:'offpage', x:snap(x), y:snap(y), w:56, h:56, name:'OFF-PAGE', number:'' }); render(); }
const nodeById = id => state.nodes.find(n=>n.id===id);

function makeEdge(from,to){
  if(!from||!to) return null;
  if(from.role!=='O' || to.role==='O') return null; // O → I/C/M only
  const e={ id:newid('e'), type:'normal',
    a:{nodeId:from.nodeId, side:from.side, role:'O'},
    b:{nodeId:to.nodeId,   side:to.side,   role:to.role},
    label:'' };
  state.edges.push(e); return e;
}
function makeStub(handle){
  const role=handle.role, axis=(role==='I'||role==='O')?'x':'y', dir=(role==='I'||role==='C')?-1:1;
  const s={ id:newid('s'), type:'stub', role,
    anchor:{nodeId:handle.nodeId, side:handle.side, role},
    axis, offset:0, length:80, dir, label:'' };
  state.stubs.push(s); return s;
}

// ---------- Selection helpers ----------
function setActiveHandle(h){
  state.activeHandle = h;
  // wipe highlights
  document.querySelectorAll('.handle').forEach(el=>el.classList.remove('active'));
  // restore if any
  if (!h) return;
  const sel = `.handle[data-node-id="${h.nodeId}"][data-side="${h.side}"]`;
  const el = svg.querySelector(sel);
  if (el) el.classList.add('active');
}

// ---------- Rendering ----------
function clearSvg(){ while(svg.firstChild) svg.removeChild(svg.firstChild); }
function appendDefs(){
  const defs = make('defs');
  const m = make('marker',{id:'arrow',viewBox:'0 0 10 10',refX:'10',refY:'5',markerWidth:'8',markerHeight:'8',orient:'auto-start-reverse'});
  m.appendChild(make('path',{d:'M 0 0 L 10 5 L 0 10 z',class:'arrowhead'}));
  defs.appendChild(m); svg.appendChild(defs);
}
function drawNode(n){
  const g = make('g', {'data-id':n.id, class:'g-node'});
  if (n.kind==='offpage'){
    const cx=n.x+28, cy=n.y+28, r=28;
    g.appendChild(make('circle',{cx,cy,r,fill:'#fff',stroke:'#64748b','stroke-width':2,'stroke-dasharray':'4 4'}));
    const t=make('text',{x:cx,y:cy,'text-anchor':'middle','dominant-baseline':'middle','font-size':10,fill:'#334155'}); t.textContent='OFF-PAGE'; g.appendChild(t);
  } else {
    g.appendChild(make('rect',{class:'node-box',x:n.x,y:n.y,width:n.w,height:n.h}));
    const name=make('text',{class:'node-name',x:n.x+n.w/2,y:n.y+n.h/2,'text-anchor':'middle'}); name.textContent=n.name; g.appendChild(name);
    const num=make('text',{class:'node-number',x:n.x+n.w-8,y:n.y+n.h-6,'text-anchor':'end'}); num.textContent=n.number||''; g.appendChild(num);
  }
  const hp=handlePoints(n);
  [{side:'left',role:'I',...hp.left},{side:'top',role:'C',...hp.top},{side:'right',role:'O',...hp.right},{side:'bottom',role:'M',...hp.bottom}]
    .forEach(h=>{ const c=make('circle',{class:'handle',cx:h.x,cy:h.y,r:6}); c.dataset.nodeId=n.id; c.dataset.side=h.side; c.dataset.role=h.role; g.appendChild(c); });
  // Drag (ignore handle clicks)
  let dragging=false,dx=0,dy=0;
  g.addEventListener('pointerdown',ev=>{ if(isHandle(ev.target)) return; dragging=true; dx=ev.clientX-n.x; dy=ev.clientY-n.y;
    window.addEventListener('pointermove',onMove); window.addEventListener('pointerup',onUp,{once:true}); });
  function onMove(ev){ if(!dragging) return; n.x=snap(ev.clientX-dx); n.y=snap(ev.clientY-dy); render(); }
  function onUp(){ dragging=false; window.removeEventListener('pointermove',onMove); }
  svg.appendChild(g);
}
function drawEdge(e){
  const A=nodeById(e.a.nodeId), B=nodeById(e.b.nodeId); if(!A||!B) return;
  const pA=handlePoints(A)[e.a.side], pB=handlePoints(B)[e.b.side];
  const d=route(pA,pB,e.a.side,e.b.side);
  svg.appendChild(make('path',{d, class:'edge-path','marker-end':'url(#arrow)'}));
  svg.appendChild(make('text',{class:'edge-label',x:(pA.x+pB.x)/2,y:(pA.y+pB.y)/2,'text-anchor':'middle'})).textContent=e.label||'';
}
function drawStub(s){
  const N=nodeById(s.anchor.nodeId); if(!N) return;
  const p=handlePoints(N)[s.anchor.side], free={x:p.x,y:p.y}; if(s.axis==='x') free.x += s.dir*s.length; else free.y += s.dir*s.length;
  let x1,y1,x2,y2; if(s.role==='O'){x1=p.x;y1=p.y;x2=free.x;y2=free.y;} else {x1=free.x;y1=free.y;x2=p.x;y2=p.y;}
  const line=make('line',{x1:snap(x1),y1:snap(y1),x2:snap(x2),y2:snap(y2),class:'stub'}); line.setAttribute('marker-end','url(#arrow)'); svg.appendChild(line);
  const lx=s.axis==='x'? free.x+(s.dir>0?20:-20):free.x, ly=s.axis==='y'? free.y+(s.dir>0?16:-16):free.y;
  svg.appendChild(make('text',{class:'stub-label',x:lx,y:ly,'text-anchor': s.axis==='x'?(s.dir>0?'start':'end'):'middle'})).textContent=s.label||'';
}
function render(){
  clearSvg(); appendDefs();
  state.edges.forEach(drawEdge);
  state.stubs.forEach(drawStub);
  state.nodes.forEach(drawNode);
  // restore selection highlight, if any
  setActiveHandle(state.activeHandle);
}

// ---------- Two-click interactions ----------
svg.addEventListener('click', ev=>{
  if (!isHandle(ev.target)) return;
  const clicked = { nodeId: ev.target.dataset.nodeId, side: ev.target.dataset.side, role: ev.target.dataset.role };

  // nothing active → activate
  if (!state.activeHandle) { setActiveHandle(clicked); return; }

  // same handle → deselect
  if (state.activeHandle.nodeId===clicked.nodeId && state.activeHandle.side===clicked.side) { setActiveHandle(null); return; }

  // try to connect; if invalid, switch selection to the clicked handle
  const edge = makeEdge(state.activeHandle, clicked);
  if (edge) { render(); setActiveHandle(null); }
  else { setActiveHandle(clicked); }
});

// S = stub; Esc = cancel
document.addEventListener('keydown', ev=>{
  const k = ev.key.toLowerCase();
  if (k==='s' && state.activeHandle) { makeStub(state.activeHandle); render(); setActiveHandle(null); }
  if (k==='escape') setActiveHandle(null);
});

// ---------- Top bar ----------
document.getElementById('btnAddBox').onclick = ()=> addFunction(160+Math.random()*360, 160+Math.random()*200);
document.getElementById('btnOffPage').onclick= ()=> addOffpage(80+Math.random()*120, 80+Math.random()*120);
document.getElementById('btnClear').onclick   = ()=>{ state.nodes=[]; state.edges=[]; state.stubs=[]; render(); setActiveHandle(null); };
document.getElementById('btnExportJson').onclick = ()=>{ const data={settings:state.settings,nodes:state.nodes,edges:state.edges,stubs:state.stubs}; const a=document.createElement('a'); a.href='data:application/json;charset=utf-8,'+encodeURIComponent(JSON.stringify(data,null,2)); a.download='diagram.json'; a.click(); };
document.getElementById('btnExportSvg').onclick  = ()=>{ const clone=svg.cloneNode(true); clone.removeAttribute('style'); const a=document.createElement('a'); a.href='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(new XMLSerializer().serializeToString(clone)); a.download='diagram.svg'; a.click(); };
document.getElementById('btnSave').onclick = ()=> localStorage.setItem('idef0_v033b', JSON.stringify({settings:state.settings,nodes:state.nodes,edges:state.edges,stubs:state.stubs}));
document.getElementById('btnLoad').onclick = ()=>{ const v=localStorage.getItem('idef0_v033b'); if(v){ const d=JSON.parse(v); Object.assign(state.settings,d.settings||{}); state.nodes=d.nodes||[]; state.edges=d.edges||[]; state.stubs=d.stubs||[]; render(); setActiveHandle(null); } };
document.getElementById('routerSelect').onchange = ()=> render();

// ---------- Seed ----------
(function init(){
  addFunction(200,180); addFunction(520,180);
  const n1=state.nodes[0], n2=state.nodes[1];
  makeEdge({nodeId:n1.id,side:'right',role:'O'},{nodeId:n2.id,side:'left',role:'I'});
  state.stubs.push({id:newid('s'), type:'stub', role:'C', anchor:{nodeId:n1.id, side:'top', role:'C'}, axis:'y', offset:0, length:80, dir:-1, label:'Regulation'});
  state.stubs.push({id:newid('s'), type:'stub', role:'M', anchor:{nodeId:n2.id, side:'bottom', role:'M'}, axis:'y', offset:0, length:80, dir:1,  label:'People'});
  render();
})();

// replace the existing loadModels() with this
async function loadModels() {
  const sel = document.getElementById('modelSelect');

  // 1) Prefer models injected by Streamlit
  if (window.__MODELS__ && Array.isArray(window.__MODELS__.models)) {
    const data = window.__MODELS__;
    sel.innerHTML = data.models.map(m=>`<option value="${m.id}">${m.name}</option>`).join('');
    sel.onchange = ()=> {
      const found = data.models.find(x=>x.id===sel.value);
      if (found && found.diagram) importJSON(JSON.stringify(found.diagram));
    };
    if (data.models[0]) { sel.value = data.models[0].id; sel.onchange(); }
    return;
  }

  // 2) Fallback: local sample file
  try {
    const res = await fetch('sample_models.json');
    const data = await res.json();
    sel.innerHTML = data.models.map(m=>`<option value="${m.id}">${m.name}</option>`).join('');
    sel.onchange = ()=> {
      const found = data.models.find(x=>x.id===sel.value);
      if (found && found.diagram) importJSON(JSON.stringify(found.diagram));
    };
    if (data.models[0]) { sel.value = data.models[0].id; sel.onchange(); }
  } catch(e) {
    console.warn('No models available (window.__MODELS__ nor sample_models.json).', e);
  }
}
