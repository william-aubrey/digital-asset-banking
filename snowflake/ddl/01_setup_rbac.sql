-- ================================================================================================
-- Snowflake RBAC Implementation Script for Digital Asset Banking (DAB)
-- ================================================================================================
-- Prequisite: This script must be run by a user with the ACCOUNTADMIN role.
-- ================================================================================================

USE ROLE ACCOUNTADMIN;

-- Step 1: Create the top-level Platform Admin role
CREATE ROLE IF NOT EXISTS DAB_PLATFORM_ADMIN 
    COMMENT = 'Top-level admin role for the DAB project. Can create users, roles, and databases.';

-- Step 2: Grant necessary privileges from SYSADMIN and SECURITYADMIN to the new Platform Admin role
USE ROLE SYSADMIN;
GRANT CREATE DATABASE ON ACCOUNT TO ROLE DAB_PLATFORM_ADMIN;
GRANT CREATE WAREHOUSE ON ACCOUNT TO ROLE DAB_PLATFORM_ADMIN;

USE ROLE SECURITYADMIN;
GRANT CREATE USER ON ACCOUNT TO ROLE DAB_PLATFORM_ADMIN;
GRANT CREATE ROLE ON ACCOUNT TO ROLE DAB_PLATFORM_ADMIN;
GRANT MANAGE GRANTS ON ACCOUNT TO ROLE DAB_PLATFORM_ADMIN;

-- Step 3: Grant the new Platform Admin role to your user for setup
-- Replace with your actual user name
GRANT ROLE DAB_PLATFORM_ADMIN TO USER "WAUBREY@PHDATA.IO";

-- ================================================================================================
-- All subsequent operations are performed by the new Platform Admin role
-- ================================================================================================

USE ROLE DAB_PLATFORM_ADMIN;

-- Step 4: Create the application's core objects
CREATE WAREHOUSE IF NOT EXISTS DAB_WAREHOUSE;
CREATE DATABASE IF NOT EXISTS DAB_DATABASE;
CREATE SCHEMA IF NOT EXISTS DAB_DATABASE.DAB_SCHEMA;

-- Step 5: Create the application's functional roles
CREATE ROLE IF NOT EXISTS DAB_ADMIN 
    COMMENT = 'Owns all DAB database objects.';
CREATE ROLE IF NOT EXISTS DAB_APP_USER 
    COMMENT = 'Role for the Streamlit application service account.';
CREATE ROLE IF NOT EXISTS DAB_ANALYST 
    COMMENT = 'Role for BI and reporting users.';
CREATE ROLE IF NOT EXISTS DAB_REGULATOR
    COMMENT = 'Read-only role for auditors.';

-- Step 6: Create the service account users
-- NOTE: Replace placeholders with secure, generated passwords.
CREATE USER IF NOT EXISTS SVC_DAB_APP 
    PASSWORD = '<secure_password_placeholder>' 
    DEFAULT_ROLE = DAB_APP_USER 
    DEFAULT_WAREHOUSE = DAB_WAREHOUSE 
    COMMENT = 'Service account for the DAB application backend.';

CREATE USER IF NOT EXISTS SVC_DAB_ANALYST
    PASSWORD = '<secure_password_placeholder>' 
    DEFAULT_ROLE = DAB_ANALYST 
    DEFAULT_WAREHOUSE = DAB_WAREHOUSE 
    COMMENT = 'Service account for BI and analytics.';
    
-- Step 7: Create the role hierarchy
GRANT ROLE DAB_ADMIN TO ROLE DAB_PLATFORM_ADMIN;
GRANT ROLE DAB_APP_USER TO ROLE DAB_ADMIN;
GRANT ROLE DAB_ANALYST TO ROLE DAB_ADMIN;
GRANT ROLE DAB_REGULATOR TO ROLE DAB_ADMIN;

-- Grant roles to the service users
GRANT ROLE DAB_APP_USER TO USER SVC_DAB_APP;
GRANT ROLE DAB_ANALYST TO USER SVC_DAB_ANALYST;

-- Step 8: Grant privileges to the functional roles
-- APP USER privileges
GRANT USAGE ON WAREHOUSE DAB_WAREHOUSE TO ROLE DAB_APP_USER;
GRANT USAGE ON DATABASE DAB_DATABASE TO ROLE DAB_APP_USER;
GRANT USAGE ON SCHEMA DAB_DATABASE.DAB_SCHEMA TO ROLE DAB_APP_USER;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA DAB_DATABASE.DAB_SCHEMA TO ROLE DAB_APP_USER;
GRANT SELECT ON ALL VIEWS IN SCHEMA DAB_DATABASE.DAB_SCHEMA TO ROLE DAB_APP_USER;


-- ANALYST privileges
GRANT USAGE ON WAREHOUSE DAB_WAREHOUSE TO ROLE DAB_ANALYST;
GRANT USAGE ON DATABASE DAB_DATABASE TO ROLE DAB_ANALYST;
GRANT USAGE ON SCHEMA DAB_DATABASE.DAB_SCHEMA TO ROLE DAB_ANALYST;
GRANT SELECT ON ALL TABLES IN SCHEMA DAB_DATABASE.DAB_SCHEMA TO ROLE DAB_ANALYST;
GRANT SELECT ON ALL VIEWS IN SCHEMA DAB_DATABASE.DAB_SCHEMA TO ROLE DAB_ANALYST;

-- Step 9: Transfer ownership of all objects to the DAB_ADMIN role for proper management
GRANT OWNERSHIP ON WAREHOUSE DAB_WAREHOUSE TO ROLE DAB_ADMIN;
GRANT OWNERSHIP ON DATABASE DAB_DATABASE TO ROLE DAB_ADMIN;
GRANT OWNERSHIP ON SCHEMA DAB_DATABASE.DAB_SCHEMA TO ROLE DAB_ADMIN;

-- Grant future object ownership to DAB_ADMIN
GRANT OWNERSHIP ON FUTURE SCHEMAS IN DATABASE DAB_DATABASE TO ROLE DAB_ADMIN;
GRANT OWNERSHIP ON FUTURE TABLES IN SCHEMA DAB_DATABASE.DAB_SCHEMA TO ROLE DAB_ADMIN;
GRANT OWNERSHIP ON FUTURE VIEWS IN SCHEMA DAB_DATABASE.DAB_SCHEMA TO ROLE DAB_ADMIN;


-- ================================================================================================
-- SETUP COMPLETE
-- ================================================================================================