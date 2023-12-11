import sqlite3
import pandas as pd
from rich.console import Console
from src.config import DB_PATH
from src.utils.helpers import remove_duplicated_columns

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
        health_sql = '''INSERT INTO StudentHealthInfo (student_id, emergency_contact_name, emergency_contact_relationship, 
                        emergency_contact_phone, medical_conditions, parent_guardian_names, allergies)
                        VALUES (?, ?, ?, ?, ?, ?, ?)'''
        cursor.execute(health_sql, (student_id, emergency_contact_name, emergency_contact_relationship,
                                    emergency_contact_phone, medical_conditions, parent_guardian_names, allergies))

        # Commit the changes
        conn.commit()

    except sqlite3.Error as e:
        console.print(f"An error occurred: {e}", style="bold red")
    finally:
        conn.close()
