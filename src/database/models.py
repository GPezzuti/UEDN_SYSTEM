from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


# TODO: Add validation on all classes or use a filling form
@dataclass
class User:
    user_id: int
    username: str
    hashed_password: str  # Store only hashed passwords
    role: str

    def is_admin(self):
        """Check if the user is an admin."""
        return self.role == 'admin'


@dataclass
class StudentBasicInfo:
    # Basic identification
    student_id: int  # Unique identifier for the student
    first_name: str  # Student's first name
    last_name: str  # Student's last name
    date_of_birth: datetime  # Student's date of birth
    gender: str  # Student's gender
    nationality: str  # Student's nationality
    national_id: Optional[int] = None  # Student's national ID
    middle_name: Optional[str] = None  # Student's middle name, if any


@dataclass
class StudentContactInfo:
    # Contact information
    student_id: int  # Unique identifier for the student
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
    enrollment_date: str
    grade_level: str
    grade: str
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
    billing_id: int
    student_id: int
    fee_id: str  # Identifier for monthly fee structure
    tuition_status: str  # Status of tuition payments


@dataclass
class StudentHealthInfo:
    # Health and emergency information
    health_id: int
    student_id: int
    emergency_contact_name: str
    emergency_contact_relationship: str
    emergency_contact_phone: str
    emergency_contact_id: int
    father_name: str
    father_phone: str
    father_id: int
    mother_name: str
    mother_phone: str
    mother_id: int
    parent_guardian_names: str
    parent_contact_relationship: str
    parent_guardian_phone: str
    parent_guardian_id: str
    medical_conditions: Optional[str] = None
    allergies: Optional[str] = None
    photo: Optional[str] = None


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
    level: str  # Basic, Primary or Secondary
    class_level: str  # Class level the fee applies to, i.e: 1st, 2nd
    period: str  # 2023-2024, ...
    type: str  # Base or Customized
