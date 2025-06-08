from kafka import KafkaConsumer
import json
import csv

print("[Storage Consumer] Starting consumer...")

value_keys = ['temperature', 'humidity', 'vibration']

consumer = KafkaConsumer(
    'temperature_data', 'humidity_data', 'vibration_data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='storage_group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

with open('sensor_data.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    for message in consumer:

        data = message.value

        value = None 
        for key in value_keys:
            if key in data:
                value = data[key]
                break 

        print(f"[Storage Consumer] Received from topic {message.topic}: {data}")
        writer.writerow([data.get('device_id'), data.get('timestamp'), value])
        print(f"[Storage Consumer] Stored data to CSV.")
