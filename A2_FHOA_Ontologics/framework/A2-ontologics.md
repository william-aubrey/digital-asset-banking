# FHOA Ontologics (A2) Process Model

This document provides the IDEF0-style decomposition for the **A2: Curate Ontology** function within the FHOA framework. Its primary purpose is to define, maintain, and refine the official IDEF0 process models that serve as the enterprise's conceptual blueprint.

---

## A2: Curate Ontology (Top-Level Function)

- **Purpose**: To translate business strategy and analytical insights into formal, standardized process models that guide enterprise operations and system development.
- **Inputs**: Improvement Insights (from A1 Analytics), Business Strategy & Goals, Subject Matter Expert (SME) Knowledge
- **Controls**: FHOA Framework Principles, IDEF0 Modeling Standard, Versioning Policy
- **Outputs**: Conceptual Process Models (to A1 Analytics & A3 Heuristics), Modeling Change Requests
- **Mechanisms**: IDEF0 Modeling Tools, Snowflake `IDEF0_MODEL_DB`, Process Architects & Ontologists, AI Assistants

---

## A2 Decomposition: The Lifecycle of a Conceptual Model

The A2 function is decomposed into four activities that represent the lifecycle of creating or refining a process model.

### A2.1: Triage Improvement Insights

- **Purpose**: To evaluate incoming `Improvement Insights` from the Analytics layer, prioritize them against business goals, and scope the required modeling effort.
- **Inputs**: Improvement Insights (from A1.4), Business Strategy & Goals
- **Controls**: Prioritization Framework, Resource Availability
- **Outputs**: Scoped Modeling Tasks, Prioritized Backlog
- **Mechanisms**: Project Management Tools, Product Manager, Lead Ontologist

### A2.2: Draft Conceptual Model

- **Purpose**: To translate a scoped modeling task into a draft IDEF0 diagram, defining new functions, inputs, controls, outputs, and mechanisms based on SME knowledge.
- **Inputs**: Scoped Modeling Tasks (from A2.1), SME Knowledge
- **Controls**: IDEF0 Modeling Standard, Existing Process Models
- **Outputs**: Draft IDEF0 Models, Clarification Questions for SMEs
- **Mechanisms**: IDEF0 Modeling Tool, Process Architect, AI Assistant

### A2.3: Validate and Reconcile Model

- **Purpose**: To review the draft model with subject matter experts and stakeholders to ensure it is accurate, complete, and aligned with business reality.
- **Inputs**: Draft IDEF0 Models (from A2.2)
- **Controls**: SME Knowledge, Business Requirements
- **Outputs**: Validated IDEF0 Models, Change Logs
- **Mechanisms**: Review Meetings, Collaboration Tools, SMEs, Business Stakeholders

### A2.4: Publish and Version Model

- **Purpose**: To formally commit the validated model to the official repository (`IDEF0_MODEL_DB`), making it the new "single source of truth" for the enterprise.
- **Inputs**: Validated IDEF0 Models (from A2.3)
- **Controls**: Versioning Policy, Access Control Rules
- **Outputs**: Conceptual Process Models (published), Publication Notifications
- **Mechanisms**: Snowflake `IDEF0_MODEL_DB`, ModelOps CI/CD Pipeline, Data Governance Team

