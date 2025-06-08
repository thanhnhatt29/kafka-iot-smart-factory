#!/bin/bash

echo "📦 Creating Kafka topics using docker exec..."

docker exec kafka1 kafka-topics --create --topic temperature_data --bootstrap-server kafka1:29092 --replication-factor 2 --partitions 3

docker exec kafka1 kafka-topics --create --topic humidity_data --bootstrap-server kafka1:29092 --replication-factor 2 --partitions 3

docker exec kafka1 kafka-topics --create --topic vibration_data --bootstrap-server kafka1:29092 --replication-factor 2 --partitions 3

echo "✅ All topics created."

# docker exec kafka1 kafka-topics --list --bootstrap-server kafka1:29092
