import os
import snowflake.connector
from snowflake.connector.cursor import SnowflakeCursor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
# It's recommended to use environment variables for security.
SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
SNOWFLAKE_WAREHOUSE = os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH')

DB_NAME = 'ONTOLOGICS'
SCHEMA_NAME = 'IDEF0'
WAREHOUSE_NAME = 'ONTOLOGICS_WH'
SQL_MODEL_FILE = '../../A2_FHOA_Ontologics/models/IDEF0/idef0-data-model.sql'

def get_snowflake_connection():
    """Establishes a connection to Snowflake."""
    try:
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            warehouse=SNOWFLAKE_WAREHOUSE
        )
        logging.info("Successfully connected to Snowflake.")
        return conn
    except snowflake.connector.errors.DatabaseError as e:
        logging.error(f"Error connecting to Snowflake: {e}")
        raise

def execute_sql_from_file(cursor: SnowflakeCursor, file_path: str):
    """Executes SQL commands from a file."""
    logging.info(f"Executing SQL from file: {file_path}")
    try:
        with open(file_path, 'r') as f:
            # Split commands by semicolon and filter out empty statements
            sql_commands = [cmd.strip() for cmd in f.read().split(';') if cmd.strip()]
            for command in sql_commands:
                logging.info(f"Executing: {command[:100]}...")
                cursor.execute(command)
        logging.info(f"Successfully executed all commands from {file_path}.")
    except FileNotFoundError:
        logging.error(f"SQL file not found at path: {file_path}")
        raise
    except Exception as e:
        logging.error(f"An error occurred while executing SQL from {file_path}: {e}")
        raise

def provision_rbac(cursor: SnowflakeCursor):
    """Creates roles and grants permissions for the Ontologics database."""
    logging.info("Provisioning RBAC (Roles and Grants)...")
    
    # Best Practice: Use SECURITYADMIN to create roles, then SYSADMIN (or the object owner) to grant privileges.
    # This script assumes the connecting user has sufficient privileges (like ACCOUNTADMIN or a custom setup role)
    # to perform these actions for simplicity in an automated script.
    
    cursor.execute("USE ROLE SECURITYADMIN;")
    logging.info("Using role SECURITYADMIN for role creation.")

    roles = {
        "ONTOLOGY_ADMIN_ROLE": f"GRANT OWNERSHIP ON DATABASE {DB_NAME} TO ROLE ONTOLOGY_ADMIN_ROLE;",
        "ONTOLOGY_MODELER_ROLE": f"""
            GRANT USAGE ON DATABASE {DB_NAME} TO ROLE ONTOLOGY_MODELER_ROLE;
            GRANT USAGE ON SCHEMA {DB_NAME}.{SCHEMA_NAME} TO ROLE ONTOLOGY_MODELER_ROLE;
            GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA {DB_NAME}.{SCHEMA_NAME} TO ROLE ONTOLOGY_MODELER_ROLE;
            GRANT SELECT, INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA {DB_NAME}.{SCHEMA_NAME} TO ROLE ONTOLOGY_MODELER_ROLE;
            GRANT USAGE ON WAREHOUSE {WAREHOUSE_NAME} TO ROLE ONTOLOGY_MODELER_ROLE;
        """,
        "ONTOLOGY_READER_ROLE": f"""
            GRANT USAGE ON DATABASE {DB_NAME} TO ROLE ONTOLOGY_READER_ROLE;
            GRANT USAGE ON SCHEMA {DB_NAME}.{SCHEMA_NAME} TO ROLE ONTOLOGY_READER_ROLE;
            GRANT SELECT ON ALL TABLES IN SCHEMA {DB_NAME}.{SCHEMA_NAME} TO ROLE ONTOLOGY_READER_ROLE;
            GRANT SELECT ON FUTURE TABLES IN SCHEMA {DB_NAME}.{SCHEMA_NAME} TO ROLE ONTOLOGY_READER_ROLE;
            GRANT USAGE ON WAREHOUSE {WAREHOUSE_NAME} TO ROLE ONTOLOGY_READER_ROLE;
        """
    }

    try:
        for role, grants in roles.items():
            logging.info(f"Creating role {role} if it does not exist.")
            cursor.execute(f"CREATE ROLE IF NOT EXISTS {role};")
            
            logging.info(f"Applying grants to role {role}.")
            # Switch to a role that can grant privileges on the objects
            cursor.execute("USE ROLE SYSADMIN;")
            # For multi-statement grants, use execute_string
            for statement in [s.strip() for s in grants.split(';') if s.strip()]:
                cursor.execute(statement)
            # Switch back for the next role creation
            cursor.execute("USE ROLE SECURITYADMIN;")

        # Grant roles to SYSADMIN for management
        logging.info("Granting new roles to SYSADMIN for manageability.")
        for role in roles:
            cursor.execute(f"GRANT ROLE {role} TO ROLE SYSADMIN;")

        logging.info("RBAC provisioning completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during RBAC provisioning: {e}")
        raise

def provision_warehouse(cursor: SnowflakeCursor):
    """Creates and configures the warehouse for the application."""
    logging.info(f"Provisioning warehouse '{WAREHOUSE_NAME}'...")
    cursor.execute("USE ROLE SYSADMIN;")
    logging.info("Using role SYSADMIN for warehouse creation.")
    cursor.execute(f"""
        CREATE WAREHOUSE IF NOT EXISTS {WAREHOUSE_NAME}
        AUTO_SUSPEND = 60;
    """)
    logging.info(f"Warehouse '{WAREHOUSE_NAME}' provisioned successfully.")

def main():
    """Main function to orchestrate the provisioning process."""
    if not all([SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD]):
        logging.error("Missing required environment variables: SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD")
        return

    conn = None
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()

        # --- A2.1.1: Execute Schema DDL ---
        # Best Practice: Use SYSADMIN to create and own database objects.
        logging.info("Using role SYSADMIN for DDL execution.")
        cursor.execute("USE ROLE SYSADMIN;")
        execute_sql_from_file(cursor, SQL_MODEL_FILE)

        # --- Provision Warehouse ---
        # Best Practice: Use SYSADMIN to create warehouses.
        provision_warehouse(cursor)

        # --- A2.1.2: Execute RBAC DCL ---
        # Best Practice: Use SECURITYADMIN for role creation and SYSADMIN for grants.
        provision_rbac(cursor)

        logging.info("Ontologics Infrastructure provisioning complete.")

    finally:
        if conn:
            conn.close()
            logging.info("Snowflake connection closed.")

if __name__ == "__main__":
    main()