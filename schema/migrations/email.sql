-- email.sql
CREATE TABLE IF NOT EXISTS emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(255),
    message_id VARCHAR(255),
    sender TEXT,
    subject TEXT,
    message TEXT,
    received_at DATE,
    UNIQUE(user_id, message_id)
);