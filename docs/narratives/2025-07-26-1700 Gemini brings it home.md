````markdown
---
date: 2025-07-26
timestamp: "2025-07-26T18:59:00Z"
agent: Gemini

session_metadata:
  session_id: "dab-debug-s3-connect-2025-07-26"
  started_at: "2025-07-26T17:30:00Z"
  last_updated: "2025-07-26T18:59:00Z"
  duration_minutes: 89
  model: "Gemini"
  files_generated:
    - DAB_4.0.py
    - infrastructure.yaml
---

# 2025-07-26: DAB S3 Integration Debugging

### Saturday Evening

This document captures the step-by-step debugging process of connecting the **Digital Asset Banking (DAB)** Streamlit application to its AWS S3 backend. The session evolved from fixing CloudFormation errors to deep-diving into application code and environment configuration.

The primary objective was to take the functional `DAB_3.0.py` application and enable it to upload files to the S3 bucket provisioned by the `infrastructure.yaml` CloudFormation template.

---

## 1. Final Working Commands (Windows CMD)

For future reference, here is the complete, working sequence to launch the application:

```cmd
:: 1. Set the required environment variables for the session
set AWS_S3_BUCKET=digital-assets-william-ryan-aubrey
set AWS_ACCESS_KEY_ID=[Your-Access-Key-ID]
set AWS_SECRET_ACCESS_KEY=[Your-Secret-Access-Key]
set AWS_DEFAULT_REGION=us-east-1

:: 2. Ensure the Boto3 library is installed
pip install boto3

:: 3. Run the application
streamlit run DAB_4.0.py
````

-----

## 2\. The Debugging Journey: A Step-by-Step Resolution

We encountered and resolved a series of cascading errors. Each step revealed a new layer of the problem.

1.  **CloudFormation Rollback**

      * **Error Encountered:** The template failed with `CREATE_FAILED` because the `iam-dab-agent` user already existed from a previous failed deployment.
      * **Resolution:** Performed a full cleanup by deleting the failed stack (`aws cloudformation delete-stack`) and manually deleting the orphaned IAM user (`aws iam delete-user`).

2.  **Silent Upload Failure**

      * **Error Encountered:** The app ran but didn't upload files. A review of the terminal screenshot showed that the `env` command was not recognized by Windows Command Prompt.
      * **Resolution:** The AWS credentials were never set. The command syntax was incorrect for the operating system. Switched to `set VAR=val`.

3.  **Missing S3 Logic in Code**

      * **Error Encountered:** A code review of `DAB_3.0.py` revealed it had no code to perform an S3 upload. It only managed an in-memory list.
      * **Resolution:** The script was completely rewritten as `DAB_4.0.py` to include full `boto3` S3 integration, error handling, and UI feedback.

4.  **Module Not Found**

      * **Error Encountered:** The new `DAB_4.0.py` script immediately failed with `ModuleNotFoundError: No module named 'boto3'`.
      * **Resolution:** The required AWS SDK for Python was not installed. Installed it using `pip install boto3`.

5.  **AWS Signature Mismatch**

      * **Error Encountered:** The final error was `SignatureDoesNotMatch`. This is a definitive credential error.
      * **Resolution:** The `AWS_SECRET_ACCESS_KEY` being set in the terminal was incorrect. Carefully re-copying and setting the correct key resolved the issue.

6.  **SUCCESS**

      * **Outcome:** The application successfully connected to AWS and uploaded the file to the correct S3 bucket and folder. The session goal was achieved.

-----

## 3\. Key Learnings

  - **Idempotency is Key**: CloudFormation templates must be designed to handle re-runs (idempotency) by using conditions and parameters to avoid "resource already exists" errors.
  - **Environment Matters**: Command-line syntax differs significantly between operating systems (e.g., `env` on Linux vs. `set` on Windows).
  - **Silent Failures Point to Deeper Issues**: When an application fails without an error message, it often indicates a fundamental problem, such as missing credentials or flawed application logic.
  - **Check Dependencies**: `ModuleNotFoundError` is a straightforward sign that a required library needs to be installed via `pip`.
  - **SignatureDoesNotMatch = Credential Error**: This specific AWS error almost always means the `SecretAccessKey` is wrong.

-----

## Appendices

### Appendix A: Final Application Code (DAB\_4.0.py)

```python
# DAB_4.0.py
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

```

### Appendix B: Final CloudFormation Template (infrastructure.yaml)

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: >
  CloudFormation template to create or update an S3 bucket and manage an IAM user
  (optionally using existing resources). Supports safe updates without failures when
  resources already exist.

Parameters:
  BucketName:
    Type: String
    Description: S3 bucket name (created if UseExistingBucket is false)
    Default: digital-assets-william-ryan-aubrey
  UseExistingBucket:
    Type: String
    AllowedValues: ["true","false"]
    Default: "false"
    Description: "Set to 'true' to use an existing bucket; 'false' to create a new one."
  UserName:
    Type: String
    Description: IAM user name to create if UseExistingUser is 'false'
    Default: iam-dab-agent
  UseExistingUser:
    Type: String
    AllowedValues: ["true","false"]
    Default: "false"
    Description: "Set to 'true' to use an existing IAM user; 'false' to create a new one."
  ExistingUserArn:
    Type: String
    Description: ARN of an existing IAM user (required if UseExistingUser is 'true')
    Default: ""

Conditions:
  CreateBucket: !Equals [ !Ref UseExistingBucket, "false" ]
  CreateUser:   !Equals [ !Ref UseExistingUser,   "false" ]

Resources:
  AssetBucket:
    Condition: CreateBucket
    Type: AWS::S3::Bucket
    DeletionPolicy: Retain
    UpdateReplacePolicy: Retain
    Properties:
      BucketName: !Ref BucketName
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

  AssetBucketPolicy:
    Type: AWS::S3::BucketPolicy
    DeletionPolicy: Retain
    UpdateReplacePolicy: Retain
    Properties:
      Bucket: !Ref BucketName
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Sid: AllowUserList
            Effect: Allow
            Principal:
              AWS: !If [ CreateUser, !GetAtt AssetUser.Arn, !Ref ExistingUserArn ]
            Action:
              - s3:ListBucket
            Resource: !Sub arn:aws:s3:::${BucketName}
          - Sid: AllowUserObjects
            Effect: Allow
            Principal:
              AWS: !If [ CreateUser, !GetAtt AssetUser.Arn, !Ref ExistingUserArn ]
            Action:
              - s3:GetObject
              - s3:PutObject
            Resource:
              - !Sub arn:aws:s3:::${BucketName}/*

  AssetUser:
    Condition: CreateUser
    Type: AWS::IAM::User
    DeletionPolicy: Retain
    Properties:
      UserName: !Ref UserName
      Path: /

  AssetUserPolicy:
    Condition: CreateUser
    Type: AWS::IAM::Policy
    DeletionPolicy: Retain
    Properties:
      PolicyName: S3AccessPolicy
      Users: [ !Ref AssetUser ]
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Action:
              - s3:ListBucket
              - s3:GetObject
              - s3:PutObject
            Resource:
              - !Sub arn:aws:s3:::${BucketName}
              - !Sub arn:aws:s3:::${BucketName}/*

  AssetUserAccessKey:
    Condition: CreateUser
    Type: AWS::IAM::AccessKey
    DeletionPolicy: Retain
    Properties:
      UserName: !Ref AssetUser

Outputs:
  BucketName:
    Description: S3 bucket name in use
    Value: !Ref BucketName

  IAMUserArn:
    Description: ARN of the IAM user (created or existing)
    Value: !If [ CreateUser, !GetAtt AssetUser.Arn, !Ref ExistingUserArn ]

  AccessKeyId:
    Condition: CreateUser
    Description: Access Key ID for the new user
    Value: !Ref AssetUserAccessKey

  SecretAccessKey:
    Condition: CreateUser
    Description: Secret Access Key for the new user
    Value: !GetAtt AssetUserAccessKey.SecretAccessKey
```

-----

## Epilogue

This document captures the final artifacts and metadata from our debugging session.

### Session Metadata

```yaml
session_metadata:
  session_id: "dab-debug-s3-connect-2025-07-26"
  agent: "Gemini"
  start_time: "2025-07-26T17:30:00Z" # Estimated
  end_time: "2025-07-26T18:59:00Z"
  duration_minutes: 89
  timezone: "EDT"
  location: "Charlotte, North Carolina, United States"
  key_technologies:
    - Python
    - Streamlit
    - AWS S3
    - AWS IAM
    - AWS CloudFormation
    - Boto3
  final_artifacts:
    - "DAB_4.0.py"
    - "infrastructure.yaml"
```

```
```