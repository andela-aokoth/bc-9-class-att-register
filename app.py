"""
	Usage:
		class_register student_add <firstname> <lastname>
		class_register student_remove <student_id>
		class_register student_list
		class_register class_list <class_id>
		class_register class_list_all
		class_register class_add <subject>...
		class_register log_start <class_id>
		class_register log_end <class_id>
		class_register check_in <student_id> <class_id>
		class_register check_out <student_id> <class_id> <reason>
		class_registe quit
	Options:
		-h, --help  Show this screen and exit
		--version  Show version
"""

from docopt import docopt, DocoptExit
import cmd
from crud import Student, Classes, ActiveSession
import crud_alchemy

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
	print("Command".upper().ljust(20) + "Purpose".upper().ljust(20))
	print("1. student_add:".ljust(20) + "adds a new student to the database".ljust(20))
	print("2. student_remove:".ljust(20) + "deletes a student from the database".ljust(20))
	print("3. student_list:".ljust(20) + "lists all students and if they're in class".ljust(20))
	print("3. class_list_all:".ljust(20) + "lists all classes stored in the database".ljust(20))
	print("4. class_list:".ljust(20) + "prints out a list of active classes".ljust(20))
	print("5. class_list_all:".ljust(20) + "lists all classes in the database".ljust(20))
	print("6. log_start:".ljust(20) + "starts the passed class_id")
	print("7. log_end:".ljust(20) + "ends a time log for an active class")
	print("8. check_in:".ljust(20) + "checks in a student to an active class")
	print("9. check_out:".ljust(20) + "checks out a student from an active class")

class ClassRegister(cmd.Cmd):
	prompt = "<class_register>"

	# Student Commands
	# This command creates a new student in the database and generate an id for the student
	@docopt_cmd
	def do_student_add(self, arg):
		"""Usage: student_add <firstname> <lastname>"""
		firstname = arg["<firstname>"]
		lastname = arg["<lastname>"]
		print(crud_alchemy.save_student(firstname, lastname))

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
		# import ipdb
		# ipdb.set_trace()
		subject = arg["<subject>"]
		subject_name = ''
		for word in subject:
			subject_name += word + ' '
		current_class = Classes(subject_name)
		print(current_class.save_class())

	@docopt_cmd
	def do_class_remove(self, arg):
		"""Usage: class_remove <class_id>"""
		class_id = arg["<class_id>"]
		print(Classes.delete_class(class_id))

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
		reason = arg["<reason>"]
		ActiveSession.check_out_student(int(student_id), int(class_id), reason)

	@docopt_cmd
	def do_quit(self, arg):
		"""Usage: quit"""
		print("Goodbye! ")
		exit()

if __name__ == "__main__":
	introduction()
	ClassRegister().cmdloop()