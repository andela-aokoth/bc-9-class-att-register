"""
	Commands:
		student_add <firstname> <lastname>
		student_remove <student_id>
		student_list
		class_list 
		class_list_all
		class_add <subject>...
		log_start <class_id>
		log_end <class_id>
		check_in <student_id> <class_id>
		check_out <student_id> <class_id> <reason>...
		quit

	Arguments:
		<firstname> Student First Name
		<lastname> Student Last Name
		<student_id> Student ID Number
		<class_id> Class ID Number
		<subject> Subject taught during a specific class
		<reason> Reason provided for checking out a student from class
	Options:
		-h, --help  Show this screen and exit
		--version  Show version
"""

from docopt import docopt, DocoptExit
import cmd
from active_session import ActiveSession
import crud_alchemy
from pyfiglet import Figlet
from old_crud import Student, Classes

def docopt_cmd(func):
	"""
	This decorator is used to simplify the try/except block and pass the result
	of the docopt parsing to the called action
	"""
	def fn(self, arg):
		try:
			opt = docopt(fn.__doc__, arg)

		except DocoptExit as e:
			# The DocoptExit is thrown when the args do not match
			# We print a message to the user and the usage block
			print('Invalid Command!')
			print(e)
			return 

		except SystemExit:
			# The SystemExit exception prints the usage for --help
			# We do not need to do the print here
			return


		return func(self, opt)

	fn.__name__ = func.__name__
	fn.__doc__ = func.__doc__
	fn.__dict__.update(func.__dict__)
	return fn


def introduction():
	print("#" * 160)
	print Figlet(font='bulbhead').renderText('CLASS ATTENDANCE REGISTER')
	print("#" * 160)
	print("Class Attendance Register: This program aids in checking in students ")
	print("in and out of class and also stores basic information about the students ")
	print("and the classes")
	print(__doc__)

class ClassRegister(cmd.Cmd):
	prompt = "<class_register>"

	# Student Commands
	# This command creates a new student in the database and generate an id for the student
	@docopt_cmd
	def do_student_add(self, arg):
		"""Usage: student_add <firstname> <lastname>"""
		firstname = arg["<firstname>"]
		lastname = arg["<lastname>"]
		student_to_save = Student(firstname, lastname)
		print(student_to_save.save_student())

	# This command deletes a student based on the student_id.
	@docopt_cmd
	def do_student_remove(self, arg):
		"""Usage: student_remove <student_id>"""
		student_id = arg["<student_id>"]
		print(crud_alchemy.delete_student(student_id))

	# List all the students and if they're currently in a class
	@docopt_cmd
	def do_student_list(self, arg):
		"""Usage: student_list """
		ActiveSession.get_students_in_class()

	# Class Commands
	@docopt_cmd
	def do_class_add(self, arg):
		"""Usage: class_add <subject>... """
		subject = arg["<subject>"]
		subject_name = ''
		for word in subject:
			subject_name += word + ' '
		# print(subject_name)
		class_to_save = Classes(subject_name.strip())
		print(class_to_save.save_class())

	@docopt_cmd
	def do_class_remove(self, arg):
		"""Usage: class_remove <class_id>"""
		class_id = arg["<class_id>"]
		print(crud_alchemy.delete_class(class_id))

	@docopt_cmd
	def do_class_list_all(self, arg):
		"""Usage: class_list_all """
		ActiveSession.get_all_classes()

	@docopt_cmd
	def do_class_list(self, arg):
		"""Usage: class_list """
		ActiveSession.get_active_classes()

	# Log Commands
	@docopt_cmd
	def do_log_start(self, arg):
		"""Usage: log_start <class_id> """
		class_id = arg["<class_id>"]
		ActiveSession.start_class(int(class_id))

	@docopt_cmd
	def do_log_end(self, arg):
		"""Usage: log_end <class_id> """
		class_id = arg["<class_id>"]
		ActiveSession.end_class(int(class_id))

	# Check In/Out Student
	@docopt_cmd
	def do_check_in(self, arg):
		"""Usage: check_in <student_id> <class_id>"""
		student_id = arg["<student_id>"]
		class_id = arg["<class_id>"]
		print(ActiveSession.check_in_student(int(student_id), int(class_id)))

	@docopt_cmd
	def do_check_out(self, arg):
		"""Usage: check_out <student_id> <class_id> <reason>"""
		student_id = arg["<student_id>"]
		class_id = arg["<class_id>"]
		reasons = arg["<reason>"]
		check_out_reason = ""
		for reason in reasons:
			check_out_reason += reason
		ActiveSession.check_out_student(int(student_id), int(class_id), check_out_reason.strip())

	@docopt_cmd
	def do_quit(self, arg):
		"""Usage: quit"""
		print("Goodbye! ")
		exit()

if __name__ == "__main__":
	introduction()
	ClassRegister().cmdloop()