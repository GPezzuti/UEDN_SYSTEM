import sqlite3
import os

db_file = 'school_management_system_v2.db'
ddl_file = 'ddl.sql'


def check_and_initialize_db():
    if not os.path.exists(db_file):
        print(f"Database {db_file} does not exist. Initializing database.")
        create_tables_from_ddl(ddl_file)
    else:
        print(f"Database {db_file} exists. Proceeding with the application.")


def create_tables_from_ddl(ddl):
    with open(ddl, 'r') as file:
        sql_script = file.read()

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    check_and_initialize_db()
