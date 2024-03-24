import os
from schema.connection import get_connection


def run_migrations():
    migration_files = sorted(os.listdir('schema/migrations'))
    conn = get_connection()
    c = conn.cursor()

    for filename in migration_files:
        migration_path = os.path.join('schema/migrations', filename)
        with open(migration_path, 'r') as file:
            migration_script = file.read()
            c.executescript(migration_script)
            print(f"Applied migration --- {migration_path} --------------------")

    conn.commit()
    conn.close()
