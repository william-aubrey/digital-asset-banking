# Data Quality Testing Framework

## Overview

This project implements a comprehensive data quality testing framework that allows for automated validation of data across multiple quality dimensions. The framework is designed to be flexible, reusable, and maintainable.

## Architecture

The framework implements a modular, layered architecture that separates test definition, execution, and result management:

### 1. **Control Tables**
- **`${ev_database}.CONTROLS.CTRL_TEST_DQ_TESTS`**: Central repository for test definitions with the following key attributes:
  - Test metadata (SOR_KEY, FILE_KEY, SCHEMA_NAME, TABLE_NAME)
  - Test specifications (TEST_INDEX, TEST_NAME, TEST_DESCRIPTION, TEST_CATEGORY)
  - Test logic (TEST_SQL_QUERY, RESULT_TYPE, RESULT_VALUE_EXPECTED)
  - Test status (ACTIVE_FLAG)

- **`${ev_database}.CONTROLS.CTRL_TEST_DQ_RESULTS`**: Stores test execution results including:
  - Test identification fields
  - Actual result values
  - Test status (PASS/FAIL)
  - Execution timestamps
  - Process step information

- **`${ev_database}.CONTROLS.CTRL_LOAD_HISTORY`**: Integrates with the framework to track overall data processing status, updated when tests fail.

### 2. **Pipeline Components**
- **`00 Simulate Test Run.orch.yaml`**: Entry point for testing that:
  - Demonstrates how to invoke the testing framework
  - Provides parameter examples (FILE_KEY, FILE_DATE, PROCESS_STEP)
  - Evaluates and displays test results
  - Shows conditional logic based on test outcomes

- **`01 DQ_Test_Orchestration.orch.yaml`**: Core orchestration pipeline that:
  - Retrieves test definitions from control tables
  - Manages test execution workflow
  - Processes test results
  - Determines overall test status
  - Updates load history on test failures

- **`02 DQ_Test_Execution.tran.yaml`**: Individual test execution pipeline that:
  - Executes parameterized SQL test queries
  - Evaluates test results against expected values
  - Records detailed test outcomes
  - Supports different result comparison types

### 3. **Data Flow**
1. Test definitions are stored in CTRL_TEST_DQ_TESTS
2. The orchestration pipeline retrieves applicable tests based on FILE_KEY and PROCESS_STEP
3. Tests are executed sequentially through a Grid Iterator
4. Each test execution:
   - Runs the test SQL query
   - Compares actual results with expected values
   - Records results in CTRL_TEST_DQ_RESULTS
5. Overall test status is determined (PASS if all tests pass, FAIL if any test fails)
6. Results are propagated back to the calling pipeline
7. On failure, CTRL_LOAD_HISTORY is updated to reflect data quality issues

### 4. **Environment Configuration**
- Framework uses environment variables (`${ev_database}`, `${ev_controls_schema}`) for database and schema references
- Supports different environments through variable substitution
- Enables deployment across development, testing, and production environments

## Test Definition and Results Structure

### Test Definition Structure

Tests are defined in the `CTRL_TEST_DQ_TESTS` table with the following attributes:

| Attribute | Description |
|-----------|-------------|
| SOR_KEY | System of Record identifier |
| FILE_KEY | File or data source identifier |
| SCHEMA_NAME | Schema containing the table to test |
| TABLE_NAME | Table to be tested |
| TEST_INDEX | Numeric identifier for test ordering |
| TEST_NAME | Brief descriptive name |
| TEST_DESCRIPTION | Detailed test description |
| TEST_CATEGORY | Data quality dimension (see below) |
| TEST_SQL_QUERY | SQL query that performs the test |
| RESULT_TYPE | How to interpret results (currently EXACT_SCALAR) |
| RESULT_VALUE_EXPECTED | Expected value from the test query |
| ACTIVE_FLAG | Boolean indicating if test is active |

#### Test Definition Best Practices

1. **Unique Identification**: Each test should have a unique combination of SOR_KEY, FILE_KEY, SCHEMA_NAME, TABLE_NAME, and TEST_INDEX
2. **Descriptive Naming**: TEST_NAME should be concise but descriptive enough to understand the test's purpose
3. **Comprehensive Description**: TEST_DESCRIPTION should provide enough detail for others to understand the test's purpose and logic
4. **SQL Query Design**: 
   - Queries should return a single scalar value for comparison
   - Use parameterized table references where possible (e.g., ${ev_database}.${schema}.${table})
   - Include appropriate error handling in complex queries
5. **Categorization**: Assign tests to the appropriate data quality dimension to enable organized reporting and analysis
6. **Test Activation**: Use ACTIVE_FLAG to enable/disable tests without deleting them

### Test Results Structure

Test results are stored in the `CTRL_TEST_DQ_RESULTS` table with the following attributes:

| Attribute | Description |
|-----------|-------------|
| SOR_KEY | System of Record identifier (matches test definition) |
| FILE_KEY | File or data source identifier (matches test definition) |
| FILE_DATE | Date associated with the file being tested |
| SCHEMA_NAME | Schema containing the tested table |
| TABLE_NAME | Table that was tested |
| TEST_INDEX | Numeric identifier matching the test definition |
| RESULT_VALUE_ACTUAL | Actual value returned by the test query |
| TEST_STATUS | Result status (PASS, FAIL) |
| TEST_TIMESTAMP | Timestamp when the test was executed |
| PROCESS_STEP | Processing stage (LAND, CLEAN) being tested |

#### Result Interpretation

1. **PASS Status**: Indicates that the actual result matches the expected result
2. **FAIL Status**: Indicates that the actual result does not match the expected result
3. **Result Analysis**: 
   - For EXACT_SCALAR tests, the comparison is a direct string equality check
   - A test passes only if the actual value exactly matches the expected value
   - Any deviation (including whitespace, case differences, or data type variations) results in a FAIL status

#### Historical Analysis

The test results table maintains a historical record of all test executions, enabling:

1. **Trend Analysis**: Track data quality over time
2. **Issue Identification**: Identify recurring or systematic data quality issues
3. **Process Validation**: Verify that data processing steps maintain data quality
4. **Audit Trail**: Maintain evidence of data quality checks for compliance purposes

#### Integration with Load History

When tests fail, the framework updates the `CTRL_LOAD_HISTORY` table to:

1. Set PROCESS_STATUS to 'FAIL'
2. Append '; DQ Test(s) Failed' to the PROCESS_NOTE field
3. Create a traceable link between data loading processes and quality validation

## Data Quality Dimensions

The framework supports six dimensions of data quality:

1. **Completeness**: Measures the presence of required data
   - Example: Count of NULL values in required fields

2. **Uniqueness**: Validates that data appears exactly once
   - Example: Count of duplicate primary keys

3. **Timeliness**: Ensures data is available when needed
   - Example: Verify data is not older than expected

4. **Validity**: Confirms data conforms to defined formats/rules
   - Example: Validate date formats, numeric ranges

5. **Accuracy**: Verifies data correctly represents real-world values
   - Example: Compare calculated totals against control values

6. **Consistency**: Ensures data is consistent across related datasets
   - Example: Verify foreign key relationships

## Test Execution Process

The framework implements a structured, multi-stage process for executing data quality tests:

### 1. Test Definition Retrieval

- The orchestration pipeline (`01 DQ_Test_Orchestration.orch.yaml`) queries the `CTRL_TEST_DQ_TESTS` table to retrieve active tests
- Tests are filtered based on:
  - FILE_KEY: Identifies the specific data source
  - PROCESS_STEP: Indicates the processing stage (LAND, CLEAN)
  - ACTIVE_FLAG: Ensures only active tests are executed
- Retrieved tests are loaded into a grid variable (`gv_Data_Quality_Tests`) for processing
- Tests are ordered by TEST_INDEX to ensure consistent execution sequence

### 2. Sequential Test Execution

- Tests are executed sequentially using a Grid Iterator component
- For each test definition row:
  - Test parameters are mapped to job variables
  - The transformation job (`02 DQ_Test_Execution.tran.yaml`) is invoked
  - The Grid Iterator is configured with "breakOnFailure: No" to ensure all tests run regardless of individual failures
  - Execution is sequential to prevent database contention and ensure consistent results

### 3. Individual Test Processing

For each test, the transformation pipeline:
- Executes the parameterized SQL query from TEST_SQL_QUERY
- Retrieves the actual result value
- Compares the actual result with the expected result based on RESULT_TYPE:
  - For EXACT_SCALAR: Performs exact string comparison
- Determines test status (PASS/FAIL)
- Records the result in the `CTRL_TEST_DQ_RESULTS` table with:
  - Test identification fields (SOR_KEY, FILE_KEY, etc.)
  - Actual result value
  - Test status
  - Execution timestamp
  - Process step information

### 4. Overall Status Determination

- After all tests are executed, the orchestration pipeline queries the `CTRL_TEST_DQ_RESULTS` table
- The overall status is determined using the following logic:
  ```sql
  SELECT 
    CASE 
      WHEN COUNT(CASE WHEN TEST_STATUS = 'FAIL' THEN 1 END) > 0 THEN 'FAIL'
      ELSE 'PASS'
    END as STATUS_OVERALL
  FROM ${ev_database}.${ev_controls_schema}.CTRL_TEST_DQ_RESULTS
  WHERE FILE_KEY = '${jv_FILE_KEY}'
  AND FILE_DATE = '${jv_FILE_DATE}'

- The result is stored in the `jv_TEST_STATUS_OVERALL` variable

### 5. Result Handling

Based on the overall test status:
- If PASS: The pipeline continues normal execution
- If FAIL: The pipeline updates the `CTRL_LOAD_HISTORY` table:
  - Sets PROCESS_STATUS to 'FAIL'
  - Appends '; DQ Test(s) Failed' to the PROCESS_NOTE field
  - This integration ensures data quality issues are reflected in the overall data processing status

### 6. Result Propagation

- The overall test status (`jv_TEST_STATUS_OVERALL`) is propagated back to the calling pipeline
- This enables conditional logic in parent pipelines based on data quality results
- The simulation pipeline (`00 Simulate Test Run.orch.yaml`) demonstrates how to implement conditional logic based on test results

This execution process ensures comprehensive data quality validation while maintaining integration with the broader data processing framework.


## Usage Guidelines

## Creating New Tests

This section provides detailed instructions for creating new data quality tests to be inserted into the `CTRL_TEST_DQ_TESTS` table. These tests should evaluate data against the six data quality dimensions (Completeness, Uniqueness, Timeliness, Validity, Accuracy, and Consistency).

### Step 1: Identify Source Table Information

When a `FILE_KEY` is provided (e.g., "Circular_YYYYMMDD.txt"), first query the `CTRL_FILE_EXTRACTS` table to retrieve essential metadata:

SELECT 
  SOR_KEY, 
  SF_SOURCE_TABLE_NAME 
FROM 
  PRX_DEV_WILLIAM.CONTROLS.CTRL_FILE_EXTRACTS 
WHERE 
  FILE_KEY = '[provided FILE_KEY]';

Note the `SOR_KEY` (e.g., "NUMERATOR") and `SF_SOURCE_TABLE_NAME` (e.g., "CIRCULAR") values, as these will be used to:
- Determine the schema name
- Identify the table to test
- Populate test definition fields

### Step 2: Determine Schema Name

The schema name follows this pattern: `[PROCESS_STEP]_[SOR_KEY]`

Where `PROCESS_STEP` is either:
- `RAW` for initial landing tables
- `CLEAN` for cleansed/transformed tables

Examples:
- `RAW_NUMERATOR` for raw data from NUMERATOR
- `CLEAN_NIELSEN` for cleansed data from NIELSEN

### Step 3: Examine Table Structure

To understand the table structure, use one of these approaches:

**Option 1: Direct query**

SELECT * 
FROM ${ev_database}.[SCHEMA_NAME].[TABLE_NAME] 
LIMIT 10;

Example:

SELECT * 
FROM ${ev_database}.RAW_NUMERATOR.CIRCULAR 
LIMIT 10;

**Option 2: Query INFORMATION_SCHEMA (recommended)**

SELECT 
  COLUMN_NAME,
  DATA_TYPE,
  CHARACTER_MAXIMUM_LENGTH,
  NUMERIC_PRECISION,
  NUMERIC_SCALE,
  IS_NULLABLE,
  COLUMN_DEFAULT,
  ORDINAL_POSITION
FROM 
  ${ev_database}.INFORMATION_SCHEMA.COLUMNS 
WHERE 
  TABLE_NAME = '[TABLE_NAME]' AND 
  TABLE_SCHEMA = '[SCHEMA_NAME]' 
ORDER BY 
  ORDINAL_POSITION;

Example:

SELECT 
  COLUMN_NAME,
  DATA_TYPE,
  IS_NULLABLE
FROM 
  ${ev_database}.INFORMATION_SCHEMA.COLUMNS 
WHERE 
  TABLE_NAME = 'CIRCULAR' AND 
  TABLE_SCHEMA = 'RAW_NUMERATOR' 
ORDER BY 
  ORDINAL_POSITION;

### Step 4: Design Tests for Data Quality Dimensions

For each data quality dimension, create appropriate tests based on the table structure:

#### 1. Completeness Tests

Check for NULL values in required fields:

SELECT COUNT(*) FROM ${ev_database}.[SCHEMA_NAME].[TABLE_NAME] WHERE [COLUMN_NAME] IS NULL

Expected result: `0` (no NULL values)

#### 2. Uniqueness Tests

Check for duplicate values in key fields:

SELECT 
  COUNT(*) - COUNT(DISTINCT [KEY_COLUMN]) 
FROM 
  ${ev_database}.[SCHEMA_NAME].[TABLE_NAME]

Expected result: `0` (no duplicates)

#### 3. Timeliness Tests

Check for data currency (if applicable):

SELECT 
  COUNT(*) 
FROM 
  ${ev_database}.[SCHEMA_NAME].[TABLE_NAME] 
WHERE 
  [DATE_COLUMN] < DATEADD(DAY, -[N], CURRENT_DATE())

Expected result: `0` (no outdated records)

#### 4. Validity Tests

Check for values within valid ranges or formats:

SELECT 
  COUNT(*) 
FROM 
  ${ev_database}.[SCHEMA_NAME].[TABLE_NAME] 
WHERE 
  [COLUMN_NAME] NOT IN ('Valid1', 'Valid2', 'Valid3')
  -- OR
  -- [COLUMN_NAME] NOT BETWEEN [MIN_VALUE] AND [MAX_VALUE]
  -- OR
  -- NOT REGEXP_LIKE([COLUMN_NAME], '[PATTERN]')

Expected result: `0` (no invalid values)

#### 5. Accuracy Tests

Compare calculated values against control totals:

SELECT 
  ABS(SUM([CALCULATED_COLUMN]) - [EXPECTED_TOTAL]) <= [TOLERANCE]
FROM 
  ${ev_database}.[SCHEMA_NAME].[TABLE_NAME]

Expected result: `TRUE` (calculated total matches expected total within tolerance)

#### 6. Consistency Tests

Check for referential integrity or cross-field consistency:

SELECT 
  COUNT(*) 
FROM 
  ${ev_database}.[SCHEMA_NAME].[TABLE_NAME] t1
  LEFT JOIN ${ev_database}.[SCHEMA_NAME].[REFERENCE_TABLE] t2
  ON t1.[FOREIGN_KEY] = t2.[PRIMARY_KEY]
WHERE 
  t2.[PRIMARY_KEY] IS NULL

Expected result: `0` (no orphaned records)

### Step 5: Create INSERT Statements

Format INSERT statements for the `CTRL_TEST_DQ_TESTS` table:

INSERT INTO ${ev_database}.CONTROLS.CTRL_TEST_DQ_TESTS (
  SOR_KEY,
  FILE_KEY,
  PROCESS_STEP,
  SCHEMA_NAME,
  TABLE_NAME,
  TEST_INDEX,
  TEST_NAME,
  TEST_DESCRIPTION,
  TEST_CATEGORY,
  TEST_SQL_QUERY,
  RESULT_TYPE,
  RESULT_VALUE_EXPECTED,
  ACTIVE_FLAG
) VALUES (
  '[SOR_KEY]',                                -- From CTRL_FILE_EXTRACTS
  '[FILE_KEY]',                               -- As provided
  '[PROCESS_STEP]',                           -- 'LAND' or 'CLEAN'
  '[SCHEMA_NAME]',                            -- Constructed as [PROCESS_STEP]_[SOR_KEY]
  '[TABLE_NAME]',                             -- From CTRL_FILE_EXTRACTS (SF_SOURCE_TABLE_NAME)
  [TEST_INDEX],                               -- Sequential number starting from 1
  '[TEST_NAME]',                              -- Brief descriptive name
  '[TEST_DESCRIPTION]',                       -- Detailed description
  '[TEST_CATEGORY]',                          -- One of the six dimensions
  '[TEST_SQL_QUERY]',                         -- SQL query that returns a scalar value
  'EXACT_SCALAR',                             -- Currently only EXACT_SCALAR is supported
  '[EXPECTED_RESULT]',                        -- Expected scalar result (usually '0' or 'TRUE')
  'TRUE'                                      -- Set to 'TRUE' to activate the test
);

### Example

For `FILE_KEY = 'Circular_YYYYMMDD.txt'`, after querying `CTRL_FILE_EXTRACTS` we find:
- `SOR_KEY = 'NUMERATOR'`
- `SF_SOURCE_TABLE_NAME = 'CIRCULAR'`

A completeness test for the `RETAILER_NAME` column would be:

INSERT INTO ${ev_database}.CONTROLS.CTRL_TEST_DQ_TESTS (
  SOR_KEY,
  FILE_KEY,
  PROCESS_STEP,
  SCHEMA_NAME,
  TABLE_NAME,
  TEST_INDEX,
  TEST_NAME,
  TEST_DESCRIPTION,
  TEST_CATEGORY,
  TEST_SQL_QUERY,
  RESULT_TYPE,
  RESULT_VALUE_EXPECTED,
  ACTIVE_FLAG
) VALUES (
  'NUMERATOR',
  'Circular_YYYYMMDD.txt',
  'LAND',
  'RAW_NUMERATOR',
  'CIRCULAR',
  1,
  'RETAILER_NAME Not Null',
  'Checks that all records have a non-null RETAILER_NAME value',
  'Completeness',
  'SELECT COUNT(*) FROM ${ev_database}.RAW_NUMERATOR.CIRCULAR WHERE RETAILER_NAME IS NULL',
  'EXACT_SCALAR',
  '0',
  'TRUE'
);

### Best Practices

1. **Test Naming**: Use consistent naming conventions (e.g., "[Column] [Test Type]")
2. **Test Indexing**: Assign sequential TEST_INDEX values within each FILE_KEY/PROCESS_STEP combination
3. **SQL Queries**: Ensure queries return exactly one scalar value
4. **Expected Results**: For most tests, '0' indicates no violations found
5. **Documentation**: Provide clear TEST_DESCRIPTION values to explain test purpose
6. **Coverage**: Create tests for all applicable data quality dimensions
7. **Performance**: Consider query performance for large tables; add appropriate filters when possible

## Prompt Format for Maia to Create New Tests
Hi Maia,

I need to create data quality tests for FILE_KEY: "[FILE_KEY_NAME]" (e.g., "Circular_YYYYMMDD.txt").

Process step: [PROCESS_STEP] (specify either "LAND" or "CLEAN")

Please create tests for the following data quality dimensions:
- Completeness: [specify columns that should not be NULL]
- Uniqueness: [specify columns or combinations that should be unique]
- Validity: [specify columns with format/range requirements]
- Consistency: [specify relationships with other tables if applicable]
- Accuracy: [specify any calculations that need validation]
- Timeliness: [specify any date-related requirements]

Additional context:
- [Any specific business rules]
- [Expected row counts]
- [Known data issues]
- [Critical columns]

Please generate the SQL INSERT statements for the CTRL_TEST_DQ_TESTS table.