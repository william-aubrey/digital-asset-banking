# Dimensions of Quality in a Data Pipeline

_Adapted from: "Dimensions of Quality in a Data Pipeline"_

Four key dimensions are used to assess the quality of an analytics platform:

## 1. Cost

Measured in dollars and resource consumption:
- Snowflake credits consumption
- Matillion server runtime hours
- Tableau license fees

> Strategies should minimize cost while balancing other quality dimensions.

## 2. Performance

Refers to data pipeline efficiency and resiliency:
- **Run-time**: Total end-to-end execution time
- **Throughput**: Volume of data processed per run
- **Idempotency**: Ability to rerun without side effects
- **Error Recovery**: Automatic recovery without human intervention

## 3. Development Velocity

Ideal pipeline automation vs. real-world tradeoffs:

> A perfect pipeline auto-generates data cataloging, ingestion schemas, semantic mappings, visual analytics, and predictive insights. In practice, development involves balancing advanced designs with maintainable, modular patterns for business analysts.

- **Process Governance**: Ensures discipline without undue bureaucracy
- **Tooling vs. Workflow**: Tradeoff between complex frameworks and agile development

## 4. Accuracy & Precision Error

- **Accuracy**: Binary correctness of calculations
- **Precision**: Consistency of business logic across layers

> Embedding logic at the database layer (vs. presentation layer) reduces risk of divergent values across dashboards.

---

# Pipeline Segments

An analysis begins by distinguishing between Systems of Record (SOR) and downstream domains.

## A. System of Record Pipeline Segments

### 1. Data Lakes

- Collects raw feeds (real-time CDC, daily extracts) into a persistent store
- Captures all data, including unintegrated feeds for historical tracking

### 2. Ingestion

Moves data from SOR/Lake into the RDBMS (e.g., Snowflake):
- **Metadata-driven**: Tables, columns, data types
- **Connectivity**: API limits, extraction methods
- **Loading strategies**:
  - Real-time streaming (Kafka, Kinesis)
  - Batch loads (COPY commands)
  - Orchestration tools (Matillion single-query components)

**Considerations & Checks**:
- Record counts vs. historical baselines (Statistical Process Control)
- Data-type validation (e.g., numeric columns contain no strings)
- Enumeration checks (e.g., boolean fields are strictly true/false)

### 3. Standardization

Harmonizes inconsistent source data:
- Normalize free-form text (e.g., "Europe" vs. "EUROPE")
- Conform shared dimensions (e.g., CRM "EMEA" vs. country-level data)

*Note: Some architectures delay standardization in favor of raw vault approaches.*

### 4. Source Vault

First stage of Data Vault 2.0:
- **Hub, Link, Satellite** structures capture raw data and state changes
- Transitions to Business Vault via transformation and rule enforcement
- Activities:
  - Data quality cleanup
  - Convergence of multiple SORs
  - Standardization and normalization of business concepts

## B. Domain Pipeline Segments

### 1. Business Vault

Integrates multiple operational systems into a unified view:
- Applies business rules to form Enterprise model
- Uses Hub/Link/Satellite for tracking over time

### 2. Dimensional Models (Data Marts)

Star schema structures for analytics:
- Central fact tables with descriptive dimension tables
- Optimized for BI tools like Tableau

### 3. Predictive Models

Data structures tailored for ML and predictive analytics workflows

### 4. Data Visualization

Final layer: dashboards and reports (e.g., Tableau Server) built on top of data marts and semantic views

---

_*End of Document*_

