# Digital Asset Banking (DAB) - Project Context

## Project Overview

The Digital Asset Banking (DAB) project is a decentralized personal data banking system that drives a business around physical trading card printing and distribution. The system allows users to create, manage, and trade valuable digital assets, which can then be manifested as physical, high-quality trading cards.

## Core Use Cases

* **Asset Creation:** Users can upload various digital materials (images, text, code, video) to create unique, valuable assets
* **Data Banking:** The platform serves as a secure repository for these digital asset deposits
* **NFT Marketplace:** System automatically packages digital assets into "Digital Trading Cards"
* **Physical Artifact Generation:** Digital trading cards can be printed as physical cards when they gain enough attention

## Technology Stack

* **Frontend:** Python, Streamlit
* **Backend:** AWS S3 (for file storage)
* **Database:** Snowflake
* **Data Processing:** Matillion DPC
* **Core Logic:** Pandas, Pillow, Boto3

## Project Structure

### Folder Structure

```
digital-asset-banking/
├── snowflake/
│   ├── ddl/                  # DDL SQL files for database setup
│   │   ├── 01_setup_rbac.sql
│   │   ├── 02_create_tables.sql
│   │   └── 03_populate_dab_idef0_model.sql
│   ├── views/               # SQL view definitions
│   └── design/              # Database design documentation
├── dpc/                     # Matillion Data Productivity Cloud pipelines
│   ├── cloud/               # Cloud pipelines
│   │   └── setup/           # Setup pipelines for users and database objects
│   ├── orchestration/       # Orchestration pipelines
│   └── transformation/      # Transformation pipelines
├── src/                     # Application source code
└── specs/                   # Project specifications
```

## Database Structure

The Snowflake data model follows a classic star schema design optimized for analytics:

### Core Tables

* **DIM_ASSETS** - Stores core attributes of each unique digital asset
* **DIM_USERS** - Stores information about users who interact with the system
* **DIM_ASSET_TYPES** - Simple dimension to classify asset types
* **FCT_ASSET_TRANSACTIONS** - Central fact table recording every key business event

### Database Objects

* **Database:** DAB_DATABASE
* **Schema:** DAB_SCHEMA
* **Warehouse:** DAB_WAREHOUSE
* **Roles:** DAB_ADMIN, DAB_USER

## Pipeline Requirements

### Data Loading Pipelines

1. **Asset Metadata Loading**
   * Extract metadata from Streamlit app uploads
   * Load into DIM_ASSETS table
   * Update FCT_ASSET_TRANSACTIONS with UPLOAD events

2. **Transaction Processing**
   * Process purchase/trade transactions
   * Update ownership information in DIM_ASSETS
   * Record transactions in FCT_ASSET_TRANSACTIONS

### Analytics Pipelines

1. **Asset Popularity Analysis**
   * Track view counts and engagement metrics
   * Identify assets ready for physical printing

2. **User Activity Reporting**
   * Monitor user engagement and transaction history
   * Generate reports for marketplace activity

## Naming Conventions

* **Cloud Setup Pipelines:** `dab_cloud_setup_[purpose].orch.yaml`
* **Orchestration Pipelines:** `dab_orch_[purpose].orch.yaml`
* **Transformation Pipelines:** `dab_tran_[purpose].tran.yaml`
* **Variables:** `dab_[scope]_[purpose]`
* **Tables:** Follow dimension/fact naming pattern (DIM_*, FCT_*)

## Reference Files

* **DDL Files:** `digital-asset-banking/snowflake/ddl/*.sql`
* **Pipeline Files:** `digital-asset-banking/dpc/*.yaml`
* **Data Model:** See `A3_FHOA_Heuristics/apps/digital-asset-banking/snowflake/design/snowflake-data-model.md`

## Development Workflow

1. Create cloud setup pipeline to execute DDL scripts and create database objects
2. Build transformation pipelines for data loading and processing
3. Implement analytics pipelines for reporting and insights
4. Connect Streamlit app to Snowflake database

## Notes

* The project is part of a larger FHOA framework (Functional Heuristics, Ontologics, and Analytics)
* The database should support future semantic views for analytics
* All pipelines should include appropriate error handling and logging
