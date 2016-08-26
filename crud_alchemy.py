from sqlalchemy.orm import sessionmaker
from db_structure import Student, Classes
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


engine = create_engine("sqlite:///register.db")

Base = declarative_base()

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Functions for students table
def save_student(firstname, lastname):
	add_student = Student(first_name=firstname, last_name=lastname)
	session.commit()
	return "Student: " + firstname + " " + lastname + " saved!"

def delete_student(student_id):
	session.query(Student).filter_by(student_id=student_id).delete()
	session.commit()
	return "Student ID: " + str(student_id) + " deleted!"

def get_all_students():
	students = []
	students_rows = session.query(Student).all()
	for students_row in students_rows:
		students.append((students_row.student_id, students_row.first_name, students_row.last_name))

	return students


def get_student_details(student_id):
	student_details = []
	details_rows = session.query(Student).filter_by(student_id=student_id).all()
	for details_row in details_rows:
		student_details.append((details_row.first_name, details_row.last_name))

	return student_details

def get_all_student_ids():
	student_ids = []
	id_rows = session.query(Student).all()
	for id_row in id_rows:
		student_ids.append(id_row.student_id)

	return student_ids

# Functions for classes table
def save_class(subject):
	subject = subject.strip()
	add_class = Classes(subject=subject)
	session.commit()
	return str(subject) + " saved!"

def get_all_classes():
	classes = []
	class_rows = session.query(Classes).all()
	for class_row in class_rows:
		classes.append((class_row.class_id, class_row.subject))

	return classes

def delete_class(class_id):
	session.query(Classes).filter_by(class_id=student_id).delete()
	session.commit()
	return "Class ID: " + str(class_id) + " deleted!"

def get_class_details(class_id):
	class_details = []
	details_rows = session.query(Classes).filter_by(class_id=class_id).all()
	for details_row in details_rows:
		class_details.append(details_row.subject)

	return class_details

def get_all_class_ids():
	class_ids = []
	id_rows = session.query(Classes).all()
	for id_row in id_rows:
		class_ids.append(id_row.class_id)

	return class_ids
