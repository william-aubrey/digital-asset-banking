# fhoa-a24.py — IDEF0 Diagrammer v0.3.3b (S1 schema adapter)
import json, math
import streamlit as st

# ---------- Page chrome (lock height, keep header/footer, show sidebar) ----------
st.set_page_config(
    layout="wide",
    page_title="IDEF0 Diagrammer v0.3.3b",
    initial_sidebar_state="expanded",
)

# Hard-lock the outer page to one screen; add robust selectors Streamlit uses internally
st.markdown("""
<style>
html, body, #root, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], section.main {
  height: 100dvh !important;
  overflow: hidden !important;
}
.block-container { padding: 0 !important; margin: 0 !important; }

/* Make the main content truly full-width */
[data-testid="stAppViewContainer"] .main { padding: 0 !important; }
[data-testid="stAppViewContainer"] .main .block-container {
  max-width: 100% !important;
  width: 100% !important;
  padding: 0 !important;
  margin: 0 !important;
}            

/* Header/footer are overlays; reveal via body.reveal-ui */
header[data-testid="stHeader"], footer {
  position: fixed; left: 0; right: 0; z-index: 10000;
  transition: transform .18s ease;
}
header[data-testid="stHeader"] { top: 0; }
footer { bottom: 0; }
body:not(.reveal-ui) header[data-testid="stHeader"] { transform: translateY(-100%); }
body:not(.reveal-ui) footer { transform: translateY(100%); }

/* Always-on-top hover sentinels (don’t consume layout height) */
#reveal-top, #reveal-bottom {
  position: fixed; left: 0; right: 0; height: 10px; z-index: 2147483647;
  background: transparent; pointer-events: auto;
}
#reveal-top { top: 0; }
#reveal-bottom { bottom: 0; }
</style>

<script>
(() => {
  const body = document.body;
  function ensureBars(){
    if (!document.getElementById('reveal-top')) {
      const t = document.createElement('div'); t.id='reveal-top'; document.body.appendChild(t);
    }
    if (!document.getElementById('reveal-bottom')) {
      const b = document.createElement('div'); b.id='reveal-bottom'; document.body.appendChild(b);
    }
  }
  ensureBars();

  let hideTimer=null; const HIDE_MS=3000;
  function show(){ clearTimeout(hideTimer); body.classList.add('reveal-ui'); }
  function hideLater(){ clearTimeout(hideTimer); hideTimer=setTimeout(()=>body.classList.remove('reveal-ui'), HIDE_MS); }

  function pointerEdge(e){
    const y=e.clientY, h=window.innerHeight;
    if (y<=10 || (h-y)<=10) show(); else hideLater();
  }
  window.addEventListener('mousemove', pointerEdge, {passive:true});
  window.addEventListener('touchmove', pointerEdge, {passive:true});

  ['mouseenter','focusin'].forEach(ev => {
    ['reveal-top','reveal-bottom'].forEach(id=>{
      const el=document.getElementById(id); if(el) el.addEventListener(ev, show);
    });
  });
  ['mouseleave','focusout'].forEach(ev => {
    ['reveal-top','reveal-bottom'].forEach(id=>{
      const el=document.getElementById(id); if(el) el.addEventListener(ev, hideLater);
    });
  });

  body.classList.remove('reveal-ui');  // start hidden until user nudges an edge
})();
</script>
<div id="reveal-top"></div>
<div id="reveal-bottom"></div>
""", unsafe_allow_html=True)

# ---------- Assets ----------
def read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

INDEX = read("index.html")
CSS   = read("styles.css")
JS    = read("app.js")

# ---------- Snowflake connection ----------
def get_snowflake_cfg():
    if "snowflake" in st.secrets:
        return st.secrets["snowflake"]
    if "connections" in st.secrets and "snowflake" in st.secrets["connections"]:
        return st.secrets["connections"]["snowflake"]
    return None

cfg = get_snowflake_cfg()
session = None
conn_status = "local sample"
if cfg:
    try:
        from snowflake.snowpark import Session
        conf = {k: v for k, v in {
            "account": cfg.get("account"),
            "user": cfg.get("user"),
            "password": cfg.get("password"),
            "authenticator": cfg.get("authenticator"),
            "role": cfg.get("role"),
            "warehouse": cfg.get("warehouse"),
            "database": cfg.get("database"),
            "schema": cfg.get("schema"),
        }.items() if v not in (None, "")}
        session = Session.builder.configs(conf).create()
        conn_status = f"{conf.get('account','?')}/{conf.get('database','?')}.{conf.get('schema','?')}"
    except Exception as e:
        conn_status = f"connection failed: {e!s}"

def fetch_df(sql: str):
    return session.sql(sql).to_pandas()

# ---------- S1 schema adapter ----------
ROLE_TO_SIDE = {"INPUT": "left", "CONTROL": "top", "MECHANISM": "bottom", "OUTPUT": "right"}
ROLE_TO_AXIS = {"INPUT": "x",    "CONTROL": "y",   "MECHANISM": "y",     "OUTPUT": "x"}
ROLE_DIR     = {"INPUT": -1,     "CONTROL": -1,    "MECHANISM": 1,       "OUTPUT": 1}

def entities_for_model(model_id: int):
    df = fetch_df(f"""
        SELECT DISTINCT e.ENTITY_NAME
        FROM FUNCTIONS f
        JOIN FUNCTION_ENTITIES fe ON fe.FUNCTION_ID = f.FUNCTION_ID
        JOIN ENTITIES e ON e.ENTITY_ID = fe.ENTITY_ID
        WHERE f.MODEL_ID = {model_id}
        ORDER BY e.ENTITY_NAME
    """)
    return [r.ENTITY_NAME for r in df.itertuples(index=False)]

def get_geom_map(model_id: int):
    try:
        df = fetch_df(f"""
            SELECT FUNCTION_ID, X, Y, W, H
            FROM FUNCTION_GEOMETRY
            WHERE MODEL_ID = {model_id}
        """)
        return {r.FUNCTION_ID: (int(r.X or 0), int(r.Y or 0), int(r.W or 220), int(r.H or 120))
                for r in df.itertuples(index=False)}
    except Exception:
        return {}

def auto_layout(nodes):
    W, H = 220, 120
    GAPX, GAPY = 120, 120
    cols = max(1, math.ceil(math.sqrt(len(nodes))))
    ptr = 0
    for n in nodes:
        if n["x"] and n["y"]: continue
        r, c = divmod(ptr, cols); ptr += 1
        n["x"] = 160 + c * (W + GAPX)
        n["y"] = 140 + r * (H + GAPY)
        n["w"] = n.get("w", W) or W
        n["h"] = n.get("h", H) or H

def diagram_from_db_s1(model_id: int):
    fn_df = fetch_df(f"""
        SELECT FUNCTION_ID, FUNCTION_NAME
        FROM FUNCTIONS
        WHERE MODEL_ID = {model_id}
        ORDER BY FUNCTION_ID
    """)
    fe_df = fetch_df(f"""
        SELECT f.FUNCTION_ID, fe.ROLE, fe.ENTITY_ID, e.ENTITY_NAME
        FROM FUNCTIONS f
        JOIN FUNCTION_ENTITIES fe ON fe.FUNCTION_ID = f.FUNCTION_ID
        JOIN ENTITIES e ON e.ENTITY_ID = fe.ENTITY_ID
        WHERE f.MODEL_ID = {model_id}
        ORDER BY f.FUNCTION_ID, fe.ENTITY_ID
    """)

    geom = get_geom_map(model_id)

    idmap, nodes = {}, []
    for i, r in enumerate(fn_df.itertuples(index=False), start=1):
        nid = f"n{i}"
        idmap[r.FUNCTION_ID] = nid
        x, y, w, h = geom.get(r.FUNCTION_ID, (0, 0, 220, 120))
        nodes.append({"id": nid, "kind":"function", "x":x, "y":y, "w":w, "h":h,
                      "name": r.FUNCTION_NAME, "number": ""})
    auto_layout(nodes)

    edges, stubs = [], []
    if not fe_df.empty:
        for entity_id, grp in fe_df.groupby("ENTITY_ID"):
            label = grp["ENTITY_NAME"].iloc[0]
            outs = grp[grp["ROLE"] == "OUTPUT"]["FUNCTION_ID"].unique().tolist()
            icm  = grp[grp["ROLE"].isin(["INPUT","CONTROL","MECHANISM"])]
            if outs and len(icm):
                for ofid in outs:
                    for _, row in icm.iterrows():
                        if ofid == row["FUNCTION_ID"]: continue
                        a = {"nodeId": idmap.get(ofid), "side":"right", "role":"O"}
                        b = {"nodeId": idmap.get(row["FUNCTION_ID"]), "side":ROLE_TO_SIDE[row["ROLE"]], "role":row["ROLE"][0]}
                        if a["nodeId"] and b["nodeId"]:
                            edges.append({"id": f"e{len(edges)+1}", "type":"normal", "a":a, "b":b, "label":label})
            else:
                for ofid in outs:
                    stubs.append({"id": f"s{len(stubs)+1}", "type":"stub", "role":"O",
                                  "anchor":{"nodeId": idmap[ofid], "side":"right","role":"O"},
                                  "axis":"x","offset":0,"length":80,"dir":1,"label":label})
                if len(outs)==0 and len(icm):
                    for _, row in icm.iterrows():
                        role = row["ROLE"]
                        stubs.append({"id": f"s{len(stubs)+1}", "type":"stub", "role":role[0],
                                      "anchor":{"nodeId": idmap[row["FUNCTION_ID"]], "side":ROLE_TO_SIDE[role], "role":role[0]},
                                      "axis":ROLE_TO_AXIS[role], "offset":0,"length":80,"dir":ROLE_DIR[role], "label":label})
    return {"settings":{"router":"ortho","cornerRadius":12,"grid":10},
            "nodes":nodes,"edges":edges,"stubs":stubs}

# ---------- Build payload ----------
models_payload = {"models": []}
if cfg and session:
    try:
        mdl_df = fetch_df("SELECT MODEL_ID, MODEL_NAME FROM MODELS ORDER BY MODEL_ID")
        for row in mdl_df.itertuples(index=False):
            models_payload["models"].append({
                "id": str(row.MODEL_ID),
                "name": row.MODEL_NAME,
                "diagram": diagram_from_db_s1(row.MODEL_ID),
                "entities": entities_for_model(row.MODEL_ID)
            })
    except Exception as e:
        st.sidebar.warning(f"Model load failed: {e!s}")

if not models_payload["models"]:
    try:
        with open("sample_models.json","r",encoding="utf-8") as f:
            models_payload = json.load(f)
    except Exception:
        models_payload = {"models": []}

# ---------- Inline assets + component ----------
injection = f"<script>window.__MODELS__ = {json.dumps(models_payload)}</script>"
html = INDEX.replace('<link rel="stylesheet" href="styles.css" />', f"<style>{CSS}</style>") \
            .replace('<link rel="stylesheet" href="styles.css">',    f"<style>{CSS}</style>") \
            .replace('<script src="app.js"></script>',               injection + f"<script>{JS}</script>")

st.components.v1.html(html, height=720, width=1920, scrolling=False)

# ---------- Sidebar dev tools ----------
with st.sidebar:
    st.subheader("Developer")
    st.caption(f"Snowflake: {('connected ' + conn_status) if session else 'local sample'}")
    if session:
        try:
            mdl_df = fetch_df("SELECT MODEL_ID, MODEL_NAME FROM MODELS ORDER BY MODEL_ID")
            names = [f"{r.MODEL_NAME} (ID {r.MODEL_ID})" for r in mdl_df.itertuples(index=False)]
            choice = st.selectbox("Target model", names) if names else None
            target_id = int(choice.rsplit("ID",1)[1].strip(") ")) if choice else None
        except Exception as e:
            st.warning(f"Could not list models: {e}")
            target_id = None

        diagram_json = st.text_area("diagram.json (paste Export JSON)", height=120,
                                    placeholder='{"nodes":[...],"edges":[...],"stubs":[...]}')

        if st.button("Save geometry", use_container_width=True, disabled=not target_id):
            try:
                payload = json.loads(diagram_json or "{}")
                nodes = payload.get("nodes", [])
                session.sql("""
                  CREATE TABLE IF NOT EXISTS FUNCTION_GEOMETRY (
                    MODEL_ID NUMBER, FUNCTION_ID NUMBER, X NUMBER, Y NUMBER, W NUMBER, H NUMBER,
                    PRIMARY KEY (MODEL_ID, FUNCTION_ID)
                  )
                """).collect()
                fn_df = fetch_df(f"SELECT FUNCTION_ID, FUNCTION_NAME FROM FUNCTIONS WHERE MODEL_ID = {target_id}")
                name_to_id = {r.FUNCTION_NAME: r.FUNCTION_ID for r in fn_df.itertuples(index=False)}
                for n in nodes:
                    fid = name_to_id.get(n.get("name"))
                    if not fid:
                        continue

                    x = int(n.get("x",200)); y=int(n.get("y",180)); w=int(n.get("w",220)); h=int(n.get("h",120))
                    session.sql(f"""
                      MERGE INTO FUNCTION_GEOMETRY t
                      USING (SELECT {target_id} MODEL_ID, {fid} FUNCTION_ID) s
                      ON t.MODEL_ID=s.MODEL_ID AND t.FUNCTION_ID=s.FUNCTION_ID
                      WHEN MATCHED THEN UPDATE SET X={x}, Y={y}, W={w}, H={h}
                      WHEN NOT MATCHED THEN INSERT (MODEL_ID, FUNCTION_ID, X, Y, W, H)
                      VALUES ({target_id}, {fid}, {x}, {y}, {w}, {h})
                    """).collect()
                st.success("Geometry saved.")
            except Exception as e:
                st.error(f"Save failed: {e}")
