class Student(object):
	def __init__(self, firstname, lastname):
		self.firstname = firstname
		self.lastname = lastname


	def save_student(self):
		add_student_query = '''
		INSERT INTO students (first_name, last_name)
		VALUES ('{0}', '{1}')
		'''.format(self.firstname, self.lastname)

		if run_cursor.execute(add_student_query):
			connection.commit()
			return "Student\n" + str(self) + " saved!"
		return "Error adding student!"


	@staticmethod
	def delete_student(student_id):
		delete_student_query = '''
		DELETE FROM students WHERE
		student_id = {0}
		'''.format(student_id)

		if run_cursor.execute(delete_student_query):
			connection.commit()
			return "Student " + str(student_id) + " deleted!"
		return "Error deleting student ID: " + str(student_id)

	@staticmethod
	def get_all_students():
		get_all_students_query = '''
		SELECT * FROM students
		'''
		if run_cursor.execute(get_all_students_query):
			students = run_cursor.fetchall()
			return students

	@staticmethod
	def get_student_details(student_id):
		get_student_details_query = '''
		SELECT first_name, last_name
		FROM students WHERE student_id = {0}
		'''.format(student_id)

		if run_cursor.execute(get_student_details_query):
			student_details = run_cursor.fetchall()
			return student_details

	@staticmethod
	def get_all_student_ids():
		get_all_student_ids_query = '''
		SELECT student_id FROM students
		'''
		if run_cursor.execute(get_all_student_ids_query):
			student_ids = [row[0] for row in run_cursor.fetchall()]
			return student_ids

	def __str__(self):
		return "First Name: " + self.firstname \
				+ ", Last Name: " + str(self.lastname)

class Classes(object):
	def __init__(self, subject):
		self.subject = subject


	def save_class(self):
		subject = self.subject
		add_subject_query = '''
		INSERT INTO classes (subject)
		VALUES ('{0}')
		'''.format(self.subject)

		if run_cursor.execute(add_subject_query):
			connection.commit()
			return str(self) + " saved!"
		return "Error adding class!"

	@staticmethod
	def delete_class(class_id):
		delete_class_query = '''
		DELETE FROM classes
		WHERE class_id = {0}
		'''.format(class_id)

		if run_cursor.execute(delete_class_query):
			connection.commit()
			return str(class_id) + " deleted!"
		return "Error deleting class ID: " + str(class_id)

	@staticmethod
	def get_all_classes():
		get_all_classes_query = '''
		SELECT * FROM classes
		'''

		if run_cursor.execute(get_all_classes_query):
			classes = run_cursor.fetchall()
			return classes


	@staticmethod
	def get_all_class_ids():
		get_all_class_ids_query = '''
		SELECT class_id FROM classes
		'''
		if run_cursor.execute(get_all_class_ids_query):
			class_ids = [row[0] for row in run_cursor.fetchall()]
			return class_ids
	

	@staticmethod
	def get_class_details(class_id):
		get_class_details_query = '''
		SELECT subject FROM classes WHERE class_id = {0}
		'''.format(class_id)

		if run_cursor.execute(get_class_details_query):
			class_details = [row[0] for row in run_cursor.fetchall()]
			return class_details


	def __str__(self):
		return "Class Subject: " + self.subject