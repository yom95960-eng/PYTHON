import openpyxl
import os

FILE_NAME = "student_records.xlsx"


# Create Excel file if it does not exist
def create_excel():
    if not os.path.exists(FILE_NAME):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Students"

        sheet.append(["Name", "Class", "Address", "Contact Number"])

        workbook.save(FILE_NAME)


# 1. New Student
def new_student():
    name = input("Enter student name: ")
    student_class = input("Enter class: ")
    address = input("Enter address: ")
    contact = input("Enter contact number: ")

    workbook = openpyxl.load_workbook(FILE_NAME)
    sheet = workbook["Students"]

    sheet.append([name, student_class, address, contact])

    workbook.save(FILE_NAME)

    print("\nStudent record saved successfully!")


# 2. View Students
def view_student():
    workbook = openpyxl.load_workbook(FILE_NAME)
    sheet = workbook["Students"]

    print("\n----- STUDENT RECORDS -----")

    for row in sheet.iter_rows(values_only=True):
        print(row)

    workbook.close()


# 3. Delete Student
def delete_student():
    name = input("Enter student name to delete: ")

    workbook = openpyxl.load_workbook(FILE_NAME)
    sheet = workbook["Students"]

    found = False

    for row in range(2, sheet.max_row + 1):

        if sheet.cell(row, 1).value == name:
            sheet.delete_rows(row)
            found = True
            break

    if found:
        workbook.save(FILE_NAME)
        print("\nStudent deleted successfully!")
    else:
        print("\nStudent not found!")

    workbook.close()


# MENU
def menu():

    create_excel()

    while True:

        print("\n==============================")
        print("      STUDENT MANAGEMENT")
        print("==============================")
        print("1. New Student")
        print("2. View Students")
        print("3. Delete Student")
        print("4. Exit")
        print("==============================")

        choice = input("Enter your choice: ")

        if choice == "1":
            new_student()

        elif choice == "2":
            view_student()

        elif choice == "3":
            delete_student()

        elif choice == "4":
            print("Thank you!")
            break

        else:
            print("Invalid choice. Please try again.")


# Start program
menu()
