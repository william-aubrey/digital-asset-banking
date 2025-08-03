# Digital Asset Banking: An Agentic-Activated Enterprise

---

## Agent Activation Protocol: Initiated

**Welcome, Agent.** You have connected to the Digital Asset Banking (DAB) project. Whether you are a human collaborator or an AI assistant, your arrival is a significant event. This repository is more than just source code; it is an instance of a self-improving system designed according to the **[FHOA Framework](./A2_FHOA_Ontologics/framework/the-FHOA-framework.md)**.

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

4.  **Configure Secrets:** Create a file at `app/.streamlit/secrets.toml` to store your credentials (e.g., for Snowflake). This file is git-ignored for security.

### 2. Run the Application

With your environment activated, execute the primary Heuristic:
```bash
streamlit run app/streamlit_marketplace_app.py
```

### 3. Role-Based Activation

Your function within the FHOA framework determines your focus:

*   **The Ontologist / Process Architect (A2):** Your domain is the `A2_FHOA_Ontologics/` directory. Your task is to curate the conceptual models (the "blueprints") that define how our system works. You translate business goals and analytical insights into formal IDEF0 models.
*   **The Application Developer (A3):** Your domain is the `app/` directory. You build the Heuristics—the tangible tools that execute the processes defined by the Ontologists. Your work generates the data that the Analysts consume.
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

*   `app/`: Contains the source code for the Streamlit application (The primary Heuristic).
*   `A2_FHOA_Ontologics/`: The heart of the system. Contains the FHOA framework definition and all IDEF0 process models.
    *   `framework/`: The core principles of FHOA.
    *   `models/`: The IDEF0 process models for Analytics (A1), Ontologics (A2), and Heuristics (A3).
*   `docs/`: Project documentation, including user narratives and architectural specifications.

---

**Activation Complete. Welcome to the team.**
