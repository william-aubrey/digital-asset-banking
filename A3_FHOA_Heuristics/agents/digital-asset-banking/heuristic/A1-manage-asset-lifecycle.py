# A1-manage-asset-lifecycle.py
"""
The primary user interface for the Digital Asset Banking (DAB) project.
This application consolidates S3 asset uploads and Snowflake data warehousing
into a single, multi-page Streamlit application, serving as the official
entrypoint for the 'digital-asset-banking' agent.
"""

import os
import tempfile
import json
import boto3
from datetime import datetime, timezone
import logging
from pathlib import Path
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, ClientError
from typing import Dict, Any, List
import streamlit as st
import pandas as pd

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Environment Variable Loading ---
# Load the .env file located in the same directory as this script (the 'heuristic' folder).
# This makes the application's environment configuration self-contained. It should contain
# AWS_S3_BUCKET and AWS_REGION.
dotenv_path = Path(__file__).parent / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
    logging.info(f"✅ Loaded environment variables from: {dotenv_path}")
else:
    logging.warning(f"⚠️ .env file not found at {dotenv_path}. Relying on system environment variables.")

# --- S3 Configuration ---
S3_BUCKET = None
s3_client = None
try:
    S3_BUCKET = os.environ.get("AWS_S3_BUCKET")
    # Explicitly set the region to improve connection stability and ensure correct endpoint usage.
    AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
    s3_client = boto3.client("s3", region_name=AWS_REGION)
    logging.info(f"✅ S3 client initialized for region: {AWS_REGION}")
except Exception:
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
    
def _a121_get_or_create_sk(
    cursor: Any, table_name: str, key_column: str, value_column: str, value: str
) -> int:
    """
    A1.2.1: A utility function that retrieves an existing surrogate key for a given business key or creates a new one if it doesn't exist.
    Generic helper to get a surrogate key from a dimension table, creating the record if it doesn't exist.
    This is a simplified approach suitable for a single-user app; for high concurrency, a MERGE statement would be better.
    """
    # Check if it exists
    cursor.execute(f"SELECT {key_column} FROM {table_name} WHERE {value_column} = ?", (value,))
    result = cursor.fetchone()
    if result:
        return result[0]
    
    # If not, insert it
    logging.info(f"Creating new entry in {table_name} for value: {value}")
    cursor.execute(f"INSERT INTO {table_name} ({value_column}) VALUES (?)", (value,))
    
    # Re-query to get the new key
    cursor.execute(f"SELECT {key_column} FROM {table_name} WHERE {value_column} = ?", (value,))
    result = cursor.fetchone()
    if not result:
        raise Exception(f"Failed to create and retrieve {key_column} from {table_name} for value: {value}")
    return result[0]

def _get_or_create_asset_type_sk(cursor: Any, asset_type_name: str) -> int:
    """Gets the surrogate key for an asset type, creating it if it doesn't exist."""
    return _a121_get_or_create_sk(cursor, "DIM_ASSET_TYPES", "ASSET_TYPE_SK", "ASSET_TYPE_NAME", asset_type_name)

def _get_or_create_user_sk(cursor: Any, user_nk: str) -> int:
    """Gets the surrogate key for a user, creating it if it doesn't exist."""
    return _a121_get_or_create_sk(cursor, "DIM_USERS", "USER_SK", "USER_NK", user_nk)

def a12_process_new_asset_upload(
    snowflake_connection: Any, file_obj: Any, file_name: str, metadata: Dict[str, Any], 
    asset_type: str = 'generic', uploader_id: str = 'default_uploader'
) -> Dict[str, Any]:
    """
    A1.2: Handles the validation, S3 upload, and database metadata registration for a new asset.
    
    Uploads a file-like object to S3 and writes its metadata to the Snowflake star schema.
    This is now wrapped in a transaction to ensure atomicity of database writes.
    """
    if not s3_client or not S3_BUCKET:
        raise ConnectionError("S3 is not configured. Cannot upload asset.")
    if not snowflake_connection:
        raise ConnectionError("Snowflake is not configured. Cannot write metadata.")

    # The S3 key determines the "folder" structure. e.g., "cyoa/my_file.png"
    s3_key = f"{asset_type}/{file_name}"

    asset_record = {
        'file_path': file_name, # Use the name for metadata purposes
        'metadata': metadata.copy(),
        'type': asset_type
    }

    try:
        logging.info(f"Attempting to upload file '{file_name}' to s3://{S3_BUCKET}/{s3_key}")
        # Use upload_fileobj for in-memory file-like objects from Streamlit
        file_obj.seek(0) # Ensure we're at the start of the file stream
        s3_client.upload_fileobj(file_obj, S3_BUCKET, s3_key)
        logging.info("Upload successful.")
        # CRITICAL: Add the s3_key to the metadata upon successful upload.
        asset_record['metadata']['s3_key'] = s3_key
    except (NoCredentialsError, ClientError) as e:
        logging.error(f"An S3 client error occurred: {e}", exc_info=True)
        raise

    plugin = _asset_type_plugins.get(asset_type)
    if plugin and hasattr(plugin, 'on_upload'):
        plugin.on_upload(asset_record)

    # --- Snowflake Star Schema INSERT Logic ---
    # This entire block is now a single transaction.
    with snowflake_connection.cursor() as cur:
        try:
            cur.execute("BEGIN TRANSACTION;")
            logging.info(f"Snowflake transaction started for asset: {file_name}")

            # 1. Get/Create ASSET_TYPE_SK
            asset_type_sk = _get_or_create_asset_type_sk(cur, asset_type)

            # 2. Get/Create uploader's USER_SK
            owner_user_sk = _get_or_create_user_sk(cur, uploader_id)

            # 3. Insert into DIM_ASSETS
            asset_name = metadata.get("name", "N/A")
            graph_role = asset_record['metadata'].get('graph_role') # From CYOA plugin
            upload_timestamp = datetime.now(timezone.utc)

            dim_assets_sql = """
            INSERT INTO DIM_ASSETS (S3_KEY, ASSET_NAME, ASSET_TYPE_SK, CURRENT_OWNER_USER_SK, GRAPH_ROLE, UPLOAD_TIMESTAMP)
            VALUES (?, ?, ?, ?, ?, ?);
            """
            cur.execute(dim_assets_sql, (s3_key, asset_name, asset_type_sk, owner_user_sk, graph_role, upload_timestamp))
            
            # 4. Get the new ASSET_SK for the fact table record
            cur.execute("SELECT ASSET_SK FROM DIM_ASSETS WHERE S3_KEY = ?", (s3_key,))
            asset_sk_result = cur.fetchone()
            if not asset_sk_result:
                raise Exception(f"Failed to retrieve new ASSET_SK for S3 key {s3_key}")
            asset_sk = asset_sk_result[0]
            
            # 5. Insert 'UPLOAD' event into FCT_ASSET_TRANSACTIONS
            fct_sql = """
            INSERT INTO FCT_ASSET_TRANSACTIONS (ASSET_SK, TRANSACTION_TYPE, TRANSACTION_TIMESTAMP)
            VALUES (?, ?, ?);
            """
            cur.execute(fct_sql, (asset_sk, 'UPLOAD', upload_timestamp))
            cur.execute("COMMIT;")
            logging.info(f"Successfully inserted asset '{asset_name}' and committed to Snowflake.")
        except Exception:
            logging.error(f"An error occurred during Snowflake metadata insertion for asset {file_name}. Rolling back.", exc_info=True)
            cur.execute("ROLLBACK;")
            raise # Re-raise the exception to notify the user and potentially trigger cleanup

    return asset_record # Return the record for UI display

def a13_execute_asset_purchase(
    snowflake_connection: Any, asset_sk: int, buyer_id: str, credits: int
) -> bool:
    """
    A1.3: Updates asset ownership and records the transaction in the database.
    
    This is now wrapped in a transaction to ensure atomicity.
    """
    if not snowflake_connection:
        raise ConnectionError("Snowflake is not configured. Cannot execute purchase.")

    logging.info(f"Attempting to purchase asset SK {asset_sk} for buyer {buyer_id}.")

    # Use a single cursor for the entire transaction
    with snowflake_connection.cursor() as cur:
        try:
            cur.execute("BEGIN TRANSACTION;")
            logging.info("Transaction started.")

            # 1. Get/Create the buyer's USER_SK
            buyer_user_sk = _get_or_create_user_sk(cur, buyer_id)

            # 2. Update the asset's owner in DIM_ASSETS
            update_sql = "UPDATE DIM_ASSETS SET CURRENT_OWNER_USER_SK = ? WHERE ASSET_SK = ?;"
            cur.execute(update_sql, (buyer_user_sk, asset_sk))
            
            if cur.rowcount == 0:
                logging.error(f"Asset with SK {asset_sk} not found in DIM_ASSETS. Rolling back.")
                cur.execute("ROLLBACK;")
                return False

            # 3. Insert 'PURCHASE' event into FCT_ASSET_TRANSACTIONS
            transaction_timestamp = datetime.now(timezone.utc)
            fct_sql = """
            INSERT INTO FCT_ASSET_TRANSACTIONS (ASSET_SK, BUYER_USER_SK, TRANSACTION_TYPE, CREDITS_SPENT, TRANSACTION_TIMESTAMP)
            VALUES (?, ?, ?, ?, ?);
            """
            cur.execute(fct_sql, (asset_sk, buyer_user_sk, 'PURCHASE', credits, transaction_timestamp))
            
            cur.execute("COMMIT;")
            logging.info(f"Transaction for asset SK {asset_sk} committed successfully.")
            return True
        except Exception:
            logging.error(f"An error occurred during the purchase transaction for asset SK {asset_sk}. Rolling back.", exc_info=True)
            cur.execute("ROLLBACK;")
            # Re-raise the exception so the UI can display a generic error message
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

def a11_display_asset_marketplace(snowflake_conn: Any) -> None:
    """
    A1.1: Queries the data warehouse to present a view of available assets to the user.
    """
    st.header("❄️ Asset Marketplace from Data Warehouse")
    if not snowflake_conn:
        st.error("Cannot display marketplace. Please configure your Snowflake connection in secrets.toml.")
        return

    try:
        # Use the correct dimension table name from the data model
        table_name = "DIM_ASSETS"
        db_name = st.secrets.connections.snowflake.database
        schema_name = st.secrets.connections.snowflake.schema
        fully_qualified_table_name = f'"{db_name}"."{schema_name}"."{table_name}"'

        # Query the dimension table, ordering by the surrogate key
        query = f"SELECT * FROM {fully_qualified_table_name} ORDER BY ASSET_SK DESC LIMIT 100;"
        st.info(f"Running query:\n```sql\n{query}\n```")

        df = snowflake_conn.query(query, ttl=600)
        st.dataframe(df, use_container_width=True)
        st.success(f"Successfully displayed {len(df)} assets from `{fully_qualified_table_name}`.")
    except Exception as e:
        st.error(f"Failed to query Snowflake. Please check if the table exists and the user role has permissions.")
        st.exception(e)

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
    a11_display_asset_marketplace(snowflake_conn)

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
                try:
                    with st.spinner('Uploading to S3...'):
                        # Pass the file-like object from Streamlit directly
                        rec = a12_process_new_asset_upload(
                            snowflake_connection=snowflake_conn,
                            file_obj=uploaded_file,
                            file_name=uploaded_file.name,
                            metadata={"name": name},
                            asset_type=asset_type
                        )
                    st.success("✅ Asset uploaded successfully!")
                    st.json(rec, expanded=False)
                    # Clear the connection cache to ensure the marketplace view is updated
                    st.cache_data.clear()
                except ClientError as e:
                    error_code = e.response.get("Error", {}).get("Code")
                    st.error(f"An S3 error occurred: {error_code}")
                    st.write("Please check your AWS credentials, region, and bucket permissions.")
                    st.exception(e)
                    logging.error("S3 Upload failed with ClientError.", exc_info=True)
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
        # The UI should ask for the Asset's Surrogate Key (SK)
        asset_sk_to_purchase = st.number_input("Asset SK to Purchase", min_value=1, step=1)
        buyer = st.text_input("Buyer ID", "test_user")
        cost = st.number_input("Credits to Spend", 10)
        if st.button("Execute Purchase"):
            try:
                with st.spinner(f"Processing purchase for asset {asset_sk_to_purchase}..."):
                    success = a13_execute_asset_purchase(
                        snowflake_connection=snowflake_conn,
                        asset_sk=asset_sk_to_purchase,
                        buyer_id=buyer,
                        credits=cost
                    )
                if success:
                    st.success(f"Asset {asset_sk_to_purchase} purchased by {buyer}!")
                    st.balloons()
                    # Clear the connection cache to ensure the marketplace view is updated
                    st.cache_data.clear()
                else:
                    st.error(f"Could not find or purchase asset with SK {asset_sk_to_purchase}.")
            except Exception as e:
                st.error("An error occurred during the purchase.")
                st.exception(e)