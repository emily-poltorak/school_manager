from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

engine = create_engine('postgresql://admin:12345@localhost/tech_track_db')
Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(Integer)

    enrollments = relationship("Enrollment", back_populates="student")

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    subject = Column(String)

    classes_taught = relationship("Class", back_populates="teacher")

class Class(Base):
    __tablename__ = 'classes'
    subject = Column(String, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))

    teacher = relationship("Teacher", back_populates="classes_taught")
    students = relationship("Enrollment", back_populates="class_info")

class Enrollment(Base):
    __tablename__ = 'enrollments'
    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    subject = Column(String, ForeignKey('classes.subject'), primary_key=True)

    student = relationship("Student", back_populates="enrollments")
    class_info = relationship("Class", back_populates="students")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def insert_into_students(name, age, grade):
    existing_student = session.query(Student).filter_by(name=name).first()

    if existing_student is None:
        new_record = Student(name=name, age=age, grade=grade)
        session.add(new_record)
        session.commit()

def insert_into_teachers(name, subject):
    existing_teacher = session.query(Teacher).filter_by(name=name).first()

    if existing_teacher is None:
        new_record = Teacher(name=name, subject=subject)
        session.add(new_record)
        session.commit()

        new_class = Class(subject=subject, teacher_id=new_record.id)
        session.add(new_class)
        session.commit()

def enroll_student(id, subject):
    student = session.query(Student).get(id)
    class_info = session.query(Class).filter_by(subject = subject).first()

    if student and class_info:
        existing_enrollment = session.query(Enrollment).filter_by(student_id = student.id, subject= class_info.subject).first()

        if existing_enrollment:
            print(f"Student with ID {student.id} is already enrolled in the class '{class_info.subject}'.")
        else:
            
            new_enrollment = Enrollment(student_id = student.id, subject = class_info.subject)
            session.add(new_enrollment)
            session.commit()

            print(f"Student with ID {student.id} enrolled successfully in the class '{class_info.subject}'.")
    else:
        print("Student or class not found. Please check the student ID and class subject.")


        
def update_record(entity_type, id, new_name=None, new_age=None, new_grade=None, new_subject=None):
    if entity_type == "student":
        record = session.query(Student).get(id)
        if record:
            if new_name is not None and new_name != "":
                record.name = new_name
            if new_age is not None and new_age != -1:
                record.age = new_age
            if new_grade is not None and new_grade != -1:
                record.grade = new_grade
            session.commit()
            print(f"Student with ID {id} updated successfully.")
        else:
            print(f"Student with ID {id} not found.")

    elif entity_type == "teacher":
        record = session.query(Teacher).get(id)
        if record:
            if new_name is not None and new_name != "":
                record.name = new_name
            if new_subject is not None and new_subject != "":
                record.subject = new_subject
            session.commit()
            print(f"Teacher with ID {id} updated successfully.")
        else:
            print(f"Teacher with ID {id} not found.")

def delete_record(entity_type, id):
    if entity_type == "student":
        record = session.query(Student).get(id)
        if record:
            session.delete(record)
            session.commit()
            print(f"Student with ID {id} deleted successfully.")
        else:
            print(f"Student with ID {id} not found.")

    elif entity_type == "teacher":
        record = session.query(Teacher).get(id)
        if record:
            session.delete(record)
            session.commit()
            print(f"Teacher with ID {id} deleted successfully.")
        else:
            print(f"Teacher with ID {id} not found.")

    else:
        print("Invalid entity type. Use 'student' or 'teacher'.")

def user_interface():
    while True:

        print("\nSelect an option:")
        print("(1) Insert student")
        print("(2) Insert teacher")
        print("(3) Update a student")
        print("(4) Update a teacher")
        print("(5) Delete a student")
        print("(6) Delete a teacher")
        print("(7) Enroll a student")
        print("(8) Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter student name: ").capitalize()
            age = int(input("Enter student age: "))
            grade = int(input("Enter student grade: "))
            insert_into_students(name, age, grade)

        elif choice == "2":
            name = input("Enter teacher name: ").capitalize()
            subject = input("Enter teacher subject: ").capitalize()
            insert_into_teachers(name, subject)

        elif choice == "3":
            student_id = int(input("Enter student ID to update: "))
            new_name = input("Enter new student name (press Enter to skip): ").capitalize()
            new_age = int(input("Enter new student age (press Enter to skip): ") or -1)
            new_grade = int(input("Enter new student grade (press Enter to skip): ") or -1)
            update_record("student", student_id, new_name, new_age, new_grade)

        elif choice == "4":
            teacher_id = int(input("Enter teacher ID to update: "))
            new_name = input("Enter new teacher name (press Enter to skip): ")
            new_subject = input("Enter new teacher subject (press Enter to skip): ").capitalize()
            update_record("teacher", teacher_id, new_name, new_subject)

        elif choice == "5":
            student_id = int(input("Enter student ID to delete: "))
            delete_record("student", student_id)

        elif choice == "6":
            teacher_id = int(input("Enter teacher ID to delete: "))
            delete_record("teacher", teacher_id)

        elif choice == "7":
            student_id = int(input("Enter student ID to enroll: "))
            subject = input("Enter class subject to enroll in: ").upper()
            enroll_student(student_id, subject)
        
        elif choice == "8":
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    user_interface()