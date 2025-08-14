# fhoa-a24.py — IDEF0 Diagrammer v0.3.3c (Streamlit-only, Snowflake-on-demand)
import json, math
import streamlit as st

st.set_page_config(layout="wide", page_title="IDEF0 Diagrammer v0.3.3c")

# Minimal, robust layout: no scroll, full width, no special header/footer tricks
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], section.main {
  height: 100dvh !important;
  overflow: hidden !important;
}
[data-testid="stAppViewContainer"] .main { padding: 0 !important; }
[data-testid="stAppViewContainer"] .main .block-container {
  max-width: 100% !important; width: 100% !important; padding: 0 !important; margin: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# --- helpers
def read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

INDEX = read("index.html")
CSS   = read("styles.css")
JS    = read("app.js")

# --- Snowflake connection from Streamlit secrets (connections.snowflake)
def get_sf_cfg():
    try:
        if "connections" in st.secrets and "snowflake" in st.secrets["connections"]:
            return st.secrets["connections"]["snowflake"]
        if "snowflake" in st.secrets:
            return st.secrets["snowflake"]
    except Exception:
        pass
    return None

def try_snowflake_session():
    cfg = get_sf_cfg()
    if not cfg:
        return None, "no secrets"
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
        s = Session.builder.configs(conf).create()
        return s, f"{conf.get('account','?')}/{conf.get('database','?')}.{conf.get('schema','?')}"
    except Exception as e:
        return None, f"failed: {e!s}"

ROLE_TO_SIDE = {"INPUT":"left","CONTROL":"top","MECHANISM":"bottom","OUTPUT":"right"}
ROLE_TO_AXIS = {"INPUT":"x",   "CONTROL":"y",  "MECHANISM":"y",     "OUTPUT":"x"}
ROLE_DIR     = {"INPUT":-1,    "CONTROL":-1,   "MECHANISM":1,       "OUTPUT":1}

def fetch_df(session, sql: str):
    return session.sql(sql).to_pandas()

def auto_layout(nodes):
    W,H=220,120; GAPX=120; GAPY=120
    cols = max(1, math.ceil(math.sqrt(len(nodes))))
    ptr=0
    for n in nodes:
        if n.get("x") and n.get("y"): continue
        r,c = divmod(ptr, cols); ptr += 1
        n["x"] = 160 + c*(W+GAPX)
        n["y"] = 140 + r*(H+GAPY)
        n["w"] = n.get("w", W) or W
        n["h"] = n.get("h", H) or H

def diagram_from_db(session, model_id: int):
    fn_df = fetch_df(session, f"""
        SELECT FUNCTION_ID, FUNCTION_NAME
        FROM FUNCTIONS
        WHERE MODEL_ID = {model_id}
        ORDER BY FUNCTION_ID
    """)
    fe_df = fetch_df(session, f"""
        SELECT f.FUNCTION_ID, fe.ROLE, fe.ENTITY_ID, e.ENTITY_NAME
        FROM FUNCTIONS f
        JOIN FUNCTION_ENTITIES fe ON fe.FUNCTION_ID = f.FUNCTION_ID
        JOIN ENTITIES e ON e.ENTITY_ID = fe.ENTITY_ID
        WHERE f.MODEL_ID = {model_id}
        ORDER BY f.FUNCTION_ID, fe.ENTITY_ID
    """)
    # optional geometry
    try:
        geo_df = fetch_df(session, f"""
          SELECT FUNCTION_ID, X, Y, W, H
          FROM FUNCTION_GEOMETRY
          WHERE MODEL_ID = {model_id}
        """)
        geom = {int(r.FUNCTION_ID):(int(r.X or 0),int(r.Y or 0),int(r.W or 220),int(r.H or 120))
                for r in geo_df.itertuples(index=False)}
    except Exception:
        geom = {}
    idmap, nodes = {}, []
    for i, r in enumerate(fn_df.itertuples(index=False), start=1):
        nid = f"n{i}"
        fid = int(r.FUNCTION_ID)
        idmap[fid] = nid
        x,y,w,h = geom.get(fid, (0,0,220,120))
        nodes.append({"id":nid, "kind":"function", "x":x, "y":y, "w":w, "h":h,
                      "name": r.FUNCTION_NAME, "number": ""})
    auto_layout(nodes)
    edges, stubs = [], []
    if not fe_df.empty:
        for entity_id, grp in fe_df.groupby("ENTITY_ID"):
            label = grp["ENTITY_NAME"].iloc[0]
            outs = grp[grp["ROLE"]=="OUTPUT"]["FUNCTION_ID"].unique().tolist()
            icm  = grp[grp["ROLE"].isin(["INPUT","CONTROL","MECHANISM"])]
            if outs and len(icm):
                for ofid in outs:
                    for _, row in icm.iterrows():
                        if int(ofid) == int(row["FUNCTION_ID"]):
                            continue
                        a = {"nodeId": idmap.get(int(ofid)), "side":"right", "role":"O"}
                        b = {"nodeId": idmap.get(int(row["FUNCTION_ID"])),
                             "side": ROLE_TO_SIDE[row["ROLE"]], "role": row["ROLE"][0]}
                        if a["nodeId"] and b["nodeId"]:
                            edges.append({"id": f"e{len(edges)+1}", "type":"normal",
                                          "a": a, "b": b, "label": label})
            else:
                for ofid in outs:
                    stubs.append({"id": f"s{len(stubs)+1}", "type":"stub", "role":"O",
                                  "anchor":{"nodeId": idmap.get(int(ofid)), "side":"right","role":"O"},
                                  "axis":"x","offset":0,"length":80,"dir":1,"label":label})
                if len(outs)==0 and len(icm):
                    for _, row in icm.iterrows():
                        role = row["ROLE"]
                        stubs.append({"id": f"s{len(stubs)+1}", "type":"stub", "role": role[0],
                                      "anchor":{"nodeId": idmap.get(int(row["FUNCTION_ID"])),
                                                "side": ROLE_TO_SIDE[role], "role": role[0]},
                                      "axis": ROLE_TO_AXIS[role], "offset":0, "length":80, "dir": ROLE_DIR[role],
                                      "label": label})
    return {"settings":{"router":"ortho","cornerRadius":12,"grid":10},
            "nodes":nodes,"edges":edges,"stubs":stubs}

def build_models_payload_from_sf(session):
    payload = {"models": []}
    mdl_df = fetch_df(session, "SELECT MODEL_ID, MODEL_NAME FROM MODELS ORDER BY MODEL_ID")
    for row in mdl_df.itertuples(index=False):
        payload["models"].append({
            "id": str(int(row.MODEL_ID)),
            "name": row.MODEL_NAME,
            "diagram": diagram_from_db(session, int(row.MODEL_ID)),
            "entities": []  # optional: add entity list if you want
        })
    return payload

# --- state: default to sample so UI loads instantly
if "models_payload" not in st.session_state:
    try:
        with open("sample_models.json","r",encoding="utf-8") as f:
            st.session_state.models_payload = json.load(f)
    except Exception:
        st.session_state.models_payload = {"models": []}

# --- sidebar controls
with st.sidebar:
    st.subheader("IDEF0 Data")
    # status
    sf_session, sf_status = try_snowflake_session()
    if sf_session:
        st.success(f"Snowflake: {sf_status}")
    else:
        st.info("Snowflake not connected (or secrets missing). Using sample until you click 'Load from Snowflake'.")

    if st.button("Load from Snowflake", type="primary", use_container_width=True, disabled=not sf_session):
        try:
            st.session_state.models_payload = build_models_payload_from_sf(sf_session)
            st.success("Loaded models from Snowflake.")
        except Exception as e:
            st.error(f"Snowflake load failed: {e!s}")

    st.divider()
    st.caption("Paste Export JSON below and click Save Geometry to persist positions to Snowflake.")
    diagram_json = st.text_area("diagram.json", height=140, placeholder='{"nodes":[...],"edges":[...],"stubs":[...]}')
    target_id = st.text_input("Target MODEL_ID (number)", value="")
    save_clicked = st.button("Save geometry", use_container_width=True, disabled=not (sf_session and target_id.strip().isdigit()))
    if save_clicked:
        try:
            payload = json.loads(diagram_json or "{}")
            nodes = payload.get("nodes", [])
            sf_session.sql("""
              CREATE TABLE IF NOT EXISTS FUNCTION_GEOMETRY (
                MODEL_ID NUMBER, FUNCTION_ID NUMBER, X NUMBER, Y NUMBER, W NUMBER, H NUMBER,
                PRIMARY KEY (MODEL_ID, FUNCTION_ID)
              )
            """).collect()
            fn_df = fetch_df(sf_session, f"SELECT FUNCTION_ID, FUNCTION_NAME FROM FUNCTIONS WHERE MODEL_ID = {int(target_id)}")
            name_to_id = {r.FUNCTION_NAME: int(r.FUNCTION_ID) for r in fn_df.itertuples(index=False)}
            for n in nodes:
                fid = name_to_id.get(n.get("name"))
                if not fid: continue
                x = int(n.get("x",200)); y=int(n.get("y",180)); w=int(n.get("w",220)); h=int(n.get("h",120))
                sf_session.sql(f"""
                  MERGE INTO FUNCTION_GEOMETRY t
                  USING (SELECT {int(target_id)} MODEL_ID, {fid} FUNCTION_ID) s
                  ON t.MODEL_ID=s.MODEL_ID AND t.FUNCTION_ID=s.FUNCTION_ID
                  WHEN MATCHED THEN UPDATE SET X={x}, Y={y}, W={w}, H={h}
                  WHEN NOT MATCHED THEN INSERT (MODEL_ID, FUNCTION_ID, X, Y, W, H)
                  VALUES ({int(target_id)}, {fid}, {x}, {y}, {w}, {h})
                """).collect()
            st.success("Geometry saved.")
        except Exception as e:
            st.error(f"Save failed: {e!s}")

# --- inject models + inline CSS/JS and render component
injection = f"<script>window.__MODELS__ = {json.dumps(st.session_state.models_payload)}</script>"
html = INDEX.replace('<link rel="stylesheet" href="styles.css" />', f"<style>{CSS}</style>") \
            .replace('<link rel="stylesheet" href="styles.css">',    f"<style>{CSS}</style>") \
            .replace('<script src="app.js"></script>',               injection + f"<script>{JS}</script>")

# Force width to beat Streamlit's column clamp; fixed height for 1280x720 work
st.components.v1.html(html, height=720, width=1920, scrolling=False)
