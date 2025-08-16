# ============================================================
# fhoa-a24.py — Streamlit wrapper for IDEF0 Diagrammer
# Loads model data from Snowflake, lets you load JSON models,
# injects them into index.html as window.MODELS, and renders.
# ============================================================

# ======================================================================
# IMPORTS
# ======================================================================
from __future__ import annotations
import json
from pathlib import Path
import streamlit as st
from snowflake.snowpark import Session

# ======================================================================
# STREAMLIT PAGE CONFIG & SESSION STATE
# ======================================================================
st.set_page_config(page_title="IDEF0 Diagrammer", layout="wide")

if "extra_models" not in st.session_state:
    st.session_state["extra_models"] = []
if "load_key" not in st.session_state:
    # bump this to reset uploader/textarea widgets after a successful load
    st.session_state["load_key"] = 0

# ======================================================================
# SNOWFLAKE CONNECTION
# ======================================================================
@st.cache_resource
def get_snowflake_cfg():
    if "connections" in st.secrets and "snowflake" in st.secrets["connections"]:
        return st.secrets["connections"]["snowflake"]
    if "snowflake" in st.secrets:
        return st.secrets["snowflake"]
    return None

@st.cache_resource
def get_session() -> Session | None:
    cfg = get_snowflake_cfg()
    if not cfg:
        st.sidebar.warning("No Snowflake credentials found in secrets.toml.")
        return None
    try:
        return Session.builder.configs(cfg).create()
    except Exception as e:
        st.sidebar.error(f"Snowflake connection failed: {e}")
        return None

# ======================================================================
# HELPER FUNCTIONS
# ======================================================================
def canon_node(node: str) -> str:
    if not node:
        return node
    node = node.strip().upper()
    return node if node == "A-0" else node.replace(".", "")

def is_root(node: str) -> bool:
    return canon_node(node) == "A-0"

def sort_children(parent_canon: str, child_nodes):
    out = []
    for raw in child_nodes:
        cc = canon_node(raw)
        if parent_canon == "A-0":
            tail = cc[1:]
        else:
            tail = cc[len(parent_canon):] if cc.startswith(parent_canon) else cc[1:]
        try:
            key = int(tail[:1]) if tail else 0
        except ValueError:
            key = 0
        out.append((key, cc, raw))
    out.sort(key=lambda x: (x[0], x[1]))
    return [orig for _, __, orig in out]

def cols(table, sf_session, db_schema_config):
    s = db_schema_config
    sch = f"{s['database']}.INFORMATION_SCHEMA.COLUMNS"
    q = f"""
    SELECT COLUMN_NAME
    FROM {sch}
    WHERE TABLE_SCHEMA = '{s['schema'].upper()}'
      AND TABLE_NAME   = '{table.upper()}'
    """
    return {r["COLUMN_NAME"].upper() for r in sf_session.sql(q).collect()}

def pick(colset, *candidates):
    for c in candidates:
        if c in colset:
            return c
    return None

# ======================================================================
# SNOWFLAKE DATA LOADING
# ======================================================================
@st.cache_data(ttl=300, show_spinner="Loading data from Snowflake...")
def load_all_from_snowflake(_sf_session: Session | None):
    if not _sf_session:
        return None, None, None

    s = get_snowflake_cfg()
    sch = f"{s['database']}.{s['schema']}"

    # MODELS (optional, used only for names)
    model_cols = cols("MODELS", _sf_session, s)
    mdl_id   = pick(model_cols, "MODEL_ID", "ID")
    mdl_name = pick(model_cols, "MODEL_NAME", "NAME", "TITLE", "LABEL")
    model_rows = []
    if mdl_id and mdl_name:
        model_rows = _sf_session.sql(
            f"SELECT {mdl_id} AS MODEL_ID, {mdl_name} AS MODEL_NAME FROM {sch}.MODELS"
        ).collect()

    # FUNCTIONS (required)
    f_cols   = cols("FUNCTIONS", _sf_session, s)
    f_id     = pick(f_cols, "FUNCTION_ID", "ID")
    f_name   = pick(f_cols, "FUNCTION_NAME", "NAME", "TITLE", "LABEL")
    f_node   = pick(f_cols, "NODE", "NODE_ID", "NODE_NUMBER", "FUNCTION_NODE", "CODE")
    f_parent = pick(f_cols, "PARENT_FUNCTION_ID", "PARENT_ID", "PARENT")
    f_model  = pick(f_cols, "MODEL_ID")

    if not all([f_id, f_name, f_node]):
        raise RuntimeError("FUNCTIONS must have id, name, and node columns.")

    fn_sql = f"SELECT {f_id} AS FUNCTION_ID, {f_name} AS NAME, {f_node} AS NODE"
    fn_sql += f", {f_parent} AS PARENT_FUNCTION_ID" if f_parent else ", NULL AS PARENT_FUNCTION_ID"
    fn_sql += f", {f_model}  AS MODEL_ID"           if f_model  else ", NULL AS MODEL_ID"
    fn_sql += f" FROM {sch}.FUNCTIONS"
    func_rows = _sf_session.sql(fn_sql).collect()

    # FUNCTION_ENTITIES + ENTITIES (optional)
    fe_cols = cols("FUNCTION_ENTITIES", _sf_session, s)
    e_cols  = cols("ENTITIES", _sf_session, s)
    fe_id_func = pick(fe_cols, "FUNCTION_ID")
    fe_ent_id  = pick(fe_cols, "ENTITY_ID")
    fe_role    = pick(fe_cols, "ROLE", "FUNCTION_ROLE")
    fe_ename   = pick(fe_cols, "ENTITY_NAME")
    ent_id   = pick(e_cols, "ENTITY_ID", "ID")
    ent_name = pick(e_cols, "ENTITY_NAME", "NAME", "LABEL")

    if not (fe_id_func and fe_ent_id and fe_role):
        fe_rows = []
    else:
        if fe_ename:
            fe_sql = f"""
            SELECT {fe_id_func} AS FUNCTION_ID, {fe_ent_id} AS ENTITY_ID,
                   {fe_role} AS ROLE, {fe_ename} AS ENTITY_NAME
            FROM {sch}.FUNCTION_ENTITIES
            """
        elif ent_id and ent_name:
            fe_sql = f"""
            SELECT fe.{fe_id_func} AS FUNCTION_ID, fe.{fe_ent_id} AS ENTITY_ID,
                   fe.{fe_role} AS ROLE, e.{ent_name} AS ENTITY_NAME
            FROM {sch}.FUNCTION_ENTITIES fe
            JOIN {sch}.ENTITIES e ON fe.{fe_ent_id} = e.{ent_id}
            """
        else:
            fe_sql = f"""
            SELECT {fe_id_func} AS FUNCTION_ID, {fe_ent_id} AS ENTITY_ID,
                   {fe_role} AS ROLE, NULL AS ENTITY_NAME
            FROM {sch}.FUNCTION_ENTITIES
            """
        fe_rows = _sf_session.sql(fe_sql).collect()

    model_name_by_id = {r["MODEL_ID"]: r["MODEL_NAME"] for r in model_rows}
    return func_rows, fe_rows, model_name_by_id

# ======================================================================
# DATA SHAPING (DATABASE ROWS -> JSON PAYLOAD)
# ======================================================================
def shape_data_into_models(func_rows, fe_rows, model_name_by_id):
    models = []
    def key_of(r): return r["MODEL_ID"] if r["MODEL_ID"] is not None else 1
    by_model = {}
    for r in func_rows:
        by_model.setdefault(key_of(r), []).append(r)

    fe_by_func = {}
    for e in (fe_rows or []):
        fe_by_func.setdefault(e["FUNCTION_ID"], []).append({
            "role": (e["ROLE"] or "").upper()[:1],  # I/C/M/O
            "name": e["ENTITY_NAME"] or f"ENTITY_{e['ENTITY_ID']}",
            "entity_id": e["ENTITY_ID"],
        })

    for model_id, rows in by_model.items():
        by_id, by_parent, root = {}, {}, None
        for r in rows:
            cnode = canon_node(r["NODE"])
            rec = {
                "id": r["FUNCTION_ID"],
                "name": r["NAME"],
                "node": r["NODE"],
                "node_canon": cnode,
                "parent_id": r["PARENT_FUNCTION_ID"],
            }
            by_id[rec["id"]] = rec
            by_parent.setdefault(rec["parent_id"], []).append(rec)
            if is_root(r["NODE"]):
                root = rec

        # Fallback if no literal A-0
        if root is None:
            nulls = by_parent.get(None) or by_parent.get("") or []
            if nulls:
                root = nulls[0]
                root["node"] = "A-0"
                root["node_canon"] = "A-0"

        def diagram_for_parent(parent_func):
            parent_c = parent_func["node_canon"]
            kids = by_parent.get(parent_func["id"], [])
            order = sort_children(parent_c, [k["node"] for k in kids])
            node_map = {k["node"]: k for k in kids}
            ordered = [node_map[n] for n in order]

            nodes = []
            x, y = 160, 140
            step_x, step_y = 340, 240
            col = 0
            for k in ordered:
                nodes.append({
                    "id": f"n{k['id']}",
                    "kind": "function",
                    "x": x + step_x * col, "y": y,
                    "w": 220, "h": 120,
                    "name": k["name"],
                    "number": k["node_canon"],
                })
                col += 1
                if col == 2:
                    col = 0
                    y += step_y

            edges, stubs = [], []
            child_ids = [k["id"] for k in ordered]
            fn_ent = {fid: fe_by_func.get(fid, []) for fid in child_ids}

            producers, consumers = {}, {}
            for fid, items in fn_ent.items():
                for it in items:
                    if it["role"] == "O":
                        producers.setdefault(it["name"], set()).add(fid)
                    elif it["role"] in ("I", "C", "M"):
                        consumers.setdefault(it["name"], set()).add(fid)

            eid = 1
            inside = set()
            for lbl, prod_set in producers.items():
                cons_set = consumers.get(lbl, set())
                for a in prod_set:
                    for b in cons_set:
                        if a == b:
                            continue
                        edges.append({
                            "id": f"e{eid}", "type": "normal",
                            "a": { "nodeId": f"n{a}", "side":"right", "role":"O" },
                            "b": { "nodeId": f"n{b}", "side":"left",  "role":"I"  },
                            "label": lbl,
                        })
                        inside.add((f"n{a}", f"n{b}", lbl)); eid += 1

            sid = 1
            for fid, items in fn_ent.items():
                nid = f"n{fid}"
                for it in items:
                    lbl, r = it["name"], it["role"]
                    in_edge  = any(n2==nid and l2==lbl for _, n2, l2 in inside)
                    out_edge = any(n1==nid and l2==lbl for n1, _, l2 in inside)
                    if r == "O" and not out_edge:
                        stubs.append({"id":f"s{sid}","type":"stub","role":"O",
                                      "anchor":{"nodeId":nid,"side":"right","role":"O"},
                                      "axis":"x","offset":0,"length":80,"dir":+1,
                                      "label":lbl}); sid+=1
                    elif r in ("I","C","M") and not in_edge:
                        side = "left" if r == "I" else ("top" if r == "C" else "bottom")
                        axis = "x" if r == "I" else "y"
                        dir_ = -1 if r in ("I","C") else +1
                        stubs.append({"id":f"s{sid}","type":"stub","role":r,
                                      "anchor":{"nodeId":nid,"side":side,"role":r},
                                      "axis":axis,"offset":0,"length":80,"dir":dir_,
                                      "label":lbl}); sid+=1

            return { "settings":{"router":"ortho","cornerRadius":12,"grid":10},
                     "nodes":nodes, "edges":edges, "stubs":stubs }

        contexts = []
        if root:
            # A-0 single box with stubs from its own FE
            def single_box(func):
                nid = f"n{func['id']}"
                nodes = [{"id":nid,"kind":"function","x":160,"y":140,"w":220,"h":120,
                          "name":func["name"],"number":"A-0"}]
                stubs, sid = [], 1
                for it in fe_by_func.get(func["id"], []):
                    r, lbl = it["role"], it["name"]
                    if r == "I":
                        stubs.append({"id":f"s{sid}","type":"stub","role":"I",
                                      "anchor":{"nodeId":nid,"side":"left","role":"I"},
                                      "axis":"x","offset":0,"length":80,"dir":-1,
                                      "label":lbl}); sid+=1
                    elif r == "C":
                        stubs.append({"id":f"s{sid}","type":"stub","role":"C",
                                      "anchor":{"nodeId":nid,"side":"top","role":"C"},
                                      "axis":"y","offset":0,"length":80,"dir":-1,
                                      "label":lbl}); sid+=1
                    elif r == "M":
                        stubs.append({"id":f"s{sid}","type":"stub","role":"M",
                                      "anchor":{"nodeId":nid,"side":"bottom","role":"M"},
                                      "axis":"y","offset":0,"length":80,"dir":+1,
                                      "label":lbl}); sid+=1
                    elif r == "O":
                        stubs.append({"id":f"s{sid}","type":"stub","role":"O",
                                      "anchor":{"nodeId":nid,"side":"right","role":"O"},
                                      "axis":"x","offset":0,"length":80,"dir":+1,
                                      "label":lbl}); sid+=1
                return {"settings":{"router":"ortho","cornerRadius":12,"grid":10},
                        "nodes":nodes,"edges":[],"stubs":stubs}

            contexts.append({"id":"A-0","label":"A-0","diagram":single_box(root)})
            contexts.append({"id":"A0","label":"A0","diagram":diagram_for_parent(root)})

        for pid, kids in {k:v for k,v in by_parent.items() if k is not None}.items():
            parent = by_id.get(pid)
            if not parent or is_root(parent["node"]):
                continue
            cid = canon_node(parent["node"])
            contexts.append({
                "id": cid,
                "label": cid,
                "diagram": diagram_for_parent(parent)
            })

        models.append({
            "id": str(model_id),
            "name": model_name_by_id.get(model_id, f"Model {model_id}"),
            "contexts": contexts,
            "entities": [],
        })
    return models

# ======================================================================
# MAIN LOGIC: LOAD DATA
# ======================================================================
sf_session = get_session()
models = []

try:
    func_rows, fe_rows, model_name_by_id = load_all_from_snowflake(sf_session)
    if func_rows:
        models = shape_data_into_models(func_rows, fe_rows, model_name_by_id)
        s_cfg = get_snowflake_cfg()
        st.sidebar.success(f"Snowflake: {s_cfg['account']}/{s_cfg['database']}.{s_cfg['schema']}")
    else:
        # This branch is hit if sf_session is None, or if the query returns no rows
        if sf_session: # Connection was successful but no data
             st.sidebar.info("No models found in Snowflake.")
        # Let it fall through to the local file load
except Exception as e:
    st.sidebar.error(f"Snowflake load failed: {e}")
    # Let it fall through to the local file load

if not models:
    st.sidebar.info("Attempting to load from local `sample_models.json`...")
    try:
        sample_path = Path(__file__).parent / "sample_models.json"
        with open(sample_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
            models = payload.get("models", [])
            st.sidebar.success("Loaded models from local `sample_models.json`.")
    except FileNotFoundError:
        st.sidebar.warning("`sample_models.json` not found. No models to display.")
    except Exception as e:
        st.sidebar.error(f"Failed to load `sample_models.json`: {e}")

# ======================================================================
# STREAMLIT SIDEBAR: LOAD LOCAL MODEL
# ======================================================================
with st.sidebar.expander("Load model", expanded=False):
    k = st.session_state["load_key"]
    up = st.file_uploader("Upload JSON", type=["json"], key=f"uploader_{k}")
    paste = st.text_area("…or paste JSON", height=140, key=f"paste_{k}")
    mode = st.radio("How to add?", ["Replace all", "Append"], index=1, horizontal=True)

    def _normalize(obj):
        # Accept {"models":[...]}, a single model {...}, or a list [...]
        if isinstance(obj, dict) and "models" in obj and isinstance(obj["models"], list):
            return obj["models"]
        elif isinstance(obj, dict):
            return [obj]
        elif isinstance(obj, list):
            return obj
        else:
            raise ValueError("Expected a model object, a list, or {'models':[...]}")

    if st.button("Load JSON"):
        try:
            raw = (up.read().decode("utf-8") if up else (paste or "")).strip()
            if not raw:
                st.warning("Choose a file or paste JSON first.")
            else:
                loaded = _normalize(json.loads(raw))
                # Ensure each model has a string id
                for i, m in enumerate(loaded, 1):
                    if "id" not in m:
                        m["id"] = f"user-{i}"
                    m["id"] = str(m["id"])
                if mode.startswith("Replace"):
                    st.session_state["extra_models"] = loaded
                else:
                    st.session_state["extra_models"].extend(loaded)
                # reset inputs so they don't re-trigger on rerun
                st.session_state["load_key"] += 1
                st.success(f"Loaded {len(loaded)} model(s).")
        except Exception as e:
            st.error(f"Could not read JSON: {e}")

    if st.button("Clear loaded models"):
        st.session_state["extra_models"] = []
        st.success("Cleared.")

# ======================================================================
# MODEL MERGING & DEBUGGING
# ======================================================================

# ---------- Merge user-loaded models into main list ----------
if st.session_state.get("extra_models"):
    models = models + [{**m, "id": str(m.get("id"))} for m in st.session_state["extra_models"]]

# ---------- Debug summary and payload download button ----------
with st.sidebar.expander("Debug: model build summary", expanded=False):
    for m in models:
        st.write({
            "model_id": m["id"],
            "model_name": m["name"],
            "contexts": [{"id": c.get("id"), "nodes": len(c.get("diagram", {}).get("nodes", []))} for c in m.get("contexts", [])],
        })

st.sidebar.download_button(
    "Download injected payload (window.MODELS)",
    data=json.dumps({"models": models}, indent=2),
    file_name="models_payload.json",
    mime="application/json"
)

# ======================================================================
# ASSET INLINING & HTML RENDERING
# ======================================================================
def inline_assets(html: str) -> str:
    """Read styles/app script from ./static or project root and inline them."""
    base = Path(__file__).parent

    def _read_first(paths):
        for p in paths:
            if p.exists():
                return p.read_text(encoding="utf-8")
        return ""

    css = _read_first([base / "static" / "styles.css", base / "styles.css"])
    js  = _read_first([base / "static" / "app.js",    base / "app.js"])

    # Insert CSS before </head>, JS before </body>. If tags are missing, append.
    if css:
        injection = f"<style id='inlined-styles'>\n{css}\n</style>\n"
        html = html.replace("</head>", injection + "</head>") if "</head>" in html else injection + html
    if js:
        injection = f"<script id='inlined-app'>\n{js}\n</script>\n"
        html = html.replace("</body>", injection + "</body>") if "</body>" in html else html + injection
    return html

# Read and prepare HTML
base = Path(__file__).parent
index_html = (base / "index.html").read_text(encoding="utf-8")
index_html = inline_assets(index_html)

# Put the models JSON into the placeholder inside index.html
placeholder = "/*__MODELS__*/"
if placeholder in index_html:
    index_html = index_html.replace(placeholder, json.dumps({"models": models}))
else:
    # Fallback: prepend (kept as last resort)
    prepend = f"<script>window.MODELS = {json.dumps({'models': models})};</script>"
    index_html = prepend + index_html

# Render the component (this is the call you were missing)
st.components.v1.html(index_html, height=700, width=1600, scrolling=False)
