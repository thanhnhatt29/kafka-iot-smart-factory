# IoT Smart Factory – Kafka Demo

## 📦 Features
- Simulates 3 types of IoT data: temperature, humidity, vibration
- Multi-topic Kafka setup with 3 brokers
- Producers simulate 100+ devices sending real-time data
- Consumers store data and detect anomalies
- Real-time visualization of incoming data
- PostgreSQL integration for long-term storage

---

## 🚀 To Run the Project

### 1. Start Kafka cluster
```bash
docker-compose up -d
````

### 2\. Create Kafka topics using dockerized shell script

```bash
bash kafka/kafka-setup.sh
```

### 3\. Start producers (multiple instances)

Run multiple simulated IoT producers with a single Python script:

```bash
python run_multiple_producers.py --count 6
```

> Replace `--count` with how many producers you want per sensor type (e.g., 6 = 18 total producers).

### 4\. Start consumers

```bash
python consumer/storage_consumer.py      # Save messages to CSV
python consumer/anomaly_detector.py      # Detect high temperatures
```

### 5\. Live data visualization (real-time plot)

```bash
python visualization/live_plot_viewer.py
```

> This will display a single dynamic plot that shows temperature, humidity, and vibration over time.

-----

## 🗃️ Optional: PostgreSQL Integration

To store all messages in a PostgreSQL database:

1.  Ensure PostgreSQL service is running (you can add to docker-compose if needed)
2.  Use the schema in `db/init.sql`
3.  Modify `storage_consumer.py` to insert data into the database

-----

## 📁 Project Structure

```
iot-smart-factory/
├── docker-compose.yml
├── kafka/
│   ├── kafka-setup.sh
│   └── kafka_setup.py (optional alternative)
├── producer/
│   ├── temperature_producer.py
│   ├── humidity_producer.py
│   └── vibration_producer.py
├── consumer/
│   ├── storage_consumer.py
│   └── anomaly_detector.py
├── utils/
│   └── data_simulation.py
├── visualization/
│   └── live_plot_viewer.py
├── db/
│   └── init.sql
├── run_multiple_producers.py
└── README.md
```

## Problems

### 🧩 **1. Basic Configuration and Architecture**

| Topic                   | Problem Description                                                              | Improvement Suggestion                                                                                             |
| ----------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Replication Factor** | The demo mentions a replication factor of 3, but the configuration is set to 2.  | The configuration should be synchronized with the documentation, or the reason for choosing RF=2 should be clearly explained. |
| **acks (acknowledgements)** | `acks` are not applied in the Producer.                                          | Apply `acks=all` to ensure data integrity in production.                                                           |
| **Idempotent Producer** | `enable.idempotence=true` is not enabled.                                        | Prevents duplicate writes in case of retries.                                                                      |
| **Offset Commit** | The offset commit method is not clear.                                           | Clearly define whether to use `enable.auto.commit` or manual commit, and correctly configure `auto_offset_reset`.  |
| **auto\_offset\_reset** | Lacks guidance on reading data from the beginning.                               | Need to add the `auto_offset_reset='earliest'` configuration in the Consumer.                                      |

-----

### 📚 **2. Advanced Features Not Implemented**

| Topic                 | Problem Description             | Improvement Suggestion                                                                      |
| --------------------- | ------------------------------- | ------------------------------------------------------------------------------------------- |
| **Kafka Streams API** | Mentioned but not demonstrated. | Create a streaming data processing pipeline: map/filter/aggregate.                          |
| **ksqlDB** | Not used.                       | Need to demo ksqlDB for SQL-like processing on Kafka topics.                                |
| **Kafka 4.0 & KRaft** | Not researched.                 | Research the Zookeeper-less architecture (KRaft mode), suitable for Kafka 4.x.              |
| **Schema Registry** | Not mentioned.                  | Apply when using Avro/Protobuf to control schemas between Producer/Consumer.                |
| **Fault Tolerance** | Description is missing.         | Add retry, backoff, circuit breaker, dead letter topic.                                     |

-----

### 🔐 **3. Security and Management**

| Topic                                 | Problem Description           | Improvement Suggestion                                                                                               |
| ------------------------------------- | ----------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Security (Authentication & Authorization)** | Not mentioned.                | Apply SSL/SASL, ACLs in Kafka to protect data.                                                                       |
| **Monitoring & Alerting** | Not integrated.               | Connect Kafka with Prometheus & Grafana, or use Confluent Control Center for system monitoring.                      |
| **Log file** | Log files are not monitored.  | Set up log rotation, save logs to a centralized system like ELK or Loki.                                             |
| **Retry & Error Handling** | No strategy in place.         | Configure `retries`, `retry.backoff.ms`, and handle send/receive errors or consumer lag.                               |
| **Connection Timeout** | Configuration is missing.     | Need to properly configure `request.timeout.ms`, `session.timeout.ms`, and `max.poll.interval.ms`.                   |

-----