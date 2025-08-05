# Digital Asset Banking (DAB) - Snowflake Data Model
> CONTEXT FILE: This document provides the data model specification for the Digital Asset Banking platform

## Executive Summary
This context file defines the star schema data model for the Digital Asset Banking (DAB) platform. The model consists of a central fact table tracking asset transactions and three dimension tables for assets, users, and asset types. The document includes ERD, table definitions, DDL scripts, ETL logic, and semantic views.

## Quick Navigation
- Entity Relationship Diagram
- Table Definitions
- DDL Scripts
- ETL Logic
- Semantic Views

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
    4. Insert a corresponding record into `FCT_ASSET_TRANSACTIONS` with `TRANSACTION_TYPE` = `'