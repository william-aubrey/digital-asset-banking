# IDEF0 Process Model for the AIM Data Pipeline (Heuristic H1)

This document provides the IDEF0 decomposition for the data pipeline that constitutes the Agentic Insight Motor (AIM). It is a specific, detailed instance of the generic `A3: Execute Heuristics` process.

The processes defined here are governed by the conceptual standards outlined in the `dimensions_of_quality_in_a_data_pipeline.md` document.

---
## A-0: Execute Data Pipeline Lifecycle (Context Diagram)

This is the highest-level view of the AIM data pipeline, defining its overall scope and purpose.

*   **Function Name**: Execute Data Pipeline Lifecycle
*   **Purpose**: To reliably and efficiently ingest raw data from source systems, transform it into analysis-ready formats, and deliver it for visualization and modeling.
*   **Viewpoint**: From the perspective of the Data Engineering team operating the Agentic Insight Motor (AIM).

### ICOMs (Inputs, Controls, Outputs, Mechanisms)

#### Inputs
*   `Raw Source Data Feeds`: The continuous stream of data from operational systems (the Heuristics being measured).

#### Controls
*   `Dimensions of Quality`: The four key standards (Cost, Performance, Velocity, Accuracy) that govern all pipeline activities. [`cite: dimensions_of_quality_in_a_data_pipeline.md`]
*   `Business Requirements`: The specific questions and metrics the business needs to answer.
*   `Data Model Schemas`: The formal definitions for target data structures (Vault, Marts).

#### Outputs
*   `Analysis-Ready Datasets`: The curated data marts and model inputs delivered to analysts.
*   `Performance Dashboards`: The visualized data products for end-users.
*   `Pipeline Operational Metrics`: Data about the pipeline's own performance (cost, runtime, etc.), which feeds back into the FHOA loop.

#### Mechanisms
*   `Agentic Insight Motor (AIM)`: The collection of tools that execute the pipeline.
*   `Snowflake Data Warehouse`: The core RDBMS for storage and compute.
*   `Matillion ETL/ELT`: The primary tool for data transformation.
*   `Data Engineers & Analysts`: The human agents who design, operate, and monitor the pipeline.

---
## A0: Execute Data Pipeline Lifecycle (Decomposition)

This diagram breaks down the A-0 box into three core stages, mapping directly to the pipeline segments described in the quality dimensions document.

*   **A1: Ingest & Stage Source Data**: Covers the "System of Record Pipeline Segments" (Data Lakes, Ingestion, Standardization). Its goal is to get raw data into the warehouse in a clean, standardized, and auditable format.
    *   **Inputs**: `Raw Source Data Feeds`
    *   **Controls**: `Ingestion & Standardization Rules`, `Data Quality Checks`
    *   **Outputs**: `Standardized & Staged Data` (to A2), `Ingestion Logs`
    *   **Mechanisms**: `Data Lake (S3)`, `Matillion (Ingestion Jobs)`, `CDC Tools`

*   **A2: Integrate & Model Business Data**: Covers the core "Domain Pipeline Segments" (Source Vault, Business Vault, Dimensional Models). Its goal is to apply business logic to create an integrated enterprise view and prepare analysis-optimized data marts.
    *   **Inputs**: `Standardized & Staged Data` (from A1)
    *   **Controls**: `Business Rules`, `Data Vault Modeling Standards`, `Dimensional Modeling Standards`
    *   **Outputs**: `Integrated Business Vault Data`, `Dimensional Data Marts` (to A3)
    *   **Mechanisms**: `Snowflake (Compute)`, `Matillion (Transformation Jobs)`, `Data Modelers`

*   **A3: Prepare & Deliver Analytical Products**: Covers the final "Domain Pipeline Segments" (Predictive Models, Data Visualization). This is the "last mile" where data is packaged into its final, consumable form.
    *   **Inputs**: `Dimensional Data Marts` (from A2)
    *   **Controls**: `BI Dashboard Requirements`, `ML Model Specifications`
    *   **Outputs**: `Performance Dashboards`, `Predictive Model Datasets`, `Published Visualizations`
    *   **Mechanisms**: `BI Tools (Tableau, Sigma)`, `ML Frameworks`, `Data Analysts`, `Data Scientists`

---

### Relationship to FHOA Framework

This entire A3.H1 process model is a Heuristic. The data it produces (`Pipeline Operational Metrics`) becomes the `Raw Transactional & Performance Data` input for the `A1: Conduct Analytics` function. This allows the FHOA framework to analyze and improve the performance of the AIM itself, creating the critical meta-feedback loop.

