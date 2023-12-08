from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import bcrypt


@dataclass
class User:
    user_id: int
    username: str
    hashed_password: str  # Store only hashed passwords
    role: str

    def verify_password(self, input_password):
        return bcrypt.checkpw(input_password.encode(), self.hashed_password.encode())


@dataclass
class StudentBasicInfo:
    # Basic identification
    student_id: int  # Unique identifier for the student
    first_name: str  # Student's first name
    last_name: str  # Student's last name
    date_of_birth: datetime  # Student's date of birth
    gender: str  # Student's gender
    nationality: str  # Student's nationality
    middle_name: Optional[str] = None  # Student's middle name, if any


@dataclass
class StudentContactInfo:
    # Contact information
    student_id: int  # Unique identifier for the student
    email: str  # Student's email address
    phone_number: str  # Student's phone number
    address: str  # Student's residential address
    city: str  # City of the student's residence
    state: str  # State of the student's residence
    country: str  # Country of the student's residence
    postal_code: str  # Postal code of the student's residence


@dataclass
class StudentAcademicInfo:
    # Academic information
    academic_id: int
    student_id: int
    previous_school: Optional[str] = None
    extracurricular_activities: Optional[str] = None
    disciplinary_record: Optional[str] = None
    attendance_record: Optional[str] = None
    grades: Optional[str] = None
    scholarships: Optional[str] = None
    scholarship_details: Optional[str] = None
    school_email: Optional[str] = None
    login_credentials: Optional[str] = None


@dataclass
class StudentBillingInfo:
    # Billing information
    student_id: int
    fee_id: str  # Identifier for monthly fee structure
    tuition_status: Optional[str] = None  # Status of tuition payments


@dataclass
class StudentHealthInfo:
    # Health and emergency information
    health_id: int
    student_id: int
    emergency_contact_name: str
    emergency_contact_relationship: str
    emergency_contact_phone: str
    parent_guardian_names: str
    medical_conditions: Optional[str] = None
    allergies: Optional[str] = None
    photo: Optional[str] = None


@dataclass
class Teacher:
    teacher_id: int  # Unique identifier for the teacher
    first_name: str  # Teacher's first name
    last_name: str  # Teacher's last name
    email: str  # Teacher's email address
    phone_number: str  # Teacher's phone number
    department: str  # Department to which the teacher belongs
    middle_name: Optional[str] = None  # Teacher's middle name, if any
    qualifications: Optional[List[str]] = None  # List of qualifications


@dataclass
class Course:
    course_id: int  # Unique identifier for the course
    name: str  # Name of the course
    teacher_id: int  # ID of the teacher assigned to the course
    schedule: str  # Schedule details (e.g., "Mon-Wed 10:00-12:00")
    description: Optional[str] = None  # Brief description of the course


@dataclass
class Enrollment:
    enrollment_id: int  # Unique identifier for the enrollment
    student_id: int  # ID of the enrolled student
    course_id: int  # ID of the course in which the student is enrolled
    enrollment_date: datetime  # Date of enrollment
    grade: Optional[str] = None  # Grade (if applicable)


@dataclass
class Billing:
    invoice_id: int
    student_id: int
    amount_due: float
    payment_method: Optional[str] = None
    payment_date: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class MonthlyFeeTable:
    fee_id: int
    amount: float
    due_day_of_month: int
    currency: str
    month: int
    month_desc: str
    type: str
    notes: Optional[str] = None


@dataclass
class MonthlyFeeTableCatalog:
    catalog_id: int  # Catalog ID
    fee_id: str  # Unique identifier for the fee structure
    level: str  # Basic, Primary or Secondary
    class_level: str  # Class level the fee applies to, i.e: 1st, 2nd
    period: str  # 2023-2024, ...
    type: str  # Base or Customized
