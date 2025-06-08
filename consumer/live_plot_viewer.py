from kafka import KafkaConsumer
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import datetime
import atexit

# --- Configuration ---
TOPICS = ['temperature_data', 'humidity_data', 'vibration_data']
BOOTSTRAP_SERVERS = 'localhost:9092'
GROUP_ID = 'live_plot_group_v2'
MAX_POINTS = 50
ANIMATION_INTERVAL_MS = 200
CONSUMER_POLL_TIMEOUT_MS = 100

# --- Kafka Consumer Setup ---
print(f"Connecting to Kafka brokers: {BOOTSTRAP_SERVERS}")
consumer = None
try:
    consumer = KafkaConsumer(
        *TOPICS,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset='latest',
        group_id=GROUP_ID,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        consumer_timeout_ms=5000
    )
    print(f"Subscribed to topics: {TOPICS}")

    def close_consumer():
        print("\nClosing Kafka consumer...")
        if consumer:
            consumer.close()
        print("Consumer closed.")

    atexit.register(close_consumer)

except Exception as e:
    print(f"ERROR: Could not connect to Kafka or subscribe to topics. {e}")
    exit()

# --- Data Storage ---
timestamps_temp = deque(maxlen=MAX_POINTS)
temperature_data = deque(maxlen=MAX_POINTS)

timestamps_hum = deque(maxlen=MAX_POINTS)
humidity_data = deque(maxlen=MAX_POINTS)

timestamps_vib = deque(maxlen=MAX_POINTS)
vibration_data = deque(maxlen=MAX_POINTS)

# --- Matplotlib Setup ---
fig, ax = plt.subplots(figsize=(10, 6))
line_temp, = ax.plot([], [], 'r-o', markersize=3, label='Temperature (°C)')
line_hum, = ax.plot([], [], 'b-o', markersize=3, label='Humidity (%)')
line_vib, = ax.plot([], [], 'g-o', markersize=3, label='Vibration (unit?)')

ax.set_title('Live IoT Sensor Data')
ax.set_xlabel('Time')
ax.set_ylabel('Sensor Values')
ax.legend(loc='upper left')
fig.autofmt_xdate()
plt.grid(True)
plt.tight_layout()

# --- Animation Update Function ---
def update_plot(frame):
    messages_processed = 0
    topic_messages = consumer.poll(timeout_ms=CONSUMER_POLL_TIMEOUT_MS)

    if not topic_messages:
        return line_temp, line_hum, line_vib

    for tp, msgs in topic_messages.items():
        for message in msgs:
            try:
                topic = message.topic
                data = message.value

                ts_unix = data.get('timestamp')
                if ts_unix is None:
                    print(f"Warning: Message missing 'timestamp': {data}")
                    continue

                dt_object = datetime.datetime.fromtimestamp(ts_unix)

                if topic == 'temperature_data':
                    temp_val = data.get('temperature')
                    if temp_val is not None:
                        timestamps_temp.append(dt_object)
                        temperature_data.append(float(temp_val))
                    else:
                        print(f"Warning: Temp message missing 'temperature': {data}")

                elif topic == 'humidity_data':
                    hum_val = data.get('humidity')
                    if hum_val is not None:
                        timestamps_hum.append(dt_object)
                        humidity_data.append(float(hum_val))
                    else:
                        print(f"Warning: Hum message missing 'humidity': {data}")

                elif topic == 'vibration_data':
                    vib_val = data.get('vibration')
                    if vib_val is not None:
                        timestamps_vib.append(dt_object)
                        vibration_data.append(float(vib_val))
                    else:
                        print(f"Warning: Vib message missing 'vibration': {data}")

                else:
                    print(f"Warning: Received message from unhandled topic: {topic}")
                    continue

                messages_processed += 1

            except json.JSONDecodeError:
                print(f"Error decoding JSON for message: {message.value}")
            except KeyError as e:
                print(f"Error: Message missing expected key {e}: {message.value}")
            except Exception as e:
                print(f"Error processing message {message.value}: {e}")

    if messages_processed > 0:
        line_temp.set_data(list(timestamps_temp), list(temperature_data))
        line_hum.set_data(list(timestamps_hum), list(humidity_data))
        line_vib.set_data(list(timestamps_vib), list(vibration_data))

        ax.relim()
        ax.autoscale_view(tight=False, scalex=True, scaley=True)

    return line_temp, line_hum, line_vib

# --- Run Animation ---
print("Starting animation... Press Ctrl+C in the terminal to stop.")
ani = animation.FuncAnimation(fig, update_plot, interval=ANIMATION_INTERVAL_MS, blit=False)

try:
    plt.show()
except KeyboardInterrupt:
    print("\nKeyboardInterrupt detected. Exiting.")
finally:
    close_consumer()

print("Script finished.")
