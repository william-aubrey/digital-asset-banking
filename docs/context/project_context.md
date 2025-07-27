# Digital Asset Banking - Project Context v4.2

**Document Purpose:** This document is the single source of truth for the Digital Asset Banking (DAB) project. It contains the business vision, user profile, technical architecture, data model, and current status.

---

## 1. Business Context and Vision

**Project Name:** Digital Asset Banking (DAB) / Computational Trading Card NFT Marketplace

**Business Vision:** To build a decentralized personal data banking system that drives a business around physical trading card printing and distribution. The system allows users to create, manage, and trade valuable digital assets, which can then be manifested as physical, high-quality trading cards.

**Core Use Cases:**

* **Asset Creation:** Users can upload various digital materials (images, text, code, video) to create unique, valuable assets.
* **Data Banking:** The platform serves as a secure repository for these digital asset deposits.
* **NFT Marketplace:** A system that automatically packages each digital asset into a “Digital Trading Card” product (ie., the front and back print-ready images of the digital asset framed as a ‘trading card’ according to the theme selected by the user.) Users deposit digital assets. The system stores the digital asset on S3. The system automatically creates a ‘digital trading card’ for the asset according to established ‘trading card templates’. It creates a metadata profile and stores that data in Snowflake. Deposits, withdrawals, trades and purchases are logged in the Snowflake database creating a permanent record of ownership and transactions.
* **Physical Artifact Generation:** Once a digital trading card asset has attained enough attention, it can become manifest as an actual trading card in volumes as low as one printing. This is estimated to be 50 cards. The ultimate goal is to generate print-ready, physical trading cards from the digital assets, complete with QR codes linking back to the digital original. The cards confer ownership or usage rights of the digital asset. Access to the digital assets on the cards is accomplished by public and private key authentication. The trading card QR code is the public key. The user has a private key encoded in another QR code on a special ‘membership badge’ trading card (NOTE: this may be replaced by traditional user authentication approaches)

---

## 2. Project Journey and Philosophy

This project represents a journey from a 30-year career in data analytics into the world of hands-on application development. The process has been a rapid, iterative collaboration with multiple AI agents, each contributing to a different stage of the project lifecycle.

**Core Philosophy:** The project's development is guided by the principle of "AI as a learning accelerator." The goal is not for the AI to simply produce code, but to act as a mentor, enabling the developer to learn by doing, overcome technical blockers, and translate a complex vision into functional reality.

**Key Milestones and Learnings:**

1.  **From Zero to "Hello, World!" (with Claude Sonnet):**
    * **Date:** July 26, 2025
    * **Time:** Morning (~10:23 AM)
        The project began with a significant hurdle: overcoming a legacy Python environment. This initial phase was a lesson in the importance of a clean development environment and the value of a patient, step-by-step AI teaching style. The first major victory was launching the initial Streamlit prototype.

2.  **Building the Foundation (with ChatGPT):**
    * **Date:** July 26, 2025
    * **Time:** Afternoon (2:30 PM - 3:50 PM)
        With a working prototype, the focus shifted to creating a robust, deployable infrastructure. This session was characterized by high-velocity generation of the core AWS components using CloudFormation and IAM, establishing the project's cloud backbone.

3.  **Bringing it all Together (with Gemini):**
    * **Date:** July 26, 2025
    * **Time:** Evening (5:30 PM - 6:59 PM)
        This phase involved a critical debugging session to connect the Streamlit frontend to the newly created AWS backend. It was a synergistic process of identifying and resolving a series of cascading errors, from incorrect environment variables to missing application logic, culminating in the first successful end-to-end file upload.

4.  **Designing the Future (with Gemini):**
    * **Date:** July 26, 2025
    * **Time:** Evening (7:45 PM - 8:38 PM)
        With the application and infrastructure connected, the final step was to design the long-term data architecture. This involved creating a scalable Snowflake star schema and a semantic layer to support future analytics and business intelligence.

This journey-based approach, capturing not just the artifacts but the story behind them, is a core part of the project's documentation strategy.


---

## 3. Developer Profile

**Learning Style:** Prefers step-by-step, guided instruction.
**Technical Background:** 30+ years in data and analytics engineering (Excel, SQL Server, Tableau, Snowflake, Matillion, Alteryx, Knime, Sigma, Omni). New to application development (Python/Streamlit).
**Environment:** Windows 10, Notepad++, comfortable with file systems and AWS S3.

---

## 4. Application Architecture and Features (v4.0)

**Technology Stack:**

* **Frontend:** Python, Streamlit
* **Backend:** AWS S3 (for file storage)
* **Database:** Snowflake
* **Core Logic:** Pandas, Pillow, Boto3
* **Analytics and Data Processing:** Matillion DPC

**Key Core Features Implemented:**

* **Asset Management:** Browse, create, and manage a personal collection of digital assets.
* **Multi-Type Asset Support:** Handles images, context files, code, video, and audio.
* **Create Asset Workflow:** A comprehensive UI for uploading files, defining metadata, and configuring asset properties.
* **S3 Integration:** The application is fully connected to an AWS S3 bucket for persistent file storage.

**Key Plugin Module Features Implemented:**

* **CYOA File Naming:** Automatically generates Choose-Your-Own-Adventure compliant filenames for assets.
* **Computational Credits:** An in-app currency system for marketplace transactions.

### 4.1. Core Application Logic (`DAB_4.0.py`)

This is the main Streamlit application script. It contains the UI, state management, and business logic that connects all components of the architecture.


---

## 5. Data and Infrastructure Architecture

### 5.1. Cloud Infrastructure (AWS)

The application's backend storage is built on AWS and managed via Infrastructure-as-Code.

#### Deployer IAM Policy (`iam-dab-agent-policy.json`)

This policy grants the necessary permissions to an administrative user or role to deploy and manage the application's infrastructure using CloudFormation.


#### CloudFormation Template (`infrastructure.yaml`)

This template provisions the S3 bucket and the application's IAM user. It is designed to be re-run safely, allowing it to use existing resources if they are present.


## 6. Current Status and Next Steps

**Current Application Version:** `DAB_4.0.py`
**Launch Command:** `streamlit run DAB_4.0.py` (after setting AWS credentials)

**Project State:**

* The Streamlit application is functional.
* The app successfully connects to and uses AWS S3 for storage.
* The Snowflake data model is designed and ready for implementation.

**Immediate Next Steps:**

1.  **Implement Snowflake Integration:** Modify the Python application to write metadata to the `DIM_ASSETS` and `FCT_ASSET_TRANSACTIONS` tables in Snowflake.
2.  **Develop QR Code Functionality:** Integrate a library to generate QR codes for assets.
3.  **Create Card Templates:** Design a system for generating visual trading card images from asset data.
4.  **Version Control:** Establish a Git repository (Bitbucket/GitLab) and commit the current codebase.

---

