CREATE SEMANTIC VIEW (Snowflake)

Overview:
`CREATE SEMANTIC VIEW` is a SQL command in Snowflake used to create a new semantic view within a specified schema. A semantic view acts as a metadata layer over existing tables, defining logical tables, relationships, facts, dimensions, and metrics. This simplifies data querying for business users.

Syntax and Parameters:

**Basic Structure:**
`CREATE [ OR REPLACE ] SEMANTIC VIEW [ IF NOT EXISTS ] <name>
TABLES ( logicalTable [ , ... ] )
[ RELATIONSHIPS ( relationshipDef [ , ... ] ) ]
[ FACTS ( semanticExpression [ , ... ] ) ]
[ DIMENSIONS ( semanticExpression [ , ... ] ) ]
[ METRICS ( semanticExpression [ , ... ] ) ]
[ COMMENT = '<comment_about_semantic_view>' ]
[ COPY GRANTS ]`

**Required Parameters:**
* **`<name>`**: The unique name for the semantic view. It must follow standard Snowflake identifier rules (e.g., starts with a letter, no spaces unless quoted).
* **`TABLES`**: A required clause to define the logical tables that form the foundation of the semantic view.

**Key Clauses:**

1.  **`TABLES`**:
    * Defines logical tables from existing Snowflake tables.
    * Parameters for each logical table:
        * `[ <table_alias> AS ] <table_name>`: An optional alias for the table. If an alias is used, it must be used for all subsequent references within the view definition.
        * `[ PRIMARY KEY ( <primary_key_column_name> [ , ... ] ) ]`: Defines the primary key(s) for the logical table.
        * `[ UNIQUE ( <unique_column_name> [ , ... ] ) ]`: Defines unique key(s) for the logical table. Multiple `UNIQUE` clauses are allowed.
        * `[ WITH SYNONYMS ]`: Specifies informational synonyms for the table (not for use in relationships or expressions).
        * `[ COMMENT ]`: Adds a comment to the logical table.

2.  **`RELATIONSHIPS`**:
    * Optional clause to define joins between logical tables.
    * `relationshipDef` syntax: `<table_alias> ( <column_name> ) REFERENCES <ref_table_alias> ( <ref_column_name> )`.
    * The referenced columns (`ref_column_name`) must be defined as a `PRIMARY KEY` or `UNIQUE` key in the logical table definition.

3.  **`FACTS`, `DIMENSIONS`, `METRICS`**:
    * At least one of these clauses is required (`DIMENSIONS` or `METRICS`).
    * Each is defined as a `semanticExpression`: `<table_alias>.<dim_fact_or_metric_name> AS <sql_expr>`.
    * **`<sql_expr>`**: A SQL expression that computes the fact, dimension, or metric.
    * `WITH SYNONYMS` and `COMMENT` are optional for each expression.
    * **Order of clauses is important**: `FACTS` must be specified before `DIMENSIONS`.

**Advanced Features:**

* **Window Function Metrics**: Metrics can be defined using window functions (`OVER (...)`).
    * `PARTITION BY { <exprs_using_dimensions_or_metrics> | EXCLUDING <dimensions> }`: Groups rows for the window function. The `EXCLUDING` keyword allows partitioning by all dimensions except a specified one.
    * `ORDER BY <exprs_using_dimensions_or_metrics>`: Orders rows within each partition.

**Usage Notes:**

* **Atomic Operation**: `CREATE OR REPLACE` is an atomic operation, meaning the old view is deleted and the new one is created in a single transaction.
* **Privileges**:
    * The executing role needs `CREATE SEMANTIC VIEW` on the schema.
    * The role needs `SELECT` on all tables/views referenced in the semantic view.
    * `USAGE` privilege on the parent database and schema is also required.
* **`COPY GRANTS`**: When using `OR REPLACE`, this optional parameter copies all privileges (except `OWNERSHIP`) from the old view to the new one. If omitted, the new view only inherits future grants.
* **Metadata**: Be mindful not to include sensitive or personal data in metadata fields (comments, etc.).