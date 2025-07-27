# dab.py
"""
Digital Asset Banking application with a core platform, CYOA plugin, 
and a Streamlit UI fully integrated with AWS S3 for file storage.
"""

# --- Core Imports ---
import os
import boto3
import logging
from botocore.exceptions import NoCredentialsError, ClientError
from typing import Dict, Any, List
import streamlit as st

# --- Logging Configuration ---
# This helps print detailed errors to the terminal for easier debugging.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- S3 Configuration ---
# Initialize the S3 client and get the bucket name from environment variables.
# This is where the credentials you set in the terminal are used.
try:
    S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
    s3_client = boto3.client('s3')
except Exception as e:
    logging.error("S3 client could not be initialized. Ensure AWS credentials and region are set.", exc_info=True)
    S3_BUCKET = None
    s3_client = None

# --- Core DAB Platform ---
ASSET_STORE: List[Dict[str, Any]] = []
_asset_type_plugins: Dict[str, Any] = {}

def register_asset_type(asset_type: str, plugin: Any) -> None:
    """Register a plugin for a specific asset_type."""
    _asset_type_plugins[asset_type] = plugin

def get_registered_types() -> List[str]:
    """Return a list of registered asset types."""
    return list(_asset_type_plugins.keys())

def upload_asset(local_file_path: str, metadata: Dict[str, Any], asset_type: str = 'generic') -> Dict[str, Any]:
    """
    Uploads a file to S3 and its metadata to the in-memory store.
    If a plugin is registered, it delegates to its on_upload method.
    """
    if not s3_client or not S3_BUCKET:
        raise ConnectionError("S3 is not configured. Cannot upload asset.")

    file_name = os.path.basename(local_file_path)
    # The S3 key determines the "folder" structure. e.g., "cyoa/my_file.png"
    s3_key = f"{asset_type}/{file_name}"
    
    asset_record = {
        'id': len(ASSET_STORE) + 1,
        'file_path': local_file_path,
        'metadata': metadata.copy(),
        'type': asset_type
    }

    # --- S3 Upload Logic ---
    try:
        logging.info(f"Attempting to upload {local_file_path} to s3://{S3_BUCKET}/{s3_key}")
        s3_client.upload_file(local_file_path, S3_BUCKET, s3_key)
        logging.info("Upload successful.")
        # CRITICAL: Add the s3_key to the metadata upon successful upload.
        asset_record['metadata']['s3_key'] = s3_key
    except FileNotFoundError:
        logging.error(f"Local file not found: {local_file_path}")
        raise
    except NoCredentialsError:
        logging.error("AWS credentials not found. Please configure them.")
        raise
    except ClientError as e:
        logging.error(f"An S3 client error occurred: {e}", exc_info=True)
        raise

    # Delegate to plugin if it exists
    plugin = _asset_type_plugins.get(asset_type)
    if plugin and hasattr(plugin, 'on_upload'):
        plugin.on_upload(asset_record)
        
    ASSET_STORE.append(asset_record)
    return asset_record

def list_assets(asset_type: str = None) -> List[Dict[str, Any]]:
    """Lists all assets, optionally filtering by asset_type."""
    if asset_type:
        return [a for a in ASSET_STORE if a['type'] == asset_type]
    return ASSET_STORE.copy()

def purchase_asset(asset_id: int, buyer_id: str, credits: int) -> bool:
    """Simulates a purchase workflow."""
    for a in ASSET_STORE:
        if a['id'] == asset_id:
            a['metadata']['owned_by'] = buyer_id
            a['metadata']['spent_credits'] = credits
            return True
    return False

# --- CYOA Plugin ---
class CYOAPlugin:
    def on_upload(self, asset_record: dict) -> None:
        """Enforces CYOA filename conventions and extracts graph metadata."""
        fn = os.path.basename(asset_record['file_path'])
        meta = asset_record['metadata']
        if fn.startswith('NODE'):
            meta['node_id'] = fn.split('_')[1].split('.')[0]
            meta['graph_role'] = 'node'
        elif fn.startswith('EDGE'):
            parts = fn.replace('EDGE_', '').split('_to_')
            src, dst = parts[0], parts[1].split('.')[0]
            meta['src_node'], meta['dst_node'] = src, dst
            meta['graph_role'] = 'edge'
        elif fn.startswith('HOPTO'):
            target = fn.replace('HOPTO_', '').split('.')[0]
            meta['hop_target'] = target
            meta['graph_role'] = 'end'
        else:
            meta['graph_role'] = 'unknown'

# Register the CYOA plugin
register_asset_type('cyoa', CYOAPlugin())

# --- Streamlit App ---
st.title("Digital Asset Banking (v4.0)")

# Check if S3 is configured and display a warning if not.
if not S3_BUCKET or not s3_client:
    st.error("S3 connection is not configured. Please set AWS environment variables and restart.")
else:
    st.sidebar.success(f"Connected to S3 Bucket: {S3_BUCKET}")

menu = ["View Assets", "Upload Asset", "Purchase Asset"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "View Assets":
    st.header("All Assets")
    assets = list_assets()
    if not assets:
        st.info("No assets have been uploaded yet.")
    for a in assets:
        st.write(f"ID: {a['id']} | Name: {a['metadata'].get('name')} | Type: {a['type']}")
        # Display the S3 key if it exists
        if 's3_key' in a['metadata']:
            st.write(f"> S3 Location: `s3://{S3_BUCKET}/{a['metadata']['s3_key']}`")
        st.write("---")

elif choice == "Upload Asset":
    st.header("Upload New Asset")
    uploaded_file = st.file_uploader("Choose a file to upload")
    name = st.text_input("Asset Name")
    types = ["generic"] + get_registered_types()
    asset_type = st.selectbox("Asset Type", types)
    
    if st.button("Upload"):
        if uploaded_file and name:
            # Save the uploaded file to a temporary local path
            temp_file_path = os.path.join(".", uploaded_file.name)
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # --- UI Error Handling ---
            try:
                with st.spinner('Uploading to S3...'):
                    rec = upload_asset(temp_file_path, {"name": name}, asset_type=asset_type)
                st.success(f"Successfully Uploaded Asset!")
                st.json(rec) # Display the full record in a nice format
            except Exception as e:
                st.error(f"Upload failed: {e}")
            finally:
                # Clean up the temporary local file
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
        else:
            st.warning("Please provide both a file and an asset name.")

elif choice == "Purchase Asset":
    st.header("Purchase Asset")
    aid = st.number_input("Asset ID", min_value=1, step=1)
    buyer = st.text_input("Buyer ID")
    credits = st.number_input("Credits to spend", min_value=0, step=1)
    if st.button("Purchase"):
        ok = purchase_asset(aid, buyer, credits)
        st.success("Purchase recorded!" if ok else "Asset not found.")

