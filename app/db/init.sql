/*
    This setup will run whenever the database
    is run for the very first time.

    It is used in the docker-compose.yml file
    under the database service.
*/

-- Create Professors Table
CREATE TABLE IF NOT EXISTS professors (
    uid TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    -- password is not needed as auth is handled in fronted by firebase 
);

-- Create Classes Table
CREATE TABLE IF NOT EXISTS classes (
    class_id SERIAL PRIMARY KEY,
    prof_id TEXT NOT NULL, -- foreign key
    schedule TEXT NOT NULL,
    section TEXT NOT NULL,
    subject_name TEXT NOT NULL,
    subject_code TEXT NOT NULL,
    FOREIGN KEY (prof_id) REFERENCES professors(uid) ON DELETE CASCADE
    -- ON DELETE CASCADE: when a prof is deleted, all their classes are
    -- deleted automatically.
);

-- Create Grade_types Table
CREATE TABLE IF NOT EXISTS grade_types (
    class_id TEXT NOT NULL,
    type_name TEXT NOT NULL,
    quantity INT NULL NULL,
    PRIMARY KEY (class_id, type_name),
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);

-- Create Grades Table
CREATE TABLE IF NOT EXISTS grades (
    class_id TEXT NOT NULL,
    type_name TEXT NOT NULL,
    score INT NOT NULL,
    student_number TEXT NOT NULL,
    FOREIGN KEY (class_id, type_name) REFERENCES grade_types(class_id, type_name),
    FOREIGN KEY (student_number) REFERENCES students(student_number) ON DELETE CASCADE
);

-- Create Students Table
CREATE TABLE IF NOT EXISTS students (
    student_number TEXT PRIMARY KEY,
    class_id TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    course TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
);

-- Create Attendance dates Table
CREATE TABLE IF NOT EXISTS attendance_dates (
    date_id SERIAL PRIMARY KEY,
    attendance_date DATE NOT NULL UNIQUE 
);

-- Create Attendance records table
CREATE TABLE IF NOT EXISTS attendance_records (
    record_id SERIAL PRIMARY KEY,
    student_number TEXT NOT NULL,
    date_id INT NOT NULL,
    record_status TEXT NOT NULL,
    FOREIGN KEY (student_number) REFERENCES students(student_number),
    FOREIGN KEY (date_id) REFERENCES attendance_dates(date_id)
);

