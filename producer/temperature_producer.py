import json
import time
import random
from kafka import KafkaProducer

print("[Temperature Producer] Starting producer...")

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

for i in range(100):
    data = {
        "device_id": f"temp-sensor-{i % 10}",
        "timestamp": time.time(),
        "temperature": round(random.uniform(20, 40), 2)
    }
    print(f"[Temperature Producer] Sending: {data}")
    producer.send('temperature_data', value=data)
    time.sleep(1)

print("[Temperature Producer] Finished sending messages.")
