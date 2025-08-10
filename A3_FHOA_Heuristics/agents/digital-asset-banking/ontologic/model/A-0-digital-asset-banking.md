# IDEF0 Process Model for Digital Asset Banking

This document provides a hierarchical decomposition of the processes for the Digital Asset Banking (DAB) platform, following the IDEF0 methodology.

---

## Table of Contents

* [A-0: Manage Digital Asset Banking Platform](#a-0-manage-digital-asset-banking-platform-context-diagram)
    * [A1: Manage Asset Lifecycle](#a1-manage-asset-lifecycle-decomposition)
        * [A1.1: Authenticate User](#a11-authenticate-user)
        * [A1.2: Create Digital Asset](#a12-create-digital-asset)
        * [A1.3: View Asset Data](#a13-view-asset-data)
        * [A1.4: Purchase Digital Asset](#a14-purchase-digital-asset)
    * [A2: Administer Platform Resources](#a2-administer-platform-resources-decomposition)
        * [A2.1: Provision Cloud Infrastructure](#a21-provision-cloud-infrastructure)
        * [A2.2: Deploy Application Code](#a22-deploy-application-code)
        * [A2.3: Manage Security & RBAC](#a23-manage-security--rbac)
        * [A2.4: Monitor Platform Health & Cost](#a24-monitor-platform-health--cost)
    * [A3: Provide Analytics & Compliance](#a3-provide-analytics--compliance-decomposition)
        * [A3.1: Ingest Transactional Data](#a31-ingest-transactional-data)
        * [A3.2: Generate Business Analytics](#a32-generate-business-analytics)
        * [A3.3: Provide Audit Trail Access](#a33-provide-audit-trail-access)

---



## A-0: Manage Digital Asset Banking Platform (Context Diagram)

This is the highest-level view, defining the overall scope and boundary of the system.

* **Function Name**: Manage Digital Asset Banking Platform
* **Purpose**: To provide a system for users to create, manage, trade, and physically manifest digital assets.
* **Viewpoint**: From the perspective of the platform owner and development team.

### ICOMs (Inputs, Controls, Outputs, Mechanisms)

#### Inputs
* `User-Provided Digital Content`: The raw files (images, code, etc.) that are transformed into assets.
* `User Stories & Requirements`: The functional and non-functional requirements that drive development.

#### Controls
* `Regulatory & Compliance Standards`: External rules like GDPR, LGPD, and SOC 2 that the platform must adhere to.
* `Architectural Specifications`: The established designs for the cloud infrastructure, data model, and RBAC policies that govern the implementation.

#### Outputs
* `Managed Digital Assets`: The final digital products, securely stored and tracked.
* `Physical Trading Cards`: A key tangible output of the platform's vision.
* `Transaction Records & Audit Logs`: Data produced to ensure compliance and provide user history.
* `Platform Analytics & Dashboards`: Aggregated data provided to stakeholders like investors.

#### Mechanisms
* `End Users & Platform Administrators`: The human actors who operate and maintain the system.
* `Cloud Infrastructure`: The underlying AWS and Snowflake platforms.
* `CI/CD Pipeline`: The automated system for deploying code and infrastructure changes.

---
## A0: Manage Digital Asset Banking Platform (Decomposition)

This diagram breaks down the A-0 box into its major sub-functions and shows the primary ICOM flows between them.

* **A1: Manage Asset Lifecycle**: Encompasses the core user-facing activities of uploading, creating, viewing, and purchasing digital assets.
    * **Inputs**: `User-Provided Digital Content`
    * **Controls**: `Architectural Specifications`
    * **Outputs**: `Managed Digital Assets`, `Transaction Records`
    * **Mechanisms**: `End Users`, `Provisioned Cloud Resources` (from A2)

* **A2: Administer Platform Resources**: Covers the operational and development activities required to build and maintain the platform, including deployment, security, and monitoring.
    * **Inputs**: `User Stories & Requirements`
    * **Controls**: `Regulatory & Compliance Standards`
    * **Outputs**: `Provisioned Cloud Resources`, `Deployed Application`, `Audit Logs`
    * **Mechanisms**: `Platform Administrators`, `Cloud Infrastructure`, `CI/CD Pipeline`

* **A3: Provide Analytics & Compliance**: Addresses the needs of stakeholders for insight and oversight, including generating analytics and providing audit trails.
    * **Inputs**: `Transaction Records` (from A1)
    * **Controls**: `Regulatory & Compliance Standards`
    * **Outputs**: `Platform Analytics & Dashboards`, `Audit Trail Report`
    * **Mechanisms**: `BI Tools`, `Cloud Infrastructure`

---
## A1: Manage Asset Lifecycle (Decomposition)

This diagram details the primary steps a user takes when interacting with assets via the Streamlit application. This model is aligned with the implementation-level model `A1-manage-asset-lifecycle.md`.

### A1.1: Display Asset Marketplace
- **Description**: Queries the data warehouse to present a view of available assets to the user.
* **Inputs**: `User Request`
* **Controls**: `Authenticated User Session`, `Data Model Schema`
* **Outputs**: `Asset Marketplace View`
* **Mechanisms**: `Streamlit Frontend`, `Backend API (Lambda)`, `Snowflake Connection`

### A1.2: Process New Asset Upload
- **Description**: Handles the validation, S3 upload, and database metadata registration for a new asset.
* **Inputs**: `File Object`, `Asset Metadata`
* **Controls**: `Authenticated User Session`, `Uploader ID`, `Asset Type`, `S3 Bucket Policy`
* **Outputs**: `Uploaded Asset Confirmation`, `Asset Database Record`, `Transaction Database Record`
* **Mechanisms**: `Streamlit Frontend`, `Backend API (Lambda)`, `S3 Client`, `Snowflake Connection`

### A1.3: Execute Asset Purchase
- **Description**: Updates asset ownership and records the transaction in the database.
* **Inputs**: `Asset ID to Purchase`
* **Controls**: `Authenticated User Session`, `Buyer ID`, `Data Model Schema`
* **Outputs**: `Purchase Confirmation`, `Updated Asset Record`, `Transaction Database Record`
* **Mechanisms**: `Streamlit Frontend`, `Backend API (Lambda)`, `Snowflake Connection`

---
## A2: Administer Platform Resources (Decomposition)

This diagram details the primary components of building and maintaining the platform.

### A2.1: Provision Cloud Infrastructure
This function represents the deployment of all necessary cloud resources using IaC.
* **Inputs**: `Infrastructure-as-Code Files`, `Configuration Variables`
* **Controls**: `Architectural Specifications`, `IAM Permissions`, `Cloud Provider API Limits`
* **Outputs**: `Provisioned Cloud Resources`, `State File`, `Deployment Logs`
* **Mechanisms**: `Platform Administrator`, `IaC Engine`, `CI/CD Pipeline`

### A2.2: Deploy Application Code
This function describes the automated process of deploying source code.
* **Inputs**: `Application Source Code`
* **Controls**: `CI/CD Pipeline Configuration`, `Automated Tests`
* **Outputs**: `Deployed Application`, `Deployment Status`
* **Mechanisms**: `Git Repository`, `CI/CD Pipeline`, `Target Compute Service`

### A2.3: Manage Security & RBAC
This function describes implementing and maintaining security policies.
* **Inputs**: `RBAC Design Document`, `IAM Policy Documents`
* **Controls**: `Principle of Least Privilege`, `Regulatory & Compliance Standards`
* **Outputs**: `Applied Snowflake Roles & Grants`, `Applied IAM Policies & Roles`
* **Mechanisms**: `Platform Administrator`, `Snowflake UI/CLI`, `AWS Console/CLI`, `IaC Engine`

#### A2.3.1: Authenticate User
This function verifies a user's identity to grant them access to the platform.
* **Inputs**: `User Credentials`
* **Controls**: `Authentication Protocol (OAuth 2.0)`, `DIM_USERS Table Schema`
* **Outputs**: `Authenticated User Session`, `User Record`
* **Mechanisms**: `Streamlit Frontend`, `Backend API (Lambda)`, `External SSO Provider`, `Snowflake Database`

### A2.4: Monitor Platform Health & Cost
This function describes observing performance and cloud spending.
* **Inputs**: `Platform Metrics & Logs`, `Cloud Billing & Usage Data`
* **Controls**: `Service Level Agreements (SLAs)`, `Cloud Budgets`, `Alerting Rules`
* **Outputs**: `Health & Performance Dashboards`, `Cost & Usage Reports`, `Alert Notifications`
* **Mechanisms**: `Platform Administrator`, `Cloud Monitoring Tools`, `Logging Services`

---
## A3: Provide Analytics & Compliance (Decomposition)

This diagram details how value and oversight are derived from platform data.

### A3.1: Ingest Transactional Data
This function represents capturing raw data and loading it into the data warehouse.
* **Inputs**: `Raw Transactional Events` (from A1)
* **Controls**: `Data Model Schema`
* **Outputs**: `Validated & Governed Data` (in Snowflake)
* **Mechanisms**: `Backend API (Lambda)`, `Snowflake Database`

### A3.2: Generate Business Analytics
This function covers creating dashboards and reports for stakeholders.
* **Inputs**: `Validated & Governed Data`
* **Controls**: `Semantic View Definition`, `RBAC Policy`
* **Outputs**: `Analytics Dashboards & Reports`
* **Mechanisms**: `Snowflake Semantic View`, `BI Tools` (e.g., Sigma, Tableau), `DAB_ANALYST` role

### A3.3: Provide Audit Trail Access
This function describes providing secure, read-only access to logs.
* **Inputs**: `Audit Request`
* **Controls**: `RBAC Policy` (`DAB_REGULATOR` role), `Data Retention Policies`
* **Outputs**: `Audit Trail Report`
* **Mechanisms**: `Platform Administrator`, `Snowflake Access History`, `AWS CloudTrail`