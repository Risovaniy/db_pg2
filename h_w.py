from pprint import pprint
import psycopg2 as pg2


def create_db():  # создает таблицы
    curs.execute("""CREATE TABLE IF NOT EXISTS Student(
        id serial PRIMARY KEY,
        name varchar(100) NOT NULL,
        gpa numeric (4,2),
        berth timestamp with time zone);
        """)

    curs.execute("""CREATE TABLE IF NOT EXISTS Course(
        id serial PRIMARY KEY,
        name varchar(100) NOT NULL);
        """)

    curs.execute("""CREATE TABLE IF NOT EXISTS student_course(
        id serial PRIMARY KEY,
        id_student integer REFERENCES Student(id),
        id_course integer REFERENCES Course(id));
        """)

    conn.commit()


def get_students(course_id):  # возвращает студентов определенного курса
    curs.execute("SELECT * FROM student_course WHERE id_course = %s;", (course_id, ))
    students = curs.fetchall()
    students_on_course = []
    for student in students:
        print(get_student(student))
        students_on_course += get_student(student)


def add_students(course_id, students):  # создает студентов и
    # записывает их на курс
    for student in students:
        add_student(student)
    try:
        for student in students:
            curs.execute("""INSERT INTO student_course (id_student, id_course)
                    VALUES (%s, %s);""", (student[id], course_id))
    except Exception as e:
        print('"add_students" failed')
        pprint(e)
        conn.rollback()
    else:
        conn.commit()


def add_student(student):  # просто создает студента
    name = student['name']
    gpa = student['gpa']
    berth = student['berth']
    try:
        curs.execute("""INSERT INTO Student (name, gpa, berth)
        VALUES (%s, %s, %s);""", (name, gpa, berth))
    except Exception as e:
        print('"add_student" failed')
        pprint(e)
        conn.rollback()
    else:
        conn.commit()



def get_student(student_id):
    curs.execute("""
        SELECT * FROM Student
        WHERE Student.id = %s;""", (student_id, )
                 )
    student_info = curs.fetchall()
    return student_info


with pg2.connect(
        dbname='netology_db',
        user='risovan',
        password='2506'
) as conn:
    with conn.cursor() as curs:
        create_db()