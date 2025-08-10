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
    (1065, 'External SSO Provider'),
    (1066, 'Snowflake Database'),
    (1067, 'Platform Metrics & Logs'),
    (1068, 'Cloud Billing & Usage Data'),
    (1069, 'Service Level Agreements (SLAs)'),
    (1070, 'Cloud Budgets'),
    (1071, 'Alerting Rules'),
    (1072, 'Health & Performance Dashboards'),
    (1073, 'Cost & Usage Reports'),
    (1074, 'Alert Notifications'),
    (1075, 'Cloud Monitoring Tools'),
    (1076, 'Logging Services'),
    (1077, 'Raw Transactional Events'),
    (1078, 'Validated & Governed Data'),
    (1079, 'Semantic View Definition'),
    (1080, 'RBAC Policy'),
    (1081, 'Analytics Dashboards & Reports'),
    (1082, 'Snowflake Semantic View'),
    (1083, 'DAB_ANALYST role'),
    (1084, 'Audit Request'),
    (1085, 'Data Retention Policies'),
    (1086, 'Snowflake Access History'),
    (1087, 'AWS CloudTrail'),
    (1088, 'RBAC Policy (DAB_REGULATOR role)');

-- 4. Insert FUNCTION_ENTITIES (The Connections)
-- This populates the junction table that connects each function to its ICOMs.
-- FUNCTION_ENTITY_ID values are assigned starting from 2001.
INSERT INTO FUNCTION_ENTITIES (FUNCTION_ENTITY_ID, FUNCTION_ID, ENTITY_ID, ROLE)
VALUES
    -- A-0: Manage Digital Asset Banking Platform (Context)
    (2001, 100, 1001, 'INPUT'),
    (2002, 100, 1002, 'INPUT'),
    (2003, 100, 1003, 'CONTROL'),
    (2004, 100, 1004, 'CONTROL'),
    (2005, 100, 1005, 'OUTPUT'),
    (2006, 100, 1006, 'OUTPUT'),
    (2007, 100, 1007, 'OUTPUT'),
    (2008, 100, 1008, 'OUTPUT'),
    (2009, 100, 1009, 'MECHANISM'),
    (2010, 100, 1010, 'MECHANISM'),
    (2011, 100, 1011, 'MECHANISM'),

    -- A1: Manage Asset Lifecycle (Decomposition)
    (2012, 110, 1001, 'INPUT'),
    (2013, 110, 1004, 'CONTROL'),
    (2014, 110, 1005, 'OUTPUT'),
    (2015, 110, 1012, 'OUTPUT'),
    (2016, 110, 1013, 'MECHANISM'),
    (2017, 110, 1014, 'MECHANISM'),

    -- A2: Administer Platform Resources (ID 120)
    (2018, 120, 1002, 'INPUT'),
    (2019, 120, 1003, 'CONTROL'),
    (2020, 120, 1014, 'OUTPUT'),
    (2021, 120, 1015, 'OUTPUT'),
    (2022, 120, 1016, 'OUTPUT'),
    (2023, 120, 1017, 'MECHANISM'),
    (2024, 120, 1010, 'MECHANISM'),
    (2025, 120, 1011, 'MECHANISM'),

    -- A3: Provide Analytics & Compliance (ID 130)
    (2026, 130, 1012, 'INPUT'),
    (2027, 130, 1003, 'CONTROL'),
    (2028, 130, 1008, 'OUTPUT'),
    (2029, 130, 1018, 'OUTPUT'),
    (2030, 130, 1019, 'MECHANISM'),
    (2031, 130, 1010, 'MECHANISM'),

    -- A1.1: Display Asset Marketplace (ID 111)
    (2032, 111, 1020, 'INPUT'),
    (2033, 111, 1021, 'CONTROL'),
    (2034, 111, 1022, 'CONTROL'),
    (2035, 111, 1023, 'OUTPUT'),
    (2036, 111, 1024, 'MECHANISM'),
    (2037, 111, 1025, 'MECHANISM'),
    (2038, 111, 1026, 'MECHANISM'),

    -- A1.2: Process New Asset Upload (ID 112)
    (2039, 112, 1027, 'INPUT'),
    (2040, 112, 1028, 'INPUT'),
    (2041, 112, 1021, 'CONTROL'),
    (2042, 112, 1029, 'CONTROL'),
    (2043, 112, 1030, 'CONTROL'),
    (2044, 112, 1031, 'CONTROL'),
    (2045, 112, 1032, 'OUTPUT'),
    (2046, 112, 1033, 'OUTPUT'),
    (2047, 112, 1034, 'OUTPUT'),
    (2048, 112, 1024, 'MECHANISM'),
    (2049, 112, 1025, 'MECHANISM'),
    (2050, 112, 1035, 'MECHANISM'),
    (2051, 112, 1026, 'MECHANISM'),

    -- A1.3: Execute Asset Purchase (ID 113)
    (2052, 113, 1036, 'INPUT'),
    (2053, 113, 1021, 'CONTROL'),
    (2054, 113, 1037, 'CONTROL'),
    (2055, 113, 1022, 'CONTROL'),
    (2056, 113, 1038, 'OUTPUT'),
    (2057, 113, 1039, 'OUTPUT'),
    (2058, 113, 1034, 'OUTPUT'),
    (2059, 113, 1024, 'MECHANISM'),
    (2060, 113, 1025, 'MECHANISM'),
    (2061, 113, 1026, 'MECHANISM'),

    -- A2.1: Provision Cloud Infrastructure (ID 121)
    (2062, 121, 1040, 'INPUT'),
    (2063, 121, 1041, 'INPUT'),
    (2064, 121, 1004, 'CONTROL'),
    (2065, 121, 1042, 'CONTROL'),
    (2066, 121, 1043, 'CONTROL'),
    (2067, 121, 1014, 'OUTPUT'),
    (2068, 121, 1044, 'OUTPUT'),
    (2069, 121, 1045, 'OUTPUT'),
    (2070, 121, 1017, 'MECHANISM'),
    (2071, 121, 1047, 'MECHANISM'),
    (2072, 121, 1011, 'MECHANISM'),

    -- A2.2: Deploy Application Code (ID 122)
    (2073, 122, 1048, 'INPUT'),
    (2074, 122, 1049, 'CONTROL'),
    (2075, 122, 1050, 'CONTROL'),
    (2076, 122, 1015, 'OUTPUT'),
    (2077, 122, 1051, 'OUTPUT'),
    (2078, 122, 1052, 'MECHANISM'),
    (2079, 122, 1011, 'MECHANISM'),
    (2080, 122, 1053, 'MECHANISM'),

    -- A3.3: Provide Audit Trail Access (ID 133)
    (2081, 133, 1084, 'INPUT'),
    (2082, 133, 1088, 'CONTROL'),
    (2083, 133, 1085, 'CONTROL'),
    (2084, 133, 1018, 'OUTPUT'),
    (2085, 133, 1017, 'MECHANISM'),
    (2086, 133, 1086, 'MECHANISM'),
    (2087, 133, 1087, 'MECHANISM');

-- End of script. The DAB functional hierarchy and all ICOMs are now loaded.