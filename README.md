# Class Attendance Register
## Introduction
> This project was developed as part of the fulfilment of the Andela Class IX Bootcamp in Nairobi, Kenya. The class attendance register is a command line application used to check-in students when they come to class.

## Usage Commands
1. `check in <student_id> <class_id>` - Checks in a student into a class at the current time. A student once checked cannot be checked into another class except the class he has been checked into has ended
2. `check out <student_id> <class_id> <reason>` - Force check out a student from a class but a reason must be provided e.g Medical, Need to go home etc.
3. `log start <class_id>` - This creates a new time log for a particular class
4. `log end <class_id>` - This ends a time log for a class that has already been started
5. `student add <firstname> <lastname>` - This command creates a new student in the database and generate an id for the student
6. `student remove <student_id>` - This command deletes a student based on the student_id.
7. `class add <subject>` - This command creates a new class in the database and generates an id for the class.
8. `class remove <class_id>` -  This command deletes a class based on the class_id.
9. `class list` -  List all the classes with their status (Shows the status of the class and the number of students in that class at the moment)
10. `class list all` - List all classes stored in the database
11. `student list` - List all the students and if they’re currently in a class

## Installation and Setup
1. Download & Install Python
 * Head over to the [Python Downloads](https://www.python.org/downloads/) Site and download a version compatible with your operating system 
 * To confirm that you have successfully installed Python:
	* Open the Command Propmpt on Windows or Terminal on Mac/Linux
	* Type python
	* If the Python installation was successfull you the Python version will be printed on your screen and the python REPL will start

2. Clone the repository to your personal computer to any folder
 * On GitHub, go to the main page of the repository [Class Attendance Register](https://github.com/arnold-okoth/bc-9-class-att-register)
 * On your right, click the green button 'Clone or download'
 * Copy the URL
 * Enter the terminal on Mac/Linux or Git Bash on Windows
 * Type `git clone ` and paste the URL you copied from GitHub
 * Press *Enter* to complete the cloning process

3. Virtual Environment Installation
 * Install the virtual environment by typing: `pip install virtualenv` on your terminal

4. Install the required modules
 * Inside the directory where you cloned the repository run `pip install -r requirements.txt`

5. Run the Class Attendance Register application:
 * On the terminal type `python app.py` to start the application

