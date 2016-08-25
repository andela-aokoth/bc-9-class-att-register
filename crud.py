import sqlite3, datetime, time

connection = sqlite3.connect("register.db")
run_cursor = connection.cursor()


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


class ActiveSession(object):
	# dictionary to store; class_id: start_time
	active_classes = {}
	# dictionary to store students in class; class_id: [list_of_students]
	students_in_class = {}

	@staticmethod
	def start_class(class_id):
		start_time = time.asctime(time.localtime(time.time()))

		all_class_ids = Classes.get_all_class_ids()
		if class_id in all_class_ids:
			ActiveSession.active_classes[class_id] = start_time
			print("Class ID: " + str(class_id) + " started\n" \
					+ "Start time: " + str(start_time))
		else:
			print("The class " + str(class_id) + " does not exist!")


	@staticmethod
	def check_in_student(student_id, class_id):
		all_student_ids = Student.get_all_student_ids()
		# print(ActiveSession.active_classes)
		if class_id in ActiveSession.active_classes.keys():
			if student_id in all_student_ids:
				if class_id in ActiveSession.students_in_class.keys():
					if student_id not in ActiveSession.students_in_class[class_id]:
						ActiveSession.students_in_class[class_id].append(student_id)
					else:
						return "Student ID: " + str(student_id) + " already in that class!"
				else:
					ActiveSession.students_in_class[class_id] = [student_id]
					return "Student ID: " + str(student_id) + " checked in to class " + str(class_id)
			else:
				return "Student ID: " + str(student_id) + " does not exist!"
		else:
			return "Class ID: " + str(class_id) + " is not in session!"


	@staticmethod
	def check_out_student(student_id, class_id, reason):
		if class_id in ActiveSession.active_classes.keys():
			students = ActiveSession.students_in_class[class_id]
			if student_id in students:
				print("Checking Out Student ID: " + str(student_id))
				print("Reason: " + reason)
				students.remove(student_id)
			else:
				print("Student ID " + str(student_id) + " is not in that class!")
		else:
			print("Class ID " + str(class_id) + " is not active!")


	@staticmethod
	def get_all_classes():
		all_classes = Classes.get_all_classes()
		# print(all_classes)
		print("-"*42)
		print("Class ID".ljust(15) + "Subject".ljust(15))
		print("-"*42)
		for a_class in all_classes:
			print(str(a_class[0]).ljust(15) + str(a_class[1].ljust(15)))


	@staticmethod
	def get_active_classes():
		if not ActiveSession.active_classes.keys():
			print('There are no active classes!')
		else:
			for class_id in ActiveSession.active_classes.keys():
				class_details = Classes.get_class_details(class_id)
				# print(class_details)
				for class_det in class_details:
					print("In Session")
					print("Class -> " + class_det)

				start_time = ActiveSession.active_classes[class_id]
				print("Start Time: " + start_time)
				if class_id in ActiveSession.students_in_class.keys():
					students = ActiveSession.students_in_class[class_id]
					print("Number of students: " + str(len(students)))
					print("\tStudents in this class")
					for student_id in students:
						print("\tStudent ID: " + str(student_id))


	@staticmethod
	def end_class(class_id):
		end_time = time.asctime(time.localtime(time.time()))
		if class_id in ActiveSession.active_classes.keys():
			ActiveSession.active_classes.pop(class_id)
			print("Class ID -> " + str(class_id) + " ended!")
			print("End Time: " + end_time)


	@staticmethod
	def get_students_in_class():
		all_student_ids = Student.get_all_student_ids()
		student_ids_in_class = []
		
		for class_id in  ActiveSession.students_in_class.keys():
			student_list = ActiveSession.students_in_class[class_id]
			for student in student_list:
				student_ids_in_class.append(student)
		
		print("-"*55)
		print("Student ID".ljust(15) + "First Name".ljust(15) + "Last Name".ljust(15) + "In Class".ljust(15))
		print("-"*55)
		for stud_id in all_student_ids:
			student_details = Student.get_student_details(stud_id)
			# print( student_details[0][1])
			if stud_id not in student_ids_in_class:
				print(str(stud_id).ljust(15) \
					+ student_details[0][0].ljust(15) \
				 	+ student_details[0][1].ljust(15) \
				 	+ "No".ljust(15))
			else:
				print(str(stud_id).ljust(15) \
					+ student_details[0][0].ljust(15) \
					+ student_details[0][1].ljust(15) \
					+ "Yes".ljust(15))

			
def main():
	pass
	# ActiveSession.start_class(1)
	# s1 = Student("Arnold", "Okoth")
	# print(s1)
	# print(str(s1))
	# print(dir(s1))
	# c1 = Classes("Introduction to Programming")
	# ActiveSession.start_class(1)
	# ActiveSession.start_class(2)
	# print("")
	# ActiveSession.check_in_student(1,1)
	# ActiveSession.check_in_student(2,1)
	# ActiveSession.check_in_student(3,2)
	# print("")
	# ActiveSession.get_active_classes()
	# print("")
	# ActiveSession.get_students_in_class()
	# ActiveSession.end_class(1)
	# ActiveSession.get_active_classes()
	# ActiveSession.get_all_classes()


# if __name__ == "__main__":
# 	main()
