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
    assessment_id SERIAL PRIMARY KEY,
    class_id INT NOT NULL,
    grade_type_id INT NOT NULL,
    assessment_name TEXT NOT NULL,  -- Renamed from 'grade_name' for clarity
    total_items INT NOT NULL DEFAULT 0,
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE,
    FOREIGN KEY (grade_type_id) REFERENCES grade_types(grade_type_id) ON DELETE CASCADE
);

-- Create Scores Table
CREATE TABLE IF NOT EXISTS scores (
    student_number TEXT NOT NULL,
    assessment_id INT NOT NULL,
    score INT NOT NULL DEFAULT 0,  -- Default score is 0
    PRIMARY KEY (student_number, assessment_id),
    FOREIGN KEY (student_number) REFERENCES students(student_number) ON DELETE CASCADE,
    FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id) ON DELETE CASCADE
);


-- Create Attendance dates Table
CREATE TABLE IF NOT EXISTS attendance_dates (
    date_id SERIAL PRIMARY KEY,
    attendance_date DATE NOT NULL UNIQUE,
    class_id INT NOT NULL,
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



-- INSERTING DUMMY DATA

INSERT INTO professors (uid, first_name, last_name, email) 
		VALUES ('a21', 'Busa', 'Ku', 'KuBusa69@yahoo.com');

INSERT INTO classes (class_size, prof_id, schedule, section, subject_name, subject_code)
		VALUES (30, 'a21', '3-4 MTH', 'COM231', 'Spot a gay', 'SPGx01');

INSERT INTO students (student_number,  class_id, first_name, last_name, course, email)
		VALUES ('2023-103824', 1, 'Luis Ryan', 'Sanisit', 'BSCS-ML', 'ryansanisit19@gmail.com');

INSERT INTO grade_types (class_id, type_name) 
		VALUES (1, 'Quiz');

INSERT INTO assessments (class_id, grade_type_id, assessment_name, total_items)
		VALUES (1, 1, 'Quiz 1: Spot a gay', 25);

INSERT INTO scores(student_number, assessment_id, score)
		VALUES ('2023-103824', 1, 20);

INSERT INTO attendance_dates (attendance_date, class_id)
		VALUES ('2025-02-25', 1);

INSERT INTO attendance_dates (attendance_date, class_id)
		VALUES ('2025-02-25', 1);
