import os
import platform
import time

import pandas as pd
import sqlite3
import bcrypt
from rich.console import Console
from rich.table import Table
from src.config import STUDENTS_COLUMNS
from src.utils.user_handler import register_user

console = Console()


def clear_console():
    # For Windows
    if platform.system() == "Windows":
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')


def get_students_data(conn):
    query = """SELECT s.student_id, s.first_name, s.last_name, s.middle_name, s.date_of_birth, s.gender, 
    s.nationality, sci.email, sci.phone_number, sci.address, sci.city, sci.state, sci.country, sci.postal_code, 
    sai.previous_school, sai.extracurricular_activities, sai.disciplinary_record, sai.attendance_record, sai.grades, 
    sai.scholarships, sai.scholarship_details, sai.school_email, sai.login_credentials, sbi.fee_id, 
    sbi.tuition_status, shi.emergency_contact_name, shi.emergency_contact_relationship, shi.emergency_contact_phone, 
    shi.medical_conditions, shi.allergies, shi.photo, shi.parent_guardian_names FROM Students s LEFT JOIN 
    StudentContactInfo sci ON s.student_id = sci.student_id LEFT JOIN StudentAcademicInfo sai ON s.student_id = 
    sai.student_id LEFT JOIN StudentBillingInfo sbi ON s.student_id = sbi.student_id LEFT JOIN StudentHealthInfo shi 
    ON s.student_id = shi.student_id"""
    return pd.read_sql_query(query, conn)


def paginate_dataframe(max_width=10, page_size=10):
    conn = sqlite3.connect('../src/database/school_management_system.db')
    df = get_students_data(conn)  # This function needs to return a Pandas DataFrame
    selected_columns = STUDENTS_COLUMNS  # Make sure this is defined and contains column names
    df = df[selected_columns]

    total_pages = (len(df) + page_size - 1) // page_size

    current_page = 0

    while True:
        console.clear()
        table = Table(title=f"Lista de estudiantes - Página {current_page + 1} de {total_pages}",
                      show_header=True, header_style="bold magenta")

        # Define the columns of the table
        for col in selected_columns:
            table.add_column(col)

        # Display rows for the current page
        start_index = current_page * page_size
        end_index = start_index + page_size
        for row in df.iloc[start_index:end_index].itertuples():
            table.add_row(*[str(getattr(row, col))[:max_width] for col in selected_columns])

        console.print(table, style="bold blue", justify="center")

        # Pagination controls
        user_input = input("Ingresa 'c' para continuar, 'r' para regresar, o 's' para salir: ").lower()
        if user_input == 'c' and current_page < total_pages - 1:
            current_page += 1
        elif user_input == 'r' and current_page > 0:
            current_page -= 1
        elif user_input == 's':
            console.clear()
            break


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password, hashed):
    # Ensure both password and hashed are byte strings
    password_bytes = password.encode()
    hashed_bytes = hashed.encode() if isinstance(hashed, str) else hashed
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def login():
    while True:
        clear_console()
        console.print("\nInicio de sesión\n", style="bold magenta")
        choice = str(input("Ingrese 1 para usuario existente, 2 para registrar usuario: "))
        if choice == "1":
            clear_console()
            username = input("Usuario: ")
            password = input("Clave: ")

            # Verify user credentials. This is a placeholder function.
            if verify_user_credentials(username, password):
                break
            else:
                console.print("Credenciales inválidas, intente de nuevo.", style="bold red")
                time.sleep(1)
        elif choice == "2":
            register_user()
            time.sleep(1)
        else:
            console.print("Opción Incorrecta\n", style="bold red", justify="center")
            time.sleep(1)


def verify_user_credentials(username, password):
    # Fetch user's hashed password from the database
    conn = sqlite3.connect('../src/database/school_management_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT hashed_password FROM Users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        hashed_password = result[0]
        return verify_password(password, hashed_password)
    return False
