from pathlib import Path
from src.utils.helpers import get_desktop_path

DESKTOP_PATH = get_desktop_path()
DB_PATH = Path('../src/database/school_management_system_v2.db').resolve()
FILE_PATH = DESKTOP_PATH / 'Información de contacto.csv'

STUDENTS_COLUMNS = [
    # Columns from the Students table
    "student_id", "first_name", "last_name", "middle_name", "date_of_birth", "gender", "nationality",

    # Columns from the StudentContactInfo table
    # "email", "phone_number", "address", "city", "state", "country", "postal_code",

    # Columns from the StudentAcademicInfo table
    #    "previous_school", "extracurricular_activities", "disciplinary_record", "attendance_record",
    #    "grades", "scholarships", "scholarship_details", "school_email", "login_credentials",

    # Columns from the StudentBillingInfo table
    "tuition_status",

    # Columns from the StudentHealthInfo table
    #    "emergency_contact_name", "emergency_contact_relationship", "emergency_contact_phone",
    #    "medical_conditions", "allergies", "photo", "parent_guardian_names"
]
