from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


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
    student_id: int
    enrollment_date: datetime  # Date of student's enrollment
    grade_level: str  # Grade level
    previous_school: Optional[str] = None  # Name of the previous school attended
    extracurricular_activities: Optional[List[str]] = None  # List of extracurricular activities
    disciplinary_record: Optional[List[str]] = None  # Record of disciplinary actions
    attendance_record: Optional[List[str]] = None  # Record of attendance
    grades: Optional[dict] = None  # Academic grades
    scholarships: Optional[List[str]] = None  # Information about scholarships received
    scholarship_details: Optional[str] = None  # Details of any scholarships or financial aid
    school_email: Optional[str] = None  # School-issued email address
    login_credentials: Optional[dict] = None  # Credentials for accessing school systems


@dataclass
class StudentBillingInfo:
    # Billing information
    student_id: int
    fee_id: str  # Identifier for monthly fee structure
    tuition_status: Optional[str] = None  # Status of tuition payments


@dataclass
class StudentHealthInfo:
    # Helth and emergency information
    student_id: int
    emergency_contact_name: Optional[str] = None  # Name of emergency contact
    emergency_contact_relationship: Optional[str] = None  # Relationship to the student
    emergency_contact_phone: Optional[str] = None  # Emergency contact phone number
    medical_conditions: Optional[str] = None  # Known medical conditions
    allergies: Optional[str] = None  # Known allergies
    photo: Optional[str] = None  # Link to a photograph of the student
    parent_guardian_names: Optional[List[str]] = None  # Names of parents or guardians


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
    invoice_id: int  # Unique identifier for the invoice
    student_id: int  # ID of the student being billed
    amount_due: float  # Amount due
    due_date: datetime  # Due date for the payment, determined by the fee table
    status: str  # Payment status (e.g., "Paid", "Pending", "Overdue")
    payment_method: Optional[str] = None  # Bank transfer, cash, etc
    payment_date: Optional[datetime] = None  # Date payment was made
    notes: Optional[str] = None


@dataclass
class MonthlyFeeTable:
    fee_id: str  # Unique identifier for the fee structure
    student_id: int  # ID of the student being billed
    amount: float  # Amount to be paid
    month: dict  # 01: Jan, 02: Feb, ...
    due_day_of_month: int  # Day of the month when payment is due
    notes: Optional[str] = None
    currency: str = "USD"


@dataclass
class MonthlyFeeTableCatalog:
    catalog_id: int  # Catalog ID
    fee_id: str  # Unique identifier for the fee structure
    level: str  # Basic, Primary or Secondary
    class_level: str  # Class level the fee applies to, i.e: 1st, 2nd
    period: str  # 2023-2024, ...
    type: str  # Base or Customized
