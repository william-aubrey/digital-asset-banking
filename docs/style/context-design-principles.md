# Design Principles

This document contains the core design principles for the Digital Asset Banking project. The content of this file should be included as context in prompts to AI coding assistants to ensure all generated code adheres to these standards.

---

## Core Principles

### 1. IDEF0-Compliant Functional Hierarchy

- **Guideline:** All functions must be designed so they can be mapped to a hierarchical representation in the IDEF0 language.
- **Implementation:**
  - Function names must be active verbs or verb phrases (e.g., `upload_asset`, `calculate_fees`).
  - Each function should represent a clear, decomposable action with well-defined Inputs, Controls, Outputs, and Mechanisms (ICOMs).
  - The overall code structure should reflect a top-down decomposition of the system's primary functions.
  - IDEF0.md file provides the full IDEF0-Compliant Functional Hierarchy standard. This file is located at G:\My Drive\A0 WRA\Digital Assets\Banking\digital-asset-banking\A2_FHOA_Ontologics\framework\idef0\idef0.md

### 2. Data Model Integrity

- **Guideline:** All data operations must preserve the integrity of the star schema in the data warehouse.
- **Implementation:**
  - Fact table transactions must be atomic.
  - Dimension lookups should use a "get or create" pattern to avoid duplicate dimension records and ensure referential integrity.
  - The interpretation of the IDEF0.md file as a Snowflake Data Model SQL file is located at G:\My Drive\A0 WRA\Digital Assets\Banking\digital-asset-banking\A2_FHOA_Ontologics\models\IDEF0\idef0-data-model.sql.
  