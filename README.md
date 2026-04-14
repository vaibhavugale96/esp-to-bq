# ESP to BigQuery - Event Streaming Loader

This project implements loading event data into Google BigQuery for real-time analytics and dashboards.

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

   The script will automatically create the table if it doesn't exist, and stream new event data each time it runs.

## Table Structure

The BigQuery table is created with the following schema and optimizations:

- **Schema**:
  - `event_id` (STRING, REQUIRED)
  - `event_type` (STRING, REQUIRED)
  - `user_id` (STRING)
  - `country` (STRING)
  - `event_timestamp` (TIMESTAMP, REQUIRED)

- **Partitioning**: By `event_timestamp` (daily partitions)
- **Clustering**: By `event_type` and `country` for efficient queries

## Functions

- `get_esp_data()`: Returns sample event data for testing. Replace with actual ESP data fetching logic when ready.

## Reference

For building real-time dashboards in Looker Studio connected to BigQuery streaming tables, refer to: [How to Build Real-Time Dashboards in Looker Studio Connected to BigQuery Streaming Tables](https://oneuptime.com/blog/post/2026-02-17-how-to-build-real-time-dashboards-in-looker-studio-connected-to-bigquery-streaming-tables/view)
