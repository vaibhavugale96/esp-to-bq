import os
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv

# Load env
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
DATASET_ID = os.getenv("DATASET_ID")
TABLE_ID = os.getenv("TABLE_ID")
CREDENTIALS_PATH = os.getenv("CREDENTIALS_PATH")

# Load credentials
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)

client = bigquery.Client(credentials=credentials, project=PROJECT_ID)


def fetch_data():
    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
        ORDER BY event_timestamp DESC
        LIMIT 1
    """

    query_job = client.query(query)

    print("📊 Latest Data:\n")

    for row in query_job:
        print(dict(row))


if __name__ == "__main__":
    fetch_data()