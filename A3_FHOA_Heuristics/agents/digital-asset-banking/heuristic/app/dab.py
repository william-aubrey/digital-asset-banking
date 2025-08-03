# dab.py
"""
The primary user interface for the Digital Asset Banking (DAB) project.
This application consolidates S3 asset uploads and Snowflake data warehousing
into a single, multi-page Streamlit application, serving as the official
entrypoint for the 'digital-asset-banking' agent.
"""

# --- Core Imports ---
import os
import tempfile
import json
import boto3
import logging
from botocore.exceptions import NoCredentialsError, ClientError
from typing import Dict, Any, List
import streamlit as st
import pandas as pd

# --- Logging Configuration ---
# This helps print detailed errors to the terminal for easier debugging.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- S3 Configuration ---
# Initialize the S3 client and get the bucket name from environment variables.
# This is where the credentials you set in the terminal are used.
S3_BUCKET = None
s3_client = None
try:
    S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
    s3_client = boto3.client('s3')
except Exception as e:
    logging.error("S3 client could not be initialized. Ensure AWS credentials and region are set.", exc_info=True)

# --- Core DAB Platform (In-Memory Operations) ---
# NOTE: This is used for upload/purchase logic but the source of truth for viewing is Snowflake.
_asset_type_plugins: Dict[str, Any] = {}

def register_asset_type(asset_type: str, plugin: Any) -> None:
    """Register a plugin for a specific asset_type."""
    _asset_type_plugins[asset_type] = plugin

def get_registered_types() -> List[str]:
    """Return a list of registered asset types."""
    return list(_asset_type_plugins.keys())

def upload_asset(snowflake_connection: Any, local_file_path: str, metadata: Dict[str, Any], asset_type: str = 'generic') -> Dict[str, Any]:
    """
    Uploads a file to S3 and writes its metadata to the Snowflake ASSETS table.
    """
    if not s3_client or not S3_BUCKET:
        raise ConnectionError("S3 is not configured. Cannot upload asset.")
    if not snowflake_connection:
        raise ConnectionError("Snowflake is not configured. Cannot write metadata.")

    file_name = os.path.basename(local_file_path)
    # The S3 key determines the "folder" structure. e.g., "cyoa/my_file.png"
    s3_key = f"{asset_type}/{file_name}"

    # This record is for local processing and return to UI.
    # The database will generate the primary key (ASSET_ID).
    asset_record = {
        'file_path': local_file_path,
        'metadata': metadata.copy(),
        'type': asset_type
    }

    try:
        logging.info(f"Attempting to upload {local_file_path} to s3://{S3_BUCKET}/{s3_key}")
        s3_client.upload_file(local_file_path, S3_BUCKET, s3_key)
        logging.info("Upload successful.")
        # CRITICAL: Add the s3_key to the metadata upon successful upload.
        asset_record['metadata']['s3_key'] = s3_key
    except (FileNotFoundError, NoCredentialsError, ClientError) as e:
        logging.error(f"An S3 client error occurred: {e}", exc_info=True)
        raise

    plugin = _asset_type_plugins.get(asset_type)
    if plugin and hasattr(plugin, 'on_upload'):
        plugin.on_upload(asset_record)

    # --- Snowflake INSERT Logic ---    
    logging.info("Writing asset metadata to Snowflake.")
    asset_name = metadata.get("name", "N/A")
    s3_key = asset_record['metadata'].get('s3_key')
    # Convert the entire metadata dictionary to a JSON string for the VARIANT column
    metadata_json = json.dumps(asset_record['metadata'])

    sql = """
    INSERT INTO ASSETS (ASSET_NAME, ASSET_TYPE, S3_KEY, METADATA_JSON)
    VALUES (%s, %s, %s, PARSE_JSON(%s));
    """
    with snowflake_connection.cursor() as cur:
        cur.execute(sql, (asset_name, asset_type, s3_key, metadata_json))
    logging.info(f"Successfully inserted asset '{asset_name}' into Snowflake.")

    return asset_record # Return the record for UI display

def purchase_asset(snowflake_connection: Any, asset_id: int, buyer_id: str, credits: int) -> bool:
    """
    Executes a purchase transaction in Snowflake by updating the asset's metadata.
    """
    if not snowflake_connection:
        raise ConnectionError("Snowflake is not configured. Cannot execute purchase.")

    logging.info(f"Attempting to purchase asset {asset_id} for buyer {buyer_id}.")

    # Step 1: Fetch the current metadata
    select_sql = "SELECT METADATA_JSON FROM ASSETS WHERE ASSET_ID = %s;"
    try:
        with snowflake_connection.cursor() as cur:
            cur.execute(select_sql, (asset_id,))
            result = cur.fetchone()
            if not result:
                logging.error(f"Asset with ID {asset_id} not found.")
                return False
            
            current_metadata = result[0]
            if isinstance(current_metadata, str):
                current_metadata = json.loads(current_metadata)

    except Exception as e:
        logging.error(f"Failed to fetch metadata for asset {asset_id}: {e}", exc_info=True)
        raise

    # Step 2: Update the metadata object
    current_metadata['owned_by'] = buyer_id
    current_metadata['spent_credits'] = credits
    updated_metadata_json = json.dumps(current_metadata)

    # Step 3: Write the updated metadata back to Snowflake
    update_sql = "UPDATE ASSETS SET METADATA_JSON = PARSE_JSON(%s) WHERE ASSET_ID = %s;"
    try:
        with snowflake_connection.cursor() as cur:
            cur.execute(update_sql, (updated_metadata_json, asset_id))
        logging.info(f"Successfully updated asset {asset_id} for buyer {buyer_id}.")
        return True
    except Exception as e:
        logging.error(f"Failed to update asset {asset_id} in Snowflake: {e}", exc_info=True)
        raise

# --- CYOA Plugin ---
class CYOAPlugin:
    def on_upload(self, asset_record: dict) -> None:
        """Enforces CYOA filename conventions and extracts graph metadata."""
        fn = os.path.basename(asset_record['file_path'])
        meta = asset_record['metadata']
        if fn.startswith('NODE'):
            meta['node_id'] = fn.split('_')[1].split('.')[0]
            meta['graph_role'] = 'node'
        # ... (rest of CYOA logic is unchanged)

register_asset_type('cyoa', CYOAPlugin())

# --- Streamlit Marketplace Application ---
st.set_page_config(page_title="DAB Marketplace", layout="wide")
st.title("🖼️ Digital Asset Banking Marketplace")

# --- Connection Checks ---
snowflake_conn = None
if not S3_BUCKET or not s3_client:
    st.sidebar.error("S3 Not Configured")
else:
    st.sidebar.success(f"S3 Connected: {S3_BUCKET}")

try:
    snowflake_conn = st.connection("snowflake")
    st.sidebar.success("Snowflake Connected")
except Exception:
    st.sidebar.error("Snowflake Not Configured")

# --- Sidebar Navigation ---
st.sidebar.header("Navigation")
menu = ["Asset Marketplace (Snowflake)", "Upload New Asset (S3)", "Purchase Asset (Snowflake)"]
choice = st.sidebar.selectbox("Menu", menu)

# --- Page 1: Asset Marketplace (from Snowflake) ---
if choice == "Asset Marketplace (Snowflake)":
    st.header("❄️ Asset Marketplace from Data Warehouse")
    if not snowflake_conn:
        st.error("Cannot display marketplace. Please configure your Snowflake connection in secrets.toml.")
    else:
        try:
            table_name = "ASSETS"
            db_name = st.secrets.connections.snowflake.database
            schema_name = st.secrets.connections.snowflake.schema
            fully_qualified_table_name = f'"{db_name}"."{schema_name}"."{table_name}"'

            query = f"SELECT * FROM {table_name} ORDER BY ASSET_ID DESC LIMIT 100;"
            st.info(f"Running query:\n```sql\n{query}\n```")

            df = snowflake_conn.query(query, ttl=600)
            st.dataframe(df, use_container_width=True)
            st.success(f"Successfully displayed {len(df)} assets from `{fully_qualified_table_name}`.")
        except Exception as e:
            st.error(f"Failed to query Snowflake. Please check if the table exists and the user role has permissions.")
            st.exception(e)

# --- Page 2: Upload New Asset (to S3) ---
elif choice == "Upload New Asset (S3)":
    st.header("⬆️ Upload New Asset to S3")
    if not s3_client:
        st.error("Cannot upload. Please configure your S3 connection via environment variables.")
    else:
        uploaded_file = st.file_uploader("Choose a file to upload")
        name = st.text_input("Asset Name")
        types = ["generic"] + get_registered_types()
        asset_type = st.selectbox("Asset Type", types)

        if st.button("Upload Asset"):
            if uploaded_file and name:
                with tempfile.NamedTemporaryFile(suffix=f"_{uploaded_file.name}") as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    temp_file_path = tmp_file.name
                    try:
                        with st.spinner('Uploading to S3...'):
                            rec = upload_asset(
                                snowflake_connection=snowflake_conn,
                                local_file_path=temp_file_path,
                                metadata={"name": name},
                                asset_type=asset_type
                            )
                        st.success("Asset uploaded successfully!")
                        st.json(rec)
                    except Exception as e:
                        st.error(f"Upload failed: {e}")
                        logging.error("Upload process failed.", exc_info=True)
            else:
                st.warning("Please provide a file and an asset name.")

# --- Page 3: Purchase Asset (Snowflake) ---
elif choice == "Purchase Asset (Snowflake)":
    st.header("💵 Purchase Asset")
    if not snowflake_conn:
        st.error("Cannot purchase. Please configure your Snowflake connection.")
    else:
        st.info("This action will execute a transaction against the Snowflake database.")
        asset_id_to_purchase = st.number_input("Asset ID to Purchase", min_value=1, step=1)
        buyer = st.text_input("Buyer ID", "test_user")
        cost = st.number_input("Credits to Spend", 10)
        if st.button("Execute Purchase"):
            try:
                with st.spinner(f"Processing purchase for asset {asset_id_to_purchase}..."):
                    success = purchase_asset(
                        snowflake_connection=snowflake_conn,
                        asset_id=asset_id_to_purchase,
                        buyer_id=buyer,
                        credits=cost
                    )
                if success:
                    st.success(f"Asset {asset_id_to_purchase} purchased by {buyer}!")
                    st.balloons()
                else:
                    st.error(f"Could not find or purchase asset with ID {asset_id_to_purchase}.")
            except Exception as e:
                st.error("An error occurred during the purchase.")
                st.exception(e)