from kafka import KafkaConsumer
import json

print("[Anomaly Detector] Starting consumer...")

THRESHOLDS = {
    'vibration': 4.0,
    'humidity': 80.0,
    'temperature': 35.0
}

consumer = KafkaConsumer(
    'temperature_data', 'humidity_data', 'vibration_data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    group_id='anomaly_group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def get_measurement_info(data):
    for key, value in data.items():
        if key not in ('device_id', 'timestamp'):
            return key, float(value)
    return None, None 

for message in consumer:
    data = message.value # Deserialized dictionary

    # Direct access - will crash if keys are missing or data is malformed
    device_id = data['device_id']
    timestamp = data['timestamp']
    measurement_type, measurement_value = get_measurement_info(data)

    if measurement_type in THRESHOLDS:
        threshold = THRESHOLDS[measurement_type]
        if measurement_value > threshold:
            # --- Print ONLY if anomaly is detected ---
            print(
                f"ALERT! Anomaly Detected: Device={device_id}, "
                f"Type={measurement_type}, Value={measurement_value}, "
                f"Threshold={threshold}, Timestamp={timestamp}"
            )