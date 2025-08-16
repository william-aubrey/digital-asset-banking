# IDEF0 Diagrammer — v0.3.3b

Baseline rollback with hard orthogonal routing and sticky stubs.

- Open `index.html` in a browser.
- Click a handle, press **S** to add a stub.
- Double-click a connector/stub label to edit (or pick from the dropdown).
- Save/Load uses localStorage. Export JSON & SVG are built-in.

Files: `index.html`, `styles.css`, `app.js`, `sample_models.json`, `schema_patch.sql`, `streamlit_idef0_page.py`.
## Running the Streamlit Application

The `fhoa-a24.py` script acts as a dynamic backend and wrapper for the IDEF0 diagrammer, using the Streamlit framework to serve the interactive frontend. It can load model data from a Snowflake database or local files.

Here is a step-by-step description of what happens when you run the script:

1.  **Start the Application**: From your terminal, navigate to the project directory and run the following command:
    ```bash
    streamlit run fhoa-a24.py
    ```

2.  **Web Server Initialization**: Streamlit starts a local web server and provides a URL (usually `http://localhost:8501`) that you can open in your web browser.

3.  **Backend Script Execution (Python)**:
    -   The `fhoa-a24.py` script is executed from top to bottom.
    -   **Data Loading**:
        -   It first attempts to connect to a Snowflake database using credentials stored in Streamlit's secrets (`.streamlit/secrets.toml`).
        -   If the connection is successful, it queries the `FUNCTIONS`, `FUNCTION_ENTITIES`, and `MODELS` tables.
        -   The script then processes this relational data, transforming it into a hierarchical JSON structure that represents the IDEF0 models. This involves calculating node positions, creating edges between functions based on shared entities, and generating stubs for external inputs/outputs.
        -   **Fallback**: If the Snowflake connection fails or returns no data, the script attempts to load a default set of models from the local `sample_models.json` file.
    -   **Sidebar UI**: A sidebar is rendered with controls. This includes an expander that allows a user to upload or paste new models in JSON format. These user-provided models are stored in the session state.
    -   **HTML Generation**:
        -   The script reads the `index.html` template file.
        -   It finds and reads the `app.js` and `styles.css` files and injects their contents directly into the HTML as `<script>` and `<style>` tags. This makes the final HTML self-contained.
        -   It combines the models loaded from Snowflake (or the local file) with any models uploaded by the user.
        -   This combined list of models is serialized into a JSON string. The script then replaces the placeholder `/*__MODELS__*/` inside `index.html` with this JSON payload.
    -   **Rendering**: The final, fully-formed HTML is passed to Streamlit's `st.components.v1.html` function, which renders it inside an iframe on the web page.

4.  **Frontend Execution (Browser)**:
    -   The browser receives and renders the HTML from the Streamlit server.
    -   The inlined `app.js` script runs. It finds the model data, which was injected by the Python script, in the global `window.MODELS` object.
    -   The script populates the "Model" and "Context" dropdown menus based on the available models.
    -   When a model and context are selected, the JavaScript code reads the corresponding diagram data and uses SVG to draw the functions, edges, and stubs on the canvas.
    -   Event listeners are attached to the SVG elements, allowing for basic interactions like selecting handles to draw new connections.

5.  **Interaction and Reruns**:
    -   When you interact with a Streamlit widget in the sidebar (e.g., uploading a new model), the Python script reruns.
    -   Streamlit's caching (`@st.cache_data` and `@st.cache_resource`) prevents expensive operations like reconnecting to Snowflake or reprocessing the same data on every rerun.
    -   The script regenerates the HTML with the updated model list and sends it to the component, causing the diagrammer to refresh.

This process creates a powerful data-driven application where the backend (Python/Streamlit) is responsible for fetching and preparing data, while the frontend (HTML/CSS/JS) is responsible for the interactive visualization.
