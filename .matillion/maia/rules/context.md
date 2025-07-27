# Project Context

This file helps Maia understand your specific project needs and requirements.

## Please include things like:
- Business context and objectives
- Warehouse naming conventions and standards
- Transformation rules and patterns
- Data source descriptions and characteristics
- Team-specific workflows

Context files are project and branch specific, stored in the `.matillion/maia/rules/` directory.

[View documentation to learn more about context files](https://docs.matillion.com/data-productivity-cloud/designer/docs/maia-context-files/)

## Documentation generation for jobs

Follow the prompt: 
 - Create the documentation for that pipeline in a code block that can be rendered in a note object in the UI.


## Layout for Pipeline documentation

#### <Replace by Job Name>

##### **Objective**

<Short explanation on the job goals>

<Bullet points with each accomplishment of that job>

##### **Logic**

<Explain the logic of the workflow with steps. Do not explain per component>

##### **Variables usage**
<Create a table format with each variable and its purpose>
|Variable | Purpose |
|---------|---------|
|Variable 1 | Purpose|
|Variable 2 | Purpose|


##### **Maintenance**
<Create a table format with a topic name of the maintenance and an explanation of what is required>

| ID | Topic | Maintenance Description |
|----|-------|-------------------------|
|ID 1| Topic Name 1 |  Topic 1 Maintenance description |
|ID 2| Topic Name 2 |  Topic 2 Maintenance description |

##### **Improvement opportunities**
<Create a table format with a topic name of the improvements detected and an explanation of what is required>

| ID | Topic | Improvement Description |
|----|-------|-------------------------|
|ID 1| Topic Name 1 |  Topic 1 Improvement description |
|ID 2| Topic Name 2 |  Topic 2 Improvement description |


# Matillion Context Configuration

# Project information
project:
  name: social-data-banking
  description: "Social Data Banking project configuration"
  version: "1.0.0"

# Default warehouse settings
warehouse:
  type: snowflake
  default_namespace:
    database: SNOWFLAKE_LEARNING_DB
    schema: PUBLIC

# Environment settings
environment:
  name: development
  region: us-east-1

