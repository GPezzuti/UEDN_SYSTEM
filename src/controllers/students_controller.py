import sqlite3
import pandas as pd
from rich.console import Console
from src.config import DB_PATH
from src.utils.helpers import remove_duplicated_columns, input_or_none

console = Console()


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


def add_new_student(): # TODO: Refactor using the models
    console.print("\nIngrese la información básica del estudiante", style="bold magenta")
    first_name = input_or_none("Nombre: ")
    last_name = input_or_none("Apellido: ")
    middle_name = input_or_none("Segundo nombre (opcional): ")
    date_of_birth = input_or_none("Fecha de nacimiento (YYYY-MM-DD): ")
    gender = input_or_none("Género: ")
    nationality = input_or_none("Nacionalidad: ")

    console.print("\nIngrese la información de contacto del estudiante", style="bold magenta")
    email = input_or_none("Email: ")
    phone_number = input_or_none("Número de teléfono: ")
    address = input_or_none("Dirección: ")
    city = input_or_none("Ciudad: ")
    state = input_or_none("Estado/Provincia: ")
    country = input_or_none("País: ")
    postal_code = input_or_none("Código Postal: ")

    console.print("\nIngrese la información académica del estudiante", style="bold magenta")
    previous_school = input_or_none("Escuela anterior (opcional): ")
    extracurricular_activities = input_or_none("Actividades extracurriculares (opcional): ")

    console.print("\nIngrese la información de salud del estudiante", style="bold magenta")
    emergency_contact_name = input_or_none("Nombre del contacto de emergencia: ")
    emergency_contact_relationship = input_or_none("Relación con el contacto de emergencia: ")
    emergency_contact_phone = input_or_none("Teléfono del contacto de emergencia: ")
    parent_guardian_names = input_or_none("Nombre del representante: ")
    medical_conditions = input_or_none("Condiciones médicas (opcional): ")
    allergies = input_or_none("Alergias (opcional): ")

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
        health_sql = '''INSERT INTO StudentHealthInfo (student_id, emergency_contact_name, emergency_contact_relationship, 
                        emergency_contact_phone, medical_conditions, parent_guardian_names, allergies)
                        VALUES (?, ?, ?, ?, ?, ?, ?)'''
        cursor.execute(health_sql, (student_id, emergency_contact_name, emergency_contact_relationship,
                                    emergency_contact_phone, medical_conditions, parent_guardian_names, allergies))

        # Commit the changes
        conn.commit()

    except sqlite3.Error as e:
        console.print(f"Error de inserción: {e}", style="bold red")
    finally:
        conn.close()
