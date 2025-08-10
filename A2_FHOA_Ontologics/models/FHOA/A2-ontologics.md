# FHOA Ontologics (A2) Process Model

This document provides the IDEF0-style decomposition for the **A2: Manage Ontologic Models** function within the FHOA framework. Its primary purpose is to define, maintain, and refine the official IDEF0 process models that serve as the enterprise's conceptual blueprint.

---
## Chapter Navigation

- FHOA Ontologics (A2) Process Model
- A2: Manage Ontologic Models (Top-Level)
- A2.1: Provision Ontologic Infrastructure
- A2.2: Create and Ingest New Process Model
  - A2.2.1: Elicit Process Knowledge
  - A2.2.2: Model Process in IDEF0
  - A2.2.3: Ingest and Persist Model
- A2.3: Refine Existing Process Model
  - A2.3.1: Triage Improvement Insights
  - A2.3.2: Draft Conceptual Model Revision
  - A2.3.3: Validate and Reconcile Model
  - A2.3.4: Publish and Version Model
- A2.4: Present Model for Analysis
 
---

# A2: Manage Ontologic Models (Top-Level Function)

- **Purpose**: To translate business strategy and analytical insights into formal, standardized process models that guide enterprise operations and system development.
- **Inputs**: Improvement Insights (from A1 Analytics), Business Strategy & Goals, Subject Matter Expert (SME) Knowledge
- **Controls**: FHOA Framework Principles, IDEF0 Modeling Standard, Versioning Policy
- **Outputs**: Conceptual Process Models (to A1 Analytics & A3 Heuristics), Modeling Change Requests
- **Mechanisms**: FHOA Synthesizer (Agent), Snowflake `IDEF0_MODEL_DB`, Process Architects & Ontologists

---

# A2 Decomposition: The Lifecycle of an Ontologic Model

The A2 function is decomposed into four sub-processes that represent the full lifecycle of an ontologic model, from infrastructure setup to ongoing refinement and analysis.

---

## A2.1: Provision Ontologic Infrastructure

- **Purpose**: To create or verify the necessary database schema and access control policies for storing and managing IDEF0 models.
- **Inputs**: `IDEF0 Data Model (SQL)`
- **Controls**: `Database Credentials`
- **Outputs**: `Provisioned Database Schema`, `Applied RBAC Policies`
- **Mechanisms**: `fhoa-a21-provision-ontologic-infrastructure (Agent)`, `Snowflake Connection`

---

## A2.2: Create and Ingest New Process Model

Describes the "zero to one" creation of a conceptual model. This involves human-led elicitation and modeling to create a markdown artifact, followed by agent-led ingestion into the database.

### A2.2.1: Elicit Process Knowledge
- **Purpose**: To gather unstructured information about a process from relevant sources to understand its current state.
- **Inputs**: `Business Requirements`, `Existing Documentation`, `Stakeholder Feedback`
- **Controls**: `IDEF0 Viewpoint & Purpose`
- **Outputs**: `Raw Process Notes`, `Unstructured Process Descriptions`
- **Mechanisms**: `Human Analyst`, `AI Assistant`, `Interview Kits`

### A2.2.2: Model Process in IDEF0
- **Purpose**: To translate unstructured process knowledge into the formal, hierarchical IDEF0 structure of functions and ICOMs, resulting in a markdown document.
- **Inputs**: `Raw Process Notes` (from A2.2.1)
- **Controls**: `IDEF0 Standard & Syntax`
- **Outputs**: `Formal IDEF0 Markdown Document`
- **Mechanisms**: `Human Analyst`, `AI Assistant`, `Text Editor`

### A2.2.3: Ingest and Persist Model
- **Purpose**: To parse the formal IDEF0 markdown document and populate the relational database in Snowflake.
- **Inputs**: `Formal IDEF0 Markdown Document` (from A2.2.2), `snowflake-rbac-policy-model.md`
- **Controls**: `IDEF0 Data Model Schema`
- **Outputs**: `Populated IDEF0 Database Records`
- **Mechanisms**: `fhoa-a223-ingest-ontologic-model (Agent)`, `Python Parser`

## A2.3: Refine Existing Process Model

Describes the "one to N" iterative improvement of an existing, published model based on analytical feedback.

- **Purpose**: To manage the lifecycle of changes to an existing model through a formal governance process, driving continuous improvement.
- **Inputs**: Improvement Insights (from A1 Analytics)
- **Controls**: Prioritization Framework, Versioning Policy
- **Outputs**: New Version of Conceptual Process Model
- **Mechanisms**: Product Manager, Process Architect, SMEs, Data Governance Team

### A2.3.1: Triage Improvement Insights
- **Purpose**: To evaluate incoming `Improvement Insights`, prioritize them against business goals, and scope the required modeling effort.
- **Inputs**: `Improvement Insights` (from A1.4), `Business Strategy & Goals`
- **Controls**: `Prioritization Framework`, `Resource Availability`
- **Outputs**: `Scoped Modeling Tasks`, `Prioritized Backlog`
- **Mechanisms**: `Project Management Tools`, `Product Manager`, `Lead Ontologist`

### A2.3.2: Draft Conceptual Model Revision
- **Purpose**: To translate a scoped modeling task into a draft revision of an existing IDEF0 markdown document.
- **Inputs**: `Scoped Modeling Tasks` (from A2.3.1), `SME Knowledge`, `Existing Process Model`
- **Controls**: `IDEF0 Modeling Standard`
- **Outputs**: `Draft IDEF0 Model Revision`, `Clarification Questions for SMEs`
- **Mechanisms**: `IDEF0 Modeling Tool`, `Process Architect`, `AI Assistant`

### A2.3.3: Validate and Reconcile Model
- **Purpose**: To review the draft model revision with stakeholders to ensure it is accurate, complete, and aligned with business reality.
- **Inputs**: `Draft IDEF0 Model Revision` (from A2.3.2)
- **Controls**: `SME Knowledge`, `Business Requirements`
- **Outputs**: `Validated IDEF0 Model`, `Change Logs`
- **Mechanisms**: `Review Meetings (Kit Cycle)`, `Collaboration Tools`, `SMEs`

### A2.3.4: Publish and Version Model
- **Purpose**: To formally commit the validated model to the `IDEF0_MODEL_DB` by ingesting the updated markdown, making it the new "single source of truth".
- **Inputs**: `Validated IDEF0 Model` (from A2.3.3)
- **Controls**: `Versioning Policy`, `Access Control Rules`
- **Outputs**: `Conceptual Process Model (New Version)`, `Publication Notifications`
- **Mechanisms**: `FHOA Synthesizer (Agent)`, `ModelOps CI/CD Pipeline`

---

## A2.4: Present Model for Analysis

- **Purpose**: To query the populated IDEF0 database and render the process hierarchy and its connections in a user-friendly web interface for analysis.
- **Inputs**: `User Request`
- **Controls**: (None)
- **Outputs**: `Visual Model Representation`
- **Mechanisms**: `Streamlit`, `Snowflake Connection`, `Graph Visualization Library`

---