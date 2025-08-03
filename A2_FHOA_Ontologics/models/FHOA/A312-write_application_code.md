# FHOA Heuristics (A3.1.2) Process Model: Write Application Code

This document provides the IDEF0-style decomposition for the **A3.1.2: Write Application Code** function. Its purpose is to detail the collaborative sub-processes between a human developer and an AI assistant to produce source code.

---

## A3.1.2: Write Application Code (Top-Level Function)

- **Purpose**: To implement the features described in the technical design by writing source code.
- **Inputs**: `Technical Design Document` (from A3.1.1)
- **Controls**: `Programming Language Standards`, `Project Coding Conventions`
- **Outputs**: `Draft Application Source Code` (to A3.1.3)
- **Mechanisms**: `Software Developer`, `AI Assistant (Gemini)`, `VS Code IDE`

---

## A3.1.2 Decomposition: The Human-AI Collaborative Coding Loop

The A3.1.2 function is decomposed into four activities that model the interactive workflow between a developer and an AI coding assistant.

### A3.1.2.1: Activate Agent(s)

- **Purpose**: To initialize a collaborative coding session by defining the immediate goal and providing necessary context to the AI assistant.
- **Inputs**: `Technical Design Document` (from A3.1.1), `Developer's Immediate Goal`
- **Controls**: `Best Practices for AI Prompts`, `Relevant Source Code Files`
- **Outputs**: `Session Goal & Context`, `Active Coding Environment`
- **Mechanisms**: `Software Developer`, `AI Assistant (Gemini)`, `VS Code IDE`

### A3.1.2.2: Generate Code Snippets

- **Purpose**: To produce functional code segments based on the developer's specific prompts and the established context.
- **Inputs**: `Session Goal & Context` (from A3.1.2.1), `Developer Prompts`
- **Controls**: `Programming Language Standards`, `Known Code Examples`
- **Outputs**: `Generated Code Snippets`, `Explanations & Alternatives`
- **Mechanisms**: `AI Assistant (Gemini)`

### A3.1.2.3: Integrate & Refactor Code

- **Purpose**: To weave the generated code into the existing codebase, ensuring it is clean, efficient, and adheres to the project's architecture.
- **Inputs**: `Generated Code Snippets` (from A3.1.2.2), `Existing Application Codebase`
- **Controls**: `Architectural Specifications`, `Developer Experience & Knowledge`
- **Outputs**: `Integrated Draft Code`
- **Mechanisms**: `Software Developer`, `VS Code IDE`

### A3.1.2.4: Review & Finalize Code

- **Purpose**: To perform a final quality check on the integrated code before it is considered ready for testing.
- **Inputs**: `Integrated Draft Code` (from A3.1.2.3)
- **Controls**: `Project Coding Conventions`, `Definition of "Done"`
- **Outputs**: `Draft Application Source Code` (to A3.1.3)
- **Mechanisms**: `Software Developer`, `AI Assistant (Gemini)`

---