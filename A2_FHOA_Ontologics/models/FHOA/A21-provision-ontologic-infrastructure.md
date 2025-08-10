# FHOA Ontologics (A2.1) Process Model: Provision Ontologic Infrastructure

This document provides the IDEF0-style decomposition for the **A2.1: Provision Ontologic Infrastructure** function within the FHOA framework. Its primary purpose is to define the steps required to create and secure the database that will store all enterprise process models.

---

## A2.1: Provision Ontologic Infrastructure (Top-Level Function)

- **Purpose**: To create or verify the necessary database schema and access control policies for storing and managing IDEF0 models.
- **Inputs**: 
  - `IDEF0 Data Model (SQL)`: The DDL script defining the tables and schema.
  - `RBAC Policy Model`: The strategy and structural definition of roles and the permissions they require.
- **Controls**: 
  - `Database Admin Credentials`: High-privilege credentials required to create databases, roles, and grant permissions.
- **Outputs**: 
  - `Provisioned Database Schema`: The live database objects in Snowflake.
  - `Applied RBAC Policies`: The roles and grants applied to the schema.
- **Mechanisms**: 
  - `fhoa-a21-provision-ontologic-infrastructure (Agent)`: The automated script that executes the provisioning.
  - `Snowflake Connection`: The database connector.

---

## A2.1 Decomposition: The Provisioning Sequence

The A2.1 function is decomposed into two sequential sub-processes.

### A2.1.1: Execute Schema DDL

- **Purpose**: To create and configure the database, schema, and tables for storing IDEF0 models.
- **Inputs**: `IDEF0 Data Model (SQL)`
- **Controls**: `Database Admin Credentials`
- **Outputs**: `Provisioned Database Schema` (to A2.1.2)
- **Mechanisms**: `Provisioning Agent`, `Snowflake Connection`

---

### A2.1.2: Execute RBAC DCL

- **Purpose**: To create roles and grant the necessary permissions for interacting with the IDEF0 database schema.
- **Inputs**: 
  - `Provisioned Database Schema` (from A2.1.1)
  - `RBAC Policy Model`
- **Controls**: `Database Admin Credentials`
- **Outputs**: `Applied RBAC Policies`
- **Mechanisms**: `Provisioning Agent`, `Snowflake Connection`