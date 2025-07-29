# IDEF0 Data Model Specification

## Overview
This document outlines the relational database structure for representing IDEF0 process models, with all object names capitalized to align with Snowflake SQL conventions.

## 1. CORE ENTITIES AS TABLES

Each distinct type of element in the IDEF0 outline corresponds to a primary table in the relational database.

### **FUNCTIONS Table**
This table stores information about each function box in the IDEF0 diagram.

* `FUNCTION_ID` (Primary Key): A unique identifier for each function (e.g., F1, F2, F3)
* `FUNCTION_NAME`: The verb-based name of the function (e.g., "Manage Data Operations", "Design Data Pipelines")
* `DESCRIPTION`: A detailed explanation of the function's activity
* `PURPOSE`: The stated purpose of the function or the overall model
* `VIEWPOINT`: The perspective from which the function or model is viewed
* `DIAGRAM_LEVEL`: Indicates the level of the diagram (e.g., 'A-0', 'A0')
* `PARENT_FUNCTION_ID` (Foreign Key to `FUNCTIONS.FUNCTION_ID`): Self-referencing foreign key establishing hierarchical decomposition

### **OUTPUTS Table**
This table represents the results, products, or transformed data produced by a function.

* `OUTPUT_ID` (Primary Key): Unique identifier for each output
* `OUTPUT_NAME`: The label of the output arrow (e.g., "Validated & Governed Data Products")
* `DESCRIPTION`: Details about the output (e.g., "curated datasets, data marts")
* `OUTPUT_TYPE`: Categorization of the output (e.g., "Data Product", "Insight", "Report")

### **INPUTS Table**
INPUTS are resources that are consumed and transformed by the function.

* `INPUT_ID` (Primary Key): Unique identifier for each input
* `INPUT_NAME`: The label of the input arrow (e.g., "Versioned Business Requirements")
* `DESCRIPTION`: Further details about the input
* `INPUT_TYPE`: Categorization of the input (e.g., "Requirement", "Raw Data", "Feedback")
* `SOURCE_OUTPUT_ID` (Foreign Key to `OUTPUTS.OUTPUT_ID`): References the originating output

### **CONTROLS Table**
CONTROLS are conditions, rules, or policies that govern or constrain the function's execution.

* `CONTROL_ID` (Primary Key): Unique identifier for each control
* `CONTROL_NAME`: The label of the control arrow (e.g., "DataOps Principles & Methodologies")
* `DESCRIPTION`: Details about the control
* `CONTROL_TYPE`: Categorization of the control (e.g., "Policy", "Standard", "Regulation")
* `SOURCE_OUTPUT_ID` (Foreign Key to `OUTPUTS.OUTPUT_ID`): References the originating output

### **MECHANISMS Table**
MECHANISMS denote the resources, tools, systems, or personnel that perform the function.

* `MECHANISM_ID` (Primary Key): Unique identifier for each mechanism
* `MECHANISM_NAME`: The label of the mechanism arrow (e.g., "Cross-Functional DataOps Teams")
* `DESCRIPTION`: Details about the mechanism
* `MECHANISM_TYPE`: Categorization of the mechanism (e.g., "Team", "Platform", "Tool")
* `SOURCE_OUTPUT_ID` (Foreign Key to `OUTPUTS.OUTPUT_ID`): References the originating output

## 2. RELATIONSHIPS AS JUNCTION TABLES

The connections between functions and their ICOMs are typically many-to-many relationships, represented using junction tables.

### **FUNCTION_INPUTS Table**
* `FUNCTION_ID` (Foreign Key to `FUNCTIONS.FUNCTION_ID`)
* `INPUT_ID` (Foreign Key to `INPUTS.INPUT_ID`)
* (Composite Primary Key: `FUNCTION_ID`, `INPUT_ID`)
* `ORDER_INDEX` (Optional): To preserve the visual order of inputs on a diagram

### **FUNCTION_CONTROLS Table**
* `FUNCTION_ID` (Foreign Key to `FUNCTIONS.FUNCTION_ID`)
* `CONTROL_ID` (Foreign Key to `CONTROLS.CONTROL_ID`)
* (Composite Primary Key: `FUNCTION_ID`, `CONTROL_ID`)
* `ORDER_INDEX` (Optional)

### **FUNCTION_OUTPUTS Table**
* `FUNCTION_ID` (Foreign Key to `FUNCTIONS.FUNCTION_ID`)
* `OUTPUT_ID` (Foreign Key to `OUTPUTS.OUTPUT_ID`)
* (Composite Primary Key: `FUNCTION_ID`, `OUTPUT_ID`)
* `ORDER_INDEX` (Optional)

### **FUNCTION_MECHANISMS Table**
* `FUNCTION_ID` (Foreign Key to `FUNCTIONS.FUNCTION_ID`)
* `MECHANISM_ID` (Foreign Key to `MECHANISMS.MECHANISM_ID`)
* (Composite Primary Key: `FUNCTION_ID`, `MECHANISM_ID`)
* `ORDER_INDEX` (Optional)

## 3. REPRESENTING HIERARCHY

The hierarchical decomposition of IDEF0 diagrams is handled by the `PARENT_FUNCTION_ID` column in the `FUNCTIONS` table, allowing for recursive queries. This structure enables traversing the entire functional hierarchy, from the top-level A-0 diagram down to the most granular sub-functions.

## 4. DDL 

-- Create Database and Schema for IDEF0 Model
CREATE DATABASE IF NOT EXISTS IDEF0_MODEL_DB;
CREATE SCHEMA IF NOT EXISTS IDEF0_MODEL_DB.DATAOPS_IDEF0_SCHEMA;

USE DATABASE IDEF0_MODEL_DB;
USE SCHEMA DATAOPS_IDEF0_SCHEMA;

-- Table for FUNCTIONS (Activity Boxes)
CREATE OR REPLACE TABLE FUNCTIONS (
    FUNCTION_ID NUMBER(38,0) PRIMARY KEY,
    FUNCTION_NAME VARCHAR(255) NOT NULL,
    DESCRIPTION VARCHAR(1000),
    PURPOSE VARCHAR(1000),
    VIEWPOINT VARCHAR(1000),
    DIAGRAM_LEVEL VARCHAR(50), -- e.g., 'A-0', 'A0'
    PARENT_FUNCTION_ID NUMBER(38,0),
    CONSTRAINT FK_PARENT_FUNCTION FOREIGN KEY (PARENT_FUNCTION_ID) REFERENCES FUNCTIONS(FUNCTION_ID)
);

-- Table for OUTPUTS (defined first as it's referenced by other ICOMs)
CREATE OR REPLACE TABLE OUTPUTS (
    OUTPUT_ID NUMBER(38,0) PRIMARY KEY,
    OUTPUT_NAME VARCHAR(255) NOT NULL,
    DESCRIPTION VARCHAR(1000),
    OUTPUT_TYPE VARCHAR(100)
);

-- Table for INPUTS
CREATE OR REPLACE TABLE INPUTS (
    INPUT_ID NUMBER(38,0) PRIMARY KEY,
    INPUT_NAME VARCHAR(255) NOT NULL,
    DESCRIPTION VARCHAR(1000),
    INPUT_TYPE VARCHAR(100),
    SOURCE_OUTPUT_ID NUMBER(38,0), -- New column to link to the originating Output
    CONSTRAINT FK_INPUT_SOURCE_OUTPUT FOREIGN KEY (SOURCE_OUTPUT_ID) REFERENCES OUTPUTS(OUTPUT_ID)
);

-- Table for CONTROLS
CREATE OR REPLACE TABLE CONTROLS (
    CONTROL_ID NUMBER(38,0) PRIMARY KEY,
    CONTROL_NAME VARCHAR(255) NOT NULL,
    DESCRIPTION VARCHAR(1000),
    CONTROL_TYPE VARCHAR(100),
    SOURCE_OUTPUT_ID NUMBER(38,0), -- New column to link to the originating Output
    CONSTRAINT FK_CONTROL_SOURCE_OUTPUT FOREIGN KEY (SOURCE_OUTPUT_ID) REFERENCES OUTPUTS(OUTPUT_ID)
);

-- Table for MECHANISMS
CREATE OR REPLACE TABLE MECHANISMS (
    MECHANISM_ID NUMBER(38,0) PRIMARY KEY,
    MECHANISM_NAME VARCHAR(255) NOT NULL,
    DESCRIPTION VARCHAR(1000),
    MECHANISM_TYPE VARCHAR(100),
    SOURCE_OUTPUT_ID NUMBER(38,0), -- New column to link to the originating Output
    CONSTRAINT FK_MECHANISM_SOURCE_OUTPUT FOREIGN KEY (SOURCE_OUTPUT_ID) REFERENCES OUTPUTS(OUTPUT_ID)
);

-- Junction Table for FUNCTION-INPUT relationships
CREATE OR REPLACE TABLE FUNCTION_INPUTS (
    FUNCTION_ID NUMBER(38,0) NOT NULL,
    INPUT_ID NUMBER(38,0) NOT NULL,
    ORDER_INDEX NUMBER(38,0),
    PRIMARY KEY (FUNCTION_ID, INPUT_ID),
    CONSTRAINT FK_FI_FUNCTION FOREIGN KEY (FUNCTION_ID) REFERENCES FUNCTIONS(FUNCTION_ID),
    CONSTRAINT FK_FI_INPUT FOREIGN KEY (INPUT_ID) REFERENCES INPUTS(INPUT_ID)
);

-- Junction Table for FUNCTION-CONTROL relationships
CREATE OR REPLACE TABLE FUNCTION_CONTROLS (
    FUNCTION_ID NUMBER(38,0) NOT NULL,
    CONTROL_ID NUMBER(38,0) NOT NULL,
    ORDER_INDEX NUMBER(38,0),
    PRIMARY KEY (FUNCTION_ID, CONTROL_ID),
    CONSTRAINT FK_FC_FUNCTION FOREIGN KEY (FUNCTION_ID) REFERENCES FUNCTIONS(FUNCTION_ID),
    CONSTRAINT FK_FC_CONTROL FOREIGN KEY (CONTROL_ID) REFERENCES CONTROLS(CONTROL_ID)
);

-- Junction Table for FUNCTION-OUTPUT relationships
CREATE OR REPLACE TABLE FUNCTION_OUTPUTS (
    FUNCTION_ID NUMBER(38,0) NOT NULL,
    OUTPUT_ID NUMBER(38,0) NOT NULL,
    ORDER_INDEX NUMBER(38,0),
    PRIMARY KEY (FUNCTION_ID, OUTPUT_ID),
    CONSTRAINT FK_FO_FUNCTION FOREIGN KEY (FUNCTION_ID) REFERENCES FUNCTIONS(FUNCTION_ID),
    CONSTRAINT FK_FO_OUTPUT FOREIGN KEY (OUTPUT_ID) REFERENCES OUTPUTS(OUTPUT_ID)
);

-- Junction Table for FUNCTION-MECHANISM relationships
CREATE OR REPLACE TABLE FUNCTION_MECHANISMS (
    FUNCTION_ID NUMBER(38,0) NOT NULL,
    MECHANISM_ID NUMBER(38,0) NOT NULL,
    ORDER_INDEX NUMBER(38,0),
    PRIMARY KEY (FUNCTION_ID, MECHANISM_ID),
    CONSTRAINT FK_FM_FUNCTION FOREIGN KEY (FUNCTION_ID) REFERENCES FUNCTIONS(FUNCTION_ID),
    CONSTRAINT FK_FM_MECHANISM FOREIGN KEY (MECHANISM_ID) REFERENCES MECHANISMS(MECHANISM_ID)
);