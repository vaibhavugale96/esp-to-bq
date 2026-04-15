# ESP to BigQuery - Event Streaming Loader

This project includes two pipelines:

- `main.py`: direct BigQuery streaming loader that inserts event data via the BigQuery API.
- `streaming_pipeline.py`: Pub/Sub-based real-time pipeline that publishes events to Pub/Sub and inserts them into BigQuery via a subscription.

## Current POC Architecture

🟡 CURRENT (POC you built)

Python Event Generator (Mock ESP)
        ↓
Pub/Sub Topic
        ↓
Python Subscriber (Callback Consumer)
        ↓
BigQuery Table

## Prerequisites

- Google Cloud account with BigQuery and Pub/Sub enabled
- Service account key with BigQuery and Pub/Sub permissions
- Python 3.x

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root with your configuration:
   ```dotenv
   PROJECT_ID=your-project-id
   DATASET_ID=your-dataset-id
   TABLE_ID=your-table-id
   TOPIC_ID=your-pubsub-topic-id
   SUBSCRIPTION_ID=your-subscription-id
   CREDENTIALS_PATH=path/to/your/service-account-key.json
   ```

3. Set up authentication:
   - Download your service account key JSON file.
   - Update `CREDENTIALS_PATH` in `.env` with the path to your key file.
   - **Security Warning**: Avoid committing `.env` or key files to version control. Add them to `.gitignore`.

4. Set up Pub/Sub and BigQuery subscription:
   - Create a Pub/Sub topic with the ID from `TOPIC_ID`.
   - Create a Pub/Sub subscription with the ID from `SUBSCRIPTION_ID`.
   - Configure the subscription to deliver messages to BigQuery, or use the local subscriber in `streaming_pipeline.py` to insert rows directly.

## Usage

### 1. Direct BigQuery streaming (`main.py`)

Run the direct API loader:
```bash
python main.py
```

This will create the target BigQuery table if needed and insert sample event rows directly.

### 2. Pub/Sub real-time pipeline (`streaming_pipeline.py`)

Run the streaming pipeline:
```bash
python streaming_pipeline.py
```

This script will:
- ensure the Pub/Sub topic exists
- ensure the Pub/Sub subscription exists
- publish events to the topic continuously
- listen on the subscription and insert received messages into BigQuery

## Table Structure

The BigQuery table is created with the following schema and optimizations:

- **Schema**:
  - `event_id` (STRING, REQUIRED)
  - `event_type` (STRING, REQUIRED)
  - `user_id` (STRING)
  - `session_id` (STRING)
  - `page_url` (STRING)
  - `referrer` (STRING)
  - `device_type` (STRING)
  - `country` (STRING)
  - `event_timestamp` (TIMESTAMP, REQUIRED)

- **Partitioning**: by `event_timestamp` (daily partitions)
- **Clustering**: by `event_type` and `country`

## Notes

- `main.py` is intended for direct event loading into BigQuery.
- `streaming_pipeline.py` is intended for real-time Pub/Sub ingestion and local subscription processing.
- Use `streaming_pipeline.py` when you want real-time event publishing every few seconds.

## Reference

For building real-time dashboards in Looker Studio connected to BigQuery streaming tables, refer to: [How to Build Real-Time Dashboards in Looker Studio Connected to BigQuery Streaming Tables](https://oneuptime.com/blog/post/2026-02-17-how-to-build-real-time-dashboards-in-looker-studio-connected-to-bigquery-streaming-tables/view)
