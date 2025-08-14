from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any
import math, os
from pathlib import Path

from snowflake.snowpark import Session
import tomllib  # Python 3.11+

# ---------------- App ----------------
app = FastAPI(title="IDEF0 API + Editor")

# Same-origin (no CORS needed), but keep permissive for future modules
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- secrets.toml loader ----------------
_secrets_cache: Dict[str, Any] | None = None
_sf_session: Session | None = None

def _secrets_path() -> Path:
    # Optional override
    env_path = os.getenv("STREAMLIT_SECRETS_PATH")
    if env_path:
        p = Path(env_path).expanduser().resolve()
        if p.is_file():
            return p
    # default: project/.streamlit/secrets.toml (near this file or its parent)
    here = Path(__file__).resolve()
    for candidate in [
        here.parent / ".streamlit" / "secrets.toml",
        here.parent.parent / ".streamlit" / "secrets.toml",
        Path(".streamlit/secrets.toml").resolve(),
    ]:
        if candidate.is_file():
            return candidate
    raise RuntimeError("secrets.toml not found. Expected at .streamlit/secrets.toml (or set STREAMLIT_SECRETS_PATH)")

def _load_secrets() -> Dict[str, Any]:
    global _secrets_cache
    if _secrets_cache is not None:
        return _secrets_cache
    with open(_secrets_path(), "rb") as f:
        _secrets_cache = tomllib.load(f)
    return _secrets_cache

def _get_sf_cfg_from_secrets() -> Dict[str, Any]:
    data = _load_secrets()
    cfg = (data.get("connections", {}) or {}).get("snowflake") or data.get("snowflake")
    if not isinstance(cfg, dict):
        raise RuntimeError("Missing [connections.snowflake] (or [snowflake]) in secrets.toml")

    out = {
        "account":       cfg.get("account"),
        "user":          cfg.get("user"),
        "password":      cfg.get("password"),
        "authenticator": cfg.get("authenticator"),
        "role":          cfg.get("role"),
        "warehouse":     cfg.get("warehouse"),
        "database":      cfg.get("database", "ONTOLOGICS"),
        "schema":        cfg.get("schema", "IDEF0"),
    }

    missing = [k for k in ("account","user","role","warehouse","database","schema") if not out.get(k)]
    if not out.get("password") and not out.get("authenticator"):
        missing.append("password_or_authenticator")
    if missing:
        raise RuntimeError("Snowflake secrets incomplete: " + ", ".join(missing))

    return {k: v for k, v in out.items() if v not in (None, "")}

def get_session() -> Session:
    global _sf_session
    if _sf_session is not None:
        return _sf_session
    cfg = _get_sf_cfg_from_secrets()
    _sf_session = Session.builder.configs(cfg).create()
    return _sf_session

# ---------------- S1 adapter helpers ----------------
ROLE_TO_SIDE = {"INPUT":"left","CONTROL":"top","MECHANISM":"bottom","OUTPUT":"right"}
ROLE_TO_AXIS = {"INPUT":"x",   "CONTROL":"y",  "MECHANISM":"y",     "OUTPUT":"x"}
ROLE_DIR     = {"INPUT":-1,    "CONTROL":-1,   "MECHANISM":1,       "OUTPUT":1}

def auto_layout(nodes):
    W,H = 220,120
    GAPX,GAPY = 120,120
    cols = max(1, math.ceil(math.sqrt(len(nodes))))
    ptr = 0
    for n in nodes:
        if n.get("x") and n.get("y"): continue
        r,c = divmod(ptr, cols); ptr += 1
        n["x"] = 160 + c*(W+GAPX)
        n["y"] = 140 + r*(H+GAPY)
        n["w"] = n.get("w", W) or W
        n["h"] = n.get("h", H) or H

def build_diagram_json(model_id: int) -> Dict[str, Any]:
    session = get_session()

    fn_df = session.sql(f"""
        SELECT FUNCTION_ID, FUNCTION_NAME
        FROM FUNCTIONS
        WHERE MODEL_ID = {model_id}
        ORDER BY FUNCTION_ID
    """).to_pandas()

    fe_df = session.sql(f"""
        SELECT f.FUNCTION_ID, fe.ROLE, fe.ENTITY_ID, e.ENTITY_NAME
        FROM FUNCTIONS f
        JOIN FUNCTION_ENTITIES fe ON fe.FUNCTION_ID = f.FUNCTION_ID
        JOIN ENTITIES e ON e.ENTITY_ID = fe.ENTITY_ID
        WHERE f.MODEL_ID = {model_id}
        ORDER BY f.FUNCTION_ID, fe.ENTITY_ID
    """).to_pandas()

    # Optional geometry
    try:
        geo_df = session.sql(f"""
            SELECT FUNCTION_ID, X, Y, W, H
            FROM FUNCTION_GEOMETRY
            WHERE MODEL_ID = {model_id}
        """).to_pandas()
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
        nodes.append({"id":nid,"kind":"function","x":x,"y":y,"w":w,"h":h,"name":r.FUNCTION_NAME,"number":""})
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
                        if int(ofid) == int(row["FUNCTION_ID"]): continue
                        a = {"nodeId": idmap.get(int(ofid)), "side":"right","role":"O"}
                        b = {"nodeId": idmap.get(int(row["FUNCTION_ID"])),
                             "side": ROLE_TO_SIDE[row["ROLE"]], "role": row["ROLE"][0]}
                        if a["nodeId"] and b["nodeId"]:
                            edges.append({"id": f"e{len(edges)+1}", "type":"normal", "a":a, "b":b, "label":label})
            else:
                for ofid in outs:
                    stubs.append({"id": f"s{len(stubs)+1}","type":"stub","role":"O",
                                  "anchor":{"nodeId": idmap.get(int(ofid)),"side":"right","role":"O"},
                                  "axis":"x","offset":0,"length":80,"dir":1,"label":label})
                if len(outs)==0 and len(icm):
                    for _, row in icm.iterrows():
                        role = row["ROLE"]
                        stubs.append({"id": f"s{len(stubs)+1}","type":"stub","role":role[0],
                                      "anchor":{"nodeId": idmap.get(int(row["FUNCTION_ID"])),
                                                "side": ROLE_TO_SIDE[role], "role": role[0]},
                                      "axis": ROLE_TO_AXIS[role], "offset":0,"length":80,"dir":ROLE_DIR[role],"label":label})
    return {"settings":{"router":"ortho","cornerRadius":12,"grid":10},
            "nodes":nodes,"edges":edges,"stubs":stubs}

# ---------------- API routes ----------------
@app.get("/api/models")
def list_models():
    session = get_session()
    df = session.sql("SELECT MODEL_ID, MODEL_NAME FROM MODELS ORDER BY MODEL_ID").to_pandas()
    return {"models": [{"id": str(int(r.MODEL_ID)), "name": r.MODEL_NAME} for r in df.itertuples(index=False)]}

@app.get("/api/models/{model_id}")
def get_model(model_id: int):
    try:
        return build_diagram_json(model_id)
    except Exception as e:
        raise HTTPException(500, f"Failed to build diagram: {e}")

@app.get("/api/models/{model_id}/entities")
def get_entities(model_id: int):
    session = get_session()
    df = session.sql(f"""
      SELECT DISTINCT e.ENTITY_NAME
      FROM FUNCTIONS f
      JOIN FUNCTION_ENTITIES fe ON fe.FUNCTION_ID = f.FUNCTION_ID
      JOIN ENTITIES e ON e.ENTITY_ID = fe.ENTITY_ID
      WHERE f.MODEL_ID = {model_id}
      ORDER BY e.ENTITY_NAME
    """).to_pandas()
    return {"entities": [r.ENTITY_NAME for r in df.itertuples(index=False)]}

class GeometryPayload(BaseModel):
    nodes: List[Dict[str, Any]] = []

@app.post("/api/models/{model_id}/geometry")
def save_geom(model_id: int, payload: GeometryPayload):
    session = get_session()
    session.sql("""
      CREATE TABLE IF NOT EXISTS FUNCTION_GEOMETRY (
        MODEL_ID NUMBER, FUNCTION_ID NUMBER, X NUMBER, Y NUMBER, W NUMBER, H NUMBER,
        PRIMARY KEY (MODEL_ID, FUNCTION_ID)
      )
    """).collect()
    fn_df = session.sql(f"SELECT FUNCTION_ID, FUNCTION_NAME FROM FUNCTIONS WHERE MODEL_ID = {model_id}").to_pandas()
    name_to_id = {r.FUNCTION_NAME: int(r.FUNCTION_ID) for r in fn_df.itertuples(index=False)}
    for n in payload.nodes:
        fid = name_to_id.get(n.get("name"))
        if not fid: 
            continue
        x = int(n.get("x",200)); y = int(n.get("y",180)); w = int(n.get("w",220)); h = int(n.get("h",120))
        session.sql(f"""
          MERGE INTO FUNCTION_GEOMETRY t
          USING (SELECT {model_id} MODEL_ID, {fid} FUNCTION_ID) s
          ON t.MODEL_ID=s.MODEL_ID AND t.FUNCTION_ID=s.FUNCTION_ID
          WHEN MATCHED THEN UPDATE SET X={x}, Y={y}, W={w}, H={h}
          WHEN NOT MATCHED THEN INSERT (MODEL_ID, FUNCTION_ID, X, Y, W, H)
          VALUES ({model_id}, {fid}, {x}, {y}, {w}, {h})
        """).collect()
    return {"ok": True}

# ---------------- Static editor (index.html, styles.css, app.js) -----------
def _find_static_dir() -> Path:
    # assumes index.html is next to api.py (or parent). Adjust if needed.
    here = Path(__file__).resolve()
    for d in [here.parent, here.parent.parent]:
        if (d / "index.html").is_file():
            return d
    return here.parent

STATIC_DIR = _find_static_dir()
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
