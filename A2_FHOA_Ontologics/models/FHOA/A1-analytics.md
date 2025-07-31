# FHOA Analytics (A1) Process Model

This document provides the IDEF0-style decomposition for the **A1: Conduct Analytics** function within the FHOA framework. Its primary purpose is to transform raw data from the Heuristics layer into actionable insights that fuel the continuous improvement cycle.

---

## A1: Conduct Analytics (Top-Level Function)

- **Purpose**: To ingest raw performance data, compare it against the conceptual models from the Ontologics layer, and produce structured, actionable insights that recommend specific improvements to the system.
- **Inputs**: Raw Transactional & Performance Data (from A3 Heuristics)
- **Controls**: Conceptual Process Models (from A2 Ontologics)
- **Outputs**: Improvement Insights (to A2 Ontologics), Performance Dashboards
- **Mechanisms**: Data Pipeline Engine, Snowflake Data Warehouse, BI Tools, ML Frameworks, Data Analysts & Scientists

> **Nomenclature**: The collection of mechanisms that perform the A1 function is formally named the **Agentic Insight Motor (AIM)**. It is the motor that drives the FHOA continuous improvement cycle.

---

## A1 Decomposition: The Cognitive Process of Analytics

The A1 function is decomposed into four sequential but distinct activities, each building upon the last to form a complete insight.

### A1.1: Perform Descriptive Analytics (What happened?)

- **Purpose**: To measure and report on key process metrics, creating the factual Observation that is the first component of an insight.
- **Inputs**: Raw Transactional & Performance Data
- **Controls**: Semantic View Definition, Business Questions
- **Outputs**: Performance Dashboards, Formatted Reports, Observations
- **Mechanisms**: BI Tools (e.g., Sigma, Tableau), SQL Queries, Data Analysts

### A1.2: Perform Diagnostic Analytics (Why did it happen?)

- **Purpose**: To analyze deviations between observations and expectations to generate a causal Hypothesis.
- **Inputs**: Observations (from A1.1), Conceptual Process Models (from A2 Ontologics)
- **Controls**: Statistical Methods, Domain Knowledge
- **Outputs**: Hypotheses, Root Cause Analysis Reports
- **Mechanisms**: Graph Visualization Libraries, Advanced SQL, Senior Analyst / Data Scientist

### A1.3: Perform Predictive Analytics (What will happen?)

- **Purpose**: To apply statistical models to historical data to generate a predicted Expectation.
- **Inputs**: Historical Performance Data
- **Controls**: Forecasting Models, Statistical Assumptions
- **Outputs**: Expectations (e.g., predicted metric values), Forecast Reports
- **Mechanisms**: ML Frameworks (e.g., Scikit-learn), Time Series Databases, MLOps Platforms, Data Scientist

### A1.4: Perform Prescriptive Analytics (What should we do about it?)

- **Purpose**: To take the understanding of a deviation and its cause (Hypothesis) and generate a specific, testable Recommendation for altering the conceptual model.
- **Inputs**: Hypotheses (from A1.2), Expectations (from A1.3)
- **Controls**: Business Goals & Constraints, Optimization Algorithms
- **Outputs**: Recommendations (proposed changes to the Ontologics model)
- **Mechanisms**: Optimization Solvers, Simulation Engines, Decision Scientist, Product Manager

---

*End of Chapter 3.1: FHOA Analytics (A1) Process Model*

