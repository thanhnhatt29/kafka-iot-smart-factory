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
```

### 2. Create Kafka topics using dockerized shell script
```bash
bash kafka/kafka-setup.sh
```

### 3. Start producers (multiple instances)
Run multiple simulated IoT producers with a single Python script:
```bash
python run_multiple_producers.py --count 6
```
> Replace `--count` with how many producers you want per sensor type (e.g., 6 = 18 total producers).

### 4. Start consumers
```bash
python consumer/storage_consumer.py        # Save messages to CSV
python consumer/anomaly_detector.py        # Detect high temperatures
```

### 5. Live data visualization (real-time plot)
```bash
python visualization/live_plot_viewer.py
```
> This will display a single dynamic plot that shows temperature, humidity, and vibration over time.

---

## 🗃️ Optional: PostgreSQL Integration
To store all messages in a PostgreSQL database:

1. Ensure PostgreSQL service is running (you can add to docker-compose if needed)
2. Use the schema in `db/init.sql`
3. Modify `storage_consumer.py` to insert data into the database

---

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
│   ├── vibration_producer.py
├── consumer/
│   ├── storage_consumer.py
│   ├── anomaly_detector.py
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

### 🧩 **1. Cấu hình và Kiến trúc Cơ bản**

| Chủ đề                      | Mô tả vấn đề                                                    | Gợi ý cải thiện                                                                              |
| --------------------------- | --------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Replication Factor**      | Demo có nói đến replication factor = 3, nhưng cấu hình lại là 2 | Cần đồng bộ cấu hình với tài liệu hoặc giải thích rõ lý do chọn RF=2                         |
| **acks (acknowledgements)** | Chưa áp dụng acks trong Producer                                | Áp dụng `acks=all` để đảm bảo tính toàn vẹn dữ liệu trong production                         |
| **Idempotent Producer**     | Chưa bật `enable.idempotence=true`                              | Tránh ghi trùng trong trường hợp retry                                                       |
| **Offset Commit**           | Chưa thấy rõ cách commit offset                                 | Xác định rõ `enable.auto.commit` hay commit thủ công, cấu hình chính xác `auto_offset_reset` |
| **auto\_offset\_reset**     | Thiếu hướng dẫn đọc dữ liệu từ đầu                              | Cần thêm cấu hình `auto_offset_reset='earliest'` trong Consumer                              |

---

### 📚 **2. Tính năng nâng cao chưa triển khai**

| Chủ đề                | Mô tả vấn đề              | Gợi ý cải thiện                                                              |
| --------------------- | ------------------------- | ---------------------------------------------------------------------------- |
| **Kafka Streams API** | Có đề cập nhưng chưa demo | Tạo pipeline xử lý dữ liệu streaming: map/filter/aggregate                   |
| **ksqlDB**            | Chưa sử dụng              | Cần demo ksqlDB để xử lý SQL-like trên Kafka topics                          |
| **Kafka 4.0 & KRaft** | Chưa nghiên cứu           | Tìm hiểu kiến trúc không dùng Zookeeper (KRaft mode), phù hợp Kafka 4.x      |
| **Schema Registry**   | Chưa đề cập               | Áp dụng khi sử dụng Avro/Protobuf để kiểm soát schema giữa Producer/Consumer |
| **Fault Tolerance**   | Thiếu mô tả               | Bổ sung retry, backoff, circuit breaker, dead letter topic                   |

---

### 🔐 **3. Bảo mật và Quản lý**

| Chủ đề                                        | Mô tả vấn đề           | Gợi ý cải thiện                                                                                 |
| --------------------------------------------- | ---------------------- | ----------------------------------------------------------------------------------------------- |
| **Security (Authentication & Authorization)** | Chưa đề cập            | Áp dụng SSL/SASL, ACLs trong Kafka để bảo vệ dữ liệu                                            |
| **Monitoring & Alerting**                     | Chưa tích hợp          | Kết nối Kafka với Prometheus & Grafana, hoặc dùng Confluent Control Center để theo dõi hệ thống |
| **Log file**                                  | Chưa giám sát file log | Thiết lập log rotation, lưu log ra centralized system như ELK hoặc Loki                         |
| **Retry & Error Handling**                    | Chưa có chiến lược     | Thiết lập `retries`, `retry.backoff.ms`, xử lý lỗi gửi/nhận hoặc consumer lag                   |
| **Connection Timeout**                        | Thiếu cấu hình         | Cần cấu hình `request.timeout.ms`, `session.timeout.ms`, `max.poll.interval.ms` phù hợp         |

---