import json
import time
import os
from kafka import KafkaConsumer
from db import init_db, get_connection

# Topic and broker configuration
TOPIC = "song_likes"
BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")

def main():
    # Initialize the database
    init_db()

    # Create Kafka Consumer
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=[BROKER_URL],
        auto_offset_reset='earliest',  # Start consuming messages from the earliest offset
        enable_auto_commit=True,       # Automatically commit message offsets
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # Deserialize message
    )

    print(f"Consumer listening on topic: {TOPIC}")
    for message in consumer:
        # Extract the data from the Kafka message
        data = message.value
        user_id = data.get("user_id")
        song_id = data.get("song_id")

        if user_id and song_id:
            # Insert the record into the database
            with get_connection() as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO user_profile (user_id, song_id) VALUES (?, ?)",
                        (user_id, song_id)
                    )
                    conn.commit()
                    print(f"[CONSUMER] Recorded like for user={user_id}, song={song_id}")
                except Exception as e:
                    print(f"[CONSUMER] DB error: {e}")

        time.sleep(0.1)  # Small delay to mimic processing time

if __name__ == "__main__":
    main()
