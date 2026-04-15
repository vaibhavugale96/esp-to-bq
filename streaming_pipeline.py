import os
import json
import uuid
import time
from datetime import datetime, timezone

from google.cloud import bigquery, pubsub_v1
from google.oauth2 import service_account
from dotenv import load_dotenv

# Load env
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
DATASET_ID = os.getenv("DATASET_ID")
TABLE_ID = os.getenv("TABLE_ID")
TOPIC_ID = os.getenv("TOPIC_ID")
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")
CREDENTIALS_PATH = os.getenv("CREDENTIALS_PATH")

# Load credentials
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)

# Clients
bq_client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
publisher = pubsub_v1.PublisherClient(credentials=credentials)
subscriber = pubsub_v1.SubscriberClient(credentials=credentials)


# =========================
# 1. SETUP PUB/SUB
# =========================
def setup_pubsub():
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

    # Create topic if not exists
    try:
        publisher.get_topic(request={"topic": topic_path})
        print("✅ Topic exists")
    except Exception:
        publisher.create_topic(request={"name": topic_path})
        print("✅ Topic created")

    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    # Create subscription if not exists
    try:
        subscriber.get_subscription(request={"subscription": subscription_path})
        print("✅ Subscription exists")
    except Exception:
        subscriber.create_subscription(
            request={
                "name": subscription_path,
                "topic": topic_path
            }
        )
        print("✅ Subscription created")


# =========================
# 2. GENERATE MOCK EVENT
# =========================
def generate_event():
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "click",
        "user_id": f"user_{uuid.uuid4().hex[:5]}",
        "session_id": f"sess_{uuid.uuid4().hex[:5]}",
        "page_url": "/home",
        "referrer": "google",
        "device_type": "mobile",
        "country": "IN",
        "event_timestamp": datetime.now(timezone.utc).isoformat(),
    }


# =========================
# 3. PUBLISH EVENTS
# =========================
def publish_events():
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

    while True:
        event = generate_event()
        data = json.dumps(event).encode("utf-8")

        publisher.publish(topic_path, data)
        print(f"📤 Published: {event['event_id']}")

        time.sleep(3)


# =========================
# 4. SUBSCRIBE + INSERT INTO BIGQUERY
# =========================
def listen_and_insert():
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    def callback(message):
        print("📩 Message received")

        data = json.loads(message.data.decode("utf-8"))
        print("DATA:", data)

        errors = bq_client.insert_rows_json(table_id, [data])

        if not errors:
            print(f"✅ Inserted: {data['event_id']}")
        else:
            print("❌ Error inserting:", errors)

        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)
    print("🎧 Listening for messages...")

    while True:
        time.sleep(10)


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    print("🚀 Starting streaming pipeline...")

    setup_pubsub()

    import threading

    # Start publisher in background thread
    threading.Thread(target=publish_events, daemon=True).start()

    # Start subscriber in main thread
    listen_and_insert()