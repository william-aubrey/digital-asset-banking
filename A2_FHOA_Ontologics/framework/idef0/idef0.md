# Integration Definition for Function Modeling (IDEF0)

*Draft Federal Information Processing Standards Publication 183*
*1993 December 21*

**Announcing the Standard for INTEGRATION DEFINITION FOR FUNCTION MODELING (IDEF0)**

Federal Information Processing Standards Publications (FIPS PUBS) are issued by the National Institute of Standards and Technology after approval by the Secretary of Commerce pursuant to Section 111(d) of the Federal Property and Administrative Services Act of 1949 as amended by the Computer Security Act of 1987, Public Law 100-235.

1.  **Name of Standard.** Integration Definition for Function Modeling (IDEF0).

2.  **Category of Standard.** Software Standard, Modeling Techniques.

3.  **Explanation.** This publication announces the adoption of the Integration Definition for Function Modeling (IDEF0) as a Federal Information Processing Standard (FIPS). This standard is based on the Air Force Wright Aeronautical Laboratories Integrated Computer- Aided Manufacturing (ICAM) Architecture, Part II, Volume IV - Function Modeling Manual (IDEF0), June 1981. This standard describes the IDEF0 modeling language (semantics and syntax), and associated rules and techniques, for developing structured graphical representations of a system or enterprise. Use of this standard permits the construction of models comprising system functions (activities, actions, processes, operations), functional relationships, and data (information or objects) that support systems integration. This standard is the reference authority for use by system or enterprise modelers required to utilize the IDEF0 modeling technique, by implementors in developing tools for implementing this technique, and by other computer professionals in understanding the precise syntactic and semantic rules of the standard.

4.  **Approving Authority.** Secretary of Commerce.

5.  **Maintenance Agency.** Department of Commerce, National Institute of Standards and Technology, Computer Systems Laboratory.

6.  **Cross Index.**
    * a. ICAM Architecture Part II-Volume IV - Function Modeling Manual (IDEF0), AFWAL-TR-81-4023, Materials Laboratory, Air Force Wright Aeronautical Laboratories, Air Force Systems Command, Wright-Patterson Air Force Base, Ohio 45433, June 1981.

---
## Introduction

This standard is composed of normative and informative sections. Compliance with the normative sections (Sections 1 through 3) is required. The informative sections (Annexes A through D) provide additional suggestions and guidance. This informative introduction discusses the background and approach of IDEF0. It provides the reader with an orientation and approach to the normative sections.

### Background:

During the 1970s, the U.S. Air Force Program for Integrated Computer Aided Manufacturing (ICAM) sought to increase manufacturing productivity through systematic application of computer technology. The ICAM program identified the need for better analysis and communication techniques for people involved in improving manufacturing productivity. As a result, the ICAM program developed a series of techniques known as the IDEF (ICAM Definition) techniques which included the following:

1.  **IDEF0**, used to produce a "function model". A function model is a structured representation of the functions, activities or processes within the modeled system or subject area.
2.  **IDEF1**, used to produce an "information model". An information model represents the structure and semantics of information within the modeled system or subject area.
3.  **IDEF2**, used to produce a "dynamics model". A dynamics model represents the time-varying behavioral characteristics of the modeled system or subject area.

### The IDEF0 Approach:

IDEF0 (Integration DEFinition language 0) is based on SADT™ (Structured Analysis and Design Technique™), developed by Douglas T. Ross and SofTech, Inc. In its original form, IDEF0 includes both a definition of a graphical modeling language (syntax and semantics) and a description of a comprehensive methodology for developing models. The result of applying IDEF0 to a system is a model that consists of a hierarchical series of diagrams, text, and glossary cross-referenced to each other. The two primary modeling components are functions (represented on a diagram by boxes) and the data and objects that inter-relate those functions (represented by arrows).

---

## 1. Overview

### 1.1 Scope
This standard describes the modeling language (syntax and semantics) which supports the IDEF0 technique for developing structured graphical representations of a system or subject area. Use of this standard permits the construction of IDEF0 models comprising system functions (actions, processes, operations), functional relationships, and the data and objects that support systems analysis and design, enterprise analysis, and business process re-engineering. This document provides three normative sections, Sections 1, 2 and 3, which define the language that supports IDEF0 modeling.

### 1.2 Purpose
The primary objectives of this standard are:

1.  To document and clarify the IDEF0 modeling technique and how to correctly use it;
2.  To provide a means for completely and consistently modeling the functions required by a system or subject area, and the data and objects that inter-relate those functions;
3.  To provide a modeling language which is independent of Computer-Aided Software Engineering (CASE) methods or tools, but which can be used in conjunction with those methods or tools;
4.  To provide a modeling language that has the following characteristics:
    * a) Generic (for analysis of systems and subject areas of varying purpose, scope and complexity);
    * b) Rigorous and precise (for production of correct, usable models);
    * c) Concise (to facilitate understanding, communication, consensus and validation);
    * d) Conceptual (for representation of functional requirements independent of physical or organizational implementations);
    * e) Flexible (to support several phases of the life cycle of a project).

    # Table of Contents: Integration Definition for Function Modeling (IDEF0)

This table of contents is synthesized from the `idef0.pdf` document.

---

### **Normative Sections**

* **1. Overview**
    * 1.1 Scope
    * 1.2 Purpose
* **2. Definitions**
* **3. IDEF0 Models**
    * 3.1 Model Concepts
    * 3.2 Syntax and Semantics
        * 3.2.1 Syntax
            * 3.2.1.1 Boxes
            * 3.2.1.2 Arrows
            * 3.2.1.3 Syntax Rules
        * 3.2.2 Semantics
            * 3.2.2.1 Box and Arrow Semantics
            * 3.2.2.2 Labels and Names
            * 3.2.2.3 Box and Arrow Semantic Rules
    * 3.3 IDEF0 Diagrams
        * 3.3.1 Types of Diagrams
        * 3.3.2 Diagram Features
        * 3.3.3 Diagram Syntax Rules
        * 3.3.4 Diagram Reference Expressions
    * 3.4 Models
        * 3.4.1 IDEF0 Model Description
        * 3.4.2 Context Diagrams
        * 3.4.3 High-Level Context Diagrams
        * 3.4.4 FEOs, Text and Glossary
        * 3.4.5 Model Name
        * 3.4.6 Presentation Rules

---

### **Informative Annexes**

* **ANNEX A - IDEF0 CONCEPTS**
    * A.1 Background
    * A.2 IDEF0 Concepts
    * A.3 Discussion of Individual IDEF0 Concepts
* **ANNEX B - CREATING AND INTERPRETING IDEF0 DIAGRAMS**
    * B.1 Reading IDEF0 Diagrams
    * B.2 Author's Guide to Creating IDEF0 Diagrams
    * B.3 Data Collection for IDEF Modeling
* **ANNEX C - REVIEW CYCLE PROCEDURES AND FORMS**
    * C.1 IDEF Teamwork Discipline
    * C.2 The IDEF Kit Cycle
    * C.3 IDEF Kits
    * C.4 Standard Diagram Form
    * C.5 Keeping Files
    * C.6 The IDEF Model Walk-Through Procedure
* **ANNEX D - Informative Definitions**

## 2. Definitions

This section contains definitions that relate to the normative sections of this document. See Annex D for definitions for the informative annexes. A term, if defined, is defined in either Section 2 or Annex D.

* **2.1 A-0 Diagram**: The special case of a one-box IDEF0 context diagram, containing the top-level function being modeled and its inputs, controls, outputs and mechanisms, along with statements of model purpose and viewpoint.
* **2.2 Arrow**: A directed line, composed of one or more arrow segments, that models an open channel or conduit conveying data or objects from source (no arrowhead) to use (with arrowhead). There are 4 arrow classes: Input Arrow, Output Arrow, Control Arrow, and Mechanism Arrow (includes Call Arrow).
* **2.3 Arrow Label**: A noun or noun phrase associated with an IDEF0 arrow or arrow segment, specifying its meaning.
* **2.4 Arrow Segment**: A line segment that originates or terminates at a box side, a branch (fork or join), or a boundary (unconnected end).
* **2.5 Boundary Arrow**: An arrow with one end (source or use) not connected to any box on a diagram. Contrast with Internal Arrow.
* **2.6 Box**: A rectangle, containing a name and number, used to represent a function.
* **2.7 Box Name**: The verb or verb phrase placed inside an IDEF0 box to describe the modeled function.
* **2.8 Box Number**: The number (0 to 6) placed inside the lower right corner of an IDEF0 box to uniquely identify the box on a diagram.
* **2.9 Branch**: A junction (fork or join) of two or more arrow segments.
* **2.10 Bundling/Unbundling**: The combining of arrow meanings into a composite meaning (bundling), or the separation of arrow meanings (unbundling), expressed by arrow join and fork syntax.
* **2.11 C-Number**: A chronological creation number that may be used to uniquely identify a diagram and to trace its history; may be used as a Detail Reference Expression to specify a particular version of a diagram.
* **2.12 Call Arrow**: A type of mechanism arrow that enables the sharing of detail between models (linking them together) or within a model.
* **2.13 Child Box**: A box on a child diagram.
* **2.14 Child Diagram**: The diagram that details a parent box.
* **2.15 Context**: The immediate environment in which a function (or set of functions on a diagram) operates.
* **2.16 Context Diagram**: A diagram that presents the context of a model, whose node number is A-n (n greater than or equal to zero). The one-box A-0 diagram is a required context diagram.
* **2.17 Control Arrow**: The class of arrows that express IDEF0 Control, i.e., conditions required to produce correct output. Control arrows are associated with the top side of an IDEF0 box.
* **2.18 Decomposition**: The partitioning of a modeled function into its component functions.
* **2.19 Detail Reference Expression (DRE)**: A reference (e.g., node number, C-number, page number) written beneath the lower right corner of an IDEF0 box to show that it is detailed and to indicate which diagram details it.
* **2.20 Diagram**: A single unit of an IDEF0 model that presents the details of a box.
* **2.21 Diagram Node Number**: That part of a diagram's node reference that corresponds to its parent box node number.
* **2.22 For Exposition Only (FEO) Diagram**: A graphic description used to expose or highlight specific facts about an IDEF0 diagram. A FEO diagram need not comply with IDEF0 rules.
* **2.23 Fork**: The junction at which an IDEF0 arrow segment (going from source to use) divides into two or more arrow segments. May denote unbundling of meaning.
* **2.24 Function**: An activity, process, or transformation (modeled by an IDEF0 box) identified by a verb or verb phrase that describes what must be accomplished.
* **2.25 Function Name**: Same as Box Name.
* **2.26 Glossary**: A listing of definitions for key words, phrases and acronyms used in conjunction with an IDEF0 node or model as a whole.
* **2.27 ICOM Code**: The acronym of Input, Control, Output, Mechanism. A code that associates the boundary arrows of a child diagram with the arrows of its parent box.
* **2.28 IDEF0 Model**: A graphic description of a system or subject that is developed for a specific purpose and from a selected viewpoint. A set of one or more IDEF0 diagrams that depict the functions of a system or subject area with graphics, text and glossary.
* **2.29 Input Arrow**: The class of arrows that express IDEF0 Input, i.e., the data or objects that are transformed by the function into output. Input arrows are associated with the left side of an IDEF0 box.
* **2.30 Interface**: A shared boundary across which data or objects are passed.
* **2.31 Internal Arrow**: An input, control or output arrow connected at both ends (source and use) to a box on a diagram. Contrast with Boundary Arrow.
* **2.32 Join**: The junction at which an IDEF0 arrow segment (going from source to use) merges with one or more other arrow segments to form a single arrow segment. May denote bundling of arrow segment meanings.
* **2.33 Mechanism Arrow**: The class of arrows that express IDEF0 Mechanism, i.e., the means used to perform a function. Mechanism arrows are associated with the bottom side of an IDEF0 box.
* **2.34 Model Note**: A textual comment that is part of an IDEF0 diagram, used to record a fact not otherwise depicted.
* **2.35 Node**: A box from which child boxes originate; a parent box.
* **2.36 Node Index**: A listing, often indented, showing nodes in an IDEF0 model in "outline" order. Same meaning and content as Node Tree.
* **2.37 Node Number**: A code assigned to a box to specify its position in the model hierarchy.
* **2.38 Node Reference**: A code assigned to a diagram to identify it and specify its position in the model hierarchy.
* **2.39 Node Tree**: The graphical representation of the parent-child relationships between the nodes of an IDEF0 model, in the form of a graphical tree. Same meaning and content as Node Index.
* **2.40 Output Arrow**: The class of arrows that express IDEF0 Output, i.e., the data or objects produced by a function. Output arrows are associated with the right side of an IDEF0 box.
* **2.41 Parent Box**: A box that is detailed by a child diagram.
* **2.42 Parent Diagram**: A diagram that contains a parent box.
* **2.43 Purpose**: A brief statement of the reason for a model's existence.
* **2.44 Semantics**: The meaning of the syntactic components of a language.
* **2.45 Squiggle**: A small jagged line that may be used to associate a label with a particular arrow segment or to associate a model note with a component of a diagram.
* **2.46 Syntax**: Structural components or features of a language and the rules that define relationships among them.
* **2.47 Text**: An overall textual (non-graphical) comment about an IDEF0 graphic diagram.
* **2.48 Title**: A verb or verb phrase that describes the overall function presented on an IDEFO diagram; the title of a child diagram corresponds to its parent box name.
* **2.49 Tunneled Arrow**: An arrow (with special notation) that does not follow the normal requirement that each arrow on a diagram must correspond to arrows on related parent and child diagrams.
* **2.50 Viewpoint**: A brief statement of the perspective of the model.


## 3. IDEF0 Models

This section discusses the basic elements of the IDEF0 modeling technique, identifies the basic components of syntax (graphical component) and semantics (meaning), specifies the rules that govern the use of the IDEFO technique, and describes the types of diagrams used. Although the components of syntax and semantics are very highly interrelated, each one is discussed separately without regard for the actual sequence of construction.

### 3.1 Model Concepts

A model is a representation of a set of components of a system or subject area. The model is developed for understanding, analysis, improvement or replacement of the system. Systems are composed of interfacing or interdependent parts that work together to perform a useful function. System parts can be any combination of things, including people, information, software, processes, equipment, products, or raw materials. The model describes what a system does, what controls it, what things it works on, what means it uses to perform its functions, and what it produces.

IDEFO is a modeling technique based on combined graphics and text that are presented in an organized and systematic way to gain understanding, support analysis, provide logic for potential changes, specify requirements, or support systems level design and integration activities. An IDEFO model is composed of a hierarchical series of diagrams that gradually display increasing levels of detail describing functions and their interfaces within the context of a system.

### 3.2 Syntax and Semantics

#### 3.2.1 Syntax

The structural components and features of a language and the rules that define relationships among them are referred to as the language's syntax. The components of the IDEFO syntax are boxes and arrows, rules, and diagrams. Boxes represent functions, defined as activities, processes or transformations. Arrows represent data or objects related to functions. Rules define how the components are used, and the diagrams provide a format for depicting models both verbally and graphically.

##### 3.2.1.1 Boxes

A box provides a description of what happens in a designated function. A typical box is shown in Figure 1. Each box shall have a name and number inside the box boundaries. The name shall be an active verb or verb phrase that describes the function. Each box on the diagram shall contain a box number inside the lower right corner.

    figure_number: "Figure 4. Label and Name Semantics"
    description: "An example IDEF0 diagram showing a single function box. The box is named 'PERFORM DETAILED DESIGN'. It has one Input from the left labeled 'Preliminary Design Data'. It has one Control from the top labeled 'Design Requirements'. It has one Output to the right labeled 'Recommended Detailed Design'. It has one Mechanism from the bottom labeled 'Design Engineer' and one Call arrow pointing down labeled 'MFG/A631'."

##### 3.2.2.3 Box and Arrow Semantic Rules
1.  A box shall be named with an active verb or verb phrase.
2.  Each side of a function box shall have a standard box/arrow relationship:
    a) Input arrows shall interface with the left side of a box.
    b) Control arrows shall interface with the top side of a box.
    c) Output arrows shall interface with the right side of the box.
    d) Mechanism arrows (except call arrows) shall point upward and shall connect to the bottom side of the box.
    e) Mechanism call arrows shall point downward, shall connect to the bottom side of the box, and shall be labeled with the reference expression for the box which details the subject box.
3.  Arrow segments, except for call arrows, shall be labeled with a noun or noun phrase unless a single arrow label clearly applies to the arrow as a whole.
4.  A "squiggle" (a small jagged line) shall be used to link an arrow with its associated label, unless the arrow/label relationship is obvious.
5.  Arrow labels shall not consist solely of any of the following terms: function, input, control, output, mechanism, or call.

### 3.3 IDEF0 Diagrams

#### 3.3.1 Types of Diagrams

IDEF0 models are composed of three types of information: graphic diagrams, text, and glossary. These diagram types are cross-referenced to each other. The graphic diagram is the major component of an IDEF0 model, containing boxes, arrows, box/arrow interconnections and associated relationships. Boxes represent each major function of a subject. These functions are broken down or decomposed into more detailed diagrams, until the subject is described at a level necessary to support the goals of a particular project. The top-level diagram in the model provides the most general or abstract description of the subject represented by the model. This diagram is followed by a series of child diagrams providing more detail about the subject.

##### 3.3.1.1 Top-Level Context Diagram

Each model shall have a top-level context diagram, on which the subject of the model is represented by a single box with its bounding arrows. This is called the A-0 diagram (pronounced A minus zero). The arrows on this diagram interface with functions outside the subject area to establish model focus. Since a single box represents the whole subject, the descriptive name written in the box is general. The A-0 diagram also sets the model scope or boundary and orientation. An example A-0 diagram is shown in Figure 5. The A-0 context diagram also shall present brief statements specifying the model's viewpoint and purpose, which help to guide and constrain the creation of the model.

    figure_number: "Figure 5. Example Top-level Diagram"
    description: "A Top-Level Context Diagram (A-0). A single box named 'PLAN NEW INFORMATION PROGRAM' with box number 0 is shown. It has two Inputs from the left: 'Issues' and 'Operations Data'. It has one Control from the top: 'Program Charter'. It has one Output to the right: 'Program Plan'. It has one Mechanism from the bottom: 'Program Team'. Below the diagram is text for PURPOSE: 'The assessment, planning, and streamlining of information management functions.' and VIEWPOINT: 'The Information Integration Assessment Team.'"

##### 3.3.1.2 Child Diagram

The single function represented on the top-level context diagram may be decomposed into its major sub-functions by creating its child diagram. In turn, each of these sub-functions may be decomposed, each creating another, lower-level child diagram. On a given diagram, some of the functions, none of the functions or all of the functions may be decomposed. Each child diagram contains the child boxes and arrows that provide additional detail about the parent box.

##### 3.3.1.3 Parent Diagram

A parent diagram is one that contains one or more parent boxes. Every ordinary (non-context) diagram is also a child diagram, since by definition it details a parent box. Thus a diagram may be both a parent diagram (containing parent boxes) and a child diagram (detailing its own parent box). The primary hierarchical relationship is between a parent box and the child diagram that details it.

    figure_number: "Figure 6. Decomposition Structure"
    description: "A diagram illustrating the hierarchical structure. It shows a high-level A-0 diagram with a box labeled '0'. This box is shown via a dashed line to be the parent of a diagram labeled 'A0'. The A0 diagram contains several boxes. A box labeled '4' on diagram A0 is shown to be the parent of a diagram labeled 'A4'. Finally, a box labeled '2' on diagram A4 is shown to be the parent of a diagram labeled 'A42'. The flow indicates a progression from 'More General' to 'More Detailed'."

The fact that a child box is detailed, and is therefore also a parent box, is indicated by the presence of a Detail Reference Expression (DRE). The DRE is a short code written below the lower right corner of the detailed (parent) box that points to its child diagram.

    figure_number: "Figure 7. Detail Reference Expression Use"
    description: "A child diagram with node reference MFG/A61, containing five function boxes. Boxes 1, 2, and 3 have Detail Reference Expressions (DREs) below their lower-right corners (A611, A612, A613 respectively), indicating they have been detailed in other diagrams. The diagram shows various inputs, outputs, and internal arrows connecting the five boxes."

##### 3.3.1.4 Text and Glossary

A diagram may have associated structured text, which is used to provide a concise overview of the diagram. The glossary shall be used to define acronyms and key words and phrases that have been used in conjunction with diagram graphics.

##### 3.3.1.5 For Exposition Only Diagrams

For Exposition Only (FEO, pronounced fee-oh) diagrams shall be used where an additional level of supplementary knowledge is required to adequately understand specific areas of a model. A FEO diagram need not comply with IDEF0 syntax rules.

#### 3.3.2 Diagram Features

##### 3.3.2.1 Arrows as Constraints

Arrows on an IDEF0 diagram represent data or objects as constraints. Only at low levels of detail can arrows represent flow or sequence. Connecting the output of one box to the input, control, or mechanism of another box shows that the function modeled by the latter box requires, and thus is constrained by, the presence of the corresponding output of the former box.

    figure_number: "Figure 8. Meaning of Constraint"
    description: "A diagram showing three function boxes numbered 1, 2, and 3. An arrow from box 1 and an arrow from box 2 both point to box 3. Text explains that the performance of function 3 requires the data/object outputs from both function 1 and function 2."

##### 3.3.2.2 Activations of a Box

A box may perform various parts of its function under different circumstances, using different combinations of its input and controls and producing different outputs. These different performances are called the different activations of the box.

##### 3.3.2.3 Concurrent Operation

Several functions in a model may be performed concurrently, if the needed constraints have been satisfied. As illustrated in Figure 9, an output of one box may provide some or all of the data and objects needed for activations of one or more other boxes.

    figure_number: "Figure 9. Concurrent Operation"
    description: "A diagram showing three function boxes numbered 1, 2, and 3. An output arrow from box 1 forks, with one branch going to box 2 and another to box 3. Text explains that once the data/object from box 1 is provided, functions 2 and 3 may operate concurrently."

##### 3.3.2.4 Arrows as Pipelines

It is useful to think of high-level arrows as pipelines or conduits. High-level arrows have general labels, while arrows on lower-level diagrams have more specific labels. If an arrow splits, forming two or more new arrow segments, each arrow segment may have a more specific label.

    figure_number: "Figure 10. Arrow Pipeline with Forking"
    description: "A diagram showing two function boxes, X (box 1) and Y (box 2). A control arrow labeled 'A' comes from the top and forks. One branch, labeled 'B', goes to box X. The other branch, labeled 'C', goes to box Y. The text explains that pipeline A splits into B and C."

##### 3.3.2.5 Branching Arrows

An arrow may branch (fork or join), indicating that the same kind of data or object may be needed or produced by more than one function. Labels on branching arrow segments provide a detailing of the arrow content. A forking arrow may denote the "unbundling" of meanings. The joining of two arrow segments may denote "bundling."

    figure_number: "Figure 11. Arrow Fork and Join Structures"
    description: "A diagram with two columns, 'GRAPHIC' and 'INTERPRETATION'. It shows four examples of arrow branching syntax. 1) A simple fork of an arrow labeled 'A' is interpreted as 'A' going down both paths. 2) A simple join of two arrows into one labeled 'A' is interpreted as both source arrows containing 'A'. 3) An arrow 'A' forking with one branch labeled 'B' is interpreted as 'A' on one path and 'B' (a portion of A) on the other. 4) Two arrows 'A' and 'B' joining is interpreted as the resulting arrow containing 'A & B'."

##### 3.3.2.6 Inter-Box Connections

Except for the single-box A-0 context diagram, a graphic diagram contains a minimum of three and a maximum of six boxes. Boxes are normally organized diagonally from the upper left corner to the lower right. Any output arrow may provide data or objects to any other box.

    figure_number: "Figure 12. Connections Between Boxes"
    description: "A diagram with three boxes: 'KEEP RECORDS' (1), 'DELIVER PRODUCTS' (2), and 'DO BILLING' (3). It demonstrates connections with annotations. An output 'Files' from box 1 forks into 'Customer Records' (input to box 2) and 'Price & Tax Tables' (control to box 3). An output 'Transactions' from box 2 and an output from box 3 join to form a new output called 'Account Entries'."

    figure_number: "Figure 13. Boundary and Internal Arrows"
    description: "A diagram showing the difference between Boundary and Internal arrows. Three boxes are arranged diagonally. Arrows that connect two of the boxes are labeled 'Internal Arrows'. Arrows that have one end unconnected at the edge of the diagram are labeled 'Boundary Arrows'."

    #### 3.3.2 Diagram Features

##### 3.3.2.1 Arrows as Constraints

Arrows on an IDEF0 diagram represent data or objects as constraints. Only at low levels of detail can arrows represent flow or sequence. Connecting the output of one box to the input, control, or mechanism of another box shows that the function modeled by the latter box requires, and thus is constrained by, the presence of the corresponding output of the former box.

    figure_number: "Figure 8. Meaning of Constraint"
    description: "A diagram showing three function boxes numbered 1, 2, and 3. An arrow from box 1 and an arrow from box 2 both point to box 3. Text explains that the performance of function 3 requires the data/object outputs from both function 1 and function 2."

##### 3.3.2.2 Activations of a Box

A box may perform various parts of its function under different circumstances, using different combinations of its input and controls and producing different outputs. These different performances are called the different activations of the box.

##### 3.3.2.3 Concurrent Operation

Several functions in a model may be performed concurrently, if the needed constraints have been satisfied. As illustrated in Figure 9, an output of one box may provide some or all of the data and objects needed for activations of one or more other boxes.

    figure_number: "Figure 9. Concurrent Operation"
    description: "A diagram showing three function boxes numbered 1, 2, and 3. An output arrow from box 1 forks, with one branch going to box 2 and another to box 3. Text explains that once the data/object from box 1 is provided, functions 2 and 3 may operate concurrently."

##### 3.3.2.4 Arrows as Pipelines

It is useful to think of high-level arrows as pipelines or conduits. High-level arrows have general labels, while arrows on lower-level diagrams have more specific labels. If an arrow splits, forming two or more new arrow segments, each arrow segment may have a more specific label.

    figure_number: "Figure 10. Arrow Pipeline with Forking"
    description: "A diagram showing two function boxes, X (box 1) and Y (box 2). A control arrow labeled 'A' comes from the top and forks. One branch, labeled 'B', goes to box X. The other branch, labeled 'C', goes to box Y. The text explains that pipeline A splits into B and C."

##### 3.3.2.5 Branching Arrows

An arrow may branch (fork or join), indicating that the same kind of data or object may be needed or produced by more than one function. Labels on branching arrow segments provide a detailing of the arrow content. A forking arrow may denote the "unbundling" of meanings. The joining of two arrow segments may denote "bundling."

    figure_number: "Figure 11. Arrow Fork and Join Structures"
    description: "A diagram with two columns, 'GRAPHIC' and 'INTERPRETATION'. It shows four examples of arrow branching syntax. 1) A simple fork of an arrow labeled 'A' is interpreted as 'A' going down both paths. 2) A simple join of two arrows into one labeled 'A' is interpreted as both source arrows containing 'A'. 3) An arrow 'A' forking with one branch labeled 'B' is interpreted as 'A' on one path and 'B' (a portion of A) on the other. 4) Two arrows 'A' and 'B' joining is interpreted as the resulting arrow containing 'A & B'."

##### 3.3.2.6 Inter-Box Connections

Except for the single-box A-0 context diagram, a graphic diagram contains a minimum of three and a maximum of six boxes. Boxes are normally organized diagonally from the upper left corner to the lower right. Any output arrow may provide data or objects to any other box.

    figure_number: "Figure 12. Connections Between Boxes"
    description: "A diagram with three boxes: 'KEEP RECORDS' (1), 'DELIVER PRODUCTS' (2), and 'DO BILLING' (3). It demonstrates connections with annotations. An output 'Files' from box 1 forks into 'Customer Records' (input to box 2) and 'Price & Tax Tables' (control to box 3). An output 'Transactions' from box 2 and an output from box 3 join to form a new output called 'Account Entries'."

    figure_number: "Figure 13. Boundary and Internal Arrows"
    description: "A diagram showing the difference between Boundary and Internal arrows. Three boxes are arranged diagonally. Arrows that connect two of the boxes are labeled 'Internal Arrows'. Arrows that have one end unconnected at the edge of the diagram are labeled 'Boundary Arrows'."

    ##### 3.3.2.7 Boundary Arrows

Boundary arrows on an ordinary (non-context) graphic diagram represent the inputs, controls, outputs, or mechanisms of the diagram's parent box. The source or use of these boundary arrows can be found only by examining the parent diagram. All boundary arrows on a child diagram (except for tunneled arrows, Section 3.3.2.9) shall correspond to the arrows that connect to its parent box.

    figure_number: "Figure 14. Boundary Arrow Correspondence"
    description: "A diagram showing a 'parent diagram' above a 'child diagram'. A box on the parent diagram, labeled 'parent box', is shown being detailed by the entire child diagram below. Dashed lines connect the arrows on the parent box to the corresponding boundary arrows on the child diagram, illustrating that an input, control, and output on the parent box match the boundary arrows on the child diagram."

##### 3.3.2.8 ICOM Coding of Boundary Arrows

ICOM codes relate boundary arrows on a child diagram to arrows connected to its parent box. A specific notation, called ICOM codes, specifies the matching connections. The letter I, C, O or M is written near the unconnected end of each boundary arrow on the child diagram. This coding identifies the arrow as an Input, Control, Output or Mechanism on the parent box. This letter is followed by a number giving the relative position at which the arrow is shown connecting to the parent box, numbering from left to right or top to bottom. For example, "C3" written on a boundary arrow on a child diagram indicates that this arrow corresponds to the third control arrow (from the left) entering its parent box.

    figure_number: "Figure 15. ICOM Codes and Changing Arrow Roles"
    description: "A diagram showing the relationship between a 'PARENT BOX' and a 'CHILD DIAGRAM'. The child diagram contains three boxes. Dashed lines illustrate how the ICOM codes on the child diagram's boundary arrows (e.g., I1, I2, C1, C2, C3, O1, O2) correspond to the physical arrows connecting to the parent box above."

##### 3.3.2.9 Tunneled Arrows

A tunneled arrow is used to provide information at a specific level of decomposition that is not required for understanding at some other levels. Using the parentheses notation, tunneling an arrow where it connects to a box side means that the data or objects expressed by that arrow shall not be shown on its child diagram. Tunneling an arrow at the unconnected end means that the data or objects are not necessary at the next higher (parent) level and hence shall not be shown connecting to the parent box.

    figure_number: "Figure 16. Arrows Tunneled at Connected End"
    description: "A diagram of a single box with four arrows (I1, C1, O1, M1). Parentheses are placed around the arrowheads where the Input, Control, and Output arrows connect to the box, and around the base of the Mechanism arrow. Text states: 'These boundary arrows do not correspond to arrows on the child diagram.'"

    figure_number: "Figure 17. Arrows Tunneled at Unconnected End"
    description: "A diagram of a single box with four boundary arrows. Parentheses are placed at the unconnected ends of all four arrows. Text states: 'These boundary arrows do not correspond to arrows connecting to the parent box.'"

    figure_number: "Figure 18. Example of Tunneled Arrows"
    description: "A diagram showing a 'parent diagram' and a 'child diagram'. On the parent, a control arrow at position C2 is shown with a tunneled connection to the parent box. On the child diagram, this C2 arrow does not appear. Additionally, an output arrow O1 on the child diagram is shown with a tunneled unconnected end, and this arrow does not appear on the parent diagram."

##### 3.3.2.10 Call Arrows

A call arrow is a special case of mechanism arrow. It signifies that the caller box does not have its own child diagram to detail it, but rather is detailed entirely by another box (and its descendants) in the same or another model. The call arrow is labeled with the node reference of the diagram containing the called box, along with the called-box number.

#### 3.3.3 Diagram Syntax Rules
1.  Context diagrams shall have node numbers A-n, where n is greater than or equal to zero.
2.  The model shall contain a A-0 context diagram, which contains only one box.
3.  The box number of the single box on the A-0 context diagram shall be 0.
4.  A non-context diagram shall have at least three boxes and no more than six boxes.
5.  Each box on a non-context diagram shall be numbered in its lower right inside corner, in order (from upper left to lower right on the diagram) from 1 to at most 6.
6.  Each box that has been detailed shall have the detail reference expression (DRE, e.g., node number, C-number, or page number) of its child diagram written beneath the lower right corner of the box.
7.  Arrows shall be drawn as horizontal and vertical straight line segments. Diagonal line segments shall not be used.
8.  Each box shall have a minimum of one control arrow and one output arrow.
9.  A box shall have zero or more input arrows.
10. A box shall have zero or more non-call mechanism arrows.
11. A box shall have 0 or 1 call arrows.
12. Control feedbacks shall be shown as "up and over." Input feedbacks shall be shown as "down and under." Mechanism feedbacks shall be shown as "down and under."
13. The unconnected end of a boundary arrow shall have the proper ICOM code specifying its connection to the parent box, or shall be tunneled.
14. Open-ended boundary arrows that represent the same data or objects shall be connected through a fork to show all the places affected, unless this results in an unreadable diagram. Multiple sources that represent the same data or objects shall join to form a single output boundary arrow.
15. Box names and arrow labels shall not consist solely of the following words: function, activity, process, input, output, control or mechanism.

#### 3.3.4 Diagram Reference Expressions

Reference expressions use codes that are assigned to model features such as diagrams, boxes, arrows and notes. Reference expressions then can be used in various contexts to refer precisely to any aspect of the model. The basic unit of reference is the node number, which applies to the place where functional decomposition is modeled by the detailing of a parent box on a child diagram.

##### 3.3.4.1 Box Numbers

Each box on a diagram shall be numbered in the lower inside right corner of the box. This numbering system is required to uniquely identify the boxes within a diagram, and to generate node numbers. The box number for the single box on the A-0 context diagram shall be 0 (zero). The box numbers for the boxes on all other graphic diagrams shall be 1, 2, 3, to at most 6.

##### 3.3.4.2 Node Numbers

A node number is based on the position of a box in the model hierarchy. Normally, a node number is formed by appending a box number to the node number of the diagram on which it appears. For example, the node number of box 2 on diagram A25 is A252. When a box is detailed by a child diagram, the node number of the parent box is assigned as the diagram node number; thus, the parent box and its child diagram have the same node number.

Every IDEF0 model has a top-level context diagram, the A-0 diagram. This diagram contains a single "top box" which is the unique parent of the entire modeled subject and bears the unique box number 0 (zero) and node number A0. The child diagram that details the A0 parent top box bears the unique node numbers A1, A2, A3, to at most A6.

###### 3.3.4.2.1 Node Index

The node index is a presentation of node information in an "outline" format. All node numbers, along with either diagram titles or box names, shall be presented in an indented form that exhibits the nested hierarchic structure of the model.

    figure_number: "Figure 19. Typical Node Index"
    description: "An indented list showing a model's hierarchy. 'A0 Manufacture Product' is at the top. Under it are 'A1 Plan

##### 3.3.4.3 Node References

Each diagram in a model has a node reference, which uniquely identifies it and its position in the model hierarchy. The node reference is composed of the abbreviated model name and the diagram node number, separated by a slash (/). For example, a model named Quality Assurance Operations might be abbreviated as QA, and a node reference might then be QA/A312. A node reference may also have a suffix, e.g., F (for FEO), T (for text), or G (for glossary), and a page number.

##### 3.3.4.4 Model Notes

Model notes are optional. They are denoted by an integer "n" inside a small square box. For a given diagram, the note numbers shall form a consecutive sequence, starting at 1. Model notes provide information that is relevant to a diagram's message but that does not conveniently fit into the box-and-arrow syntax.

##### 3.3.4.5 Reference Notation

A standard notation is used in writing text and notes to refer to diagrams and specific parts of diagrams. References are based on box numbers, node numbers, ICOM codes, and note numbers. The following table provides examples of reference notations.

| REFERENCE NOTATION | MEANING |
|---|---|
| `2I1` | Box 2 Input 1 |
| `O2` | The boundary arrow with ICOM code O2 |
| `2O

### 3.4 Models

#### 3.4.1 IDEF0 Model Description

One of the most important features of IDEF0 as a modeling concept is that it gradually introduces greater and greater levels of detail through the diagram structure comprising the model. In this way, communication is enhanced by providing the reader with a well-bounded topic with a manageable amount of detail to learn from each diagram.

An IDEF0 model starts by presenting the whole subject as a single unit a box with external-arrow boundary conditions connecting it to functions and resources outside the subject. The single box is called the "top box" of the model. Since the single top box of an IDEF0 model represents the subject as a whole, the descriptive name in the box is general.

#### 3.4.2 Context Diagrams

The diagram in which the A0 top box appears represents the context of the model and is called a context diagram. The minimum context for a model is the special context diagram with the node number A-0. The A-0 context diagram has only the single named A0 top box, with its labeled external arrows, and also textual definitions of the Viewpoint and Purpose of the model.

Sometimes, however, in order to provide a more complete exposition of the environmental context of the model, an optional A-1 context diagram is also presented.

#### 3.4.3 High-Level Context Diagrams

High-level context diagrams have node numbers of the form A-n, for n greater than one. By providing a more complete description of the model's environmental context, context modeling provides more-constraining specifications on the boundary conditions of the A0 diagram of the model.

    figure_number: "Figure 21. Negative Node-Numbered Context"
    description: "A complex node tree illustrating high-level context. The top-most node is 'A-2', which has a parental context of 'NONE'. It branches to 'A-21', 'A-22', 'A-1', and 'A-24'. The 'A-1' node then branches to 'A-11', 'A0', 'A-13', and 'A-14'. The 'A0' node is shown with a parental context of 'TOP A-0 (With Viewpoint & Purpose)'. 'A0' then branches down to the model's primary children, 'A1', 'A2', 'A3', and 'A4'."

#### 3.4.4 FEOs, Text and Glossary

The node-numbering scheme provides the basis for coordinating FEOs, text, and glossary terms. For each form, the node-numbering extension notation consists of a single letter appended to the associated node number (e.g., A312F for FEO, A312G for Glossary, A312T for Text). If there is more than one page, they should be designated with an additional number (e.g., A312F1, A312F2).

#### 3.4.5 Model Name

Each model has a unique, descriptive name that distinguishes it from other models. This model name is normally abbreviated (uniquely) for use in node references. For example, a model named Manufacturing Operations may be abbreviated MFG.

#### 3.4.6 Presentation Rules

1.  When there is text, it shall accompany the associated graphic diagram.
2.  In non-publication models, the glossary associated with a specific graphic diagram shall accompany the diagram.
3.  In publication models, a glossary section shall define the key words, phrases and acronyms in alphabetical order for the entire model.
4.  When a table of contents is provided for a model, it shall be presented as a node tree or node index, and shall contain node numbers, diagram titles and box names.

## ANNEX A - IDEF0 CONCEPTS

### A.1 Background

The desire of the U.S. Air Force to reduce costs and lead times by assisting the aerospace industry in its modernization efforts is evidenced in its many "Tech Mod" (Technology Modernization) programs. A similar goal, but using an industry-wide target rather than individual companies, was established under the ICAM (Integrated Computer Aided Manufacturing) Program.

To develop the architecture, a "language" was needed in which to express and document current aerospace industry operations. The SADT (Structured Analysis and Design Technique) originally developed in 1972 by Douglas T. Ross, of SofTech, was selected as "The Architecture Method". The activity modeling technique was further developed and used in the follow-on ICAM Part I Program. The major subset of this technique used by the ICAM Part II Program Office was later re-named and documented as "IDEF0".

### A.2 IDEFO Concepts

The original IDEF0 methodology incorporated basic concepts which address each of the needs listed above. These basic IDEF concepts are:

1.  **Activity Modeling Graphic Representation.** The "box and arrow" graphics of an IDEF0 diagram show the manufacturing operation as the box, and the interfaces to/from the operation as the arrows entering/leaving the box.
2.  **Conciseness.** The documentation of a manufacturing architecture must be concise to permit encompassing the subject matter. The two-dimensional form provided by a blueprint-like language has the desired conciseness.
3.  **Communication.** There are several IDEF0 concepts which are designed to enhance communications:
    * Diagrams based upon very simple box and arrow graphics.
    * English text to specify box (function) and arrow (data or objects) meanings.
    * Gradual exposition of detail, featuring a hierarchy with major functions at the top and successive levels of sub-functions revealing well-bounded detail breakout.
    * A node index for locating details within the hierarchic structure of diagrams.
    * Limitation of detail on each successive diagram to not more than six sub-functions.
4.  **Rigor and Precision.** The rules of IDEF0 enforce sufficient rigor and precision to satisfy ICAM architecture needs without overly constraining the analyst.
5.  **Methodology.** Step-by-step procedures are provided for modeling, review and interview tasks.
6.  **Organization vs. Function.** The separation of organization from function is included in the purpose of the model and carried out by the selection of functions and arrow labels during model development.

### A.3 Discussion of Individual IDEFO Concepts

#### A.3.1 Activity Modeling Graphics

The IDEF0 methodology may be used to model a wide variety of automated and non-automated "systems". The result of applying IDEFO is a model. A model consists of diagrams, text and glossary, cross-referenced to each other. Diagrams are the major components of a model.

The position at which the arrow attaches to a box conveys the specific role of the interface. The controls enter the top of the box. The inputs enter the box from the left. The outputs of the operation leave the right-hand side of the box. Mechanism arrows that provide supporting means join (point up to) the bottom of the box.

    figure_number: "Figure A1. Function Box and Data/Objects Arrows"
    description: "A diagram showing a central function box labeled 'FUNCTION NAME'. Four arrows indicate the standard ICOM roles. An 'Input' arrow enters from the left. A 'Control' arrow enters from the top. An 'Output' arrow exits to the right. A 'Mechanism' arrow points up to the bottom. A 'Call' arrow points down from the bottom."

    figure_number: "Figure A2. Constraint Diagrams"
    description: "A diagram showing three function boxes labeled 'Function A', 'Function B', and 'Function C'. Arrows show the relationships between them. An output from Function A becomes an input to Function B. Another arrow from an external source acts as a control on Function A, and a separate arrow acts as a control on Function B. An output from Function B becomes an input to Function C."

#### A.3.2 Communication by Gradual Exposition of Detail

One of the most important features of IDEF0 is that it gradually introduces greater and greater levels of detail through the diagram structure. An IDEF0 model starts by representing the whole system as a single unit a box with arrow interfaces to functions outside the system. This is the "context diagram."

    figure_number: "Figure A3. IDEF0 Model Structure"
    description: "A duplicate of Figure 6, illustrating the hierarchical structure. It shows a high-level A-0 diagram with a box '0'. This box is shown to be the parent of a diagram labeled 'A0' which contains several boxes. Box '4' on diagram A0 is shown to be the parent of a diagram labeled 'A4'. Finally, box '2' on diagram A4 is shown to be the parent of a diagram labeled 'A42', moving from 'More General' to 'More Detailed'."

The box that represents the system as a single module is then detailed on another diagram with boxes connected by interface arrows. These boxes represent major sub-functions of the single parent function. Each of these sub-functions may be similarly decomposed to expose even more detail. A box, if detailed, is always detailed on a child diagram into no fewer than three boxes, but no more than six boxes.

#### A.3.3 Disciplined Teamwork

The IDEF0 methodology includes procedures for developing and critiquing models by a large group of people. The creation of a model is a dynamic process which usually requires the participation of more than one person. Throughout a project, authors create initial diagrams which are distributed to project members for review and comment. The discipline requires that each person expected to make comments about a diagram shall make them in writing and submit them to the author of the diagram. The author replies, also in writing. This cycle continues until the diagrams, and eventually the entire model, are officially accepted.


## ANNEX B - CREATING AND INTERPRETING IDEF0 DIAGRAMS

### B.1 Reading IDEF0 Diagrams

A model is made up of a collection of diagrams and associated materials arranged in a hierarchic manner. A node index (or table of contents) shall be provided. Placing the diagrams in hierarchical order gives an overall view of the model and allows access to any portion. Reading is done top-down, considering each diagram as a context bounded by its parent box.

    figure_number: "Figure B1. Page-Pair Format"
    description: "An illustration of a bound document opened to a two-page spread. The left page contains helpful text and a small version of the parent diagram. The right page shows the 'current diagram' being described."

    figure_number: "Figure B2. Node Index Showing Diagram Order"
    description: "A textual list showing a node index. An arrow points downwards along the list, indicating the 'Order of diagrams in a document'. The list shows A0, A1, A2 (with children A21, A22, A23), A3, and A4."

#### B.1.1 Approaching a Model

Models provide an overview of the whole system or subject area as well as details of a particular subject. To read a model for its overview, use the index to find all high-level diagrams. To read a model for detail, use the index to find all diagrams detailing the subject of interest.

    figure_number: "Figure B3. Node Index Showing Overview Diagrams"
    description: "A node index is shown with the high-level diagrams (A0, A1, A2, A3) highlighted, indicating how to get an overview of the model."

    figure_number: "Figure B4. Node Index Showing Specific Detailed Diagram"
    description: "A node index is shown with a specific detail path (A2, A23) highlighted, indicating how to find details on a specific subject."

#### B.1.2 Diagram Reading Steps

The following reading sequence is recommended:
1.  Scan the boxes of the diagram to gain an impression of what is being described.
2.  Refer back to the parent diagram and note the arrow connections to the parent box.
3.  Consider the arrows of the current diagram. Try to determine if there is a main path.
4.  Mentally walk through the diagram, from upper left to lower right, using the main path as a guide.
5.  Check to see if a related FEO diagram exists.
6.  Finally, read the text and glossary, if provided.

    figure_number: "Figure B5. Example of Main Path"
    description: "A sample FEO diagram titled 'Maintain Reparable Spares'. The diagram shows a main path of arrows flowing from an 'In-service asset' through functions like 'Remove & replace', 'Schedule into shop', 'Inspect or repair', and 'Monitor & route' to a final 'Completed asset' output."

#### B.1.3 Semantics of Boxes and Arrows

The fundamental notion which must guide the interpretation of any diagram is: Only that which is explicitly stated is necessarily implied. The corollary is that: Any further detailing not explicitly prohibited is implicitly allowed.

    figure_number: "Figure B6. Example of Constraint"
    description: "A diagram with two boxes. Box 1, 'Measure operating conditions', takes 'Environment' as an input and produces 'Temperature' as an output. The 'Temperature' output becomes an input to Box 2, 'Monitor temperature'. Box 2 also takes 'Tolerance' as a control and produces 'Danger signal' as an output."

    figure_number: "Figure B7. Two boxes using the contents of the same arrow"
    description: "A diagram shows an output arrow 'X' from box 1 forking to become an input to box 2 and box 3."

    figure_number: "Figure B8. Illustration of ICOM coding"
    description: "A single, generic function box is shown with multiple arrows for each ICOM role: three inputs (I1, I2, I3), four controls (C1, C2, C3, C4), three mechanisms (M1, M2, M3), and three outputs (O1, O2, O3)."

    figure_number: "Figure B9. FEO representing detailing of multiple ICOMS"
    description: "The same box from Figure B8 is shown, but with a smaller box inside labeled '1'. This inner box shows that inputs I1 and I2 and control C1 are used to produce output O1, illustrating that not all ICOMs are needed for all activations."

    ### B.2 Author's Guide to Creating IDEF0 Diagrams

When creating any IDEF0 diagram, the requirements to be satisfied are that:
a. its purpose and viewpoint shall match the stated purpose and viewpoint of the overall model;
b. its boundary arrows shall correspond to the arrows that connect to its parent box;
c. its content shall be exactly everything in its parent box.

#### B.2.1 Basic Steps of Authoring

The step-by-step discipline of authoring makes it possible to create diagrams that form useful and coherent models. The discipline to follow is:
a. Bound the subject matter more precisely than the name of the function box suggests.
b. Study the bounded set of subject matter and form possible sub-functions of the total function.
c. Look for natural patterns of connection of those sub-functions.
d. Split and cluster sub-functions to make suitable boxes.
e. Draw a final version of the diagram with careful attention to layout and clarity.

##### B.2.1.1 Selecting a Context, Viewpoint and Purpose

Before beginning any model, it is important to determine the model's orientation. This includes the context, viewpoint and purpose. The context establishes the subject of the model as part of a larger whole. The viewpoint determines what can be "seen" within the context, and from what "slant" or perspective. The purpose establishes the intent of the model or the goal of communication that it serves.

##### B.2.1.2 Creating the Context Diagram

To start a model, create the A-0 diagram. Draw a single box containing the name of the function which encompasses the entire scope of the system being described. Use input, control and output arrows entering and leaving the box to represent the data and object interfaces of the system to its environment.

#### B.2.2 Drawing an IDEF0 Diagram

Diagram creation is the most subjective and creative activity of the modeling process. The steps presented here are a proven sequence and are designed to assist a new author in drawing IDEF0 diagrams.

a. Create a relevant, but not yet structured list of data.
b. Name functions that act on the listed data and draw boxes around the names.
c. Sketch appropriate arrows. As each box is drawn, leave arrow "stubs" to make the box more meaningful.
d. Draft a layout that presents the clearest box and arrow arrangement. Bundle arrows together if the structure is too detailed.
e. Create text, glossary and FEO diagrams, if necessary, to highlight aspects which are important.

##### B.2.2.1 Generating Function Boxes

Function boxes are generated using the major sub-functions of the parent. The number of boxes can be modified by clustering (grouping two or more boxes) and splitting (breaking a single box into parts) to conform to the three-to-six-box rule.

**Boxes**
1.  In most cases, lay out boxes diagonally from upper left to lower right.
2.  Boxes placed in the upper left "dominate" boxes placed lower and to the right through the control arrows that link them.
3.  Number each box in its lower right inside corner. The last digit of the node number is this box number.

    figure_number: "Figure B10. Box Number and Node Number"
    description: "A diagram of a single function box. The box has a 'Name' inside. In the lower right corner, inside the box, is the number '2'. Below the lower right corner, outside the box, is the node number 'A42', indicating this is box 2 on diagram A4."

4.  On working or draft copies, write the node number or C-number below the lower right corner of any box that is detailed.
5.  No diagram may contain more than six boxes.

##### B.2.2.2 Creating Interface Arrows

Sketch interface arrows connecting to each individual box. Connect ends of arrows to show which outputs supply which inputs and controls.

* Recall that input data/objects are transformed by the function to produce the output.
* If an arrow contains both input and control data/objects, show it as a control.
* Bundle groups of related arrows whenever possible. The level of detail of arrows should match the level of detail of boxes.
* Think control and constraint, not flow. Make the diagram structure show relationships that must be true no matter which sequence is followed.
* Label carefully. Don't clutter your diagrams with too much information.
* Leave out questionable arrows. If there is any doubt whether an arrow is needed, leave it out. Later detailing will demonstrate whether or not the arrow is really needed.

##### B.2.2.3 Level of Effort

The initial goal in generating a diagram should be a clear diagram that represents a definite message and does not violate any syntax rules. Reworking of diagrams will always be a necessary part of the process. The key idea is to use a review cycle to make progress on paper. IDEF0 is a thought-forming methodology, not just a diagram-making exercise.

#### B.2.3 Re-Drawing an IDEF0 Diagram

##### B.2.3.1 Modifying Boxes

When first creating a diagram, 3-6 function boxes of approximately the same level of detail are derived. Clustering and splitting will provide a boundary which is more easily understood or which will provide a simpler interaction between the function boxes. Most often, clustering and splitting work together. Boxes are split and the resulting pieces clustered into new boxes which more closely convey the intended message.

##### B.2.3.2 Bundling Arrows

Both arrows and boxes should be at a corresponding level of abstraction in a diagram. There are two basic ways to achieve this:
1.  Bundle arrows with the same source and destination under a single more general label, and make one arrow.
2.  Rename some boxes (using Split and Cluster) to better distribute the sub-functions and re-label resulting arrows.

It is always true that an excess of arrows is bad if the message is obscured. The ability of readers to understand what is being said should guide the number of arrows used.

##### B.2.3.3 Proposing Modifications to the Context

The detailed understanding revealed by creating a new diagram may uncover errors or oversights in the parent diagram. Parent modification is a natural and anticipated event. When the rule is "if there is any doubt whether an arrow is needed by a function box, leave it out," this is the point where such questions are resolved. Parent diagram changes may present various degrees of difficulty. When proposing a change, think it through carefully and assess its complexity.

##### B.2.3.4 ICOM Syntax for Connecting Diagrams

An important aspect of understanding diagrams is the ability to find and understand facts that are needed. Node numbers show the structure of the function decomposition (box detailing). The arrow network provides interface connections. ICOM codes are written on all arrows having one end unconnected on the diagram. These boundary arrows connect the arrow network across diagrams. Each boundary arrow is labeled with an ICOM code to specify the connection of the arrow to the parent box.

#### B.2.4 Graphic Layout

Lay out the boxes diagonally according to the constraint structure, from the upper left to lower right. Control feedbacks go up and left, and input feedback arrows go down and left. Draw all boundary arrows shown on the parent diagram and then add the remaining arrows.

##### B.2.4.1 Constraints on the Diagram

1.  Function boxes shall always have control arrows, though they need not always have inputs.
2.  When an entry arrow serves both control and input functions, show it as control.
3.  In general, do not split an arrow into both a control and an input to the same box.
4.  Iterated activity (memory storage or feedback) may be shown with an output arrow looping back to become an input or control for the same box.
5.  Try to avoid redundancies where the box name merely repeats the message conveyed by the arrows (e.g., a box named "MAKE X" with an output arrow labeled "X").

##### B.2.4.2 Arrow Placement

1.  Draw arrows along horizontal and vertical lines, not diagonally or as curves (except at corners).
2.  Place arrow corners, crossings and labels a reasonable distance away from boxes.
3.  Don't use the keywords, i.e., "data", "function", "input", "output", "control" or "mechanism" in names or labels, unless absolutely necessary.
4.  If an arrow is long, label it twice.
5.  Place ICOM codes at the unconnected ends of arrows.
6.  Connect open-ended boundary arrows to show all the places affected.
7.  Space parallel arrows adequately.

#### B.2.5 Writing Text

##### B.2.5.1 Text and Glossary

The text that may accompany each diagram presents a brief integrating overview of the diagram, citing important relations, patterns, or subtle interactions between the boxes and arrows. It highlights features that the author feels are of special interest or significance. It does not duplicate every detail shown on the diagram itself.

Write the text only after a diagram has received a fairly high level of review and approval. Waiting to write the text forces the diagram itself to properly communicate the intended message.

Use glossary definitions to summarize the special meanings that may arise for key terms, words, phrases and acronyms used in the diagram.

##### B.2.5.2 Notes and References

There are two kinds of notes, model notes and reader notes. Model notes are part of the diagram on which they appear. In sharp contrast, reader notes explicitly are on the diagram, not part of the diagram. Reader notes are strictly informative, not normative, and may be about the modeled subject matter or about its modeled presentation.

A standard notation is used in writing text and notes to refer to diagrams and specific parts of diagrams. References are based on box numbers, ICOM codes, node numbers, and note numbers.

### B.3 Data Collection for IDEF Modeling

#### B.3.1 Introduction

When analyzing or designing any system, it may be necessary to obtain or verify facts about the system or subject matter at hand. There are many sources of factual information. One might do the following:
* Read existing documents.
* Observe the system in operation.
* Survey a large group of people.
* Talk to one or more experts.
* Use whatever is already known by the author.
* Guess or invent a hypothetical description, and ask readers to help bring it closer to reality.

Of all these methods, the most important is face-to-face interaction with an expert.

#### B.3.2 The Interview Process

The purpose of an interview is to gather information from an individual who possesses an expertise considered important to the analytical effort. There are four types of interviews that might be conducted:
(a) Fact Finding for understanding current operations.
(b) Problem Identification to assist in the establishment of future requirements.
(c) Solution Discussion regarding future system capabilities.
(d) IDEF Author/Reader Talk Session to resolve problems.

By constantly classifying the respondents' remarks, the interviewer can better appreciate the expert's point of view.

#### B.3.3 The Interview Kit

A "standard" interview kit can be used for recording the interview. It may be stored in an interview file and distributed to appropriate project individuals. The interview kit would contain:
1.  Cover Page (Kit cover)
2.  Interview and Record Follow-up
    (a) Interviewer Name
    (b) Interview Date
    (c) Interview Duration
    (d) Respondent Name
    (e) Respondent Title and Organizational Responsibility
    (f) Respondent Telephone Number
    (g) Additional Sources of Information Identified
    (h) Essential Elements of Information—A Summary
    (i) Follow-up questions
    (j) New Terms for Project Glossary
3.  Activity and Data/Objects List
4.  Interview Agenda
5.  Interview Notes and Rough Diagrams

## ANNEX C - REVIEW CYCLE PROCEDURES AND FORMS

### C.1 IDEF Teamwork Discipline

The development of any IDEF model is a dynamic process which requires the participation of more than one person. Throughout a project, the draft portions of a model are created by authors and distributed to others (project members, experts in the subject matter, management, etc.) for review and comment. These draft portions of a model are called Kits.

The IDEF teamwork discipline identifies all persons interested in the review of a model as reviewers. Reviewers who are assigned to make a written critique of a Kit are called commenters. Reviewers who receive a Kit for information only are not expected to make written comments and are called readers. The author and the commenters share responsibility for the quality of the model.

The discipline requires that each person expected to make comments about a Kit shall make them in writing using reader notes and submit them to the author of the Kit. The author responds to each note in writing. This cycle continues until the model is complete and recommended for publication.

### C.2 The IDEF Kit Cycle

In creating a document, materials written or gathered by an author are distributed, in the form of a Standard Kit, to commenters, reviewers and other readers. Commenters review the material and write comments about it. The commenters return the Kit to the author who reacts to comments and may use the comments to revise or expand the material. This is known as a Kit Cycle.

    figure_number: "Figure C1. Kit Cycle"
    description: "A flowchart illustrating the IDEF Kit Cycle between an Author, a Library, and a Commenter. The Author produces a new kit and sends a control copy to the Library. The Library sends the kit to the Commenter. The Commenter writes comments on the kit and returns the commented kit to the Author. The Author writes reactions to the comments. A discussion may occur between the Author and Commenter. The author sends the kit with reactions back to the Commenter for filing, and files a control copy in the Library."

The steps of the Kit Cycle are as follows:
* The author assembles the material to be reviewed into a Standard Kit.
* Within the response time specified, the commenter reads the kit and writes comments directly on the copy.
* The author responds in writing directly on each commenter's copy.
* The reader reads the author’s responses and, if satisfied, files the kit. If an assigned commenter does not agree, a meeting is arranged.

#### C.2.1 Personnel Roles
The roles and functions of people involved are:
* **Authors (Analysts)**: People who prepare any IDEF model.
* **Commenters (Experts or other Authors)**: People assigned to make a written critique of a kit.
* **Readers (Experts or anyone who wishes to be on the reader list)**: People who review documents for information but are not expected to make written comments.
* **Librarian**: A person assigned the responsibility of maintaining a file of documents, making copies, distributing kits and keeping records.

##### C.2.1.1 Author
An author interviews experts, analyzes the information, organizes it into diagrams and creates models.

##### C.2.1.2 Commenter
Assigned commenters read material produced by an author and verify its technical accuracy. They are responsible for finding errors and suggesting improvements.

#### C.2.2 Guidelines for Authors and Readers and Commenters
Overall guidelines for commenting are:
* Make notes brief, thorough and specific.
* Use the reader notes notation to identify comments.
* Make constructive criticisms.
* Take time to gather overall comments.

##### C.2.2.3 Meeting Guidelines
When a meeting is required, the procedure is as follows:
1. Each meeting should be limited in length.
2. Each session must start with a specific agenda.
3. Each session should terminate when productivity has dropped.
4. Each session must end with an agreed list of action items.

### C.3 IDEF Kits

A Kit is a technical document. It may contain diagrams, text, glossaries, decision summaries, background information or anything packaged for review and comment. An appropriate cover sheet distinguishes the material as a kit. There are two types of IDEF Kits:

* **Standard Kit**: To be distributed for comment. It is considered a “working paper” to assist the author in refining his total model.
* **Update Kit**: Contains the latest version of a model. It is sent for information only and is designed to aid in maintaining current information about the total model.

Standard Kits contain portions of a model and are submitted frequently as work progresses. Update Kits are submitted at regular intervals and contain the latest version of the model.

#### C.3.1 Completing a Kit Cover Sheet

An appropriate cover sheet distinguishes the material as a kit. The cover sheet has fields for author, date, project, document number, title, status and notes.

    figure_number: "Figure C2. IDEF Kit Cover Sheet"
    description: "An example of a standard IDEF Kit Cover Sheet form. It includes sections for Project Information, Kit Information, a Review Cycle log with dates, a list of Reviewers, Copying Instructions, a Node Index/Table of Contents for the kit, and a comments/special instructions area."

#### C.3.2 How to Prepare a Standard Kit

To

### C.4 Standard Diagram Form

The IDEF Diagram Form has minimum structure and constraints. It supports the functions important to the discipline of structured analysis: establishment of context, cross-referencing, and notes. The form is divided into three major sections:
* Working Information (top)
* Message Field (center)
* Identification Fields (bottom)

    figure_number: "Figure C4. Standard Diagram Form"
    description: "An example of a blank standard IDEF Diagram Form. The top 'Working Information' section includes fields for Author, Date, Project, Reader Notes, Status, and Reader/Date. The large central 'Message' field is for the diagram itself. The bottom 'Identification Fields' section includes fields for Used At, Context, Node, Title, and Number."

#### C.4.1 Working Information

##### C.4.1.1 The “Author/Date/Project” Field
This tells who originally created the diagram, the date that it was first drawn and the project title under which it was created.

##### C.4.1.2 The "Reader Notes" Field
This provides a check-off for reader notes written on the diagram sheet. As a comment is made on a page, the corresponding note number is crossed out.

##### C.4.1.3 The “Status” Field
The status classifications indicate stages of approval. They are:
* **WORKING**: The diagram is a major change, restarts the approval sequence.
* **DRAFT**: The diagram is a minor change and has reached some agreed-upon level of acceptance.
* **RECOMMENDED**: Both this diagram and its supporting text have been reviewed and approved by a technical committee.
* **PUBLICATION**: This page may be forwarded as is for final printing and publication.

##### C.4.1.4 The “Reader/Date” Field
This area is where a reader should initial and date each form.

##### C.4.1.5 The “Context” Field
A sketch of only the box layout of the parent diagram, with the parent box highlighted. The parent diagram’s node number is written in the lower left of the Context Field.

    figure_number: "Figure C5. Illustration of context field"
    description: "An example of the 'Context' field from the diagram form. It shows a small sketch of a four-box diagram, with the fourth box highlighted. The node number 'A32' is written below the sketch, and the box number '4' is written inside the highlighted box."

##### C.4.1.6 The “Used At” Field
This is a list of diagrams, other than the parent context, which use or reference this diagram-form page in some way, often for Call Arrow support.

#### C.4.2 The “Message” Field
The Message field contains the primary message to be conveyed. The field is normally used for diagramming with an IDEF graphical language, but can be used for any purpose: glossary, checklists, notes, sketches, etc.

#### C.4.3 The “Node” Field
This field contains the complete node reference for the sheet (including model name, slash, Node Number, and optional suffix like “F” for FEO).

#### C.4.4 The “Title” Field
The Title field contains the name of the material presented. If the Message field contains a diagram, then the contents of the Title field must precisely match the name written in the parent box.

#### C.4.5 The “Number” Field
The large area contains the C-number, a unique ID composed of the author’s initials and a sequential number. The small rectangle area at the right is for a kit page number, written by the librarian.

### C.5 Keeping Files

Each officially-assigned participant in a project shall maintain Reader/Author files of the documents received. The librarian shall maintain the official Master and Reference files of the project, archiving each kit submitted during the course of the project. Variations in the filing process may occur based on individual preferences, but the following files, maintained in alphabetically-sorted reference number order, are the minimum:

* **Standard Kit Files**: Maintained by authors, commenters and perhaps other readers.
* **Updated Current Model Files**: Maintained by authors, commenters and readers from Update Kits that are received.
* **Working Files**: Maintained by authors—and any Reader who initiates any ad hoc interchange between participants.
* **Project Files**: Maintained by the librarian to standards set by the project management.

### C.6 The IDEF Model Walk-Through Procedure

In addition to the Kit Cycle, a Walk-Through Procedure has been developed as a guide for presenting model information to a group of “reviewers”. It does not substitute for the Reader/Author Cycle review process.

1.  **Present the model to be analyzed by using its node index.** This provides a quick overview of what is to come.
2.  **Present selected glossary terms.** Encourage each reviewer to replace personal meanings of words with those that the presenting team has chosen.
3.  **Present each diagram for review.** The diagram walk-through process is an orderly, step-by-step process where questions can be asked. Six steps of a structured walk-through follow below.

**Step 1: Scan the diagram.**
This step allows the reader to obtain general impressions about the content of the diagram.
*Criteria for acceptance:*
1.  The decomposition is useful for its purpose and is complete within the context of its parent box.
2.  The diagram reflects a relevant point of view based on the purpose of the model.
3.  There is enough new information provided to extend understanding of the parent box, but not so much detail that the diagram appears complex.

**Step 2: Look at the parent.**
Once the reader understands the current diagram’s decomposition, the parent diagram should be reviewed to insure compatibility.
*Criteria for acceptance:*
1.  The decomposition covers all of the points the reviewer anticipated when reading the parent diagram.
2.  The detail which the reviewer envisioned for this box should still seem correct.

**Step 3: Connect the parent box and the detail diagram.**
This step tests the arrow interface connections from the parent to

## ANNEX D - Informative Definitions

This section contains definitions which relate to the informative annexes of this document. See Section 2 for definitions for the normative sections.

* **D.1 Approval Level**: One of the following four words assigned to an IDEF model to indicate its relative degree of review and approval: Working, Draft, Recommended, Publication.
* **D.2 Author**: The person who prepares and is responsible for any specific IDEF model or diagram.
* **D.3 Clustering**: The grouping of two or more boxes to form a single box. Its goal is to combine multiple functions into a single more general function.
* **D.4 Commenter**: An assigned reader who shares responsibility with the author for the quality of an IDEF kit, model, diagram or other IDEF result.
* **D.5 Draft**: See approval level.
* **D.6 Expert**: A person familiar with a part of the real world system (or subject) being modeled.
* **D.7 IDEF Role**: A position in an IDEF project. See author, expert, commenter, reader and librarian.
* **D.8 Kit**: A standardized package of diagrams containing portions of or complete-to-date models to be reviewed.
* **D.9 Kit Cover Sheet**: A special form used to control the routing of a kit through a kit cycle.
* **D.10 Kit Cycle**: A formal Reader/Author Cycle procedure which uses kits for obtaining peer or expert review during model development.
* **D.11 Librarian**: The person responsible for routing and tracking of kits and keeping orderly project files and archives.
* **D.12 Project Field**: The field on the IDEF diagram form which records the name of the organized task for which an IDEF model is prepared.
* **D.13 Publication**: See approval level.
* **D.14 Reader**: A person with (limited) training in an IDEF technique, sufficient to accurately interpret syntax and basic meanings.
* **D.15 Reader/Author Cycle**: A procedure using reader notes for obtaining peer or expert review during model development.
* **D.16 Reader Note**: A textual comment by