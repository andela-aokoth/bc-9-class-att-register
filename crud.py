import sqlite3, datetime, time

connection = sqlite3.connect("register.db")
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

	@staticmethod
	def get_all_students():
		get_all_students_query = '''
		SELECT * FROM students
		'''
		if run_cursor.execute(get_all_students_query):
			students = run_cursor.fetchall()
			return students

	@staticmethod
	def get_all_student_ids():
		get_all_student_ids_query = '''
		SELECT student_id FROM students
		'''
		if run_cursor.execute(get_all_student_ids_query):
			student_ids = [row[0] for row in run_cursor.fetchall()]
			return student_ids

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
		VALUES ('{subject}')
		'''.format(subject=subject)

		if run_cursor.execute(add_subject_query):
			connection.commit()
			return str(self) + " saved!"
		else:
			return "Error adding class!"

	@staticmethod
	def get_all_classes():
		get_all_classes_query = '''
		SELECT * FROM classes
		'''

		if run_cursor.execute(get_all_classes_query):
			classes = [row[0] for row in run_cursor.fetchall()]
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
		SELECT subject FROM classes WHERE class_id = {class_id}
		'''.format(class_id=class_id)

		if run_cursor.execute(get_class_details_query):
			class_details = [row[0] for row in run_cursor.fetchall()]
			return class_details


	def __str__(self):
		return "Class Subject: " + self.get_subject()

class ClassInSession(object):
	# dictionary to store: id: class_id, subject: subject, start_time, end_time]
	active_classes = {}
	# dictionary to store students in class: class_id [list_of_students]
	students_in_class = {}

	@staticmethod
	def start_class(class_id):
		start_time = time.asctime(time.localtime(time.time()))

		all_class_ids = Classes.get_all_class_ids()

		if class_id in all_class_ids:
			ClassInSession.active_classes[class_id] = [start_time]
			print("Class ID: " + str(class_id) + " started\n" \
					+ "Start time: " + str(start_time))
		else:
			return "The class " + str(class_id) + " does not exist!"


	@staticmethod
	def check_in_student(student_id, class_id):
		all_student_ids = Student.get_all_student_ids()
		if class_id in ClassInSession.active_classes.keys():
			if student_id in all_student_ids:
				# ClassInSession.students_in_class[class_id] = [student_id]
				if class_id in ClassInSession.students_in_class.keys():
					if student_id not in ClassInSession.students_in_class[class_id]:
						ClassInSession.students_in_class[class_id].append(student_id)
					else:
						print("Student ID: " + str(student_id) + " already in that class!")
				else:
					ClassInSession.students_in_class[class_id] = [student_id]
					print("Student ID: " + str(student_id) + " checked in to class " + str(class_id))
			else:
				print("Student ID: " + str(student_id) + " does not exist!")
		else:
			print("Class ID: " + str(class_id) + " is not in session!")


	@staticmethod
	def check_out_student(student_id, class_id, reason):
		if class_id in ClassInSession.active_classes.keys():
			students = ClassInSession.students_in_class[class_id]
			if student_id in students:
				students.remove(student_id)
			else:
				print("Student ID " + str(student_id) + " is not in that class!")
		else:
			print("Class ID " + str(class_id) + " is not active!")


	@staticmethod
	def get_active_classes():
		if not ClassInSession.active_classes.keys():
			print('There are no active classes!')
		else:
			for class_id in ClassInSession.active_classes.keys():
				class_details = Classes.get_class_details(class_id)
				# print(class_details)
				for class_det in class_details:
					print("In Session")
					print("Class -> " + class_det)

				start_time = ClassInSession.active_classes[class_id]
				print("\tStart Time: " + start_time[0])
				print("\tStudents in this class")
				students = ClassInSession.students_in_class[class_id]
				for student_id in students:
					# print("\t" + "-" * 20)
					print("\tStudent ID: " + str(student_id))
					# print("\t" + "-" * 20)


	@staticmethod
	def end_class(class_id):
		end_time = time.asctime(time.localtime(time.time()))
		if class_id in ClassInSession.active_classes.keys():
			ClassInSession.active_classes.pop(class_id)
			print("Class ID -> " + str(class_id) + " ended!")
			print("End Time: " + end_time)

			
def main():
	ClassInSession.start_class(1)
	ClassInSession.start_class(2)
	print("")
	ClassInSession.check_in_student(1,1)
	ClassInSession.check_in_student(2,1)
	ClassInSession.check_in_student(3,2)
	print("")
	ClassInSession.get_active_classes()
	print("")
	# ClassInSession.end_class(1)
	# ClassInSession.get_active_classes()


if __name__ == "__main__":
	main()
