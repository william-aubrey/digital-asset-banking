    # --- Fetch and Display Data ---
    st.header("Query Your Data Warehouse")

    # --- Dynamic Configuration from Secrets ---
    # Read database and schema from the secrets file for better portability.
    # This avoids hardcoding environment details in the script.
    db_name = st.secrets.connections.snowflake.database
    schema_name = st.secrets.connections.snowflake.schema
    table_name = "ASSETS"
    # Use quotes to handle potential case-sensitivity and special characters.
    fully_qualified_table_name = f'"{db_name}"."{schema_name}"."{table_name}"'

    # Perform query.
    # `ttl` caches the result for 10 minutes (600 seconds) to prevent re-running
    # the query on every interaction, saving costs and improving performance.
    query = f"SELECT * FROM {fully_qualified_table_name} LIMIT 100;"
    
    st.info(f"Running the following query on Snowflake:\n```sql\n{query}\n```")

