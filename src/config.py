import os
from pathlib import Path


def get_desktop_path():
    # Get the home directory
    home = Path.home()

    # Append the Desktop folder depending on the OS
    if os.name == 'nt':  # Windows
        desktop = home / 'Desktop'
    elif os.name == 'posix':  # macOS and Linux
        # On macOS, it's also in the home directory
        # On Linux, this might vary, but usually it's in the home directory
        desktop = home / 'Desktop'
    else:
        raise OSError('Unsupported operating system.')

    return desktop


DESKTOP_PATH = get_desktop_path()

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
