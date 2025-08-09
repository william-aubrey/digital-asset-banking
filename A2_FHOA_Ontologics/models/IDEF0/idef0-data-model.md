# IDEF0 Relational Ontology: A Context for Agentic AI

**Document Purpose**: This document provides the complete context for building, monitoring, and enhancing IDEF0 process models as a relational database. It distills the core principles of the Federal Information Processing Standard for IDEF0 (FIPS 183) and integrates them with a sophisticated relational schema. This is the single source of truth for understanding our data-centric approach to process modeling.

---

## 1. Core IDEF0 Principles (The "Blueprint")

These concepts are derived directly from the FIPS 183 standard and form the theoretical basis of our model.

* **Function (The Box)**: A function is an activity, process, or transformation. It is represented by a box and named with a verb or verb phrase (e.g., "Manufacture Product").
* **ICOMs (The Arrows)**: These are the data or objects that inter-relate functions and act as constraints. An arrow's role is defined by the side of the box it connects to:
    * **Input**: Enters the left side. It is the data or object that is transformed by the function.
    * **Control**: Enters the top. It specifies the conditions or rules required for the function to produce correct output.
    * **Output**: Exits the right side. It is the data or object produced by the function.
    * **Mechanism**: Enters the bottom. It represents the means (tools, people, systems) used to perform the function.
* **Decomposition**: The core hierarchical principle. A single, high-level **parent box** is detailed by a **child diagram** containing three to six more specific child boxes. The child diagram covers the exact same scope as its parent box.
* **Bundling and Unbundling**: A single arrow on a parent diagram (e.g., "Tires") can be "unbundled" into multiple, more specific arrows on the child diagram (e.g., four separate "Tire" arrows). This allows for a clean high-level view while providing necessary detail at lower levels.

---

## 2. The Relational Ontology (The "Database")

Our central insight is that a complete IDEF0 model, including all its rules and visual notations, can be stored as structured data. This allows for powerful machine-driven analysis and programmatic diagram generation. This is the schema we will build.

### **The FHOA Ontology Schema (Version 1.2)**

#### **`MODELS` Table**
* `MODEL_ID` (PK), `MODEL_NAME`
* *Purpose*: The top-level container for a distinct modeling effort.

#### **`FUNCTIONS` Table**
* `FUNCTION_ID` (PK), `MODEL_ID` (FK), `FUNCTION_NAME`, `PARENT_FUNCTION_ID` (FK to self)
* *Purpose*: Represents the function boxes. The self-referencing `PARENT_FUNCTION_ID` creates the decomposition hierarchy.

#### **`ENTITIES` Table**
* `ENTITY_ID` (PK), `ENTITY_NAME`, `DESCRIPTION`
* *Purpose*: The master list of all unique "things" (data, objects, concepts) that can be represented by an arrow.

#### **`FUNCTION_ENTITIES` Table**
* `FUNCTION_ENTITY_ID` (PK), `FUNCTION_ID` (FK), `ENTITY_ID` (FK), `ROLE`
* *Purpose*: The core of the system. Each row represents a specific instance of an **Entity** serving a specific **Role** (Input, Control, etc.) for a specific **Function**.
* **Parent Link**:
    * `PARENT_FUNCTION_ENTITY_ID` (FK to self, nullable): This is the key to our bundling/unbundling concept. An unbundled arrow on a child diagram uses this field to point directly to the primary key of the bundled arrow on the parent diagram.
* **Source Traceability**:
    * `SOURCE_MODEL_ID` (FK), `SOURCE_FUNCTION_ID` (FK), `SOURCE_ENTITY_ID` (FK) (all nullable): These fields provide direct traceability for any Input, Control, or Mechanism back to the Function and Entity that produced it as an Output, even across different models. If these are `NULL`, it signifies an external boundary arrow.
* **Visual Metadata**:
    * `TUNNEL_STATUS` (Enum): Stores the graphical rule for tunneling, allowing the system to control information visibility across layers.

---

## 3. Directives for Agentic AI

Your primary function is to interact with this relational ontology to build, analyze, and visualize IDEF0 models.

1.  **Embrace the Poly-Model Goal**: The purpose of this schema is to serve two masters. You must be able to:
    * **Perform Process Analysis**: Use the relational links (`SOURCE_*` fields) to trace dependencies, perform impact analysis, and audit the logical flow of the process model based on the data.
    * **Generate Visual Diagrams**: Use the complete schema, including the **Visual Metadata** (`TUNNEL_STATUS`) and the **Parent Link** (`PARENT_FUNCTION_ENTITY_ID`), to programmatically construct 100% compliant and accurate IDEF0 diagrams for human review.

2.  **Respect the Hierarchy**: All interactions must honor the parent-child relationships defined in the `FUNCTIONS` table and the bundling/unbundling links in the `FUNCTION_ENTITIES` table. When a parent function is decomposed, you are responsible for ensuring all its ICOMs are correctly distributed and linked to the child functions.

3.  **Prioritize Clarity**: When populating the database, adhere to the principle of using a single, bundled arrow (e.g., `4 Tire(s)`) on parent diagrams where appropriate, and unbundling it into specific instances only on the child diagrams. This maintains the clarity and analytical integrity we have established.
