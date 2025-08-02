import streamlit as st
import pandas as pd

# Set the page title and a welcoming message
st.set_page_config(page_title="DAB Snowflake Connection", layout="wide")
st.title("❄️ Digital Asset Banking - Snowflake Connector")
st.write(
    "This app demonstrates connecting to your Snowflake data warehouse to retrieve "
    "and display asset metadata. This is the next step in bringing your vision to life!"
)

# --- Connection to Snowflake ---
# Uses st.connection to securely connect to Snowflake using credentials
# from .streamlit/secrets.toml
try:
    conn = st.connection("snowflake")
    st.success("Successfully connected to Snowflake!")

    # --- Fetch and Display Data ---
    st.header("Query Your Data Warehouse")

    # --- Configuration for Snowflake Objects ---
    # Replace these with the actual names from your Snowflake account.
    # These should match what you have in secrets.toml and your setup script.
    # NOTE: Using placeholders here for demonstration. In a real app, you might
    # pull these from your secrets.toml as well.
    db_name = "YOUR_DAB_DATABASE"  # <-- Replace with your DB name
    schema_name = "YOUR_DAB_SCHEMA" # <-- Replace with your Schema name
    table_name = "ASSETS"
    fully_qualified_table_name = f"{db_name}.{schema_name}.{table_name}"

    # Perform query.
    # `ttl` caches the result for 10 minutes (600 seconds) to prevent re-running
    # the query on every interaction, saving costs and improving performance.
    query = f"SELECT * FROM {fully_qualified_table_name} LIMIT 100;"
    
    st.info(f"Running the following query on Snowflake:\n```sql\n{query}\n```")

    try:
        df = conn.query(query, ttl=600)

        # Display the data in an interactive table
        st.dataframe(df, use_container_width=True)

        st.success(f"Successfully retrieved and displayed {len(df)} rows from the `{fully_qualified_table_name}` table.")

    except Exception as e:
        st.error(f"Failed to query the table `{fully_qualified_table_name}`. Please check if the table exists and the user role has the correct permissions.")
        st.exception(e)


except Exception as e:
    st.error("Failed to connect to Snowflake.")
    st.error("Please check your `secrets.toml` file and ensure the credentials are correct and the user has access.")
    st.info(
        "Your `.streamlit/secrets.toml` file should look like this:\n"
        """
        ```toml
        [connections.snowflake]
        account = "your_snowflake_account_identifier"
        user = "YOUR_SNOWFLAKE_USER"
        password = "YOUR_SNOWFLAKE_PASSWORD"
        role = "YOUR_SNOWFLAKE_ROLE"
        warehouse = "YOUR_SNOWFLAKE_WAREHOUSE"
        database = "YOUR_DAB_DATABASE"
        schema = "YOUR_DAB_SCHEMA"
        ```
        """
    )
    st.exception(e)