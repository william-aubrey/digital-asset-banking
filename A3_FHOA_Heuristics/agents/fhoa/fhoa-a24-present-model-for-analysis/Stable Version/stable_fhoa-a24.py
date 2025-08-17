import json
import streamlit as st

st.set_page_config(layout="wide", page_title="IDEF0 Diagrammer v0.3.3b")

# --- load static assets ---
def read(p: str) -> str:
    with open(p, "r", encoding="utf-8") as f:
        return f.read()

INDEX = read("index.html")
CSS   = read("styles.css")
JS    = read("app.js")

# --- models payload (may come from Snowflake or sample) ---
models_payload = {"models": []}

# --- secrets helper: support both [snowflake] and [connections.snowflake] ---
def get_snowflake_cfg():
    # st.secrets behaves like a dict; guard every access
    if "snowflake" in st.secrets:
        return st.secrets["snowflake"]
    if "connections" in st.secrets:
        conn = st.secrets["connections"]
        if conn and "snowflake" in conn:
            return conn["snowflake"]
    return None

session = None
cfg = get_snowflake_cfg()
if cfg:
    try:
        from snowflake.snowpark import Session
        # Build configs dict only with present keys (avoids indexing None)
        conf = {}
        for k in ("account","user","password","authenticator","role","warehouse","database","schema"):
            if k in cfg and cfg[k] not in (None, ""):
                conf[k] = cfg[k]
        # If you use SSO, set authenticator="externalbrowser" and omit password.
        session = Session.builder.configs(conf).create()
    except Exception as e:
        st.warning(f"Snowflake connection failed; using local sample. ({e})")
else:
    st.info("No Snowflake credentials found; using local sample_models.json.")

def fetch_df(sql: str):
    if not session:
        raise RuntimeError("No Snowflake session available")
    return session.sql(sql).to_pandas()

def diagram_from_db(model_id: int):
    nodes_df = fetch_df(f"""
      SELECT FUNCTION_ID, NAME,
             COALESCE(X,200) X, COALESCE(Y,180) Y,
             COALESCE(W,220) W, COALESCE(H,120) H,
             COALESCE(BOX_NUMBER,'') NUMBER,
             COALESCE(KIND,'FUNCTION') KIND
      FROM FUNCTIONS
      WHERE MODEL_ID = {model_id}
      ORDER BY FUNCTION_ID
    """)

    edges_df = fetch_df(f"""
      SELECT CONNECTOR_ID,
             A_FUNCTION_ID, A_SIDE, A_ROLE,
             B_FUNCTION_ID, B_SIDE, B_ROLE,
             COALESCE(LABEL,'') LABEL
      FROM CONNECTORS
      WHERE MODEL_ID = {model_id}
      ORDER BY CONNECTOR_ID
    """)

    stubs_df = fetch_df(f"""
      SELECT STUB_ID, FUNCTION_ID, SIDE, ROLE, AXIS, OFFSET, LENGTH, DIR,
             COALESCE(LABEL,'') LABEL
      FROM STUBS
      WHERE MODEL_ID = {model_id}
      ORDER BY STUB_ID
    """)

    # FUNCTION_ID -> frontend id map
    idmap, out_nodes = {}, []
    for i, r in enumerate(nodes_df.itertuples(index=False), start=1):
        nid = f"n{i}"
        idmap[r.FUNCTION_ID] = nid
        out_nodes.append({
            "id": nid,
            "kind": (r.KIND or "FUNCTION").lower(),   # 'function' | 'offpage'
            "x": int(r.X), "y": int(r.Y),
            "w": int(r.W), "h": int(r.H),
            "name": r.NAME, "number": r.NUMBER,
        })

    out_edges = []
    for j, e in enumerate(edges_df.itertuples(index=False), start=1):
        a_id, b_id = idmap.get(e.A_FUNCTION_ID), idmap.get(e.B_FUNCTION_ID)
        if not a_id or not b_id:
            continue
        out_edges.append({
            "id": f"e{j}", "type": "normal",
            "a": {"nodeId": a_id, "side": e.A_SIDE.lower(), "role": e.A_ROLE},
            "b": {"nodeId": b_id, "side": e.B_SIDE.lower(), "role": e.B_ROLE},
            "label": e.LABEL,
        })

    out_stubs = []
    for k, s in enumerate(stubs_df.itertuples(index=False), start=1):
        nid = idmap.get(s.FUNCTION_ID)
        if not nid:
            continue
        out_stubs.append({
            "id": f"s{k}", "type": "stub", "role": s.ROLE,
            "anchor": {"nodeId": nid, "side": s.SIDE.lower(), "role": s.ROLE},
            "axis": (s.AXIS or "x").lower(),
            "offset": int(s.OFFSET or 0),
            "length": int(s.LENGTH or 80),
            "dir": int(s.DIR or 1),
            "label": s.LABEL,
        })

    return {"settings": {"router": "ortho", "cornerRadius": 12, "grid": 10},
            "nodes": out_nodes, "edges": out_edges, "stubs": out_stubs}

# Build models list from Snowflake if connected; otherwise fallback to local sample
if session:
    try:
        models_df = fetch_df("SELECT MODEL_ID, MODEL_NAME FROM MODELS ORDER BY MODEL_ID")
        for row in models_df.itertuples(index=False):
            models_payload["models"].append({
                "id": str(row.MODEL_ID),
                "name": row.MODEL_NAME,
                "diagram": diagram_from_db(row.MODEL_ID),
            })
    except Exception as e:
        st.warning(f"Failed to load MODELS from Snowflake; falling back to sample. ({e})")
        models_payload = {"models": []}

if not models_payload["models"]:
    try:
        with open("sample_models.json", "r", encoding="utf-8") as f:
            models_payload = json.load(f)
    except Exception as e:
        st.warning(f"No Snowflake data and sample_models.json not found ({e}). Continuing with empty model list.")
        models_payload = {"models": []}

# --- inject models + inline CSS/JS ---
injection = f"<script>window.__MODELS__ = {json.dumps(models_payload)}</script>"

html = INDEX
# Replace either self-closing or non-self-closing link tags with inline CSS
html = html.replace('<link rel="stylesheet" href="styles.css" />', f"<style>{CSS}</style>")
html = html.replace('<link rel="stylesheet" href="styles.css">',    f"<style>{CSS}</style>")
# Inline JS and add the models injection
html = html.replace('<script src="app.js"></script>', injection + f"<script>{JS}</script>")

st.title("IDEF0 Diagrammer v0.3.3b")
st.caption("Two-click handles • Stubs • Orthogonal routing • Snowpark-backed (fallback to local sample)")
st.components.v1.html(html, height=820, scrolling=True)
