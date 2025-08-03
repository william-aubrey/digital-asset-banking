# ETL Loading Logic for Digital Asset Banking

This document outlines the step-by-step ETL (Extract, Transform, Load) processes for populating the Snowflake data warehouse. These processes are designed to be triggered by actions within the main `dab.py` application.

---

## 1. On Asset Upload

This process is triggered when a user successfully uploads a file through the application's `upload_asset` function. The application will pass the asset's metadata (S3 key, name, asset type name, and upload timestamp) to this ETL workflow.

* **1. Check if Asset Type Exists**: The process first checks the `DIM_ASSET_TYPES` table to see if a record for the given `ASSET_TYPE_NAME` already exists.
    * If it does not exist, a new record is inserted into `DIM_ASSET_TYPES`, and the newly generated `ASSET_TYPE_SK` is retrieved.
    * If it already exists, the existing `ASSET_TYPE_SK` is retrieved.
   

* **2. Insert into `DIM_ASSETS`**: A new record is inserted into the `DIM_ASSETS` table with the asset's core metadata, including the `S3_KEY`, `ASSET_NAME`, the `ASSET_TYPE_SK` retrieved in the previous step, and the `UPLOAD_TIMESTAMP`. The `CURRENT_OWNER_USER_SK` is initially set to `NULL`.

* **3. Insert into `FCT_ASSET_TRANSACTIONS`**: After the asset is successfully inserted into the dimension table, its new `ASSET_SK` is retrieved. A corresponding record is then inserted into the `FCT_ASSET_TRANSACTIONS` table with the following values:
    * `TRANSACTION_TYPE`: 'UPLOAD'
    * `BUYER_USER_SK`: `NULL`
    * `CREDITS_SPENT`: `NULL`
   

---

## 2. On Asset Purchase

This process is triggered when a user executes the `purchase_asset` function in the application. The application will pass the asset's `S3_KEY`, the buyer's user ID (`USER_NK`), the credits spent, and the transaction timestamp to this workflow.

* **1. Check if User Exists**: The process first checks the `DIM_USERS` table to see if a record for the given `USER_NK` (the buyer's ID) already exists.
    * If it does not exist, a new record is inserted into `DIM_USERS`, and the newly generated `USER_SK` is retrieved.
    * If it already exists, the existing `USER_SK` is retrieved.
   

* **2. Update `DIM_ASSETS` Owner**: The `DIM_ASSETS` table is updated to set the `CURRENT_OWNER_USER_SK` to the `USER_SK` of the buyer for the specified asset.

* **3. Insert into `FCT_ASSET_TRANSACTIONS`**: A new transaction record is inserted into the `FCT_ASSET_TRANSACTIONS` table with the following values:
    * `TRANSACTION_TYPE`: 'PURCHASE'
    * `BUYER_USER_SK`: The `USER_SK` of the buyer.
    * `CREDITS_SPENT`: The amount of credits spent on the purchase.
   

---

## 3. Application Integration

The `dab.py` application will need to be modified to trigger these ETL jobs instead of updating its in-memory list. This will likely involve making API calls to a Matillion endpoint or placing a message on an SQS queue that Matillion listens to, passing the necessary metadata for each event.