from datetime import datetime
import os
import platform
import time
import getpass
import pandas as pd
import sqlite3
import bcrypt
from rich.console import Console
from rich.table import Table
from src.config import STUDENTS_COLUMNS, DESKTOP_PATH, DB_PATH
from src.utils.user_handler import register_user

console = Console()


def clear_console():
    # For Windows
    if platform.system() == "Windows":
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')


def get_students_data():
    query = """SELECT *
            FROM Students s
            LEFT JOIN StudentContactInfo sci ON s.student_id = sci.student_id
            LEFT JOIN StudentAcademicInfo sai ON s.student_id = sai.student_id
            LEFT JOIN StudentBillingInfo sbi ON s.student_id = sbi.student_id
            LEFT JOIN StudentHealthInfo shi ON s.student_id = shi.student_id"""

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    df = remove_duplicated_columns(df)

    return df


def paginate_dataframe(df, title, selected_columns, max_width=10, page_size=10):

    df_sliced = df[selected_columns].copy()

    total_pages = (len(df_sliced) + page_size - 1) // page_size
    current_page = 0

    while True:
        console.clear()
        table = Table(title=f"{title} - Página {current_page + 1} de {total_pages}",
                      show_header=True, header_style="bold magenta")

        # Define the columns of the table
        for col in selected_columns:
            table.add_column(col)

        # Display rows for the current page
        start_index = current_page * page_size
        end_index = start_index + page_size

        for row in df_sliced.iloc[start_index:end_index].itertuples():
            table.add_row(*[str(getattr(row, col))[:max_width] for col in selected_columns])

        console.print(table, style="bold blue", justify="center")

        # Pagination controls
        user_input = input("'f' filtros, 's' siguiente, 'a' atrás, 'q' salir, 'r' resetear: ").strip().lower()

        if user_input == 'f':
            df_sliced = filter_dataframe(df_sliced)
            total_pages = (len(df_sliced) + page_size - 1) // page_size
            current_page = 0
        elif user_input == 's' and current_page < total_pages - 1:
            current_page += 1
        elif user_input == 'a' and current_page > 0:
            current_page -= 1
        elif user_input == 'q':
            console.clear()
            break
        elif user_input == 'r':
            df_sliced = df[selected_columns].copy()  # Reset DataFrame to the original data
            total_pages = (len(df_sliced) + page_size - 1) // page_size
            current_page = 0  # Reset to the first page
        elif user_input not in ['f', 's', 'a', 'q']:
            console.print("Opción Incorrecta\n", style="bold red", justify="center")
            time.sleep(1)


def filter_dataframe(df):
    console.print("\nOpciones de Filtro", style="bold magenta")

    # Display column names
    for i, col in enumerate(df.columns):
        console.print(f"[{i}] {col}", style="bold cyan")

    while True:
        col_input = input("\nSelecciona el índice de la columna para filtrar o 'q' para salir: ")

        if col_input.strip().lower() == 'q':
            return df  # Return the original DataFrame if the user chooses to go back

        try:
            col_index = int(col_input)
            if col_index not in range(len(df.columns)):
                raise ValueError
            filter_col = df.columns[col_index]
            break
        except ValueError:
            console.print("\nÍndice inválido. Por favor, intenta de nuevo.", style="bold red")

    filter_value = input(f"\nIngresa el valor para filtrar en '{filter_col}' o 'q' para salir: ").strip().lower()

    if filter_value == 'q':
        return df  # Return the original DataFrame if the user chooses to go back

    # Apply filter with case-insensitive partial match
    filtered_df = df[df[filter_col].astype(str).str.lower().str.startswith(filter_value)]
    return filtered_df


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
        choice = str(input("Ingrese 1 para usuario existente, 2 para registrar usuario, 0 para salir: ").strip().lower())
        if choice == "1":
            clear_console()
            username = input("Usuario: ")
            password = getpass.getpass("Clave: ")  # Password will not be echoed

            # Verify user credentials. This is a placeholder function.
            if verify_user_credentials(username, password):
                break
            else:
                console.print("Credenciales inválidas, intente de nuevo.", style="bold red")
                time.sleep(1)

        elif choice == "2":
            while True:
                console.print("\nIngrese un usuario administrador", style="cyan")
                username = input("Usuario: ")
                password = getpass.getpass("Clave: ")  # Password will not be echoed

                if verify_user_credentials(username, password) and (get_user_role(username) == "admin"):
                    console.print("\nRegistro de usuario:", style="green")
                    register_user()
                    time.sleep(1)
                    break
                elif verify_user_credentials(username, password) is False:
                    console.print("Credenciales Inválidas", style="bold red")
                else:
                    console.print("Usuario con pocos privilegios", style="bold red")
        elif choice == "0":
            clear_console()
            print("OK")
            exit()
        else:
            console.print("Opción Incorrecta\n", style="bold red", justify="center")
            time.sleep(1)


def verify_user_credentials(username, password):
    # Fetch user's hashed password from the database
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT hashed_password FROM Users WHERE username = ?", (username,))
        result = cursor.fetchone()

    if result:
        hashed_password = result[0]
        return verify_password(password, hashed_password)
    return False


def get_user_role(username):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM Users WHERE username = ?", (username,))
        result = cursor.fetchone()

    if result:
        return result[0]  # Return the role


def remove_duplicated_columns(df):
    seen = set()
    return df.loc[:, ~df.columns.duplicated()]


def add_new_student():
    console.print("\nIngrese la información básica del estudiante", style="bold magenta")
    first_name = input("Nombre: ")
    last_name = input("Apellido: ")
    middle_name = input("Segundo nombre (opcional): ")
    date_of_birth = input("Fecha de nacimiento (YYYY-MM-DD): ")
    gender = input("Género: ")
    nationality = input("Nacionalidad: ")

    console.print("\nIngrese la información de contacto del estudiante", style="bold magenta")
    email = input("Email: ")
    phone_number = input("Número de teléfono: ")
    address = input("Dirección: ")
    city = input("Ciudad: ")
    state = input("Estado/Provincia: ")
    country = input("País: ")
    postal_code = input("Código Postal: ")

    console.print("\nIngrese la información académica del estudiante", style="bold magenta")
    previous_school = input("Escuela anterior (opcional): ")
    extracurricular_activities = input("Actividades extracurriculares (opcional): ")

    console.print("\nIngrese la información de salud del estudiante", style="bold magenta")
    emergency_contact_name = input("Nombre del contacto de emergencia: ")
    emergency_contact_relationship = input("Relación con el contacto de emergencia: ")
    emergency_contact_phone = input("Teléfono del contacto de emergencia: ")
    parent_guardian_names = input("Nombre del representante: ")
    medical_conditions = input("Condiciones médicas (opcional): ")
    allergies = input("Alergias (opcional): ")

    # Insert into the database
    insert_student(first_name, last_name, middle_name, date_of_birth, gender, nationality,
                   email, phone_number, address, city, state, country, postal_code, previous_school,
                   extracurricular_activities, emergency_contact_name, emergency_contact_relationship,
                   emergency_contact_phone, medical_conditions, parent_guardian_names, allergies)


def insert_student(first_name, last_name, middle_name, date_of_birth, gender, nationality,
                   email, phone_number, address, city, state, country, postal_code, previous_school,
                   extracurricular_activities, emergency_contact_name, emergency_contact_relationship,
                   emergency_contact_phone, medical_conditions, parent_guardian_names, allergies):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Insert into Students Table
        student_sql = '''INSERT INTO Students (first_name, last_name, middle_name, date_of_birth, gender, nationality)
                         VALUES (?, ?, ?, ?, ?, ?)'''
        cursor.execute(student_sql, (first_name, last_name, middle_name, date_of_birth, gender, nationality))
        student_id = cursor.lastrowid

        # Insert into StudentContactInfo Table
        contact_sql = '''INSERT INTO StudentContactInfo (student_id, email, phone_number, address, city, state, country, postal_code)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        cursor.execute(contact_sql, (student_id, email, phone_number, address, city, state, country, postal_code))

        # Insert into StudentAcademicInfo Table
        academic_sql = '''INSERT INTO StudentAcademicInfo (student_id, previous_school, extracurricular_activities)
                          VALUES (?, ?, ?)'''
        cursor.execute(academic_sql, (student_id, previous_school, extracurricular_activities))

        # Insert into StudentHealthInfo Table
        health_sql = '''INSERT INTO StudentHealthInfo (student_id, emergency_contact_name, emergency_contact_relationship, emergency_contact_phone, medical_conditions, allergies)
                        VALUES (?, ?, ?, ?, ?, ?, ?)'''
        cursor.execute(health_sql, (student_id, emergency_contact_name, emergency_contact_relationship,
                                    emergency_contact_phone, medical_conditions, parent_guardian_names, allergies))

        # Commit the changes
        conn.commit()

    except sqlite3.Error as e:
        console.print(f"An error occurred: {e}", style="bold red")
    finally:
        conn.close()
