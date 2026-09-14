import tkinter as tk
from tkinter import ttk, messagebox
from openpyxl import Workbook, load_workbook
import os

EXCEL_FILE = "student_results.xlsx"

#EXCELL FILE

def create_excel_file():
    if not os.path.exists(EXCEL_FILE):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Student Results"

        sheet.append([
            "Name",
            "Roll No",
            "Class",
            "Subject 1",
            "Subject 2",
            "Subject 3",
            "Subject 4",
            "Subject 5",
            "Total Marks",
            "Percentage",
            "Result"
        ])

        workbook.save(EXCEL_FILE)


#CLEAR INPUTS

def clear_inputs():
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    class_entry.delete(0, tk.END)

    for entry in subject_entries:
        entry.delete(0, tk.END)

#SAVE INPUT

def save_student():

    name = name_entry.get().strip()
    roll = roll_entry.get().strip()
    student_class = class_entry.get().strip()

    # Check basic details
    if name == "" or roll == "" or student_class == "":
        messagebox.showerror(
            "Error",
            "Please enter Name, Roll No. and Class."
        )
        return

    # Get subject marks
    marks = []

    for entry in subject_entries:

        value = entry.get().strip()

        if value == "":
            messagebox.showerror(
                "Error",
                "Please enter marks for all 5 subjects."
            )
            return

        try:
            mark = float(value)

            if mark < 0 or mark > 100:
                messagebox.showerror(
                    "Error",
                    "Marks must be between 0 and 100."
                )
                return

            marks.append(mark)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter numbers only for marks."
            )
            return

    # Open Excel
    try:
        workbook = load_workbook(EXCEL_FILE)
        sheet = workbook["Student Results"]

        # Check duplicate roll number
        for row in sheet.iter_rows(min_row=2, values_only=True):

            if str(row[1]) == roll:
                messagebox.showerror(
                    "Error",
                    "This Roll No. already exists!"
                )
                workbook.close()
                return

        # Calculate total
        total = sum(marks)

        # Calculate percentage
        percentage = total / 5

        # Calculate result
        if all(mark >= 35 for mark in marks):
            result = "PASS"
        else:
            result = "FAIL"

        # Save data to Excel
        sheet.append([
            name,
            roll,
            student_class,
            marks[0],
            marks[1],
            marks[2],
            marks[3],
            marks[4],
            total,
            percentage,
            result
        ])

        workbook.save(EXCEL_FILE)
        workbook.close()

        messagebox.showinfo(
            "Success",
            "Student saved successfully!\n\n"
            f"Total Marks: {total}\n"
            f"Percentage: {percentage:.2f}%\n"
            f"Result: {result}"
        )

        clear_inputs()

    except PermissionError:
        messagebox.showerror(
            "Excel Error",
            "Please CLOSE student_results.xlsx and try again."
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"Something went wrong:\n{error}"
        )

#GET RESULT

def get_result():

    roll = search_roll_entry.get().strip()

    if roll == "":
        messagebox.showerror(
            "Error",
            "Please enter Roll No."
        )
        return

    # Clear previous result
    for item in result_table.get_children():
        result_table.delete(item)

    try:
        workbook = load_workbook(EXCEL_FILE)
        sheet = workbook["Student Results"]

        found = False

        for row in sheet.iter_rows(min_row=2, values_only=True):

            if str(row[1]) == roll:

                found = True

                result_table.insert(
                    "",
                    tk.END,
                    values=(
                        row[0],
                        row[1],
                        row[2],
                        row[8],
                        f"{row[9]:.2f}%",
                        row[10]
                    )
                )

                break

        workbook.close()

        if not found:
            messagebox.showwarning(
                "Not Found",
                "No student found with this Roll No."
            )

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"Could not read Excel file:\n{error}"
        )

#SHOW RESULT

def show_all_results():

    # Clear table
    for item in result_table.get_children():
        result_table.delete(item)

    try:
        workbook = load_workbook(EXCEL_FILE)
        sheet = workbook["Student Results"]

        for row in sheet.iter_rows(min_row=2, values_only=True):

            result_table.insert(
                "",
                tk.END,
                values=(
                    row[0],
                    row[1],
                    row[2],
                    row[8],
                    f"{row[9]:.2f}%",
                    row[10]
                )
            )

        workbook.close()

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"Could not read Excel file:\n{error}"
        )


#MAIN WINDOW

create_excel_file()

root = tk.Tk()

root.title("Student Result Management System")
root.geometry("900x700")
root.resizable(False, False)

#TITLE

title = tk.Label(
    root,
    text="STUDENT RESULT MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold")
)

title.pack(pady=20)


#STUDENTFRAME
student_frame = tk.LabelFrame(
    root,
    text="1. Add Student",
    font=("Arial", 14, "bold"),
    padx=20,
    pady=20
)

student_frame.pack(
    padx=30,
    fill="x"
)


# NAME

tk.Label(
    student_frame,
    text="Name:",
    font=("Arial", 12)
).grid(row=0, column=0, padx=10, pady=10, sticky="w")

name_entry = tk.Entry(
    student_frame,
    width=30,
    font=("Arial", 12)
)

name_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


# ROLL NUMBER

tk.Label(
    student_frame,
    text="Roll No.:",
    font=("Arial", 12)
).grid(row=0, column=2, padx=10, pady=10, sticky="w")

roll_entry = tk.Entry(
    student_frame,
    width=20,
    font=("Arial", 12)
)

roll_entry.grid(
    row=0,
    column=3,
    padx=10,
    pady=10
)


# CLASS

tk.Label(
    student_frame,
    text="Class:",
    font=("Arial", 12)
).grid(row=1, column=0, padx=10, pady=10, sticky="w")

class_entry = tk.Entry(
    student_frame,
    width=30,
    font=("Arial", 12)
)

class_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)


#SUBJECT MARKS

tk.Label(
    student_frame,
    text="Enter Marks (Out of 100)",
    font=("Arial", 13, "bold")
).grid(
    row=2,
    column=0,
    columnspan=4,
    pady=15
)


subject_entries = []

for i in range(5):

    tk.Label(
        student_frame,
        text=f"Subject {i + 1}:",
        font=("Arial", 11)
    ).grid(
        row=3,
        column=i,
        padx=8,
        pady=5
    )

    entry = tk.Entry(
        student_frame,
        width=10,
        font=("Arial", 11)
    )

    entry.grid(
        row=4,
        column=i,
        padx=8,
        pady=5
    )

    subject_entries.append(entry)


#SAVE AND CLEAR BUTTONS

button_frame = tk.Frame(student_frame)

button_frame.grid(
    row=5,
    column=0,
    columnspan=5,
    pady=20
)


save_button = tk.Button(
    button_frame,
    text="SAVE STUDENT",
    command=save_student,
    font=("Arial", 12, "bold"),
    width=18
)

save_button.pack(
    side="left",
    padx=10
)


clear_button = tk.Button(
    button_frame,
    text="CLEAR",
    command=clear_inputs,
    font=("Arial", 12, "bold"),
    width=12
)

clear_button.pack(
    side="left",
    padx=10
)

#RESULT FRAME
result_search_frame = tk.LabelFrame(
    root,
    text="2. Get Result",
    font=("Arial", 14, "bold"),
    padx=20,
    pady=15
)

result_search_frame.pack(
    padx=30,
    pady=20,
    fill="x"
)


tk.Label(
    result_search_frame,
    text="Enter Roll No.:",
    font=("Arial", 12)
).pack(
    side="left",
    padx=10
)


search_roll_entry = tk.Entry(
    result_search_frame,
    width=20,
    font=("Arial", 12)
)

search_roll_entry.pack(
    side="left",
    padx=10
)


get_button = tk.Button(
    result_search_frame,
    text="GET RESULT",
    command=get_result,
    font=("Arial", 11, "bold"),
    width=15
)

get_button.pack(
    side="left",
    padx=10
)


show_button = tk.Button(
    result_search_frame,
    text="SHOW ALL RESULTS",
    command=show_all_results,
    font=("Arial", 11, "bold"),
    width=18
)

show_button.pack(
    side="left",
    padx=10
)


#RESULT TABLE

table_frame = tk.LabelFrame(
    root,
    text="3. Student Results",
    font=("Arial", 14, "bold"),
    padx=10,
    pady=10
)

table_frame.pack(
    padx=30,
    fill="both",
    expand=True
)


columns = (
    "Name",
    "Roll No.",
    "Class",
    "Total Marks",
    "Percentage",
    "Result"
)


result_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=8
)


for column in columns:

    result_table.heading(
        column,
        text=column
    )

    result_table.column(
        column,
        width=130,
        anchor="center"
    )


result_table.pack(
    fill="both",
    expand=True
)

root.mainloop()
