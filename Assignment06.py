# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: This assignment demonstrates using functions with structured error handling,
#       adding the use of methods, classes and Separation of Concerns pattern
# Change Log: (Who, When, What)
#   R.Root, 2030/01/01, Created Starter Script
#   G.DuBuque, 2024/08/05, Updated script for Assignment 06, added SOC pattern,
#                           classes FileProcessor and IO, and their functions.
# ------------------------------------------------------------------------------------------ #
import json

# Data --------------------------------------------------------------------- #
# Define the global Constants (GD)
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the global Variables (GD)
students: list = []     # List of student data as dictionaries
menu_choice: str = ''   # Holds the choice made by the user.


# Processing --------------------------------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions to work with JSON files.

    ChangeLog: (Who, When, What)
    G.DuBuque, 2024/08/05, Created Class
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """ This function reads data from a JSON file and returns the data
        in a list.

        :param file_name: Name of the JSON file
        :param student_data: List of student data
        :return: List of student data

        ChangeLog: (Who, When, What)
        G.DuBuque, 2024/08/05, Created function
        """
        try:
            file = open(file_name, "r")
            student_data = json.load(file)
            file.close()
        except FileNotFoundError as e:
            IO.output_error_messages("Text file must exist before running this script!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        finally:
            if not file.closed:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a JSON file.

        :param file_name: Name of the JSON file
        :param student_data: List of student data
        :return: None

        ChangeLog: (Who, When, What)
        G.DuBuque, 2024/08/05, Created function
        """
        try:
            file = open(file_name, "w")
            json.dump(student_data, file)
            file.close()
        except TypeError as e:
            IO.output_error_messages("Please check that the data is a valid JSON format", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        finally:
            if not file.closed:
                file.close()
            print("File saved successfully!")


# Presentation ------------------------------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output.

    ChangeLog: (Who, When, What)
    G.DuBuque, 2024/08/05, Created Class
    """

    @staticmethod
    def output_error_messages(message: str = None, error: Exception = None):
        """ This function displays a given custom error message and the
        built-in error messages of a given Exception object to the user.

        :param message: Custom error message
        :param error: Exception object
        :return: None

        ChangeLog: (Who, When, What)
        G.DuBuque, 2024/08/05, Created function, added default of None to
        message parameter to add robustness to function
        """
        if message is None:  # In case of not providing a custom message
            print("There was an error!", "\n")
        else:
            print(message, "\n")
        if error is not None:  # Print built-in error messages
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user.

        :param menu: Menu to display
        :return: None

        ChangeLog: (Who, When, What)
        G.DuBuque, 2024/08/05, Created function
        """
        print(menu)

    @staticmethod
    def input_menu_choice():
        """ This function returns the menu of choice of the user as a string.

        :param: None
        :return: String with the user's choice

        ChangeLog: (Who, When, What)
        G.DuBuque, 2024/08/05, Created function
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):
                raise Exception("Please choose only 1, 2, 3 or 4")
        except Exception as e:
            IO.output_error_messages(error=e)  # Print error messages

        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """ This function displays the complete list of registration data
        to the user in a formatted string.

        :param student_data: List of student data
        :return: None

        ChangeLog: (Who, When, What)
        G.DuBuque, 2024/08/05, Created function
        """
        print("-" * 50)
        for student in student_data:
            print(f"Student {student["FirstName"]} "
                  f"{student["LastName"]} is enrolled in {student["CourseName"]}")
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the student's first name, last name and
        course name from the user, and updates and returns the list with the
        new data.

        :param student_data: List of student data
        :return: Updated list of student data

        ChangeLog: (Who, When, What)
        G.DuBuque, 2024/08/05, Created function
        """
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should not contain numbers.")

            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")

            course_name = input("Please enter the name of the course: ")

            student = {"FirstName": student_first_name,
                       "LastName": student_last_name,
                       "CourseName": course_name}
            student_data.append(student)
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages("The data entered is not in the correct format!", e)
        except Exception as e:
            IO.output_error_messages(error=e)
        return student_data


# Main body of script ------------------------------------------------------ #
# Get current data
students = FileProcessor.read_data_from_file(FILE_NAME, students)

# Present and Process the data
while True:
    IO.output_menu(MENU)  # Present the menu of choices

    menu_choice = IO.input_menu_choice()  # Get menu choice

    if menu_choice == "1":  # Input user data
        students = IO.input_student_data(students)
        continue

    elif menu_choice == "2":  # Show current data
        IO.output_student_courses(students)
        continue

    elif menu_choice == "3":  # Save the data to a file
        FileProcessor.write_data_to_file(FILE_NAME, students)
        continue

    elif menu_choice == "4":  # Stop the program
        break  # out of the loop

print("Program Ended")
