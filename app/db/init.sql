/*
    This setup will run whenever the database
    is run for the very first time.

    It is used in the docker-compose.yml file
    under the database service.
*/

-- Create Professors Table.
-- The users are the professors.
CREATE TABLE IF NOT EXISTS professors (
    uid TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
    -- password is not needed as auth is handled in fronted by firebase 
);


-- Create Classes Table
CREATE TABLE IF NOT EXISTS classes (
    class_id SERIAL PRIMARY KEY,
    class_size INT NOT NULL,
    prof_id TEXT NOT NULL, -- foreign key
    schedule TEXT NOT NULL,
    section TEXT NOT NULL,
    subject_name TEXT NOT NULL,
    subject_code TEXT NOT NULL,
    FOREIGN KEY (prof_id) REFERENCES professors(uid) ON DELETE CASCADE
    -- ON DELETE CASCADE: when a prof is deleted, all their classes are
    -- deleted automatically.
);


-- Create Grade Types Table
CREATE TABLE IF NOT EXISTS grade_types (
    grade_type_id SERIAL PRIMARY KEY,
    class_id INT NOT NULL,
    type_name TEXT NOT NULL,
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE
);

-- Create Students Table
CREATE TABLE IF NOT EXISTS students (
    student_number TEXT PRIMARY KEY,
    class_id INT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    course TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE
);

-- Create Assessments Table
CREATE TABLE IF NOT EXISTS assessments (
    grade_id SERIAL PRIMARY KEY,
    class_id INT NOT NULL,
    grade_type_id INT NOT NULL,
    assessment_name TEXT NOT NULL,  -- Renamed from 'grade_name' for clarity
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE,
    FOREIGN KEY (grade_type_id) REFERENCES grade_types(grade_type_id) ON DELETE CASCADE
);

-- Create Scores Table
CREATE TABLE IF NOT EXISTS scores (
    student_number TEXT NOT NULL,
    grade_id INT NOT NULL,
    score INT NOT NULL DEFAULT 0,  -- Default score is 0
    PRIMARY KEY (student_number, grade_id),
    FOREIGN KEY (student_number) REFERENCES students(student_number) ON DELETE CASCADE,
    FOREIGN KEY (grade_id) REFERENCES assessments(grade_id) ON DELETE CASCADE
);


-- Create Attendance dates Table
CREATE TABLE IF NOT EXISTS attendance_dates (
    date_id SERIAL PRIMARY KEY,
    attendance_date DATE NOT NULL UNIQUE,
    class id INT NOT NULL,
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE
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

