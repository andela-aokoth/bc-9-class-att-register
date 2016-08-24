"""
	Usage:
		class_register student_add <firstname> <lastname>
		class_register student_remove <student_id>
		class_register class_list <class_id>
		class_register class_add -s <subject>
		class_register log_start <class_id>
		class_register log_end <class_id>
		class_register check_in <student_id> <class_id>
		class_register check_out <student_id> <class_id> <reason>
	Options:
		-h, --help Show this screen and exit
		--version Show version
"""

from docopt import docopt, DocoptExit
import cmd
from crud import Student, Classes, ActiveSession

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


class ClassRegister(cmd.Cmd):
	prompt = "<class_register>"

	# Student Commands
	# This command creates a new student in the database and generate an id for the student
	@docopt_cmd
	def do_student_add(self, arg):
		"""Usage: student_add <firstname> <lastname>"""
		pass

	# This command deletes a student based on the student_id.
	@docopt_cmd
	def do_student_remove(self, arg):
		pass

	# List all the students and if they're currently in a class
	@docopt_cmd
	def do_student_list(self, arg):
		"""Usage: student_list """
		pass

	# Class Commands
	@docopt_cmd
	def do_class_add(self, arg):
		"""Usage: class_add -s <subject> """
		pass

	@docopt_cmd
	def do_class_list(self, arg):
		"""Usage: class_list """
		pass

	# Log Commands
	@docopt_cmd
	def do_log_start(self, arg):
		"""Usage: log_start <class_id> """
		pass

	@docopt_cmd
	def do_log_end(self, arg):
		"""Usage: log_end <class_id> """
		pass

	# Check In/Out Student
	@docopt_cmd
	def do_check_in(self, arg):
		"""Usage: check_in <student_id> <class_id>"""
		pass
	
	@docopt_cmd
	def do_check_out(self, arg):
		"""Usage: check_out <student_id> <class_id> <reason>"""
		pass


if __name__ == "__main__":
	ClassRegister().cmdloop()