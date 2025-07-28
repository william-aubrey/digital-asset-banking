# Snowflake RBAC Design for Digital Asset Banking

This document outlines the Role-Based Access Control (RBAC) model for the DAB platform in Snowflake, ensuring security and compliance with project specifications.

## 1. Role Definitions

Based on the project's user stories and specifications, we will create the following functional roles:

* **`DAB_PLATFORM_ADMIN`**: The top-level administrative role for the DAB project. It has the necessary privileges to create other roles, users, and databases.
* **`DAB_APP_USER`**: A service account role for the Streamlit/backend application.
* **`DAB_ANALYST`**: A role for business intelligence and analytics.
* **`DAB_ADMIN`**: A role for system administrators to manage the application's database objects.
* **`DAB_REGULATOR`**: A highly restricted, read-only role for auditors.

## 2. User Definitions

* **Platform Administrator (Human User)**: The `DAB_PLATFORM_ADMIN` role will be granted directly to your own user account for initial setup and management.
    * `GRANT ROLE DAB_PLATFORM_ADMIN TO USER "WAUBREY@PHDATA.IO";`
* **Application Service User**: This user will be used by the Streamlit application to connect to Snowflake.
    * `CREATE USER SVC_DAB_APP PASSWORD = '<secure_password_placeholder>' DEFAULT_ROLE = DAB_APP_USER DEFAULT_WAREHOUSE = DAB_WAREHOUSE COMMENT = 'Service account for the DAB application backend.';`
* **Analyst Service User**: This user can be used by BI tools (like Tableau or Sigma) to connect for reporting.
    * `CREATE USER SVC_DAB_ANALYST PASSWORD = '<secure_password_placeholder>' DEFAULT_ROLE = DAB_ANALYST DEFAULT_WAREHOUSE = DAB_WAREHOUSE COMMENT = 'Service account for BI and analytics.';`
* **Admin Service User**: This user can be used for automated administrative or operational scripts.
    * `CREATE USER SVC_DAB_ADMIN PASSWORD = '<secure_password_placeholder>' DEFAULT_ROLE = DAB_ADMIN DEFAULT_WAREHOUSE = DAB_WAREHOUSE COMMENT = 'Service account for administrative tasks.';`

_**Note on Passwords:** For this design, we are using placeholders. In a real implementation, we would generate strong, random passwords and store them securely in a secrets manager._

## 3. Privilege Model

### `DAB_PLATFORM_ADMIN` Privileges
This role is for initial setup and user/role management.

* `GRANT CREATE DATABASE ON ACCOUNT TO ROLE DAB_PLATFORM_ADMIN;`
* `GRANT CREATE WAREHOUSE ON ACCOUNT TO ROLE DAB_PLATFORM_ADMIN;`
* `GRANT CREATE USER ON ACCOUNT TO ROLE DAB_PLATFORM_ADMIN;`
* `GRANT CREATE ROLE ON ACCOUNT TO ROLE DAB_PLATFORM_ADMIN;`
* `GRANT MANAGE GRANTS ON ACCOUNT TO ROLE DAB_PLATFORM_ADMIN;`

### `DAB_APP_USER` Privileges
This role needs to be able to read and write to the application's tables.

* **Database & Schema Access**:
    * `GRANT USAGE ON DATABASE DAB_DATABASE TO ROLE DAB_APP_USER;`
    * `GRANT USAGE ON SCHEMA DAB_DATABASE.DAB_SCHEMA TO ROLE DAB_APP_USER;`
* **Table Access**:
    * `GRANT SELECT, INSERT, UPDATE ON TABLE DIM_ASSETS TO ROLE DAB_APP_USER;`
    * `GRANT SELECT, INSERT ON TABLE DIM_USERS TO ROLE DAB_APP_USER;`
    * `GRANT SELECT, INSERT ON TABLE DIM_ASSET_TYPES TO ROLE DAB_APP_USER;`
    * `GRANT SELECT, INSERT ON TABLE FCT_ASSET_TRANSACTIONS TO ROLE DAB_APP_USER;`

### `DAB_ANALYST` Privileges
This role needs read-only access to a curated, non-sensitive view of the data for BI and reporting.

* **Create a Secure View for Analytics**:
    * `CREATE OR REPLACE SECURE VIEW VW_ANALYTICS_ASSET_TRANSACTIONS AS SELECT TRANSACTION_PK, ASSET_SK, TRANSACTION_TYPE, CREDITS_SPENT, TRANSACTION_TIMESTAMP FROM FCT_ASSET_TRANSACTIONS;`
* **Database & Schema Access**:
    * `GRANT USAGE ON DATABASE DAB_DATABASE TO ROLE DAB_ANALYST;`
    * `GRANT USAGE ON SCHEMA DAB_DATABASE.DAB_SCHEMA TO ROLE DAB_ANALYST;`
* **View & Table Access**:
    * `GRANT SELECT ON VIEW VW_ANALYTICS_ASSET_TRANSACTIONS TO ROLE DAB_ANALYST;`
    * `GRANT SELECT ON TABLE DIM_ASSETS TO ROLE DAB_ANALYST;`
    * `GRANT SELECT ON TABLE DIM_ASSET_TYPES TO ROLE DAB_ANALYST;`

### `DAB_ADMIN` Privileges
This role will own all application objects and manage the warehouse.

* **Warehouse Access**:
    * `GRANT USAGE, MONITOR ON WAREHOUSE DAB_WAREHOUSE TO ROLE DAB_ADMIN;`
* **Database Ownership**:
    * `GRANT OWNERSHIP ON DATABASE DAB_DATABASE TO ROLE DAB_ADMIN;`
* **Schema Ownership**:
    * `GRANT OWNERSHIP ON ALL SCHEMAS IN DATABASE DAB_DATABASE TO ROLE DAB_ADMIN;`
* **Table Ownership**:
    * `GRANT OWNERSHIP ON ALL TABLES IN SCHEMA DAB_DATABASE.DAB_SCHEMA TO ROLE DAB_ADMIN;`

## 4. Object Ownership and Hierarchy

All DAB-related objects (databases, schemas, tables) will be owned by the `DAB_ADMIN` role, which will then grant specific privileges to other roles. The `DAB_PLATFORM_ADMIN` will create the initial roles and the `DAB_ADMIN` user.

## 5. Implementation Script

*(This section will be generated from our design)*