CREATE TABLE IF NOT EXISTS Students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    middle_name TEXT,
    date_of_birth TEXT,
    gender TEXT,
    nationality TEXT
);

CREATE TABLE IF NOT EXISTS StudentContactInfo (
    contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    email TEXT,
    phone_number TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    postal_code TEXT,
    FOREIGN KEY (student_id) REFERENCES Students (student_id)
);

CREATE TABLE IF NOT EXISTS StudentAcademicInfo (
    academic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    enrollment_date TEXT,
    grade_level TEXT,
    previous_school TEXT,
    extracurricular_activities TEXT,
    disciplinary_record TEXT,
    attendance_record TEXT,
    grades TEXT,
    scholarships TEXT,
    scholarship_details TEXT,
    school_email TEXT,
    login_credentials TEXT,
    FOREIGN KEY (student_id) REFERENCES Students (student_id)
);

CREATE TABLE IF NOT EXISTS StudentBillingInfo (
    billing_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    fee_id INTEGER,
    tuition_status TEXT,
    FOREIGN KEY (student_id) REFERENCES Students (student_id),
    FOREIGN KEY (fee_id) REFERENCES MonthlyFeeTable (fee_id)
);

CREATE TABLE IF NOT EXISTS StudentHealthInfo (
    health_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    emergency_contact_name TEXT,
    emergency_contact_relationship TEXT,
    emergency_contact_phone TEXT,
    medical_conditions TEXT,
    allergies TEXT,
    photo TEXT,
    parent_guardian_names TEXT,
    FOREIGN KEY (student_id) REFERENCES Students (student_id)
);

CREATE TABLE IF NOT EXISTS Teachers (
    teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    middle_name TEXT,
    email TEXT,
    phone_number TEXT,
    department TEXT,
    qualifications TEXT
);

CREATE TABLE IF NOT EXISTS Courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    teacher_id INTEGER,
    schedule TEXT,
    description TEXT,
    FOREIGN KEY (teacher_id) REFERENCES Teachers (teacher_id)
);

CREATE TABLE IF NOT EXISTS Enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    enrollment_date TEXT,
    grade TEXT,
    FOREIGN KEY (student_id) REFERENCES Students (student_id),
    FOREIGN KEY (course_id) REFERENCES Courses (course_id)
);

CREATE TABLE IF NOT EXISTS Billing (
    invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    amount_due REAL,
    due_date TEXT,
    status TEXT,
    payment_method TEXT,
    payment_date TEXT,
    notes TEXT,
    FOREIGN KEY (student_id) REFERENCES Students (student_id)
);

CREATE TABLE IF NOT EXISTS MonthlyFeeTable (
    fee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    due_day_of_month INTEGER,
    notes TEXT,
    currency TEXT
);
