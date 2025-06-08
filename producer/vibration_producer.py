import json
import time
import random
from kafka import KafkaProducer

print("[Vibration Producer] Starting producer...")

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

for i in range(100):
    data = {
        "device_id": f"vibration-sensor-{i % 10}",
        "timestamp": time.time(),
        "vibration": round(random.uniform(0.1, 5.0), 2)
    }
    print(f"[Vibration Producer] Sending: {data}")
    producer.send('vibration_data', value=data)
    time.sleep(1)

print("[Vibration Producer] Finished sending messages.")
