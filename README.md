# ESP to BigQuery - Banking Transactions Loader

This project implements loading JSON data (banking transaction examples) into Google BigQuery.

## Prerequisites

- Google Cloud account with BigQuery enabled
- Service account key with BigQuery permissions
- Python 3.x

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root with your configuration:
   ```
   PROJECT_ID=your-project-id
   DATASET_ID=your-dataset-id
   TABLE_ID=your-table-id
   CREDENTIALS_PATH=path/to/your/service-account-key.json
   ```

3. Set up authentication:
   - Download your service account key JSON file.
   - Update the `CREDENTIALS_PATH` in `.env` with the path to your key file.
   - **Security Warning**: Avoid committing the `.env` file or key files to version control. Add them to `.gitignore`.

## Usage

1. Update the configuration in `.env` if needed (default table is 'transactions').

2. Run the script:
   ```
   python main.py
   ```

   The script will automatically create the table if it doesn't exist, and append new data each time it runs.

## Functions

- `get_esp_data()`: Placeholder for fetching data from ESP. Currently falls back to demo data. Implement this when ESP integration is ready.

## Reference

For building real-time dashboards in Looker Studio connected to BigQuery streaming tables, refer to: [How to Build Real-Time Dashboards in Looker Studio Connected to BigQuery Streaming Tables](https://oneuptime.com/blog/post/2026-02-17-how-to-build-real-time-dashboards-in-looker-studio-connected-to-bigquery-streaming-tables/view)
