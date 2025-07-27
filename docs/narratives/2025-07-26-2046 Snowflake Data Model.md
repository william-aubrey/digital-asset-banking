# Snowflake Data Model: Digital Asset Banking

This document outlines the Snowflake data model for the **Digital Asset Banking (DAB)** platform. The model uses a star schema, which is optimized for analytic queries and reporting. It consists of a central fact table (`FCT_ASSET_TRANSACTIONS`) surrounded by descriptive dimension tables (`DIM_ASSETS`, `DIM_USERS`, and `DIM_ASSET_TYPES`).

## 1. Entity-Relationship Diagram (ERD)

The following diagram illustrates the relationships between the tables.

```mermaid
erDiagram
    DIM_USERS ||--o{ FCT_ASSET_TRANSACTIONS : "is buyer in"
    DIM_ASSETS ||--o{ FCT_ASSET_TRANSACTIONS : "is subject of"
    DIM_ASSET_TYPES ||--o{ DIM_ASSETS : "classifies"
    DIM_USERS ||--o{ DIM_ASSETS : "is current owner of"

    FCT_ASSET_TRANSACTIONS {
        NUMBER(38,0) TRANSACTION_PK "PK"
        NUMBER(38,0) ASSET_SK "FK"
        NUMBER(38,0) BUYER_USER_SK "FK"
        VARCHAR TRANSACTION_TYPE
        NUMBER CREDITS_SPENT
        TIMESTAMP_NTZ TRANSACTION_TIMESTAMP
    }

    DIM_ASSETS {
        NUMBER(38,0) ASSET_SK "PK"
        VARCHAR S3_KEY "NK"
        VARCHAR ASSET_NAME
        NUMBER(38,0) ASSET_TYPE_SK "FK"
        NUMBER(38,0) CURRENT_OWNER_USER_SK "FK"
        VARCHAR GRAPH_ROLE
        TIMESTAMP_NTZ UPLOAD_TIMESTAMP
    }

    DIM_USERS {
        NUMBER(38,0) USER_SK "PK"
        VARCHAR USER_NK "NK"
    }

    DIM_ASSET_TYPES {
        NUMBER(38,0) ASSET_TYPE_SK "PK"
        VARCHAR ASSET_TYPE_NAME
    }
```

## 2. Table Definitions

### `DIM_ASSETS`
Stores the core attributes of each unique digital asset. This is the "what" dimension.

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `ASSET_SK` | `NUMBER(38,0)` | `PK` | Surrogate key for the asset. |
| `S3_KEY` | `VARCHAR` | `NK, UNIQUE` | Natural key; the unique S3 object key for the asset file. |
| `ASSET_NAME` | `VARCHAR` | `NOT NULL` | User-provided name for the asset. |
| `ASSET_TYPE_SK` | `NUMBER(38,0)` | `FK` | Foreign key to `DIM_ASSET_TYPES`. |
| `CURRENT_OWNER_USER_SK` | `NUMBER(38,0)` | `FK` | Foreign key to `DIM_USERS`, identifying the current owner. |
| `GRAPH_ROLE` | `VARCHAR` | | Role in CYOA graph (e.g., 'node', 'edge'). |
| `UPLOAD_TIMESTAMP` | `TIMESTAMP_NTZ` | `NOT NULL` | Timestamp when the asset was first uploaded. |

### `DIM_USERS`
Stores information about users who interact with the system. This is the "who" dimension.

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `USER_SK` | `NUMBER(38,0)` | `PK` | Surrogate key for the user. |
| `USER_NK` | `VARCHAR` | `NK, UNIQUE` | Natural key; the user ID from the application. |

### `DIM_ASSET_TYPES`
A simple dimension to classify asset types.

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `ASSET_TYPE_SK` | `NUMBER(38,0)` | `PK` | Surrogate key for the asset type. |
| `ASSET_TYPE_NAME` | `VARCHAR` | `UNIQUE` | The name of the type (e.g., 'generic', 'cyoa'). |

### `FCT_ASSET_TRANSACTIONS`
The central fact table, recording every key business event (e.g., uploads, purchases).

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `TRANSACTION_PK` | `NUMBER(38,0)` | `PK` | Primary key for the transaction event. |
| `ASSET_SK` | `NUMBER(38,0)` | `FK, NOT NULL` | Foreign key to the asset involved in the transaction. |
| `BUYER_USER_SK` | `NUMBER(38,0)` | `FK` | Foreign key to the user who purchased the asset (nullable). |
| `TRANSACTION_TYPE` | `VARCHAR` | `NOT NULL` | Type of event (e.g., 'UPLOAD', 'PURCHASE'). |
| `CREDITS_SPENT` | `NUMBER(38,0)` | | The number of credits spent in a 'PURCHASE' transaction. |
| `TRANSACTION_TIMESTAMP` | `TIMESTAMP_NTZ` | `NOT NULL` | The exact time the transaction occurred. |

## 3. Snowflake DDL Script
Here is the complete SQL DDL to create the schema in Snowflake, using canonical data types.

```sql
-- Dimension for Asset Types
CREATE OR REPLACE TABLE DIM_ASSET_TYPES (
    ASSET_TYPE_SK   NUMBER(38,0) IDENTITY PRIMARY KEY,
    ASSET_TYPE_NAME VARCHAR(50) UNIQUE NOT NULL COMMENT 'The name of the type (e.g., generic, cyoa)'
);

-- Dimension for Users
CREATE OR REPLACE TABLE DIM_USERS (
    USER_SK NUMBER(38,0) IDENTITY PRIMARY KEY,
    USER_NK VARCHAR(255) UNIQUE NOT NULL COMMENT 'Natural key; the user ID from the application'
);

-- Dimension for Assets
CREATE OR REPLACE TABLE DIM_ASSETS (
    ASSET_SK                NUMBER(38,0) IDENTITY PRIMARY KEY,
    S3_KEY                  VARCHAR(1024) UNIQUE NOT NULL COMMENT 'Natural key; the unique S3 object key for the asset file',
    ASSET_NAME              VARCHAR(255) NOT NULL,
    ASSET_TYPE_SK           NUMBER(38,0) NOT NULL FOREIGN KEY (ASSET_TYPE_SK) REFERENCES DIM_ASSET_TYPES(ASSET_TYPE_SK),
    CURRENT_OWNER_USER_SK   NUMBER(38,0) FOREIGN KEY (CURRENT_OWNER_USER_SK) REFERENCES DIM_USERS(USER_SK),
    GRAPH_ROLE              VARCHAR(50),
    UPLOAD_TIMESTAMP        TIMESTAMP_NTZ NOT NULL
);

-- Fact table for all transactions
CREATE OR REPLACE TABLE FCT_ASSET_TRANSACTIONS (
    TRANSACTION_PK        NUMBER(38,0) IDENTITY PRIMARY KEY,
    ASSET_SK              NUMBER(38,0) NOT NULL FOREIGN KEY (ASSET_SK) REFERENCES DIM_ASSETS(ASSET_SK),
    BUYER_USER_SK         NUMBER(38,0) FOREIGN KEY (BUYER_USER_SK) REFERENCES DIM_USERS(USER_SK),
    TRANSACTION_TYPE      VARCHAR(50) NOT NULL COMMENT 'Type of event (e.g., UPLOAD, PURCHASE)',
    CREDITS_SPENT         NUMBER(38,0),
    TRANSACTION_TIMESTAMP TIMESTAMP_NTZ NOT NULL
);
```

## 4. ETL Loading Logic

* **On Asset Upload**:
    1. When a file is uploaded via `upload_asset` in the Streamlit app:
    2. Check if the `ASSET_TYPE_NAME` exists in `DIM_ASSET_TYPES`. If not, insert it.
    3. Insert a new record into `DIM_ASSETS` with the asset's details. The initial `CURRENT_OWNER_USER_SK` can be null or assigned to the uploader.
    4. Insert a corresponding record into `FCT_ASSET_TRANSACTIONS` with `TRANSACTION_TYPE` = `'UPLOAD'`.

* **On Asset Purchase**:
    1. When an asset is purchased via `purchase_asset`:
    2. Check if the `buyer_id` exists in `DIM_USERS` (as `USER_NK`). If not, insert it.
    3. Update the `CURRENT_OWNER_USER_SK` in `DIM_ASSETS` for the corresponding asset.
    4. Insert a new record into `FCT_ASSET_TRANSACTIONS` with `TRANSACTION_TYPE` = `'PURCHASE'`, populating `BUYER_USER_SK` and `CREDITS_SPENT`.

## 5. Snowflake Semantic Views
A semantic view provides a logical layer over the physical data model, exposing data in business-friendly terms with pre-defined relationships, dimensions, and metrics. This simplifies querying and ensures consistency for analytics.

### Semantic View DDL Script
```sql
CREATE OR REPLACE SEMANTIC VIEW DAB_SEMANTIC_VIEW
    COMMENT = 'Semantic model for Digital Asset Banking analytics.'

    -- Define logical tables from the physical star schema
    TABLES (
        fct AS FCT_ASSET_TRANSACTIONS
            PRIMARY KEY (TRANSACTION_PK),
        assets AS DIM_ASSETS
            PRIMARY KEY (ASSET_SK)
            UNIQUE (S3_KEY),
        users AS DIM_USERS
            PRIMARY KEY (USER_SK)
            UNIQUE (USER_NK),
        types AS DIM_ASSET_TYPES
            PRIMARY KEY (ASSET_TYPE_SK)
            UNIQUE (ASSET_TYPE_NAME)
    )

    -- Define the relationships (joins) between the logical tables
    RELATIONSHIPS (
        transaction_asset AS fct(ASSET_SK) REFERENCES assets(ASSET_SK),
        transaction_buyer AS fct(BUYER_USER_SK) REFERENCES users(USER_SK),
        asset_type AS assets(ASSET_TYPE_SK) REFERENCES types(ASSET_TYPE_SK),
        asset_owner AS assets(CURRENT_OWNER_USER_SK) REFERENCES users(USER_SK)
    )

    -- Define dimensions (descriptive attributes)
    DIMENSIONS (
        assets.ASSET_NAME AS asset_name,
        types.ASSET_TYPE_NAME AS asset_type,
        assets.GRAPH_ROLE AS graph_role,
        fct.TRANSACTION_TYPE AS transaction_type,
        fct.TRANSACTION_TIMESTAMP AS transaction_time,
        users.USER_NK AS user_id
    )

    -- Define metrics (quantifiable measures)
    METRICS (
        fct.total_credits_spent AS SUM(fct.CREDITS_SPENT),
        fct.transaction_count AS COUNT(fct.TRANSACTION_PK)
    );
```

## 6. Session Metadata

```yaml
session_metadata:
  session_id: "dab-datamodel-2025-07-26"
  agent: "Gemini"
  start_time: "2025-07-26T19:45:00Z"
  last_updated: "2025-07-26T20:38:00Z"
  duration_minutes: 53
  
  context_window:
    token_limit: 1000000
    estimated_tokens_used: 18500
    estimated_tokens_remaining: 981500
    percentage_used: "~1.85%"
    status: "HEALTHY. Ample context remaining."

  key_technologies_in_context:
    - Snowflake
    - SQL DDL
    - Data Modeling
    - Star Schema
    - ETL Logic
    - Semantic Views
    - Markdown Formatting
