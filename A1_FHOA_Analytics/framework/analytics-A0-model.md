# FHOA Analytics - A0-Level Process Model

This document outlines the top-level conceptual activities of the `FHOA_Analytics` layer, framed as an IDEF0 A0-level decomposition.

The primary function of the analytics layer is **"Provide System Performance Insights."** This function is decomposed into the following five core sub-functions (A1-A5).

---

### A1: Ingest and Stage Data

*   **Purpose:** To acquire raw performance data from the Heuristics layer and land it in the analytics environment with perfect fidelity.
*   **Key Inputs:** Raw data streams, application logs.
*   **Key Controls:** Source system schemas, API contracts.
*   **Key Outputs:** Staged, raw data assets (the contents of the `sources` directory).

### A2: Integrate and Historize Data

*   **Purpose:** To transform and combine raw data from multiple sources into a single, non-volatile, auditable, enterprise-wide view.
*   **Key Inputs:** Staged raw data.
*   **Key Controls:** Data Vault 2.0 modeling standards, business rules.
*   **Key Outputs:** The integrated Data Vault (the contents of the `vault` directory).

### A3: Shape and Serve Data

*   **Purpose:** To transform the integrated data from the `vault` into high-performance, easy-to-use models tailored for specific business domains.
*   **Key Inputs:** Data from the `vault`.
*   **Key Controls:** Business requirements, dimensional modeling principles.
*   **Key Outputs:** Dimensional data marts (the contents of the `marts` directory).

### A4: Analyze and Productize Insights

*   **Purpose:** To actively use the prepared data to answer questions, generate predictions, and deliver value back to the FHOA loop.
*   **Key Inputs:** Data from `marts` and `vault`.
*   **Key Controls:** Business questions, statistical methods, visualization best practices.
*   **Key Outputs:** BI dashboards, analytical reports, trained ML models (the contents of the `products` directory).

### A5: Govern and Operate Analytics

*   **Purpose:** A cross-cutting function to ensure the entire analytics system is cost-effective, secure, compliant, and of high quality.
*   **Key Inputs:** Cost data, audit logs, performance metrics.
*   **Key Controls:** Budgets, compliance policies (GDPR, SOC2), SLAs.
*   **Key Outputs:** Governance policies, operational procedures, cost reports, quality dashboards (the contents of the `governance` directory).