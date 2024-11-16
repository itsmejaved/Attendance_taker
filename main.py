from logo import logo, logo2, logo3
from student_list import student_rolls, names
from prettytable import PrettyTable
from prettytable import PrettyTable

print(logo)
print(logo3)


# Utility function to update the student_list.py file
def update_student_list_file():
    with open("student_list.py", "w") as f:
        f.write(f"student_rolls = {student_rolls}\n")
        f.write(f"names = {names}\n")


# Sort the lists and update the file
def register_student_and_update_file(student_id, name):
    # Register the student and sort the lists
    student_rolls.append(student_id)
    names.append(name)

    # Sort lists based on student_id (assuming student_rolls contains unique IDs)
    sorted_pairs = sorted(zip(student_rolls, names))
    student_rolls[:], names[:] = zip(*sorted_pairs)

    # Update the file with the sorted lists
    update_student_list_file()


class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.attendance_given = False


# -----------------Admin Register--------------------
class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # --------------Login-----------------------------
    def login(self, username, password):
        return self.username == username and self.password == password

    # --------------New Admin------------------------
    def update_credentials(self, new_username, new_password):
        self.username = new_username
        self.password = new_password


# --------------- Attendance -----------------------
class AttendanceSystem:
    def __init__(self, subject, lecturer, room_number, admin_username, admin_password, student_rolls, names):
        self.students = {}  # Dictionary to store students
        self.subject = subject
        self.lecturer = lecturer
        self.room_number = room_number
        self.attendance = set()  # Set to store student IDs for attendance
        self.admin = Admin(admin_username, admin_password)

        # Pre-register students in the background
        self.pre_register_students(student_rolls, names)

    def pre_register_students(self, student_rolls, names):
        for student_id, name in zip(student_rolls, names):
            self.students[student_id] = Student(student_id, name)

    def register_student(self, student_id, name):
        # Ask for admin password to validate the action
        entered_password = input("Admin Password: ")
        if entered_password != self.admin.password:
            print("Incorrect password. Registration aborted.")
            return

        if student_id in self.students:
            print(f"Student {name} is already registered.")
        else:
            self.students[student_id] = Student(student_id, name)
            register_student_and_update_file(student_id, name)  # Register and update the file
            print(f"Student {name} has been registered successfully.")

    def give_attendance(self, student_id):
        if student_id not in self.students:
            # If student is not registered, prompt to register
            print("Student is not registered in this class.")
            name = input("Enter Student Name to register: ")
            self.register_student(student_id, name)
            # After registering, mark attendance
            self.attendance.add(student_id)
            print(f"Attendance recorded for {name}.")
        elif student_id in self.attendance:
            print("Alert: You have already given your attendance.")
        else:
            self.attendance.add(student_id)
            print(f"Attendance recorded for {self.students[student_id].name}.")

    def class_status(self):
        print("\nClass Information")
        print(f"Subject: {self.subject}")
        print(f"Lecturer: {self.lecturer}")
        print(f"Room Number: {self.room_number}")
        print(f"Total Students Registered: {len(self.students)}")

    # Update the show_summary function to use PrettyTable
    def show_summary(self):
        print("\n--- Attendance Summary ---")

        # Create a PrettyTable instance for summary
        table = PrettyTable()
        table.field_names = ["Status", "Total Students"]

        table.add_row(["Registered", len(self.students)])
        table.add_row(["Present", len(self.attendance)])
        table.add_row(["Absent", len(self.students) - len(self.attendance)])

        print(table)

        # Create another table for Present Students
        print("\nPresent Students:")
        present_table = PrettyTable()
        present_table.field_names = ["Student ID", "Name"]
        for student_id in self.attendance:
            present_table.add_row([student_id, self.students[student_id].name])
        print(present_table)

        # Create another table for Absent Students
        print("\nAbsent Students:")
        absent_table = PrettyTable()
        absent_table.field_names = ["Student ID", "Name"]
        for student_id, student in self.students.items():
            if student_id not in self.attendance:
                absent_table.add_row([student_id, student.name])
        print(absent_table)


# Function for admin command interface
def admin_interface(attendance_system):
    def show_menu():
        print("\nChoose an action:")
        print("1 - Register a Student")
        print("2 - Mark Attendance")
        print("3 - View Attendance Summary")
        print("4 - Complete Session")

    while True:
        show_menu()
        command = input("\nEnter the number of your action choice (1, 2, 3, or 4): ").strip()

        if command == "1":
            try:
                student_id = int(input("Enter Student ID to register: "))
                name = input("Enter Student Name: ")
                attendance_system.register_student(student_id, name)
            except ValueError:
                print("Invalid Student ID. Please enter a numerical ID.")
            finally:
                attendance_system.class_status()

        elif command == "2":
            print("\nEntering attendance mode. Enter '0' or 'exit' to stop taking attendance.")
            while True:
                student_id_input = input("Enter Student ID for attendance: ").strip()
                if student_id_input == "0" or student_id_input.lower() == "exit":
                    print("\nExiting attendance mode.")
                    break
                try:
                    student_id = int(student_id_input)
                    attendance_system.give_attendance(student_id)
                except ValueError:
                    print("Invalid input. Please enter a valid Student ID or '0'/'exit'.")


        elif command == "3":
            attendance_system.show_summary()

        elif command == "4":
            print("\nSession complete. Final summary:")
            attendance_system.show_summary()
            break

        else:
            print("Invalid choice. Please enter a valid option (1, 2, 3, or 4).")


# Initialize system and attempt admin login
admin_username = "admin"
admin_password = "password"

attendance_system = AttendanceSystem(
    "COMPUTER ORGANIZATION", "Dr. MD FAHIM AKHTAB", "Room 101", admin_username, admin_password,
    student_rolls, names
)

# Prompt for admin login
username = input("Admin Username: ")
password = input("Admin Password: ")

if attendance_system.admin.login(username, password):
    print("\nAdmin Login Successful.")
    attendance_system.class_status()  # Display initial class information
    admin_interface(attendance_system)  # Launch admin interface
else:
    print("\nAdmin login failed. Please try again.")

