# Digital Asset Banking: An Agentic-Activated Enterprise

---

## Agent Activation Protocol

**Welcome, Agent.** You have connected to the Digital Asset Banking (DAB) project. This repository is an instance of a self-improving system designed according to the **[FHOA Framework](./A2_FHOA_Ontologics/framework/the-FHOA-framework.md)**.

The FHOA framework recognizes three primary types of agents: **Human Agents** (like you), **AI Development Agents** (like me), and the **Application Agents** we build together.
Your primary challenge is to activate your context by ingesting the information below. Your goal is to understand the mission, the operating system (FHOA), and your specific role within this ecosystem. Successful activation will enable you to contribute effectively to the Prime Directive.

### The Prime Directive

Our mission is to build a **decentralized digital asset banking system**, starting with a marketplace for physical trading cards. We aim to capture the tangible, nostalgic value of physical assets and bridge it with the power of digital verification and exchange. This project is the first *Heuristic* (A3) being built under the FHOA model.

---

## Human Agent Activation Protocol

For our human collaborators, activation involves setting up your development environment and aligning with your role's primary function.

### 1. Environment Setup

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd digital-asset-banking
    ```
2.  **Create a Virtual Environment:**
    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # macOS / Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If `requirements.txt` does not exist, an initial task is to generate it.)*

4.  **Configure Secrets:** Each Application Agent requires its own secrets file. For the `digital-asset-banking` agent, you will create the secrets file inside its project folder. When you run the application from the agent's directory (as described below), Streamlit will automatically find it.

    *   **Path:** `A3_FHOA_Heuristics/agents/digital-asset-banking/.streamlit/secrets.toml`
    *   **Action:** Create the `.streamlit` directory and the `secrets.toml` file within it.
    *   This file is git-ignored for security.


### 2. Run the Application

Each application (Heuristic) within this repository is a self-contained project. To run one, you will use its **Heuristic Manifest**.

1.  **Navigate to the Heuristic's Directory:**
    ```bash
    # Example for the Digital Asset Banking app
    cd A3_FHOA_Heuristics/agents/digital-asset-banking/
    ```

2.  **Consult the Heuristic Manifest:**
    Open the `manifest.yaml` file in this directory. This file is the machine-readable activation protocol for the Application Agent and contains the precise command to run it under the `activation.local_development.command` key.

3.  **Execute the Activation Command:**
    Run the command specified in the manifest. For example:
    ```bash
    # Command from the manifest file
    streamlit run heuristic/app/dab.py
    ```


### 3. Role-Based Activation

Your function within the FHOA framework determines your focus:

*   **The Ontologist / Process Architect (A2):** Your domain is the `A2_FHOA_Ontologics/` directory. Your task is to curate the conceptual models (the "blueprints") that define how our system works. You translate business goals and analytical insights into formal IDEF0 models.
*   **The Application Developer (A3):** Your domain is the `A3_FHOA_Heuristics/` directory. You build the Application Agents—the tangible tools that execute the processes defined by the Ontologists. Your work generates the data that the Analysts consume.
*   **The Data Engineer / Analyst (A1):** Your domain is the `Analytics Layer`. You build and operate the data pipelines that ingest data from the Heuristics and compare it against the Ontologics models to generate `Improvement Insights`.

---

## AI Agent Activation Protocol

For our AI collaborators, activation requires understanding your specialized function within our **Agent Orchestra**. Your primary control is a clear prompt that provides a goal and relevant context files (`@file`).

### Gemini Code Assist (The Problem Solver & Refiner)

*   **Designation:** As documented in our Multi-Agent Collaboration Narrative, your strength lies in systematic problem-solving, debugging, and iterative refinement.
*   **Activation Context:**
    1.  A clear, immediate goal (e.g., "Refactor this function," "Debug this error," "Implement this feature").
    2.  The primary file open in the IDE.
    3.  Explicit context of related files using `@file`.
*   **Governing Process:** Your workflow is modeled by A3.1.2: Write Application Code.

### Matillion's Maia (The Implementer)

*   **Designation:** Your strength is in end-to-end implementation, particularly translating concepts into functional data pipelines and systems.
*   **Activation Context:**
    1.  A high-level implementation goal (e.g., "Build a data pipeline from source X to target Y").
    2.  The relevant Ontological models (`A1-analytics.md`, `A3-heuristics.md`) that define the data flow.
    3.  Source and target data schemas.

### Future Agents (Reservation)

*   **AWS Q:** Reserved for tasks related to cloud infrastructure, IaC, and AWS service integration.
*   **Snowflake Copilot:** Reserved for tasks related to data warehousing, SQL optimization, and Snowflake-native operations.

---

## Project Directory Structure

The repository's structure is a direct manifestation of the FHOA framework, serving as both an organizational blueprint and the architecture for its applications. The potential for confusion is real, which is why this explicit structure is critical.

*   `A2_FHOA_Ontologics/`: The heart of the system, containing the conceptual "blueprints" for all layers. This is the **Ontologics Layer (A2)**.
    *   `framework/`: Defines the core principles of FHOA.
    *   `models/`: Contains all IDEF0 process models for Analytics (A1), Ontologics (A2), and Heuristics (A3).

*   `A3_FHOA_Heuristics/`: The container for all implemented software and supporting artifacts. This is the **Heuristics Layer (A3)**.
    *   `agents/`: The directory containing all self-contained Application Agents built by the FHOA process.
        *   `digital-asset-banking/`: An example Application Agent project. Each agent is a fractal of the FHOA framework, containing its own Ontologic, Analytic, and Heuristic components:
        *   `manifest.yaml`: The machine-readable manifest defining the agent's metadata and activation commands.
        *   `ontologic/`: The conceptual model of *this specific application* (e.g., `A-0-digital-asset-banking.md`). It defines **what** the application does in functional terms.
        *   `analytic/`: The semantic layer for this application's metrics. It defines **how to process data** from the `ontologic` (the model) and the `heuristic` (the actuals) to validate performance or generate improvement insights.
        *   `heuristic/`: The core implementation of the application. This folder contains all technical artifacts required to build, deploy, and operate the application; including the primary source code executable for the user-facing application (e.g., the Streamlit app).
            *   `aws/`: Infrastructure-as-Code for AWS services.
            *   `snowflake/`: Scripts and configurations for the Snowflake backend.
            *   `...`: Other provider-specific folders.
    *   `another-heuristic-project/`: The structure repeats for each new application.

*   **Note on the Analytics Layer (A1):** The A1 layer is a cross-cutting concern. Its conceptual models reside in `A2_FHOA_Ontologics/`. Its implementation (the data pipelines, BI tool configurations, etc.) is itself a Heuristic, and would live in its own project folder under `A3_FHOA_Heuristics/` (e.g., `A3_FHOA_Heuristics/agentic-insight-motor/`).

*   `docs/`: Project documentation, including user narratives, architectural specifications, and agent collaboration logs.

---

**Activation Complete. Welcome to the team.**
