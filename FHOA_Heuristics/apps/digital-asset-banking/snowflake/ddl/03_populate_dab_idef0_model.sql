-- ================================================================================================
-- SQL INSERT Script for DAB IDEF0 Process Model
-- ================================================================================================
-- Prequisite: This script assumes the tables from IDEF0-data-model.md have been created.
-- ================================================================================================

USE DATABASE IDEF0_MODEL_DB;
USE SCHEMA DATAOPS_IDEF0_SCHEMA;

-- Step 1: Insert all unique FUNCTIONS
INSERT INTO FUNCTIONS (FUNCTION_ID, FUNCTION_NAME, DESCRIPTION, DIAGRAM_LEVEL, PARENT_FUNCTION_ID) VALUES
-- A-0 Level
(100, 'Manage Digital Asset Banking Platform', 'Top-level function defining the overall scope and boundary of the system.', 'A-0', NULL),
-- A0 Level
(200, 'Manage Asset Lifecycle', 'Encompasses the core user-facing activities of uploading, creating, viewing, and purchasing digital assets.', 'A0', 100),
(300, 'Administer Platform Resources', 'Covers the operational and development activities required to build and maintain the platform.', 'A0', 100),
(400, 'Provide Analytics & Compliance', 'Addresses the needs of stakeholders for insight and oversight.', 'A0', 100),
-- A1 Level
(201, 'Authenticate User', 'Verifies a user''s identity to grant them access to the platform.', 'A1', 200),
(202, 'Create Digital Asset', 'Covers the workflow for a user uploading a file and metadata.', 'A1', 200),
(203, 'View Asset Data', 'Represents a user Browse the collection of available assets.', 'A1', 200),
(204, 'Purchase Digital Asset', 'Handles the transaction where a user takes ownership of an asset.', 'A1', 200),
-- A2 Level
(301, 'Provision Cloud Infrastructure', 'Represents the deployment of all necessary cloud resources using IaC.', 'A2', 300),
(302, 'Deploy Application Code', 'Describes the automated process of deploying source code.', 'A2', 300),
(303, 'Manage Security & RBAC', 'Describes implementing and maintaining security policies.', 'A2', 300),
(304, 'Monitor Platform Health & Cost', 'Describes observing performance and cloud spending.', 'A2', 300),
-- A3 Level
(401, 'Ingest Transactional Data', 'Represents capturing raw data and loading it into the data warehouse.', 'A3', 400),
(402, 'Generate Business Analytics', 'Covers creating dashboards and reports for stakeholders.', 'A3', 400),
(403, 'Provide Audit Trail Access', 'Describes providing secure, read-only access to logs.', 'A3', 400);

-- Step 2: Insert all unique INPUTS
INSERT INTO INPUTS (INPUT_ID, INPUT_NAME) VALUES
(1001, 'User-Provided Digital Content'),
(1002, 'User Stories & Requirements'),
(1003, 'User Credentials'),
(1004, 'Asset Metadata'),
(1005, 'User Request'),
(1006, 'User Purchase Request'),
(1007, 'Infrastructure-as-Code Files'),
(1008, 'Configuration Variables'),
(1009, 'Application Source Code'),
(1010, 'RBAC Design Document'),
(1011, 'IAM Policy Documents'),
(1012, 'Platform Metrics & Logs'),
(1013, 'Cloud Billing & Usage Data'),
(1014, 'Raw Transactional Events'),
(1015, 'Validated & Governed Data'),
(1016, 'Audit Request');

-- Step 3: Insert all unique CONTROLS
INSERT INTO CONTROLS (CONTROL_ID, CONTROL_NAME) VALUES
(2001, 'Regulatory & Compliance Standards'),
(2002, 'Architectural Specifications'),
(2003, 'Authentication Protocol (OAuth 2.0)'),
(2004, 'DIM_USERS Table Schema'),
(2005, 'Authenticated User Session'),
(2006, 'S3 Bucket Policy'),
(2007, 'Data Model Schema'),
(2008, 'RBAC Policy'),
(2009, 'IAM Permissions'),
(2010, 'Cloud Provider API Limits'),
(2011, 'CI/CD Pipeline Configuration'),
(2012, 'Automated Tests'),
(2013, 'Principle of Least Privilege'),
(2014, 'Service Level Agreements (SLAs)'),
(2015, 'Cloud Budgets'),
(2016, 'Alerting Rules'),
(2017, 'Semantic View Definition'),
(2018, 'Data Retention Policies');

-- Step 4: Insert all unique OUTPUTS
INSERT INTO OUTPUTS (OUTPUT_ID, OUTPUT_NAME) VALUES
(3001, 'Managed Digital Assets'),
(3002, 'Physical Trading Cards'),
(3003, 'Transaction Records & Audit Logs'),
(3004, 'Platform Analytics & Dashboards'),
(3005, 'Authenticated User Session'),
(3006, 'User Record'),
(3007, 'Stored Asset'),
(3008, 'Asset Database Record'),
(3009, 'Transaction Database Record'),
(3010, 'Confirmation Message'),
(3011, 'Asset Data Display'),
(3012, 'Updated Asset Record'),
(3013, 'Provisioned Cloud Resources'),
(3014, 'State File'),
(3015, 'Deployment Logs'),
(3016, 'Deployed Application'),
(3017, 'Deployment Status'),
(3018, 'Applied Snowflake Roles & Grants'),
(3019, 'Applied IAM Policies & Roles'),
(3020, 'Health & Performance Dashboards'),
(3021, 'Cost & Usage Reports'),
(3022, 'Alert Notifications'),
(3023, 'Validated & Governed Data'),
(3024, 'Analytics Dashboards & Reports'),
(3025, 'Audit Trail Report');

-- Step 5: Insert all unique MECHANISMS
INSERT INTO MECHANISMS (MECHANISM_ID, MECHANISM_NAME) VALUES
(4001, 'End Users & Platform Administrators'),
(4002, 'Cloud Infrastructure'),
(4003, 'CI/CD Pipeline'),
(4004, 'Streamlit Frontend'),
(4005, 'Backend API (Lambda)'),
(4006, 'External SSO Provider'),
(4007, 'Snowflake Database'),
(4008, 'AWS S3 Bucket'),
(4009, 'Platform Administrator'),
(4010, 'IaC Engine'),
(4011, 'Git Repository'),
(4012, 'Target Compute Service'),
(4013, 'Snowflake UI/CLI'),
(4014, 'AWS Console/CLI'),
(4015, 'Cloud Monitoring Tools'),
(4016, 'Logging Services'),
(4017, 'BI Tools'),
(4018, 'Snowflake Semantic View'),
(4019, 'Snowflake Access History'),
(4020, 'AWS CloudTrail');


-- Step 6: Link all ICOMs to their FUNCTIONS using Junction Tables

-- A-0: Manage Digital Asset Banking Platform
INSERT INTO FUNCTION_INPUTS (FUNCTION_ID, INPUT_ID) VALUES (100, 1001), (100, 1002);
INSERT INTO FUNCTION_CONTROLS (FUNCTION_ID, CONTROL_ID) VALUES (100, 2001), (100, 2002);
INSERT INTO FUNCTION_OUTPUTS (FUNCTION_ID, OUTPUT_ID) VALUES (100, 3001), (100, 3002), (100, 3003), (100, 3004);
INSERT INTO FUNCTION_MECHANISMS (FUNCTION_ID, MECHANISM_ID) VALUES (100, 4001), (100, 4002), (100, 4003);

-- A1.1: Authenticate User
INSERT INTO FUNCTION_INPUTS (FUNCTION_ID, INPUT_ID) VALUES (201, 1003);
INSERT INTO FUNCTION_CONTROLS (FUNCTION_ID, CONTROL_ID) VALUES (201, 2003), (201, 2004);
INSERT INTO FUNCTION_OUTPUTS (FUNCTION_ID, OUTPUT_ID) VALUES (201, 3005), (201, 3006);
INSERT INTO FUNCTION_MECHANISMS (FUNCTION_ID, MECHANISM_ID) VALUES (201, 4004), (201, 4005), (201, 4006), (201, 4007);

-- A1.2: Create Digital Asset
INSERT INTO FUNCTION_INPUTS (FUNCTION_ID, INPUT_ID) VALUES (202, 1001), (202, 1004);
INSERT INTO FUNCTION_CONTROLS (FUNCTION_ID, CONTROL_ID) VALUES (202, 2005), (202, 2006), (202, 2007);
INSERT INTO FUNCTION_OUTPUTS (FUNCTION_ID, OUTPUT_ID) VALUES (202, 3007), (202, 3008), (202, 3009), (202, 3010);
INSERT INTO FUNCTION_MECHANISMS (FUNCTION_ID, MECHANISM_ID) VALUES (202, 4004), (202, 4005), (202, 4008), (202, 4007);

-- A1.3: View Asset Data
INSERT INTO FUNCTION_INPUTS (FUNCTION_ID, INPUT_ID) VALUES (203, 1005);
INSERT INTO FUNCTION_CONTROLS (FUNCTION_ID, CONTROL_ID) VALUES (203, 2005), (203, 2007), (203, 2008);
INSERT INTO FUNCTION_OUTPUTS (FUNCTION_ID, OUTPUT_ID) VALUES (203, 3011);
INSERT INTO FUNCTION_MECHANISMS (FUNCTION_ID, MECHANISM_ID) VALUES (203, 4004), (203, 4005), (203, 4007);

-- A1.4: Purchase Digital Asset
INSERT INTO FUNCTION_INPUTS (FUNCTION_ID, INPUT_ID) VALUES (204, 1006);
INSERT INTO FUNCTION_CONTROLS (FUNCTION_ID, CONTROL_ID) VALUES (204, 2005), (204, 2007), (204, 2008);
INSERT INTO FUNCTION_OUTPUTS (FUNCTION_ID, OUTPUT_ID) VALUES (204, 3012), (204, 3009), (204, 3010);
INSERT INTO FUNCTION_MECHANISMS (FUNCTION_ID, MECHANISM_ID) VALUES (204, 4004), (204, 4005), (204, 4007);

-- A2.1: Provision Cloud Infrastructure
INSERT INTO FUNCTION_INPUTS (FUNCTION_ID, INPUT_ID) VALUES (301, 1007), (301, 1008);
INSERT INTO FUNCTION_CONTROLS (FUNCTION_ID, CONTROL_ID) VALUES (301, 2002), (301, 2009), (301, 2010);
INSERT INTO FUNCTION_OUTPUTS (FUNCTION_ID, OUTPUT_ID) VALUES (301, 3013), (301, 3014), (301, 3015);
INSERT INTO FUNCTION_MECHANISMS (FUNCTION_ID, MECHANISM_ID) VALUES (301, 4009), (301, 4010), (301, 4003);

-- A2.2: Deploy Application Code
INSERT INTO FUNCTION_INPUTS (FUNCTION_ID, INPUT_ID) VALUES (302, 1009);
INSERT INTO FUNCTION_CONTROLS (FUNCTION_ID, CONTROL_ID) VALUES (302, 2011), (302, 2012);
INSERT INTO FUNCTION_OUTPUTS (FUNCTION_ID, OUTPUT_ID) VALUES (302, 3016), (302, 3017);
INSERT INTO FUNCTION_MECHANISMS (FUNCTION_ID, MECHANISM_ID) VALUES (302, 4011), (302, 4003), (302, 4012);

-- A2.3: Manage Security & RBAC
INSERT INTO FUNCTION_INPUTS (FUNCTION_ID, INPUT_ID) VALUES (303, 1010), (303, 1011);
INSERT INTO FUNCTION_CONTROLS (FUNCTION_ID, CONTROL_ID) VALUES (303, 2013), (303, 2001);
INSERT INTO FUNCTION_OUTPUTS (FUNCTION_ID, OUTPUT_ID) VALUES (303, 3018), (303, 3019);
INSERT INTO FUNCTION_MECHANISMS (FUNCTION_ID, MECHANISM_ID) VALUES (303, 4009), (303, 4013), (303, 4014), (303, 4010);

-- A2.4: Monitor Platform Health & Cost
INSERT INTO FUNCTION_INPUTS (FUNCTION_ID, INPUT_ID) VALUES (304, 1012), (304, 1013);
INSERT INTO FUNCTION_CONTROLS (FUNCTION_ID, CONTROL_ID) VALUES (304, 2014), (304, 2015), (304, 2016);
INSERT INTO FUNCTION_OUTPUTS (FUNCTION_ID, OUTPUT_ID) VALUES (304, 3020), (304, 3021), (304, 3022);
INSERT INTO FUNCTION_MECHANISMS (FUNCTION_ID, MECHANISM_ID) VALUES (304, 4009), (304, 4015), (304, 4016);

-- A3.1: Ingest Transactional Data
INSERT INTO FUNCTION_INPUTS (FUNCTION_ID, INPUT_ID) VALUES (401, 1014);
INSERT INTO FUNCTION_CONTROLS (FUNCTION_ID, CONTROL_ID) VALUES (401, 2007);
INSERT INTO FUNCTION_OUTPUTS (FUNCTION_ID, OUTPUT_ID) VALUES (401, 3023);
INSERT INTO FUNCTION_MECHANISMS (FUNCTION_ID, MECHANISM_ID) VALUES (401, 4005), (401, 4007);

-- A3.2: Generate Business Analytics
INSERT INTO FUNCTION_INPUTS (FUNCTION_ID, INPUT_ID) VALUES (402, 1015);
INSERT INTO FUNCTION_CONTROLS (FUNCTION_ID, CONTROL_ID) VALUES (402, 2017), (402, 2008);
INSERT INTO FUNCTION_OUTPUTS (FUNCTION_ID, OUTPUT_ID) VALUES (402, 3024);
INSERT INTO FUNCTION_MECHANISMS (FUNCTION_ID, MECHANISM_ID) VALUES (402, 4018), (402, 4017);

-- A3.3: Provide Audit Trail Access
INSERT INTO FUNCTION_INPUTS (FUNCTION_ID, INPUT_ID) VALUES (403, 1016);
INSERT INTO FUNCTION_CONTROLS (FUNCTION_ID, CONTROL_ID) VALUES (403, 2008), (403, 2018);
INSERT INTO FUNCTION_OUTPUTS (FUNCTION_ID, OUTPUT_ID) VALUES (403, 3025);
INSERT INTO FUNCTION_MECHANISMS (FUNCTION_ID, MECHANISM_ID) VALUES (403, 4009), (403, 4019), (403, 4020);


-- ================================================================================================
-- SCRIPT COMPLETE
-- ================================================================================================