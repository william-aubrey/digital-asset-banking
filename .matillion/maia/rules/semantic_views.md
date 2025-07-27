CREATE SEMANTIC VIEW
Creates a new semantic view in the current/specified schema.

The semantic view must comply with these validation rules.

See also
DESCRIBE SEMANTIC VIEW , DROP SEMANTIC VIEW , SHOW SEMANTIC VIEWS

Syntax
CREATE [ OR REPLACE ] SEMANTIC VIEW [ IF NOT EXISTS ] <name>
  TABLES ( logicalTable [ , ... ] )
  [ RELATIONSHIPS ( relationshipDef [ , ... ] ) ]
  [ FACTS ( semanticExpression [ , ... ] ) ]
  [ DIMENSIONS ( semanticExpression [ , ... ] ) ]
  [ METRICS ( semanticExpression [ , ... ] ) ]
  [ COMMENT = '<comment_about_semantic_view>' ]
  [ COPY GRANTS ]
where:

The parameters for logical tables are:

logicalTable ::=
  [ <table_alias> AS ] <table_name>
  [ PRIMARY KEY ( <primary_key_column_name> [ , ... ] ) ]
  [
    UNIQUE ( <unique_column_name> [ , ... ] )
    [ ... ]
  ]
  [ WITH SYNONYMS [ = ] ( '<synonym>' [ , ... ] ) ]
  [ COMMENT = '<comment_about_table>' ]
The parameters for relationships are:

relationshipDef ::=
  [ <relationship_identifier> AS ]
  <table_alias> ( <column_name> [ , ... ] )
  REFERENCES
  <ref_table_alias> [ ( <ref_column_name> [ , ... ] ) ]
The parameters for expressions in the definitions of facts, dimensions, and metrics are:

semanticExpression ::=
  <table_alias>.<dim_fact_or_metric> AS <sql_expr>
  [ WITH SYNONYMS [ = ] ( '<synonym>' [ , ... ] ) ]
  [ COMMENT = '<comment_about_dim_fact_or_metric>' ]
You can define a metric that uses a window function (a window function metric) by using the following syntax:

windowFunctionMetricDefinition ::=
  <window_function>( <metric> ) OVER (
    [ PARTITION BY { <exprs_using_dimensions_or_metrics> | EXCLUDING <dimensions> } ]
    [ ORDER BY <exprs_using_dimensions_or_metrics> [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...] ]
    [ <windowFrameClause> ]
  )
For information about this syntax, see Parameters for window function metrics.

Note

The order of the clauses is important. For example, you must specify the FACTS clause before the DIMENSIONS clause.

You can refer to semantic expressions that are defined in later clauses. For example, even if fact_2 is defined after fact_1, you can still use fact_2 in the definition of fact_1.

Required parameters
name
Specifies the name of the semantic view; the name must be unique for the schema in which the table is created.

In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier string is enclosed in double quotes (for example, "My object"). Identifiers enclosed in double quotes are also case-sensitive.

For more information, see Identifier requirements.

Optional parameters
COMMENT = 'comment_about_semantic_view'
Specifies a comment about the semantic view.

COPY GRANTS
When you specify OR REPLACE to replace an existing semantic view with a new semantic view, you can set this parameter to copy any privileges granted on the existing semantic view to the new semantic view.

The command copies all privilege grants except OWNERSHIP from the existing semantic view to the new semantic view. The role that executes the CREATE SEMANTIC VIEW statement owns the new view.

The new semantic view does not inherit any future grants defined for the object type in the schema.

The operation to copy grants occurs atomically with the CREATE SEMANTIC VIEW statement (in other words, within the same transaction).

If you omit COPY GRANTS, the new semantic view does not inherit any explicit access privileges granted on the existing semantic view but does inherit any future grants defined for the object type in the schema.

Parameters for logical tables
These parameters are part of the syntax for logical tables:

table_alias AS
Specifies an optional alias for the logical table.

If you specify an alias, you must use this alias when referring to the logical table in relationships, facts, dimensions, and metrics.

If you do not specify an alias, you use the unqualified logical table name to refer to the table.

table_name
Specifies the name of the logical table.

PRIMARY KEY ( primary_key_column_name [ , ... ] )
Specifies the names of one or more columns in the logical table that serve as the primary key of the table.

UNIQUE ( unique_column_name [ , ... ] )
Specifies the name of a column containing a unique value or the names of columns that contain unique combinations of values.

For example, if the column service_id contains unique values, specify:

TABLES(
  ...
  product_table UNIQUE (service_id)
If the combination of values in the product_area_id and product_id columns is unique, specify:

TABLES(
  ...
  product_table UNIQUE (product_area_id, product_id)
  ...
You can identify multiple columns and multiple combinations of columns as unique in a given logical table:

TABLES(
  ...
  product_table UNIQUE (product_area_id, product_id) UNIQUE (service_id)
  ...
Note

If you already identified a column as a primary key column (by using PRIMARY KEY), do not add the UNIQUE clause for that column.

WITH SYNONYMS [ = ] ( 'synonym' [ , ... ] )
Specifies one or more synonyms for the logical table. Unlike aliases, synonyms are used for informational purposes only. You do not use synonyms to refer to the logical table in relationships, dimensions, metrics, and facts.

COMMENT = 'comment_about_table'
Specifies a comment about the logical table.

Parameters for relationships
These parameters are part of the syntax for relationships:

relationship_identifier AS
Specifies an optional identifier for the relationship.

table_alias ( column_name [ , ... ] )
Specifies one of the logical tables and one or more of its columns that refers to columns in another logical table.

ref_table_alias [ ( ref_column_name [ , ... ] ) ]
Specifies the other logical table and one or more of its columns that are referred to by the first logical table.

The columns must be identified as a PRIMARY KEY or UNIQUE in the logical table definition.

Parameters for facts, dimensions, and metrics
In a semantic view, you must define at least one dimension or metric, which means that you must specify at least one DIMENSIONS or METRICS clause.

These parameters are part of the syntax for defining a fact, dimension, or metric:

table_alias.semantic_expression_name AS sql_expr
Specifies a name for a dimension, fact, or metric and the SQL expression for computing that dimension, fact, or metric.

See How Snowflake validates semantic views for the rules for defining a valid semantic view.

WITH SYNONYMS [ = ] ( 'synonym' [ , ... ] )
Specifies one or more optional synonyms for the dimension, fact, or metric. Note that synonyms are used for informational purposes only. You cannot use a synonym to refer to a dimension, fact, or metric in another dimension, fact, or metric.

COMMENT = 'comment_about_dim_fact_or_metric'
Specifies an optional comment about the dimension, fact, or metric.

Parameters for window function metrics
These parameters are part of the syntax for defining window function metrics:

metric
Specifies a metric expression for this window function. You can specify a metric or any valid metric expression that you can use to define a metric in this entity.

PARTITION BY ...
Groups rows into partitions. You can either partition by a specified set of expressions or by all dimensions (except selected dimensions) specified in the query:

PARTITION BY exprs_using_dimensions_or_metrics
Groups rows into partitions by SQL expressions. In the SQL expression:

Any dimensions in the expression must be accessible from the same entity that defines the window function metric.

Any metrics must belong to the same table where this metric is being defined.

You cannot specify aggregates, window functions, or subqueries.

PARTITION BY EXCLUDING dimensions
Groups rows into partitions by all of the dimensions specified in the SEMANTIC_VIEW clause of the query, except for the dimensions specified by dimensions.

dimensions must only refer to dimensions that are accessible from the entity that defines the window function metric.

For example, suppose that you exclude the dimension table_1.dimension_1 from partitioning:

CREATE SEMANTIC VIEW sv
  ...
  METRICS (
    table_1.metric_2 AS SUM(table_1.metric_1) OVER
      (PARTITION BY EXCLUDING table_l.dimension_1 ORDER BY table_1.dimension_2)
  )
  ...
Suppose that you run a query that specifies the dimension table_1.dimension_1:

SELECT * FROM SEMANTIC VIEW(
  sv
  METRICS (
    table_1.metric_2
  )
  DIMENSIONS (
    table_1.dimension_1,
    table_1.dimension_2,
    table_1.dimension_3
  );
In the query, the metric table_1.metric_2 is evaluated as:

SUM(table_1.metric_1) OVER (
  PARTITION BY table_1.dimension_2, table_1.dimension_3
  ORDER BY table_1.dimension_2
)
Note how table_1.dimension_1 is excluded from the PARTITION BY clause.

Note

You cannot use EXCLUDING outside of metric definitions in semantic views. EXCLUDING is not supported in window function calls in any other context.

ORDER BY exprs_using_dimensions_or_metrics  [ ASC | DESC ] [ NULLS  FIRST | LAST  ] [, ... ]
Orders rows within each partition. In the SQL expression:

Any dimensions in the expression must be accessible from the same entity that defines the window function metric.

Any metrics must belong to the same table where this metric is being defined.

You cannot specify aggregates, window functions, or subqueries.

windowFrameClause
See Window function syntax and usage.

For additional information about the parameters for window functions and examples, see Defining and querying window function metrics.

Access control requirements
A role used to execute this operation must have the following privileges at a minimum:

Privilege

Object

Notes

CREATE SEMANTIC VIEW

Schema

Required to create a new semantic view.

SELECT

Table, view

Required on any tables and/or views used in the semantic view definition.

The USAGE privilege on the parent database and schema are required to perform operations on any object in a schema.

For instructions on creating a custom role with a specified set of privileges, see Creating custom roles.

For general information about roles and privilege grants for performing SQL actions on securable objects, see Overview of Access Control.

Usage notes
The semantic view must be valid and must follow the rules described in How Snowflake validates semantic views.

Regarding metadata:

Attention

Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see Metadata fields in Snowflake.

CREATE OR REPLACE <object> statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.