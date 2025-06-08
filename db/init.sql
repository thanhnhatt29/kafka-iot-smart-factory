-- Example if using PostgreSQL
CREATE TABLE IF NOT EXISTS sensor_data (
    id SERIAL PRIMARY KEY,
    device_id TEXT,
    timestamp TIMESTAMP,
    data JSONB
);