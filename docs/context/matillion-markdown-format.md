## Matillion Markdown Formatting Guide

This section provides a detailed guide for formatting documents according to the Matillion standard.

### Text Styling

* **Bold:** Use double asterisks (`**text**`) to highlight clickable UI elements and menu names.
    * Example: Click **Admin** → **User Configuration**.
* **Italics:** Use single underscores (`_text_`) for emphasis. Do not use single asterisks.
* **Underline:** Do not use underlining.

### User Input and Code

* **User Input Text:** For text that a user needs to type, use straight double quotes.
    * Example: In the search bar, type "amplitude" and press ENTER.
* **Inline Code and Technical Terms:** Use single backticks (`` ` ``) for inline code, filenames, file paths, class/method names, and console output.
    * Example: The main application is `DAB_4.0.py`.
* **Code Blocks:** Use triple backticks (```` ````) for multi-line, copyable code blocks.
    * Specify the language immediately after the opening backticks (e.g., ` ```python`).
    * Use four spaces for indentation.
    * Wrap lines at 80-100 characters for readability.

### Structure and Content

* **Component Parameters:** Document component parameters using the following structure:
    ```
    `PARAMETER-NAME` = _PARAMETER-TYPE_
    PARAMETER-DESCRIPTION
    ***
    ```
    * Example:
        `Name` = _string_
        A human-readable name for the component.
        ***
* **Ampersand:** Use "and" instead of the ampersand symbol (`&`) unless it is part of a literal UI element or menu name.
* **Blockquotes:** Use blockquotes (`> text`) only for direct quotes from external sources. The quoted text should also be italicized.
    * Example:
        To directly quote "Working with Warehouses" from docs.snowflake.com:
        > _If you choose "Started", the warehouse starts consuming credits once all the compute resources are provisioned for the warehouse._
* **End of Page:** Ensure the document ends with a single blank newline.

---

