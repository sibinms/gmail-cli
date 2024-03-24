import sqlite3
import pytest

from schema.utils import parse_email_date, get_or_create_email


@pytest.fixture
def db_connection():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    with open('./schema/migrations/email.sql', 'r') as sql_file:
        cursor.executescript(sql_file.read())
    conn.commit()
    yield conn
    conn.close()


class TestEmailsTable:
    def test_table_creation(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='emails';")
        result = cursor.fetchone()
        assert result is not None, "Emails table was not created"

    def test_unique_constraint(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute("""
            INSERT INTO emails (user_id, message_id, sender, subject, message, received_at)
            VALUES ('user123', 'message123', 'sender@example.com', 'Test Subject', 'Test Message', '2024-03-25');
        """)
        db_connection.commit()

        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO emails (user_id, message_id, sender, subject, message, received_at)
                VALUES ('user123', 'message123', 'sender@example.com', 'Test Subject', 'Test Message', '2024-03-25');
            """)
            db_connection.commit()


class TestParseEmailDate:
    def test_parse_email_date_valid(self):
        date_str = 'Fri, 22 Mar 2024 12:58:04 +0000 (UTC)'
        expected_date = '2024-03-22 12:58:04'
        assert parse_email_date(date_str) == expected_date

    def test_parse_email_date_invalid(self):
        date_str = 'Invalid date string'
        assert parse_email_date(date_str) is None
