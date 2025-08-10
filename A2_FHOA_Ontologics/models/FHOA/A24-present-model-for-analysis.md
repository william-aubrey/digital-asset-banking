# FHOA Ontologics (A2.4) Process Model: Present Model for Analysis

This document provides the IDEF0-style decomposition for the **A2.4: Present Model for Analysis** function. Its purpose is to detail the sub-processes required for a Streamlit application to query the `ONTOLOGICS_DB`, process the data, and render an interactive visualization of an IDEF0 model.

---

## A2.4: Present Model for Analysis (Top-Level Function)

- **Purpose**: To query the populated IDEF0 database and render the process hierarchy and its connections in a user-friendly web interface for analysis.
- **Inputs**: `User Request` (to view a model)
- **Controls**: `Snowflake Connection Secrets`, `RBAC Policy Model`
- **Outputs**: `Visual Model Representation`
- **Mechanisms**: `fhoa-a24-present-model-for-analysis (Agent)`, `Streamlit`, `Snowflake Connection`, `Graph Visualization Library`

---

## A2.4 Decomposition: The Model Presentation Application Flow

The A2.4 function is decomposed into four sequential activities that model the workflow of a data-driven Streamlit application.

### A2.4.1: Establish Secure Session

- **Purpose**: To initialize the Streamlit application and establish a secure, authenticated connection to the Snowflake database.
- **Inputs**: `User Request` (initiates the app run)
- **Controls**: `Snowflake Connection Secrets` (from `.streamlit/secrets.toml`), `RBAC Policy Model`
- **Outputs**: `Authenticated Snowflake Session` (to A2.4.2)
- **Mechanisms**: `Streamlit Connection Manager (st.connection)`, `Snowflake Python Connector`

### A2.4.2: Fetch IDEF0 Model Data

- **Purpose**: To execute SQL queries against the `ONTOLOGICS_DB` to retrieve the hierarchical data for a specified IDEF0 model.
- **Inputs**: `Authenticated Snowflake Session` (from A2.4.1), `Model Selection Criteria` (from user UI)
- **Controls**: `IDEF0 Data Model Schema`
- **Outputs**: `Raw Model Data (DataFrames)` (to A2.4.3)
- **Mechanisms**: `Snowflake Connection Query Method (conn.query)`, `SQL Queries`

### A2.4.3: Construct Graph Representation

- **Purpose**: To transform the raw, tabular model data into a structured graph format (nodes and edges) suitable for visualization.
- **Inputs**: `Raw Model Data (DataFrames)` (from A2.4.2)
- **Controls**: `Graph Data Structure Definition`
- **Outputs**: `Graph Object` (to A2.4.4)
- **Mechanisms**: `Pandas DataFrame Manipulation`, `Graph Library Object Model (e.g., graphviz.Digraph)`

### A2.4.4: Render Model Visualization

- **Purpose**: To render the graph object as an interactive visual diagram within the Streamlit user interface.
- **Inputs**: `Graph Object` (from A2.4.3)
- **Controls**: `Streamlit UI Component Parameters`
- **Outputs**: `Visual Model Representation` (displayed in UI)
- **Mechanisms**: `Streamlit Graphviz Component (st.graphviz_chart)`, `User's Web Browser`

---