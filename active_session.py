import sqlite3, datetime, time
import crud_alchemy

connection = sqlite3.connect("register.db")
run_cursor = connection.cursor()


class ActiveSession(object):
	# dictionary to store; class_id -> start_time
	active_classes = {}
	# dictionary to store students in class; class_id -> [list_of_students]
	students_in_class = {}

	class_logs = []

	@staticmethod
	def start_class(class_id):
		start_time = time.asctime(time.localtime(time.time()))

		all_class_ids = crud_alchemy.get_all_class_ids()
		if class_id in all_class_ids:
			ActiveSession.active_classes[class_id] = start_time
			print("Class ID: " + str(class_id) + " started\n" \
					+ "Start time: " + str(start_time))
		else:
			print("The class " + str(class_id) + " does not exist!")


	@staticmethod
	def check_in_student(student_id, class_id):
		all_student_ids = crud_alchemy.get_all_student_ids()
		student_ids_in_class = []
		for class_id in  ActiveSession.students_in_class.keys():
			student_list = ActiveSession.students_in_class[class_id]
			for student in student_list:
				student_ids_in_class.append(student)

		if class_id in ActiveSession.active_classes.keys() and student_id in all_student_ids:
			if class_id in ActiveSession.students_in_class.keys():
				if student_id not in student_ids_in_class:
					ActiveSession.students_in_class[class_id].append(student_id)
				else:
					return "Student ID: " + str(student_id) + " already in a class!"
			else:
				ActiveSession.students_in_class[class_id] = [student_id]
			return "Student ID: " + str(student_id) + " checked in to class " + str(class_id)
			
		else:
			return "Class ID/Student ID" + str(class_id) + "does not exist!"


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
		all_classes = crud_alchemy.get_all_classes()
		print("\t" + "-"*42)
		print("\tCLASS ID".ljust(15) + "SUBJECT".ljust(16))
		print("\t" +"-"*42)
		for a_class in all_classes:
			print("\t" + str(a_class[0]).ljust(15) + str(a_class[1].ljust(16)))


	@staticmethod
	def get_active_classes():
		if not ActiveSession.active_classes.keys():
			print('\tThere are currently no active classes!')
		else:
			for class_id in ActiveSession.active_classes.keys():
				class_details = crud_alchemy.get_class_details(class_id)
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
		else:
			print("Class ID: " + str(class_id) + " not in session!")


	@staticmethod
	def get_students_in_class():
		all_student_ids = crud_alchemy.get_all_student_ids()
		student_ids_in_class = []
		
		for class_id in  ActiveSession.students_in_class.keys():
			student_list = ActiveSession.students_in_class[class_id]
			for student in student_list:
				student_ids_in_class.append(student)
		
		print("-"*55)
		print("Student ID".ljust(15) + "First Name".ljust(15) + "Last Name".ljust(15) + "In Class".ljust(15))
		print("-"*55)
		for stud_id in all_student_ids:
			student_details = crud_alchemy.get_student_details(stud_id)
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
