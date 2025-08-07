# Digital Asset Banking - Improvement Backlog

This document serves as the technical backlog for the Digital Asset Banking (DAB) platform. It captures improvement insights, technical debt, and feature requests derived from various domains, including analytics, operations, and user feedback.

The goal is to maintain a clear, actionable list of tasks that can be prioritized for future development sprints.

---

## Backlog Item Template

Use this template to add new items to the backlog.

```markdown
### [ID] - [Title]

- **ID**: `BACKLOG-XXX`
- **Status**: New | In Progress | Done | Won't Do
- **Priority**: High | Medium | Low
- **Effort**: Small | Medium | Large
- **Source/Domain**: Analytics | Operations | User Feedback | Security
- **Date Created**: YYYY-MM-DD
- **Related Artifacts**:
  - [Link to relevant dashboard, query, or document]

**Description**:
(A clear and concise description of the problem or opportunity. What is the current state?)

**Hypothesis/Benefit**:
(What is the expected positive outcome of this change? How will it improve the platform, user experience, or business value?)
```

---

## Current Backlog

### BACKLOG-001 - Refactor Purchase Logic to Use Atomic Transactions

- **ID**: `BACKLOG-001`
- **Status**: New
- **Priority**: High
- **Effort**: Small
- **Source/Domain**: Operations / Code Quality
- **Date Created**: 2023-10-27
- **Related Artifacts**:
  - `heuristic/main.py` (the `purchase_asset` function)

**Description**:
The current `purchase_asset` function in `main.py` performs two separate SQL statements: an `UPDATE` on `DIM_ASSETS` and an `INSERT` into `FCT_ASSET_TRANSACTIONS`. If the second statement fails for any reason (e.g., transient network issue, constraint violation), the ownership of the asset will have been updated, but the transaction record will be missing. This leaves the data in an inconsistent state.

**Hypothesis/Benefit**:
By wrapping these two operations in a single database transaction (`BEGIN`, `COMMIT`, `ROLLBACK`), we can ensure atomicity. This guarantees that either both operations succeed or neither does, preventing data corruption and improving the reliability of the platform.

### BACKLOG-002 - Add Search and Filter to Asset Marketplace

- **ID**: `BACKLOG-002`
- **Status**: New
- **Priority**: Medium
- **Effort**: Medium
- **Source/Domain**: User Feedback / Analytics
- **Date Created**: 2023-10-27
- **Related Artifacts**:
  - `heuristic/main.py` (the "Asset Marketplace (Snowflake)" page)
  - `VW_DAB_SEMANTIC` (potential source for filterable fields)

**Description**:
The "Asset Marketplace" page currently displays the last 100 assets uploaded. As the number of assets grows, users will find it difficult to locate specific items. There is no way to search by `ASSET_NAME` or filter by `ASSET_TYPE`.

**Hypothesis/Benefit**:
Implementing search and filter controls (e.g., `st.text_input` for search, `st.multiselect` for `ASSET_TYPE`) will significantly improve the user experience. It will allow users to find assets more efficiently, which could lead to increased engagement and more purchase transactions. Analytics on search terms could also provide insights into user interests.

### BACKLOG-003 - Low Engagement with 'generic' Asset Type

- **ID**: `BACKLOG-003`
- **Status**: New
- **Priority**: Low
- **Effort**: Small
- **Source/Domain**: Analytics
- **Date Created**: 2023-10-27
- **Related Artifacts**:
  - Query on `VW_DDAB_SEMANTIC`: `SELECT ASSET_TYPE, COUNT(*) FROM VW_DAB_SEMANTIC WHERE TRANSACTION_TYPE = 'PURCHASE' GROUP BY 1;`

**Description**:
Analysis of the `VW_DAB_SEMANTIC` view shows that assets of type 'cyoa' are purchased 10x more frequently than assets of type 'generic'. This suggests that either the 'generic' assets are less appealing or they are not presented in an engaging way.

**Hypothesis/Benefit**:
By investigating the cause, we could increase the value derived from generic assets. A potential first step (Small effort) would be to add a more descriptive "details" page or a better thumbnail/preview for generic assets in the marketplace UI. This could increase their purchase rate and overall platform activity.