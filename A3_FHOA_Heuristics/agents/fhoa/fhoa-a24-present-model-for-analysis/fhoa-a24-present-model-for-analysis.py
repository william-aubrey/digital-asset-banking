import streamlit as st
import pandas as pd
import graphviz

# A2.4.1: Establish Secure Session
def a241_establish_secure_session():
    """
    Initializes the Streamlit application and establishes a secure,
    authenticated connection to the Snowflake database.
    """
    st.set_page_config(layout="wide", page_title="FHOA IDEF0 Model Viewer")
    st.title("A2.4: Present Model for Analysis")

    try:
        # This uses the connection information from .streamlit/secrets.toml
        conn = st.connection("snowflake")
        st.success("Snowflake connection established.")
        return conn
    except Exception as e:
        st.error(f"Failed to connect to Snowflake: {e}")
        return None

# A2.4.2: Fetch IDEF0 Model Data
def a242_fetch_idef0_model_data(conn, model_id):
    """
    Executes SQL queries against the ONTOLOGICS_DB to retrieve the
    hierarchical data for a specified IDEF0 model.
    """
    if not conn or not model_id:
        return None, None

    with st.spinner(f"Fetching data for model {model_id}..."):
        try:
            # Query for FUNCTIONS (boxes) based on the DDL
            boxes_query = f"SELECT * FROM ONTOLOGICS.IDEF0.FUNCTIONS WHERE MODEL_ID = {model_id};"
            boxes_df = conn.query(boxes_query)

            # Query for FUNCTION_ENTITIES (arrows) and join with ENTITIES to get names
            # This query gets all arrow-like connections for a given model.
            arrows_query = f"""
                SELECT fe.*, e.ENTITY_NAME, e.DESCRIPTION
                FROM ONTOLOGICS.IDEF0.FUNCTION_ENTITIES fe
                JOIN ONTOLOGICS.IDEF0.ENTITIES e ON fe.ENTITY_ID = e.ENTITY_ID
                JOIN ONTOLOGICS.IDEF0.FUNCTIONS f ON fe.FUNCTION_ID = f.FUNCTION_ID
                WHERE f.MODEL_ID = {model_id};
            """
            arrows_df = conn.query(arrows_query)

            return boxes_df, arrows_df
        except Exception as e:
            st.error(f"Failed to fetch model data: {e}")
            return None, None


# A2.4.3: Construct Graph Representation
def a243_construct_graph_representation(boxes_df, arrows_df, model_id):
    """
    Transforms the raw, tabular model data into a structured graph
    format (nodes and edges) suitable for visualization.
    """
    if boxes_df is None or arrows_df is None or boxes_df.empty:
        st.warning("No data available to construct the graph.")
        return None

    # Initialize a directed graph with attributes for an IDEF0-like appearance
    dot = graphviz.Digraph(
        comment=f'IDEF0 Model {model_id}',
        graph_attr={'rankdir': 'LR', 'splines': 'ortho'}
    )

    # Add nodes (functions/boxes)
    for index, row in boxes_df.iterrows():
        # Use HTML-like labels for better formatting (name on top, node number below)
        label = f"<{row['FUNCTION_NAME']}<br/><font point-size='10'>A{row['NODE']}</font>>"
        dot.node(
            name=str(row['FUNCTION_ID']),
            label=label,
            shape='box'
        )

    # Add edges for internal connections (where a source function exists in the model)
    internal_arrows = arrows_df.dropna(subset=['SOURCE_FUNCTION_ID'])
    for index, row in internal_arrows.iterrows():
        source_id = str(int(row['SOURCE_FUNCTION_ID']))
        dest_id = str(row['FUNCTION_ID'])
        attrs = {
            'label': row['ENTITY_NAME'],
            'tailport': 'e' # Outputs always come from the east (right) side of a box
        }
        # Set arrow destination based on its role (Input, Control)
        if row['ROLE'] == 'INPUT':
            attrs['headport'] = 'w' # Inputs connect to the west (left) side
        elif row['ROLE'] == 'CONTROL':
            attrs['headport'] = 'n' # Controls connect to the north (top) side

        dot.edge(source_id, dest_id, **attrs)

    # Add edges for external arrows (inputs/controls from outside the diagram's scope)
    external_arrows = arrows_df[arrows_df['SOURCE_FUNCTION_ID'].isna()]
    for index, row in external_arrows.iterrows():
        dest_id = str(row['FUNCTION_ID'])
        # Create a small, invisible node to be the source of the external arrow
        source_name = f"ext_{row['FUNCTION_ENTITY_ID']}"
        dot.node(source_name, label="", shape="point", width="0")

        attrs = {'label': row['ENTITY_NAME']}
        if row['ROLE'] == 'INPUT':
            attrs['headport'] = 'w'
        elif row['ROLE'] == 'CONTROL':
            attrs['headport'] = 'n'

        dot.edge(source_name, dest_id, **attrs)

    return dot


# A2.4.4: Render Model Visualization
def a244_render_model_visualization(graph_object):
    """
    Renders the graph object as a visual diagram within
    the Streamlit user interface.
    """
    if graph_object:
        st.write("### IDEF0 Model Diagram")
        st.graphviz_chart(graph_object)
    else:
        st.warning("No graph object to render.")


def main():
    """Main function to run the Streamlit application."""
    conn = a241_establish_secure_session()

    if conn:
        # In a real app, you'd get this from a selectbox querying available models
        model_id_input = st.text_input("Enter Model ID to visualize:", "0")

        if st.button("Present Model"):
            boxes, arrows = a242_fetch_idef0_model_data(conn, model_id_input)

            # Display raw data in expanders for debugging
            if boxes is not None and not boxes.empty:
                with st.expander("Show Raw Function (Box) Data"):
                    st.dataframe(boxes)
            if arrows is not None and not arrows.empty:
                 with st.expander("Show Raw Entity (Arrow) Data"):
                    st.dataframe(arrows)

            graph = a243_construct_graph_representation(boxes, arrows, model_id_input)
            a244_render_model_visualization(graph)

if __name__ == "__main__":
    main()