# Core Principles of IDEF0 (FIPS 183)

**Document Purpose**: This document is a concise distillation of the Integration Definition for Function Modeling (IDEF0) standard as specified in FIPS Publication 183. Its purpose is to provide a foundational context for agentic AIs on the core philosophy, components, and rules of the IDEF0 methodology in its pure form.

---

## 1. Guiding Philosophy

[cite_start]The primary objective of IDEF0 is to provide a standardized language for modeling the functions of a system or enterprise[cite: 39]. [cite_start]It is designed to be a "blueprint" that describes what a system does, what controls it, what it works on, what means it uses, and what it produces[cite: 278, 285]. The language is intended to be:

* [cite_start]**Comprehensive and Expressive**: Capable of graphically representing complex operations to any level of detail[cite: 125].
* [cite_start]**Simple and Coherent**: Providing for rigorous and precise expression while being easy to learn[cite: 126, 127].
* [cite_start]**A Communication Tool**: Enhancing communication and consensus between analysts, developers, and users[cite: 127].

---

## 2. The Building Blocks: Syntax and Semantics

[cite_start]An IDEF0 model is composed of two primary components: boxes and arrows, which are governed by a set of semantic rules[cite: 305, 306].

### **Boxes (Functions)**
[cite_start]A box is a rectangle used to represent a **function**, which is an activity, process, or transformation[cite: 199, 225].
* [cite_start]Every box must have a **name** written inside it, which must be an active verb or verb phrase (e.g., "Develop Model")[cite: 312, 407].
* [cite_start]Every box on a diagram has a **box number** (1-6) in its lower right corner for identification[cite: 202, 313].

### **Arrows (ICOMs)**
[cite_start]An arrow is a directed line that represents data or objects[cite: 192]. [cite_start]Arrows do not represent flow or sequence; they represent **constraints** that govern the function[cite: 324, 530]. [cite_start]The role of an arrow is defined by the side of the box it connects to[cite: 363]:

* [cite_start]**Input (Left Side)**: Represents the data or objects that are **transformed or consumed** by the function to produce outputs[cite: 193, 234, 364, 365].
* [cite_start]**Control (Top Side)**: Represents the conditions, rules, or standards that **govern the function** and are required for it to produce correct output[cite: 193, 214, 365, 366]. [cite_start]Every function box must have at least one control arrow[cite: 738].
* [cite_start]**Output (Right Side)**: Represents the data or objects **produced by the function**[cite: 193, 256, 367]. [cite_start]Every function box must have at least one output arrow[cite: 738].
* [cite_start]**Mechanism (Bottom Side)**: Represents the **means** (people, tools, systems) used to perform the function[cite: 193, 242, 368].

---

## 3. Managing Complexity: The Hierarchical Structure

[cite_start]IDEF0's primary method for managing complexity is through gradual, hierarchical decomposition[cite: 280, 1060].

* [cite_start]**Top-Level Context Diagram (A-0)**: Every model begins with a single box that represents the entire system or subject[cite: 435]. [cite_start]This A-0 diagram establishes the model's overall scope, purpose, and viewpoint[cite: 191, 440, 442].
* [cite_start]**Decomposition**: The core principle where a single **parent box** is detailed on a **child diagram**[cite: 217, 210]. [cite_start]The child diagram contains three to six boxes that represent the major sub-functions of the parent[cite: 730, 1091].
* [cite_start]**Bounded Context**: The child diagram is a direct, detailed view of the "inside" of its parent box[cite: 467]. [cite_start]Except for tunneled arrows, all boundary arrows on the child diagram **must correspond exactly** to the arrows that connect to its parent box[cite: 623, 1100].

---

## 4. Essential Rules and Notations

To maintain consistency and clarity, IDEF0 employs a set of strict rules and notations.

* [cite_start]**ICOM Codes**: A notation (e.g., `C1`, `I2`, `O1`) written next to a boundary arrow on a child diagram[cite: 651]. [cite_start]Its purpose is to explicitly state which corresponding arrow on the parent box it matches, ensuring traceability and **connection integrity** between layers[cite: 229, 649, 755].
* [cite_start]**Bundling/Unbundling**: The practice of combining multiple arrow meanings into a single, more general arrow on a high-level diagram (bundling) and separating it into distinct arrows on a lower-level diagram (unbundling)[cite: 204, 570].
* [cite_start]**Tunneling**: A notation using parentheses `( )` around the end of an arrow to control its visibility across the hierarchy[cite: 267, 679]. [cite_start]It is used to either hide a high-level arrow from its child diagram or hide a low-level arrow from its parent diagram to reduce clutter and improve clarity[cite: 677, 689].