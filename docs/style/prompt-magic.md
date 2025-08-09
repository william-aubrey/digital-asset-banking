# Word Magic

This document contains a collection of "magic prompts" designed to elicit specific, structured, and near-deterministic responses from Gemini Code Assist. Each recipe is designed to solve a common task.

---

## 1. Markdown conversation

Please provide the complete raw markdown source of our conversation. Format the entire output as a single indented code block by prefixing every line with four spaces. This should prevent the chat window from rendering any markdown within it.



## 2. Markdown upcoming response

Please provide your response in the form of the complete raw markdown source of my prompt and your response. Format the entire output as a single indented code block by prefixing every line with four spaces. This should prevent the chat window from rendering any markdown within it.

Create a new file located at this file path G:\My Drive\A0 WRA\Digital Assets\Banking\digital-asset-banking\docs\sessions.  The file naming convention is YYYY-MM-DD-HHMM-gemini-chat.md. The date is [YYYY-MM-DD-HHMM].

Copy the contents from your output into this file and save the file.


## 3. Markdown last response

Please provide the complete raw markdown source of my last prompt and your last response. Format the entire output as a single indented code block by prefixing every line with four spaces. This should prevent the chat window from rendering any markdown within it.

Create a new file located at this file path G:\My Drive\A0 WRA\Digital Assets\Banking\digital-asset-banking\docs\sessions.  The file naming convention is YYYY-MM-DD-HHMM-gemini-chat.md. The date is [YYYY-MM-DD-HHMM].

Copy the contents from your output into this file and save the file.



## A. TERMINAL PROMPTS
.venv\scripts\activate

streamlit run main.py



---

## APPENDICES

---
Appendix 1
Author: Gemini Code Assist
Date: 2025-08-08-1833

---

# My Prompt Engineering Playbook

This document contains a collection of "magic prompts" designed to elicit specific, structured, and near-deterministic responses from Gemini Code Assist. Each recipe is designed to solve a common task.

---

## 1. Knowledge Capture & Formatting

### 1.1. Get Raw Markdown Source of a Conversation

*   **Goal:** To get the complete, raw, un-rendered markdown source of our conversation, suitable for logging.
*   **Challenge:** The chat UI often tries to render nested code blocks, breaking the output into multiple sections.
*   **The "Magic" Prompt:**
    ```
    Please provide the complete raw markdown source of our conversation. Format the entire output as a single indented code block by prefixing every line with four spaces. This should prevent the chat window from rendering any markdown within it.
    ```
*   **Expected Output:** A single, pre-formatted code block containing the entire markdown source, which can be copied with a single click.

---

## 2. Workflow Automation

### 2.1. Create a VS Code Task

*   **Goal:** To generate a complete, cross-platform `tasks.json` file for a specific workflow.
*   **Context to Provide:**
    *   A clear description of the workflow (e.g., "Save clipboard to a new timestamped file and open it").
    *   Any platform-specific tools required (e.g., `xclip` on Linux).
*   **The "Magic" Prompt:**
    ```
    I need to create a VS Code task to automate a workflow.

    **Workflow Description:** {{DESCRIPTION_OF_WORKFLOW}}

    Please provide a complete `tasks.json` file that accomplishes this. The task should:
    1. Be cross-platform (support Windows, macOS, and Linux).
    2. Use a `promptString` input to ask for a filename, with a timestamped default value (e.g., `YYYY-MM-DD-HHMM-my-file.md`).
    3. Execute the necessary shell commands to perform the action.
    4. Open the resulting file in VS Code.
    5. Include comments explaining what each part of the command does.
    ```
*   **Expected Output:** A single JSON code block containing a valid `tasks.json` structure.

---

## 3. Code Evaluation & Troubleshooting

### 3.1. Analyze a Shell Error

*   **Goal:** To understand a command-line error and get a specific solution.
*   **Context to Provide:** The full, unedited error message from the terminal.
*   **The "Magic" Prompt:**
    ```
    Please help me evaluate this error I'm seeing in my terminal.

    **Error Output:**
    ```
    {{PASTE_FULL_ERROR_HERE}}
    ```

    Please provide an answer with the following structure:
    1.  **Analysis of the Errors:** A breakdown of each error message and why it's happening.
    2.  **The Root Cause:** A clear, concise explanation of the primary problem.
    3.  **The Solution:** The exact, corrected command or code block to fix the issue.
    ```
*   **Expected Output:** A markdown response with three specific H3 headings: "Analysis of the Errors", "The Root Cause", and "The Solution", each with detailed explanations.

---

## 4. Code Generation & Refactoring

### 4.1. Generate Code with Design Constraints

*   **Goal:** To generate or refactor code that must adhere to specific, non-obvious design principles (like IDEF0).
*   **Challenge:** The AI needs to be explicitly reminded of the design constraints during each request to ensure compliance.
*   **The "Magic" Prompt:**
    ```
    <OBJECTIVE>
    {{Briefly describe the goal, e.g., "Refactor the purchase_asset function."}}
    </OBJECTIVE>

    <GUIDING_PRINCIPLES>
    - **IDEF0 Hierarchy:** All functions must be designed so they can be mapped to a hierarchical representation in IDEF0 language. Functions should be named with active verbs and represent a clear, decomposable action.
    - **[Other Principle]:** {{Add any other principles as needed.}}
    </GUIDING_PRINCIPLES>

    <REQUEST>
    {{Your specific request, e.g., "Please refactor the following function..."}}
    </REQUEST>
    ```
*   **Expected Output:** Code that not only fulfills the request but is also explicitly designed and evaluated against the stated principles.
*   **Expected Output:** A markdown response with three specific H3 headings: "Analysis of the Errors", "The Root Cause", and "The Solution", each with detailed explanations.
