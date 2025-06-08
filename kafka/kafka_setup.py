from confluent_kafka.admin import AdminClient, NewTopic

# Connect to Kafka cluster via bootstrap servers
admin_client = AdminClient({
    "bootstrap.servers": "kafka1:9092,kafka2:9093,kafka3:9094"
})

# Define topics to create
topics_to_create = [
    NewTopic("temperature_data", num_partitions=3, replication_factor=2),
    NewTopic("humidity_data", num_partitions=3, replication_factor=2),
    NewTopic("vibration_data", num_partitions=3, replication_factor=2)
]

# Attempt to create topics
fs = admin_client.create_topics(topics_to_create)

# Check results
for topic, f in fs.items():
    try:
        f.result()  # Wait for topic creation
        print(f"✅ Topic '{topic}' created successfully.")
    except Exception as e:
        print(f"⚠️ Failed to create topic '{topic}': {e}")
