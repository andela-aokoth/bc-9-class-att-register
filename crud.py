import sqlite3, datetime

connection = sqlite3.connect('register.db')
run_cursor = connection.cursor()

class Student(object):
	def __init__(self, firstname, lastname):
		self.set_firstname(firstname)
		self.set_lastname(lastname)

	def set_firstname(self, firstname):
		self.firstname = firstname

	def set_lastname(self,lastname):
		self.lastname = lastname

	def get_firstname(self): 
		return self.firstname

	def get_lastname(self):
		return self.lastname

	def save_student(self):
		firstname = self.get_firstname()
		lastname = self.get_lastname()

		add_student_query = '''
		INSERT INTO students (first_name, last_name)
		VALUES ('{first_name}', '{last_name}')
		'''.format(first_name=firstname, last_name=lastname)

		if run_cursor.execute(add_student_query):
			connection.commit()
			return "Student\n" + str(self) + " saved!"
		else:
			return "Error adding student!"

	def get_all_students(self):
		get_all_students_query = '''
		SELECT * FROM students
		'''
		if run_cursor.execute(get_all_students_query):
			students = run_cursor.fetchall()
			return students

	def __str__(self):
		return "First Name: " + self.get_firstname() \
				+ ", Last Name: " + str(self.get_lastname())


class Classes(object):
	def __init__(self, subject):
		self.set_subject(subject)

	def set_subject(self, subject):
		self.subject = subject

	def get_subject(self):
		return self.subject

	def save_class(self):
		subject = self.get_subject()
		add_subject_query = '''
		INSERT INTO classes (subject)
		VALUES ('{subject}'})
		'''.format(subject=subject)

		if run_cursor.execute(add_subject_query):
			connection.commit()
			return str(self) + " saved!"
		else:
			return "Error adding class!"

	def get_all_classes(self):
		get_all_classes_query = '''
		SELECT * FROM classes
		'''

		if run_cursor.execute(get_all_classes_query):
			classes = run_cursor.fetchall()
			return classes

	def __str__(self):
		return "Class Subject: " + self.get_subject()


class ClassInSession(object):
	