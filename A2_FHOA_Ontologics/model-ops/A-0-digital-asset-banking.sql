-- FHOA Ontologics: Model Operations
-- This script populates the IDEF0 model for the Digital Asset Banking (DAB) platform.
-- It inserts the hierarchical process decomposition from 'A-0-digital-asset-banking.md'
-- into the 'MODELS' and 'FUNCTIONS' tables defined in 'snowflake-object-ddl.sql'.

-- Set the context for the operations
USE DATABASE ONTOLOGICS;
USE SCHEMA IDEF0;

-- 1. Insert the top-level Model definition
-- This represents the A-0 context diagram for the entire system.
INSERT INTO MODELS (MODEL_ID, MODEL_NAME, NODE)
VALUES (1, 'Manage Digital Asset Banking Platform', 'A-0');

-- 2. Insert the Function hierarchy
-- The FUNCTION_ID values are manually assigned to preserve the hierarchical structure.
-- The PARENT_FUNCTION_ID links each function to its parent, with the top-level A-0 having a NULL parent.

-- Level 0: The main system function
INSERT INTO FUNCTIONS (FUNCTION_ID, MODEL_ID, NODE, FUNCTION_NAME, PARENT_FUNCTION_ID)
VALUES (100, 1, 'A-0', 'Manage Digital Asset Banking Platform', NULL);

-- Level 1: Major sub-functions of A-0
INSERT INTO FUNCTIONS (FUNCTION_ID, MODEL_ID, NODE, FUNCTION_NAME, PARENT_FUNCTION_ID)
VALUES
    (110, 1, 'A1', 'Manage Asset Lifecycle', 100),
    (120, 1, 'A2', 'Administer Platform Resources', 100),
    (130, 1, 'A3', 'Provide Analytics & Compliance', 100);

-- Level 2: Decomposition of A1 (Manage Asset Lifecycle)
INSERT INTO FUNCTIONS (FUNCTION_ID, MODEL_ID, NODE, FUNCTION_NAME, PARENT_FUNCTION_ID)
VALUES
    (111, 1, 'A1.1', 'Display Asset Marketplace', 110),
    (112, 1, 'A1.2', 'Process New Asset Upload', 110),
    (113, 1, 'A1.3', 'Execute Asset Purchase', 110);

-- Level 3: Decomposition of A1.2 (Process New Asset Upload)
INSERT INTO FUNCTIONS (FUNCTION_ID, MODEL_ID, NODE, FUNCTION_NAME, PARENT_FUNCTION_ID)
VALUES
    (1121, 1, 'A1.2.1', 'Get or Create Surrogate Key', 112);

-- Level 2: Decomposition of A2 (Administer Platform Resources)
INSERT INTO FUNCTIONS (FUNCTION_ID, MODEL_ID, NODE, FUNCTION_NAME, PARENT_FUNCTION_ID)
VALUES
    (121, 1, 'A2.1', 'Provision Cloud Infrastructure', 120),
    (122, 1, 'A2.2', 'Deploy Application Code', 120),
    (123, 1, 'A2.3', 'Manage Security & RBAC', 120),
    (124, 1, 'A2.4', 'Monitor Platform Health & Cost', 120);

-- Level 3: Decomposition of A2.3 (Manage Security & RBAC)
INSERT INTO FUNCTIONS (FUNCTION_ID, MODEL_ID, NODE, FUNCTION_NAME, PARENT_FUNCTION_ID)
VALUES
    (1231, 1, 'A2.3.1', 'Authenticate User', 123);

-- Level 2: Decomposition of A3 (Provide Analytics & Compliance)
INSERT INTO FUNCTIONS (FUNCTION_ID, MODEL_ID, NODE, FUNCTION_NAME, PARENT_FUNCTION_ID)
VALUES
    (131, 1, 'A3.1', 'Ingest Transactional Data', 130),
    (132, 1, 'A3.2', 'Generate Business Analytics', 130),
    (133, 1, 'A3.3', 'Provide Audit Trail Access', 130);

-- End of script. The DAB functional hierarchy is now loaded into the data model.

-- 3. Insert ENTITIES (The Arrows/ICOMs)
-- This populates the master list of all Inputs, Controls, Outputs, and Mechanisms
-- identified in the A-0-digital-asset-banking.md model.
-- Entity IDs are assigned starting from 1001.
INSERT INTO ENTITIES (ENTITY_ID, ENTITY_NAME)
VALUES
    (1001, 'User-Provided Digital Content'),
    (1002, 'User Stories & Requirements'),
    (1003, 'Regulatory & Compliance Standards'),
    (1004, 'Architectural Specifications'),
    (1005, 'Managed Digital Assets'),
    (1006, 'Physical Trading Cards'),
    (1007, 'Transaction Records & Audit Logs'),
    (1008, 'Platform Analytics & Dashboards'),
    (1009, 'End Users & Platform Administrators'),
    (1010, 'Cloud Infrastructure'),
    (1011, 'CI/CD Pipeline'),
    (1012, 'Transaction Records'),
    (1013, 'End Users'),
    (1014, 'Provisioned Cloud Resources'),
    (1015, 'Deployed Application'),
    (1016, 'Audit Logs'),
    (1017, 'Platform Administrators'),
    (1018, 'Audit Trail Report'),
    (1019, 'BI Tools'),
    (1020, 'User Request'),
    (1021, 'Authenticated User Session'),
    (1022, 'Data Model Schema'),
    (1023, 'Asset Marketplace View'),
    (1024, 'Streamlit Frontend'),
    (1025, 'Backend API (Lambda)'),
    (1026, 'Snowflake Connection'),
    (1027, 'File Object'),
    (1028, 'Asset Metadata'),
    (1029, 'Uploader ID'),
    (1030, 'Asset Type'),
    (1031, 'S3 Bucket Policy'),
    (1032, 'Uploaded Asset Confirmation'),
    (1033, 'Asset Database Record'),
    (1034, 'Transaction Database Record'),
    (1035, 'S3 Client'),
    (1036, 'Asset ID to Purchase'),
    (1037, 'Buyer ID'),
    (1038, 'Purchase Confirmation'),
    (1039, 'Updated Asset Record'),
    (1040, 'Infrastructure-as-Code Files'),
    (1041, 'Configuration Variables'),
    (1042, 'IAM Permissions'),
    (1043, 'Cloud Provider API Limits'),
    (1044, 'State File'),
    (1045, 'Deployment Logs'),
    (1047, 'IaC Engine'),
    (1048, 'Application Source Code'),
    (1049, 'CI/CD Pipeline Configuration'),
    (1050, 'Automated Tests'),
    (1051, 'Deployment Status'),
    (1052, 'Git Repository'),
    (1053, 'Target Compute Service'),
    (1054, 'RBAC Design Document'),
    (1055, 'IAM Policy Documents'),
    (1056, 'Principle of Least Privilege'),
    (1057, 'Applied Snowflake Roles & Grants'),
    (1058, 'Applied IAM Policies & Roles'),
    (1059, 'Snowflake UI/CLI'),
    (1060, 'AWS Console/CLI'),
    (1061, 'User Credentials'),
    (1062, 'Authentication Protocol (OAuth 2.0)'),
    (1063, 'DIM_USERS Table Schema'),
    (1064, 'User Record'),
    (1065, 'External SSO Provider')