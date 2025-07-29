## AI Agent Session Logging Standard

This appendix provides a standardized template and guide for capturing metadata from collaborative sessions with AI agents. The goal is to create a consistent, comparable record of work for project management and analysis.

### 1. Session Log YAML Template

At the end of a session, request the AI agent to populate the following YAML template.

```yaml
session_name: "A brief, descriptive name for the session's goal"
agent_model: "The specific model used (e.g., Gemini, Claude Sonnet 4, ChatGPT o4-mini)"
session_id: "A unique identifier for the session"
session_type: "Primary category of work (e.g., Prototyping, Debugging, Infrastructure, Design)"
agent_activation: "Subjective rating (High, Medium, Low) and description of the human-AI synergy"
session_value_proposition: "A concise summary of the tangible and intangible value created"
started_at: "YYYY-MM-DDTHH:MM:SSZ"
last_updated: "YYYY-MM-DDTHH:MM:SSZ"
duration_minutes: 0
messages_exchanged: 0
canvases_created: 0
context_token_limit: 0 # Agent's maximum context window
current_context_tokens: 0 # Estimated tokens used in the session
hit_context_limit: false
key_accomplishments:
  - "Bulleted list of major achievements"
files_generated:
  - "List of all new files created (code, config, narrative, etc.)"
files_modified:
  - "List of existing files that were updated"
# --- Agent-Specific Extensions (Example for a data pipeline agent) ---
# pipelines_executed:
#   - "pipeline_name.orch.yaml": "SUCCESS"
# data_objects_created:
#   - "DATABASE.SCHEMA.TABLE (table)"
```

### 2. Field Descriptions

* **`session_name`**: A human-readable title for the work session (e.g., "S3 Debugging").
* **`agent_model`**: The specific version of the AI model used.
* **`session_id`**: A unique, machine-readable ID, often combining the project name, date, and task.
* **`session_type`**: The main category of the task performed.
* **`agent_activation`**: A qualitative measure of the collaboration's effectiveness.
* **`session_value_proposition`**: The "so what?" of the session. What business or project value was delivered?
* **`started_at` / `last_updated`**: Timestamps in ISO 8601 format (UTC/Zulu time).
* **`duration_minutes`**: Total active time of the session.
* **`messages_exchanged`**: The total number of user prompts and agent responses.
* **`canvases_created`**: The number of distinct documents or major artifacts generated.
* **`context_token_*`**: Metrics related to the agent's context window usage.
* **`key_accomplishments`**: A high-level summary of what was achieved.
* **`files_generated` / `files_modified`**: A complete list of all file artifacts produced or changed during the session.
* **Agent-Specific Extensions**: The template can be extended with fields specific to the agent's capabilities (e.g., `pipelines_executed` for a data orchestration agent).

### 3. Generation Prompt

To generate this log, use a prompt similar to the following at the conclusion of a session:

> "Please generate a complete session metadata log for our conversation. Use the standard project YAML template to capture all relevant quantitative and qualitative metrics, including session type, agent activation, value proposition, and a full list of all files generated or modified."

