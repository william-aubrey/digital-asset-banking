# Snowflake Data Model: Digital Asset Banking

This document outlines the data model's object hierarchy, which is implemented as a classic star schema. This design is optimized for analytics and consists of a central fact table surrounded by descriptive dimension tables.

---
## 1. Entity-Relationship Diagram (ERD)

The following diagram illustrates the relationships between the tables. The "crows-foot" notation shows the one-to-many relationships from the dimension tables to the fact table.

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

### 1a. Relationship Summary

The data model is centered around the **`FCT_ASSET_TRANSACTIONS`** table, which records every key event in the system (e.g., 'UPLOAD', 'PURCHASE').

This fact table is linked to the following dimension tables, which provide descriptive context:

* **`DIM_ASSETS`**: Each transaction in the fact table is linked to one specific asset in this dimension table. This answers the question, "What asset was this transaction for?"
* **`DIM_USERS`**: The fact table is linked to the `DIM_USERS` table in two ways:
    * Through the `BUYER_USER_SK` to identify the user who purchased an asset.
    * Indirectly through `DIM_ASSETS`, which links to `DIM_USERS` to identify the asset's current owner.
* **`DIM_ASSET_TYPES`**: The `DIM_ASSETS` table links to `DIM_ASSET_TYPES` to classify each asset (e.g., 'generic', 'cyoa').

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