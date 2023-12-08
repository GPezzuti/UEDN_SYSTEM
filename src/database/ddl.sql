CREATE TABLE IF NOT EXISTS Students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    middle_name TEXT,
    date_of_birth TEXT NOT NULL,
    gender TEXT NOT NULL,
    nationality TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS StudentContactInfo (
    contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    country TEXT NOT NULL,
    postal_code TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students (student_id)
);

CREATE TABLE IF NOT EXISTS StudentAcademicInfo (
    academic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
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
    tuition_status TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students (student_id),
    FOREIGN KEY (fee_id) REFERENCES MonthlyFeeTable (fee_id)
);

CREATE TABLE IF NOT EXISTS StudentHealthInfo (
    health_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    emergency_contact_name TEXT NOT NULL,
    emergency_contact_relationship TEXT NOT NULL,
    emergency_contact_phone TEXT NOT NULL,
    medical_conditions TEXT,
    allergies TEXT,
    photo TEXT,
    parent_guardian_names TEXT NOT NULL,
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
    enrollment_date TEXT NOT NULL,
    grade_level TEXT NOT NULL,
    grade TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students (student_id),
    FOREIGN KEY (course_id) REFERENCES Courses (course_id)
);

CREATE TABLE IF NOT EXISTS Billing (
    invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    amount REAL,
    payment_method TEXT,
    payment_date TEXT,
    notes TEXT,
    FOREIGN KEY (student_id) REFERENCES Students (student_id)
);

CREATE TABLE IF NOT EXISTS MonthlyFeeTable (
	fee_id INTEGER,
	amount REAL,
	due_day_of_month INTEGER,
	notes TEXT,
	currency TEXT,
	month INTEGER NOT NULL,
	month_desc TEXT NOT NULL,
	type TEXT NOT NULL,
	PRIMARY KEY(fee_id AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS MonthlyFeeTableCatalog (
    catalog_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fee_id INTEGER,
    level TEXT NOT NULL,
    class_level TEXT NOT NULL,
    period TEXT NOT NULL,
    type TEXT NOT NULL,
    FOREIGN KEY (fee_id) REFERENCES MonthlyFeeTable (fee_id)
);

CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    role TEXT NOT NULL  -- e.g., 'admin', 'user'
);
