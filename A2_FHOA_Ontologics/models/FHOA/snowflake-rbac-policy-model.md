# Ontology Snowflake RBAC Strategy

**Author:** Gemini Code Assist (as Snowflake DBA)
**Date:** 2025-08-09
**Status:** Proposed

---

## 1. Overview

This document outlines the Role-Based Access Control (RBAC) strategy for the Ontologics database (`ONTOLOGICS_DB`) in Snowflake. The primary goal is to establish a secure, manageable, and scalable permissions model that supports the various functions of the framework, from automated provisioning to application-level data manipulation and analysis.

The core principle is the separation of concerns between object ownership, functional access, and application-level service accounts.

## 2. Core RBAC Components

Our RBAC model is built upon three main components: a dedicated service user for the application, a hierarchy of functional roles, and a dedicated warehouse for resource management.

### 2.1. Service User

To adhere to the principle of least privilege and to support automated processes, we will create a single, dedicated service user.

-   **User Name:** `SVC_ONTOLOGICS_USER`
-   **Purpose:** This user will be used by all Ontologics agents and applications to connect to Snowflake. It will **not** own any database objects. Instead, it will be granted functional roles to perform its tasks.
-   **Authentication:** This user should be configured with key-pair authentication for programmatic access, avoiding the need to store passwords in application code.

### 2.2. Functional Roles

We will implement a set of functional roles that correspond to the types of operations performed within the framework. These roles are defined in the `fhoa-a21-provision-ontologic-infrastructure.py` agent.

| Role Name             | Description                                                                                                                            | Granted To                               |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| `ONTOLOGY_ADMIN_ROLE`   | Has `OWNERSHIP` of the database and schema. Used for provisioning, schema modifications, and managing top-level grants.                  | Database Administrators (Human Users)    |
| `ONTOLOGY_MODELER_ROLE` | Has full CRUD (SELECT, INSERT, UPDATE, DELETE) privileges on all tables within the `IDEF0_SCHEMA`. This is the primary operational role. | `SVC_ONTOLOGICS_USER`                    |
| `ONTOLOGY_READER_ROLE`  | Has read-only (`SELECT`) privileges on all tables. Used for analytical queries, reporting, and read-only application functions.        | Analytical Tools, Read-Only Applications |

### 2.3. Warehouse

-   **Warehouse Name:** `ONTOLOGICS_WH`
-   **Purpose:** A dedicated virtual warehouse for all Ontologics-related queries. This allows for clear cost attribution and performance monitoring of the system.
-   **Permissions:** `USAGE` on this warehouse will be granted to the `ONTOLOGY_MODELER_ROLE` and `ONTOLOGY_READER_ROLE`.

## 3. Implementation and Grant Strategy

The implementation follows a clear hierarchy:

1.  **Ownership:** The `ONTOLOGY_ADMIN_ROLE` will own the `ONTOLOGICS_DB` database and all objects within it. This role is managed by DBAs and is set up by the provisioning agent.
2.  **Functional Grants:** The `ONTOLOGY_ADMIN_ROLE` grants specific privileges to the functional roles (`ONTOLOGY_MODELER_ROLE`, `ONTOLOGY_READER_ROLE`).
3.  **User Grants:** The `SVC_ONTOLOGICS_USER` is granted the `ONTOLOGY_MODELER_ROLE`. This gives the application the necessary permissions to function without being an object owner.

The following example SQL demonstrates this setup using the principle of least privilege by leveraging the `SYSADMIN` and `SECURITYADMIN` roles rather than the all-powerful `ACCOUNTADMIN` role.

### 3.1. RBAC Policy Definition

```sql
-- This script assumes the database, schema, and roles have been created
-- by the fhoa-a21-provision-ontologic-infrastructure agent.
--
-- Best Practice: Avoid using ACCOUNTADMIN for routine tasks. Instead, use
-- specific administrative roles like SECURITYADMIN (for users/roles) and
-- SYSADMIN (for objects like warehouses) to follow the principle of least privilege.

-- Step 1: Use a role with user and role management privileges (e.g., SECURITYADMIN).
USE ROLE SECURITYADMIN;

-- Create the dedicated service user (use key-pair auth in production).
CREATE USER IF NOT EXISTS SVC_ONTOLOGICS_USER
  PASSWORD = '[PASSWORD_VALUE]' -- Replace with a secure method or key-pair auth
  DEFAULT_ROLE = ONTOLOGY_MODELER_ROLE
  DEFAULT_WAREHOUSE = ONTOLOGICS_WH
  COMMENT = 'Service User for the Ontologics Framework applications and agents.';

-- Grant the operational role to the service user. SECURITYADMIN can grant any role.
GRANT ROLE ONTOLOGY_MODELER_ROLE TO USER SVC_ONTOLOGICS_USER;


-- Step 2: Use a role with object creation privileges (e.g., SYSADMIN).
USE ROLE SYSADMIN;

-- Create the warehouse and grant usage to the functional roles.
CREATE WAREHOUSE IF NOT EXISTS ONTOLOGICS_WH
  AUTO_SUSPEND = 60;
GRANT USAGE ON WAREHOUSE ONTOLOGICS_WH TO ROLE ONTOLOGY_MODELER_ROLE;
GRANT USAGE ON WAREHOUSE ONTOLOGICS_WH TO ROLE ONTOLOGY_READER_ROLE;


-- Step 3: Grant roles to SYSADMIN for easier management.
USE ROLE SECURITYADMIN;

GRANT ROLE ONTOLOGY_ADMIN_ROLE TO ROLE SYSADMIN;
GRANT ROLE ONTOLOGY_MODELER_ROLE TO ROLE SYSADMIN;
GRANT ROLE ONTOLOGY_READER_ROLE TO ROLE SYSADMIN;


### 3.2. Object Grants (Applied by Agent)

The `fhoa-a21-provision-ontologic-infrastructure` agent applies the following grants to the functional roles after the database objects are created. This ensures a clean separation of concerns where `SYSADMIN` owns the objects and functional roles are granted the minimum necessary privileges.

#### **ONTOLOGY_ADMIN_ROLE Grants:**
```sql
-- Grant full ownership of the database to the admin role.
-- This is a powerful role intended for schema evolution and management.
GRANT OWNERSHIP ON DATABASE ONTOLOGICS TO ROLE ONTOLOGY_ADMIN_ROLE;
```

#### **ONTOLOGY_MODELER_ROLE Grants:**
```sql
-- Allow usage of the database, schema, and warehouse
GRANT USAGE ON DATABASE ONTOLOGICS TO ROLE ONTOLOGY_MODELER_ROLE;
GRANT USAGE ON SCHEMA ONTOLOGICS.IDEF0 TO ROLE ONTOLOGY_MODELER_ROLE;
GRANT USAGE ON WAREHOUSE ONTOLOGICS_WH TO ROLE ONTOLOGY_MODELER_ROLE;

-- Allow full CRUD on all current and future tables in the schema
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA ONTOLOGICS.IDEF0 TO ROLE ONTOLOGY_MODELER_ROLE;
GRANT SELECT, INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA ONTOLOGICS.IDEF0 TO ROLE ONTOLOGY_MODELER_ROLE;
```

#### **ONTOLOGY_READER_ROLE Grants:**
```sql
-- Allow usage of the database, schema, and warehouse
GRANT USAGE ON DATABASE ONTOLOGICS TO ROLE ONTOLOGY_READER_ROLE;
GRANT USAGE ON SCHEMA ONTOLOGICS.IDEF0 TO ROLE ONTOLOGY_READER_ROLE;
GRANT USAGE ON WAREHOUSE ONTOLOGICS_WH TO ROLE ONTOLOGY_READER_ROLE;

-- Allow SELECT on all current and future tables in the schema
GRANT SELECT ON ALL TABLES IN SCHEMA ONTOLOGICS.IDEF0 TO ROLE ONTOLOGY_READER_ROLE;
GRANT SELECT ON FUTURE TABLES IN SCHEMA ONTOLOGICS.IDEF0 TO ROLE ONTOLOGY_READER_ROLE;

