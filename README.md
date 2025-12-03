# Vital Signs Telemetry

This project simulates a vital signs telemetry system, generating realistic vital signs data, streaming it to a Kafka topic, and monitoring for critical conditions.

## Prerequisites

-   Docker and Docker Compose: Required for setting up the Kafka infrastructure.
-   Python 3.9: Required for running the data generation and monitoring scripts.
-   `python-dotenv`: Required for loading environment variables from `.env` file.
-   Kafka Cluster with SASL Authentication: Ensure a Kafka cluster with SASL authentication is set up or use the Docker Compose configuration provided.

## Project Structure

```
vital-signs-project/
├── docker-compose.yml  # Kafka and Zookeeper setup using Docker Compose
├── main.py             # Python script to generate and stream vital signs data to Kafka
├── monitor.py          # Python script to consume data from Kafka and monitor for high heart rates
├── requirements.txt    # Lists Python dependencies
├── .env                # Stores Kafka configuration (topic, bootstrap servers, authentication)
├── .gitignore          # Specifies intentionally untracked files that Git should ignore
└── README.md           # This file
```

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Gautam0610/vital-signs-project.git
cd vital-signs-project
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory with the following variables:

```
KAFKA_TOPIC=<your_kafka_topic>
KAFKA_BOOTSTRAP_SERVERS=<your_kafka_bootstrap_servers>
KAFKA_SASL_MECHANISM=<your_sasl_mechanism>  # e.g., PLAIN, SCRAM-SHA-512
KAFKA_SASL_PLAIN_USERNAME=<your_sasl_username>
KAFKA_SASL_PLAIN_PASSWORD=<your_sasl_password>
KAFKA_SECURITY_PROTOCOL=<your_security_protocol> # e.g., SASL_SSL, SASL_PLAINTEXT
```

Replace the placeholder values with your actual Kafka configuration.

### 3. Start Kafka Infrastructure (Using Docker Compose)

This project includes a `docker-compose.yml` file for easily setting up a local Kafka and Zookeeper cluster.

```bash
docker-compose up -d
```

This command starts the Zookeeper and Kafka containers in detached mode. Give them some time to initialize.

### 4. Install Python Dependencies

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate  # On Windows
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 5. Run the Data Generation Script

This script generates realistic vital signs data and streams it to the Kafka topic specified in your `.env` file.

```bash
python main.py
```

### 6. Run the Monitoring Script

This script consumes vital signs data from the Kafka topic and monitors for high heart rates, printing an alert if a heart rate exceeds 100.

```bash
python monitor.py
```