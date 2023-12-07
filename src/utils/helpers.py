import os
import platform


def clear_console():
    # For Windows
    if platform.system() == "Windows":
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')


def get_students_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, first_name, last_name, date_of_birth FROM Students")
    return cursor.fetchall()


def sort_students_by_last_name(students_data):
    return sorted(students_data, key=lambda x: x[1])
