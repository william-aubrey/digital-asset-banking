sql
-- ================================================================================================
-- Snowflake DDL Script for Digital Asset Banking (DAB) Semantic View
-- ================================================================================================
-- Prequisite: This script should be run by a user with the DAB_ADMIN role
-- after the base tables have been created.
-- ================================================================================================

USE ROLE DAB_ADMIN;
USE WAREHOUSE DAB_WAREHOUSE;
USE SCHEMA DAB_DATABASE.DAB_SCHEMA;

CREATE OR REPLACE SEMANTIC VIEW VW_DAB_SEMANTIC
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

    -- Define dimensions (descriptive attributes for slicing and dicing)
    DIMENSIONS (
        assets.ASSET_NAME AS asset_name,
        types.ASSET_TYPE_NAME AS asset_type,
        assets.GRAPH_ROLE AS graph_role,
        fct.TRANSACTION_TYPE AS transaction_type,
        fct.TRANSACTION_TIMESTAMP AS transaction_time,
        users.USER_NK AS user_id
    )

    -- Define measures (quantifiable metrics for aggregation)
    MEASURES (
        total_credits_spent AS SUM(fct.CREDITS_SPENT),
        transaction_count AS COUNT(fct.TRANSACTION_PK)
    );
