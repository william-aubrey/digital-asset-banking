# lib.py
import os
import boto3
from datetime import datetime, timezone
import logging
from pathlib import Path
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, ClientError
from typing import Dict, Any, List

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Environment Variable Loading ---
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
    AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
    s3_client = boto3.client("s3", region_name=AWS_REGION)
    logging.info(f"✅ S3 client initialized for region: {AWS_REGION}")
except Exception:
    logging.error("S3 client could not be initialized. Ensure AWS credentials and region are set.", exc_info=True)

# --- Core DAB Platform (In-Memory Operations) ---
_asset_type_plugins: Dict[str, Any] = {}

def register_asset_type(asset_type: str, plugin: Any) -> None:
    """Register a plugin for a specific asset_type."""
    _asset_type_plugins[asset_type] = plugin

def get_registered_types() -> List[str]:
    """Return a list of registered asset types."""
    return list(_asset_type_plugins.keys())
    
def _get_or_create_sk(cursor: Any, table_name: str, key_column: str, value_column: str, value: str) -> int:
    """
    Generic helper to get a surrogate key from a dimension table, creating the record if it doesn't exist.
    """
    cursor.execute(f"SELECT {key_column} FROM {table_name} WHERE {value_column} = ?", (value,))
    result = cursor.fetchone()
    if result:
        return result[0]
    
    logging.info(f"Creating new entry in {table_name} for value: {value}")
    cursor.execute(f"INSERT INTO {table_name} ({value_column}) VALUES (?)", (value,))
    
    cursor.execute(f"SELECT {key_column} FROM {table_name} WHERE {value_column} = ?", (value,))
    result = cursor.fetchone()
    if not result:
        raise Exception(f"Failed to create and retrieve {key_column} from {table_name} for value: {value}")
    return result[0]

def _get_or_create_asset_type_sk(cursor: Any, asset_type_name: str) -> int:
    """Gets the surrogate key for an asset type, creating it if it doesn't exist."""
    return _get_or_create_sk(cursor, "DIM_ASSET_TYPES", "ASSET_TYPE_SK", "ASSET_TYPE_NAME", asset_type_name)

def _get_or_create_user_sk(cursor: Any, user_nk: str) -> int:
    """Gets the surrogate key for a user, creating it if it doesn't exist."""
    return _get_or_create_sk(cursor, "DIM_USERS", "USER_SK", "USER_NK", user_nk)

def upload_asset(snowflake_connection: Any, file_obj: Any, file_name: str, metadata: Dict[str, Any], asset_type: str = 'generic', uploader_id: str = 'default_uploader') -> Dict[str, Any]:
    """
    Uploads a