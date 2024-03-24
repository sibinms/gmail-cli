from schema.connection import get_connection
from datetime import datetime


def parse_email_date(date_str):
    try:
        parsed_date = datetime.strptime(date_str.split('(')[0].strip(), "%a, %d %b %Y %H:%M:%S %z")
        sqlite_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
        return sqlite_date
    except ValueError:
        return None


def get_or_create_email(user_id, message_id, sender, subject, body, date):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT id FROM emails WHERE user_id = ? AND message_id = ?", (user_id, message_id)
    )
    existing_row = c.fetchone()
    if existing_row:
        email_id = existing_row[0]
        email = (email_id, user_id, message_id, sender, subject, body, date)
        created = False
    else:
        date = parse_email_date(date)
        c.execute(
            "INSERT INTO emails (user_id, message_id, sender, subject, message, received_at) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, message_id, sender, subject, body, date)
        )
        conn.commit()
        email_id = c.lastrowid
        email = (email_id, user_id, message_id, sender, subject, body, date)
        created = True

    conn.close()
    return email, created
