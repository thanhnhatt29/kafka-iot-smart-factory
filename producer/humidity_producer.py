import json
import time
import random
from kafka import KafkaProducer

print("[Humidity Producer] Starting producer...")

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

for i in range(100):
    data = {
        "device_id": f"humidity-sensor-{i % 10}",
        "timestamp": time.time(),
        "humidity": round(random.uniform(30, 90), 2)
    }
    print(f"[Humidity Producer] Sending: {data}")
    producer.send('humidity_data', value=data)
    time.sleep(1)

print("[Humidity Producer] Finished sending messages.")
