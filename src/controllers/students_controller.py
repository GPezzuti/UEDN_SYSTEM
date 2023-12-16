import sqlite3
import pandas as pd
from rich.console import Console
from src.config import DB_PATH
from src.utils.helpers import remove_duplicated_columns
from datetime import datetime
from unidecode import unidecode

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


def clean_column_name(name):
    """Clean a column name by removing accents, replacing spaces with underscores, and converting to lowercase."""
    return unidecode(name).strip().replace(" ", "_").lower()


def parse_and_insert_student_data(file_path):
    # Read the Excel file
    df = pd.read_csv(file_path)

    # Clean column names
    df.columns = [clean_column_name(col) for col in df.columns]

    with sqlite3.connect(DB_PATH) as conn:
        # Connect to the database
        cursor = conn.cursor()

        # Iterate through each row in the DataFrame
        for index, row in df.iterrows():
            try:
                # Extract and format data for each student using the cleaned column names
                first_name = row['primer_nombre']
                last_name = row['primer_apellido']
                middle_name = row.get('segundo_nombre', None)
                date_of_birth = datetime.strptime(row['fecha_de_nacimiento'], '%Y-%m-%d').date() if pd.notna(
                    row['fecha_de_nacimiento']) else None

                gender = row['genero']
                nationality = row['nacionalidad']
                national_id = row.get('cedula_de_identidad', None)

                row.get('email', None)
                row.get('numero_telefonico', None)
                address = row['direccion_de_residencia']
                city = row['ciudad']
                state = row['estado']
                country = row['pais']
                postal_code = row['codigo_postal']

                emergency_contact_name = row['nombre_completo_del_contacto_de_emergencia']
                emergency_contact_relationship = row['relacion_con_el_contacto_de_emergencia']
                emergency_contact_phone = row['numero_del_contacto_de_emergencia']
                emergency_contact_id = row['cedula_del_contacto_de_emergencia']

                father_name = row.get('nombre_completo_del_padre', None)
                father_id = row.get('cedula_del_padre', None)
                father_phone = row.get('numero_telefonico_del_padre', None)

                mother_name = row.get('nombre_completo_de_la_madre', None)
                mother_id = row.get('cedula_de_la_madre', None)
                mother_phone = row.get('numero_telefonico_de_la_madre', None)

                parent_guardian_names = row['nombre_completo_del_representante']
                parent_relationship = row['relacion_del_representante']
                parent_guardian_id = row['cedula_del_representante']
                parent_guardian_phone = row['numero_telefonico_del_representante']

                medical_conditions = row.get('condiciones_medicas', None)
                allergies = row.get('alergias', None)
                photo = row.get('foto_carnet', None)

                enrollment_date = row.get('fecha_de_ingreso', None)
                grade_level = row.get('nivel', None)
                grade = row.get('grado', None)
                previous_school = row.get('escuela_anterior', None)
                extracurricular_activities = row.get('actividades_extracurriculares', None)
                disciplinary_record = row.get('registro_disciplinario', None)
                attendance_record = row.get('registro_de_asistencias', None)
                grades = row.get('promedio_de_notas', None)
                scholarships = row.get('becas', None)
                scholarship_details = row.get('detalle_de_becas', None)

                # Insert data into Students Table
                student_sql = '''INSERT INTO Students (first_name, last_name, middle_name, date_of_birth, 
                                gender, nationality, national_id)
                                VALUES (?, ?, ?, ?, ?, ?, ?)'''
                cursor.execute(student_sql,
                               (first_name, last_name, middle_name, date_of_birth, gender, nationality, national_id))
                student_id = cursor.lastrowid

                # Insert data into StudentContactInfo Table
                contact_sql = '''INSERT INTO StudentContactInfo (student_id, address, city, state, country, postal_code)
                                 VALUES (?, ?, ?, ?, ?, ?)'''

                cursor.execute(contact_sql, (student_id, address, city, state, country, postal_code))

                # Insert data into StudentHealthInfo Table
                health_sql = '''INSERT INTO StudentHealthInfo (student_id, emergency_contact_name, 
                emergency_contact_relationship, emergency_contact_phone, emergency_contact_id, father_name, 
                father_id, father_phone, mother_name, mother_id, mother_phone, parent_guardian_names, 
                parent_relationship, parent_guardian_id, parent_guardian_phone, medical_conditions, allergies, 
                photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

                cursor.execute(health_sql, (student_id, emergency_contact_name, emergency_contact_relationship,
                                            emergency_contact_phone, emergency_contact_id, father_name, father_id,
                                            father_phone,
                                            mother_name, mother_id, mother_phone, parent_guardian_names,
                                            parent_relationship,
                                            parent_guardian_id, parent_guardian_phone, medical_conditions, allergies,
                                            photo))

                # Insert data into StudentAcademicInfo Table
                academic_sql = '''INSERT INTO StudentAcademicInfo (student_id, previous_school, 
                                extracurricular_activities, disciplinary_record, attendance_record, 
                                grades, scholarships, scholarship_details, enrollment_date, grade_level, grade)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
                cursor.execute(academic_sql, (
                    student_id, previous_school, extracurricular_activities, disciplinary_record, attendance_record,
                    enrollment_date, grade_level, grade, grades, scholarships, scholarship_details))

                # Commit the changes for each student
                conn.commit()

            except Exception as e:
                print(f"Error processing row {index + 1}: {e}")
                print(f"Row data: {row}")

        console.print("Registro Exitoso\n", style="bold green", justify="center")