import os
import uuid
import datetime
from datetime import timezone
from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud.exceptions import NotFound
from dotenv import load_dotenv

# Load env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))


# Demo event data (simulate ESP)
def get_event_data():
    return [
        {
            "event_id": str(uuid.uuid4()),
            "event_type": "page_view",
            "user_id": "user_1",
            "session_id": "sess_101",
            "page_url": "/home",
            "referrer": "google.com",
            "device_type": "mobile",
            "country": "IN",
            "event_timestamp": datetime.datetime.now(timezone.utc).isoformat(),
        },
        {
            "event_id": str(uuid.uuid4()),
            "event_type": "click",
            "user_id": "user_2",
            "session_id": "sess_102",
            "page_url": "/pricing",
            "referrer": "direct",
            "device_type": "desktop",
            "country": "US",
            "event_timestamp": datetime.datetime.now(timezone.utc).isoformat(),
        }
    ]


def create_table_if_not_exists(client, dataset_id, table_id):
    table_ref = client.dataset(dataset_id).table(table_id)

    try:
        client.get_table(table_ref)
        print("✅ Table already exists.")
    except NotFound:
        print("⚠️ Table not found. Creating table...")

        schema = [
            bigquery.SchemaField("event_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("event_type", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("user_id", "STRING"),
            bigquery.SchemaField("session_id", "STRING"),
            bigquery.SchemaField("page_url", "STRING"),
            bigquery.SchemaField("referrer", "STRING"),
            bigquery.SchemaField("device_type", "STRING"),
            bigquery.SchemaField("country", "STRING"),
            bigquery.SchemaField("event_timestamp", "TIMESTAMP", mode="REQUIRED"),
        ]

        table = bigquery.Table(table_ref, schema=schema)

        # ✅ Partitioning
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="event_timestamp",
        )

        # ✅ Clustering
        table.clustering_fields = ["event_type", "country"]

        # ✅ Cost protection
        table.require_partition_filter = True

        table.description = "Real-time events table fed by streaming inserts"

        client.create_table(table)
        print("✅ Table created successfully!")

    return table_ref


def stream_to_bigquery(client, table_ref, data):
    errors = client.insert_rows_json(table_ref, data)

    if errors:
        print("❌ Errors while inserting:")
        for error in errors:
            print(error)
    else:
        print("✅ Data streamed successfully!")


if __name__ == "__main__":

    PROJECT_ID = os.getenv('PROJECT_ID')
    DATASET_ID = os.getenv('DATASET_ID')
    TABLE_ID = os.getenv('TABLE_ID')
    CREDENTIALS_PATH = os.getenv('CREDENTIALS_PATH')

    if CREDENTIALS_PATH and not os.path.isabs(CREDENTIALS_PATH):
        CREDENTIALS_PATH = os.path.join(BASE_DIR, CREDENTIALS_PATH)

    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
    client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

    # Step 1: Ensure table exists
    table_ref = create_table_if_not_exists(client, DATASET_ID, TABLE_ID)

    # Step 2: Get data
    data = get_event_data()

    # Step 3: Stream data
    stream_to_bigquery(client, table_ref, data)