# Design: Snowflake Semantic View

This document explains the purpose, structure, and benefits of the `VW_DAB_SEMANTIC` view, which serves as the primary interface for all business intelligence and analytics.

---

## 1. Purpose of a Semantic View

A semantic view provides a logical layer over the physical data model, exposing data in business-friendly terms with pre-defined relationships, dimensions, and metrics. This approach solves several key problems:
* **Simplicity**: Analysts don't need to write complex `JOIN` statements across the star schema. They can query one logical view.
* **Consistency**: Business logic (like how to calculate "total credits spent") is defined once in the view, ensuring everyone uses the same calculations.
* **Security**: The view can be used to hide or abstract sensitive columns from the underlying tables.

---

## 2. The `VW_DAB_SEMANTIC` View

Our semantic view is the single source of truth for answering business questions. It is composed of two main types of fields:

* **Dimensions**: These are descriptive attributes used for filtering, grouping, and slicing the data. Our primary dimensions are:
    * `asset_name`
    * `asset_type`
    * `graph_role`
    * `transaction_type`
    * `transaction_time`
    * `user_id`

* **Measures**: These are the quantifiable, numeric values that you aggregate. Our primary measures are:
    * `total_credits_spent`
    * `transaction_count`

---

## 3. Example Use Cases

An analyst can now answer complex questions with simple queries against the view:

**"What were the total credits spent by asset type last month?"**
```sql
SELECT 
    asset_type,
    SUM(total_credits_spent)
FROM VW_DAB_SEMANTIC
WHERE transaction_time >= DATEADD(month, -1, CURRENT_DATE())
GROUP BY 1;
```

**"How many assets were purchased yesterday?"**
```sql
SELECT
    SUM(transaction_count)
FROM VW_DAB_SEMANTIC
WHERE transaction_type = 'PURCHASE'
  AND transaction_time >= DATEADD(day, -1, CURRENT_DATE());
```