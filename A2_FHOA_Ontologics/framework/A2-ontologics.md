# FHOA Ontologics (A2) Process Model

## FHOA Ontologics (A2) Process Model

This document provides the IDEF0-style decomposition for the **A2: Curate Ontology** function within the FHOA framework. Its primary purpose is to define, maintain, and refine the official IDEF0 process models that serve as the enterprise's conceptual blueprint.

---
## Chapter Navigation

- FHOA Ontologics (A2) Process Model
- A2: Curate Ontology (Top-Level Function)
- A2 Decomposition: The Lifecycle of a Conceptual Model
- A2.1: Bootstrap New Process Model (First Time)
  - A2.1.1: Elicit Process Knowledge
  - A2.1.2: Model Process in IDEF0
  - A2.1.3: Persist Model to Database
- A2.2: Refine Existing Process Model (Ongoing)
  - A2.2.1: Triage Improvement Insights
  - A2.2.2: Draft Conceptual Model Revision
  - A2.2.3: Validate and Reconcile Model
  - A2.2.4: Publish and Version Model

---

## A2: Curate Ontology (Top-Level Function)

- **Purpose**: To translate business strategy and analytical insights into formal, standardized process models that guide enterprise operations and system development.
- **Inputs**: Improvement Insights (from A1 Analytics), Business Strategy & Goals, Subject Matter Expert (SME) Knowledge
- **Controls**: FHOA Framework Principles, IDEF0 Modeling Standard, Versioning Policy
- **Outputs**: Conceptual Process Models (to A1 Analytics & A3 Heuristics), Modeling Change Requests
- **Mechanisms**: IDEF0 Modeling Tools, Snowflake `IDEF0_MODEL_DB`, Process Architects & Ontologists, AI Assistants

---

## A2 Decomposition: The Lifecycle of a Conceptual Model

The A2 function is decomposed into two distinct sub-processes that represent the two primary pathways of ontological work: creating a new model from scratch and refining an existing one.

---

### A2.1: Bootstrap New Process Model (First Time)

Describes the "zero to one" creation of a conceptual model for a process that has never been formally documented.

- **Purpose**: To take unstructured knowledge about a new process and produce the first version-controlled, validated model.
- **Inputs**: Business Requirements, SME Knowledge
- **Controls**: IDEF0 Viewpoint & Purpose
- **Outputs**: Version 1 Conceptual Process Model
- **Mechanisms**: Human Analyst, AI Assistant, IDEF0 Data Collection App

#### A2.1.1: Elicit Process Knowledge

- **Purpose**: To gather unstructured information about a process from relevant sources to understand its current state.
- **Inputs**: Business Requirements, Existing Documentation, Stakeholder Feedback
- **Controls**: IDEF0 Viewpoint & Purpose
- **Outputs**: Raw Process Notes, Unstructured Process Descriptions
- **Mechanisms**: Human Analyst, AI Assistant, IDEF0 Data Collection App

#### A2.1.2: Model Process in IDEF0

- **Purpose**: To translate unstructured process knowledge into the formal, hierarchical IDEF0 structure of functions and ICOMs.
- **Inputs**: Raw Process Notes, Unstructured Process Descriptions (from A2.1.1)
- **Controls**: IDEF0 Standard & Syntax
- **Outputs**: Formal IDEF0 Markdown Document
- **Mechanisms**: Human Analyst, AI Assistant

#### A2.1.3: Persist Model to Database

- **Purpose**: To translate the formal IDEF0 model into a physical representation by populating the relational database in Snowflake.
- **Inputs**: Formal IDEF0 Markdown Document (from A2.1.2)
- **Controls**: IDEF0 Data Model Schema
- **Outputs**: Populated IDEF0 Database Records, SQL INSERT Script
- **Mechanisms**: Human Analyst, AI Assistant, Snowflake Database

---

### A2.2: Refine Existing Process Model (Ongoing)

Describes the "one to N" iterative improvement of an existing, published model based on analytical feedback.

- **Purpose**: To manage the lifecycle of changes to an existing model through a formal governance process, driving continuous improvement.
- **Inputs**: Improvement Insights (from A1 Analytics)
- **Controls**: Prioritization Framework, Versioning Policy
- **Outputs**: New Version of Conceptual Process Model
- **Mechanisms**: Product Manager, Process Architect, SMEs, Data Governance Team

#### A2.2.1: Triage Improvement Insights

- **Purpose**: To evaluate incoming Improvement Insights, prioritize them against business goals, and scope the required modeling effort.
- **Inputs**: Improvement Insights (from A1.4), Business Strategy & Goals
- **Controls**: Prioritization Framework, Resource Availability
- **Outputs**: Scoped Modeling Tasks, Prioritized Backlog
- **Mechanisms**: Project Management Tools, Product Manager, Lead Ontologist

#### A2.2.2: Draft Conceptual Model Revision

- **Purpose**: To translate a scoped modeling task into a draft revision of an existing IDEF0 diagram.
- **Inputs**: Scoped Modeling Tasks (from A2.2.1), SME Knowledge, Existing Process Model
- **Controls**: IDEF0 Modeling Standard
- **Outputs**: Draft IDEF0 Model Revision, Clarification Questions for SMEs
- **Mechanisms**: IDEF0 Modeling Tool, Process Architect, AI Assistant

#### A2.2.3: Validate and Reconcile Model

- **Purpose**: To review the draft model revision with stakeholders to ensure it is accurate, complete, and aligned with business reality.
- **Inputs**: Draft IDEF0 Model Revision (from A2.2.2)
- **Controls**: SME Knowledge, Business Requirements
- **Outputs**: Validated IDEF0 Model, Change Logs
- **Mechanisms**: Review Meetings, Collaboration Tools, SMEs, Business Stakeholders

#### A2.2.4: Publish and Version Model

- **Purpose**: To formally commit the validated model to the `IDEF0_MODEL_DB`, making it the new "single source of truth".
- **Inputs**: Validated IDEF0 Model (from A2.2.3)
- **Controls**: Versioning Policy, Access Control Rules
- **Outputs**: Conceptual Process Model (New Version), Publication Notifications
- **Mechanisms**: Snowflake `IDEF0_MODEL_DB`, ModelOps CI/CD Pipeline, Data Governance Team

---