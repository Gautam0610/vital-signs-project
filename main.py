import json
import os
import random
import time
from dotenv import load_dotenv
from kafka import KafkaProducer
from kafka.errors import KafkaError

load_dotenv()

# Kafka configuration from .env file
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_SASL_MECHANISM = os.getenv("KAFKA_SASL_MECHANISM", "PLAIN")  # Default to PLAIN if not set
KAFKA_SASL_PLAIN_USERNAME = os.getenv("KAFKA_SASL_PLAIN_USERNAME")
KAFKA_SASL_PLAIN_PASSWORD = os.getenv("KAFKA_SASL_PLAIN_PASSWORD")
KAFKA_SECURITY_PROTOCOL = os.getenv("KAFKA_SECURITY_PROTOCOL", "SASL_SSL")  # Default to SASL_SSL

def generate_vital_signs():
    """Generates random but realistic vital signs."""
    heart_rate = random.randint(60, 100)
    temperature = round(random.uniform(97.0, 99.0), 1)
    systolic_bp = 120
    diastolic_bp = 80
    return {
        "heart_rate": heart_rate,
        "temperature": temperature,
        "systolic_bp": systolic_bp,
        "diastolic_bp": diastolic_bp,
        "timestamp": time.time()
    }

def main():
    """Streams vital signs to Kafka."""
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            sasl_mechanism=KAFKA_SASL_MECHANISM,
            sasl_plain_username=KAFKA_SASL_PLAIN_USERNAME,
            sasl_plain_password=KAFKA_SASL_PLAIN_PASSWORD,
            security_protocol=KAFKA_SECURITY_PROTOCOL,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("Kafka producer initialized successfully.")

        while True:
            vital_signs = generate_vital_signs()
            try:
                producer.send(KAFKA_TOPIC, vital_signs)
                print(f"Sent: {vital_signs}")
            except KafkaError as e:
                print(f"Error sending message: {e}")
            time.sleep(1)  # Send every 1 second

    except Exception as e:
        print(f"Failed to initialize Kafka producer: {e}")

    finally:
        if 'producer' in locals():
            producer.close()
            print("Kafka producer closed.")

if __name__ == "__main__":
    main()
