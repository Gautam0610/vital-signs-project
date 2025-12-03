import json
import os
from dotenv import load_dotenv
from kafka import KafkaConsumer

load_dotenv()

# Kafka configuration from .env file
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_SASL_MECHANISM = os.getenv("KAFKA_SASL_MECHANISM", "PLAIN")  # Default to PLAIN if not set
KAFKA_SASL_PLAIN_USERNAME = os.getenv("KAFKA_SASL_PLAIN_USERNAME")
KAFKA_SASL_PLAIN_PASSWORD = os.getenv("KAFKA_SASL_PLAIN_PASSWORD")
KAFKA_SECURITY_PROTOCOL = os.getenv("KAFKA_SECURITY_PROTOCOL", "SASL_SSL")  # Default to SASL_SSL


def main():
    """Consumes vital signs from Kafka and alerts on high heart rate."""
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            sasl_mechanism=KAFKA_SASL_MECHANISM,
            sasl_plain_username=KAFKA_SASL_PLAIN_USERNAME,
            sasl_plain_password=KAFKA_SASL_PLAIN_PASSWORD,
            security_protocol=KAFKA_SECURITY_PROTOCOL,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='latest'  # Start consuming from the latest message
        )
        print("Kafka consumer initialized successfully.")

        for message in consumer:
            vital_signs = message.value
            print(f"Received: {vital_signs}")
            heart_rate = vital_signs.get("heart_rate")

            if heart_rate and heart_rate > 100:
                print("ALERT: Heart rate exceeds 100!")

    except Exception as e:
        print(f"Failed to initialize Kafka consumer: {e}")

if __name__ == "__main__":
    main()
