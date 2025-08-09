# IDEF0 Model: A1 Manage Asset Lifecycle

*   **Version**: 1.0
*   **Date**: 2025-08-09
*   **Source Code**: `A3_FHOA_Heuristics/agents/digital-asset-banking/heuristic/main-gemini.py`
*   **Parent Model**: `A-0-digital-asset-banking-organism.md`

This document serves as the implementation-level "digital twin" for the `A1: Manage Asset Lifecycle` function.

---

## Table of Contents

*   A1: Manage Asset Lifecycle (Context)
*   A1: Decomposition of "Manage Asset Lifecycle"
    *   A1.1: Display Asset Marketplace (node A11)
    *   A1.2: Process New Asset Upload (node A12))
    *   A1.3: Execute Asset Purchase (node A13))
*   A1.2: Decomposition of "Process New Asset Upload"
    *   A1.2.1: Get or Create Surrogate Key (node A121))
*   Appendix: SQL INSERT Statements

---

## A1: Manage Asset Lifecycle (Context)

-   **Description**: Encompasses the core user-facing activities of uploading, creating, viewing, and purchasing digital assets. Implemented primarily by `main-gemini.py`.

---

## A1: Decomposition of "Manage Asset Lifecycle"

This diagram details the primary steps a user takes when interacting with assets via the Streamlit application.

### A1.1: Display Asset Marketplace

-   **Description**: Queries the data warehouse to present a view of available assets to the user.
-   **Inputs**: (None)
-   **Controls**: (None)
-   **Outputs**: `Asset Marketplace View`
-   **Mechanisms**: `Snowflake Connection`

### A1.2: Process New Asset Upload

-   **Description**: Handles the validation, S3 upload, and database metadata registration for a new asset. Implemented by `upload_asset()`.
-   **Inputs**: `File Object`, `Asset Metadata`
-   **Controls**: `Uploader ID`, `Asset Type`
-   **Outputs**: `Uploaded Asset Confirmation`
-   **Mechanisms**: `Snowflake Connection`, `S3 Client`, `Asset Type Plugins`, `Get or Create Surrogate Key` (Call)

### A1.3: Execute Asset Purchase

-   **Description**: Updates asset ownership and records the transaction in the database. Implemented by `purchase_asset()`.
-   **Inputs**: `Asset ID to Purchase`
-   **Controls**: `Buyer ID`
-   **Outputs**: `Purchase Confirmation`
-   **Mechanisms**: `Snowflake Connection`

---

## A1.2: Decomposition of "Process New Asset Upload"

This level details the sub-functions within the asset upload process.

### A1.2.1: Get or Create Surrogate Key

-   **Description**: A utility function that retrieves an existing surrogate key for a given business key or creates a new one if it doesn't exist. Implemented by `_get_or_create_sk()`.
-   **Inputs**: `Table Name`, `Business Key`
-   **Controls**: (None)
-   **Outputs**: `Surrogate Key`
-   **Mechanisms**: `Snowflake Connection`

---

## Appendix: SQL INSERT Statements

```sql
-- Use the correct database and schema
USE DATABASE FHOA_ONTOLOGY_DB;
USE SCHEMA IDEF0_SCHEMA;

-- 1. Populate the MODELS table
INSERT INTO MODELS (MODEL_ID, MODEL_NAME) VALUES (1, 'Digital Asset Banking');

-- 2. Populate the FUNCTIONS table (The Boxes)
-- Note: PARENT_FUNCTION_ID is NULL for top-level functions or utilities.
INSERT INTO FUNCTIONS (FUNCTION_ID, MODEL_ID, FUNCTION_NAME, PARENT_FUNCTION_ID) VALUES
(1, 1, 'Manage Digital Asset Lifecycle', NULL),
(2, 1, 'Display Asset Marketplace', 1),
(3, 1, 'Process New Asset Upload', 1),
(4, 1, 'Execute Asset Purchase', 1),
(5, 1, 'Get or Create Surrogate Key', 3); -- Child of 'Process New Asset Upload'

-- 3. Populate the ENTITIES table (The Arrows)
INSERT INTO ENTITIES (ENTITY_ID, ENTITY_NAME, DESCRIPTION) VALUES
(1, 'User Menu Choice', 'The user selection from the Streamlit sidebar menu.'),
(2, 'Snowflake Connection', 'The active connection object to the Snowflake data warehouse.'),
(3, 'S3 Client', 'The Boto3 client object for interacting with AWS S3.'),
(4, 'Asset Marketplace View', 'The data displayed to the user showing available assets.'),
(5, 'File Object', 'The raw binary data of the asset being uploaded.'),
(6, 'Asset Metadata', 'User-provided information about the asset (e.g., name, description).'),
(7, 'Uploader ID', 'The unique identifier for the user uploading the asset.'),
(8, 'Asset Type', 'A string indicating the type of asset (e.g., ''CYOA_STORY'').'),
(9, 'Asset Type Plugins', 'A dictionary of specialized processing logic for different asset types.'),
(10, 'Uploaded Asset Confirmation', 'A dictionary containing the S3 key and database IDs of the new asset.'),
(11, 'Asset ID to Purchase', 'The unique identifier of the asset the user wishes to buy.'),
(12, 'Buyer ID', 'The unique identifier for the user purchasing the asset.'),
(13, 'Purchase Confirmation', 'A message or record indicating the success of the purchase transaction.'),
(14, 'Table Name', 'The name of the dimension table for a surrogate key lookup.'),
(15, 'Business Key', 'The natural key of a dimension record (e.g., user_id, asset_type_name).'),
-(16, 'Surrogate Key', 'The integer primary key for a dimension record.');

-- Connections for A1.2: Process New Asset Upload (FUNCTION_ID = 12)
INSERT INTO FUNCTION_ENTITIES (FUNCTION_ID, ENTITY_ID, ROLE, SOURCE_FUNCTION_ID) VALUES
(12, 5, 'INPUT', NULL),     -- File Object
(12, 6, 'INPUT', NULL),     -- Asset Metadata
(12, 7, 'CONTROL', NULL),   -- Uploader ID
(12, 8, 'CONTROL', NULL),   -- Asset Type
(12, 2, 'MECHANISM', NULL), -- Snowflake Connection
(12, 3, 'MECHANISM', NULL), -- S3 Client
(12, 9, 'MECHANISM', NULL), -- Asset Type Plugins
(12, 10, 'OUTPUT', NULL),  -- Uploaded Asset Confirmation
(12, 17, 'MECHANISM', 14);  -- Call to Get or Create Surrogate Key (calls function 14)

-- (Additional connections for A1.1, A1.3, and A1.2.1 would be added here)
```


