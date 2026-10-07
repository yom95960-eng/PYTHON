# ==========================================================
# PHASE 4 PROJECT - PROJECT NO. 3
# STUDENT SUBJECT-WISE MARKS ANALYSIS DASHBOARD
#
# Python + NumPy + Pandas + Matplotlib + Tkinter
#
# DATA IS TAKEN FROM AN EXCEL FILE USING pd.read_excel()
# ==========================================================

import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#datainputs

print("==============================================")
print(" STUDENT SUBJECT-WISE MARKS ANALYSIS")
print("==============================================")

file_name = input("Enter Excel file name/path (press Enter for student_resultsph4.xlsx): ")

if file_name == "":
    file_name = "student_resultsph4.xlsx"

try:
    data = pd.read_excel(file_name)
except Exception as e:
    print("\nExcel file could not be opened.")
    print("Check the file name and make sure the Excel file is")
    print("in the same folder as this Python program.")
    print("\nError:", e)
    input("\nPress Enter to close...")
    exit()

#exceldata

subjects = ["Subject 1", "Subject 2", "Subject 3",
            "Subject 4", "Subject 5"]

required_columns = ["Name"] + subjects

for column in required_columns:
    if column not in data.columns:
        print("\nMissing column:", column)
        print("Your Excel file should contain:")
        print("Name, Subject 1, Subject 2, Subject 3, Subject 4, Subject 5")
        input("\nPress Enter to close...")
        exit()

# Convert marks into numbers
for subject in subjects:
    data[subject] = pd.to_numeric(data[subject], errors="coerce")

# Remove rows where name or marks are missing
data = data.dropna(subset=required_columns)

if len(data) == 0:
    print("No valid student data found in the Excel file.")
    input("\nPress Enter to close...")
    exit()


#numpycalculations
marks = data[subjects].to_numpy()

# Total marks of each student
data["Total"] = np.sum(marks, axis=1)

# Average marks of each student
data["Average"] = np.mean(marks, axis=1)

# Percentage
data["Percentage"] = (data["Total"] / 500) * 100

# Highest marks
data["Highest"] = np.max(marks, axis=1)

# Lowest marks
data["Lowest"] = np.min(marks, axis=1)

# Pass / Fail
data["Result"] = np.where(data["Lowest"] >= 40, "PASS", "FAIL")


#topper

topper_index = data["Average"].idxmax()
topper_name = data.loc[topper_index, "Name"]
topper_average = data.loc[topper_index, "Average"]

class_average = data["Average"].mean()

pass_students = (data["Result"] == "PASS").sum()
fail_students = (data["Result"] == "FAIL").sum()


#dashboard

window = tk.Tk()
window.title("Student Marks Dashboard")
window.geometry("1000x700")
window.configure(bg="white")


#title

title = tk.Label(
    window,
    text="Student Marks Dashboard",
    font=("Arial", 18, "bold"),
    bg="white"
)
title.pack(pady=8)


#other parts of dashboard

top_frame = tk.Frame(window, bg="white")
top_frame.pack(fill="both", expand=True)

bottom_frame = tk.Frame(window, bg="white")
bottom_frame.pack(fill="both", expand=True)


left_top = tk.Frame(
    top_frame,
    bg="white",
    relief="solid",
    borderwidth=1
)
left_top.pack(
    side="left",
    fill="both",
    expand=True,
    padx=5,
    pady=5
)


right_top = tk.Frame(
    top_frame,
    bg="white",
    relief="solid",
    borderwidth=1
)
right_top.pack(
    side="left",
    fill="both",
    expand=True,
    padx=5,
    pady=5
)


left_bottom = tk.Frame(
    bottom_frame,
    bg="white",
    relief="solid",
    borderwidth=1
)
left_bottom.pack(
    side="left",
    fill="both",
    expand=True,
    padx=5,
    pady=5
)


right_bottom = tk.Frame(
    bottom_frame,
    bg="white",
    relief="solid",
    borderwidth=1
)
right_bottom.pack(
    side="left",
    fill="both",
    expand=True,
    padx=5,
    pady=5
)


#bargraph

average_marks = []

for subject in subjects:
    average_marks.append(data[subject].mean())

figure1, axis1 = plt.subplots(figsize=(5, 3))

axis1.bar(subjects, average_marks)

axis1.set_title("Subject Average Marks")
axis1.set_xlabel("Subjects")
axis1.set_ylabel("Average Marks")
axis1.set_ylim(0, 100)

axis1.tick_params(axis="x", rotation=20)

figure1.tight_layout()

canvas1 = FigureCanvasTkAgg(
    figure1,
    master=left_top
)

canvas1.draw()

canvas1.get_tk_widget().pack(
    fill="both",
    expand=True
)


#line graph

figure2, axis2 = plt.subplots(figsize=(5, 3))

x = np.arange(1, 6)

for index, row in data.iterrows():

    student_marks = row[subjects].to_numpy()

    axis2.plot(
        x,
        student_marks,
        marker="o",
        label=row["Name"]
    )

axis2.set_title("Student Marks Trend")
axis2.set_xlabel("Subjects")
axis2.set_ylabel("Marks")
axis2.set_ylim(0, 100)

axis2.set_xticks(x)
axis2.set_xticklabels(
    ["Subject 1", "Subject 2", "Subject 3",
     "Subject 4", "Subject 5"]
)

axis2.legend(fontsize=7)

figure2.tight_layout()

canvas2 = FigureCanvasTkAgg(
    figure2,
    master=right_top
)

canvas2.draw()

canvas2.get_tk_widget().pack(
    fill="both",
    expand=True
)


#piechart

figure3, axis3 = plt.subplots(figsize=(5, 3))

axis3.pie(
    [pass_students, fail_students],
    labels=["PASS", "FAIL"],
    autopct="%1.1f%%",
    startangle=90
)

axis3.set_title("Student Result Distribution")

figure3.tight_layout()

canvas3 = FigureCanvasTkAgg(
    figure3,
    master=left_bottom
)

canvas3.draw()

canvas3.get_tk_widget().pack(
    fill="both",
    expand=True
)


#student details

heading = tk.Label(
    right_bottom,
    text="Student Performance Details",
    font=("Arial", 12, "bold"),
    bg="white"
)

heading.pack(pady=8)


details = tk.Label(
    right_bottom,
    text=(
        "Average Marks : " + str(round(class_average, 2)) + "\n"
        "Highest Mark  : " + str(int(data[subjects].max().max())) + "\n"
        "Lowest Mark   : " + str(int(data[subjects].min().min())) + "\n"
        "Topper        : " + str(topper_name) + "\n"
        "Topper Average: " + str(round(topper_average, 2)) + "\n"
        "Total Students: " + str(len(data)) + "\n"
        "Pass Students : " + str(pass_students) + "\n"
        "Fail Students : " + str(fail_students)
    ),
    font=("Arial", 10),
    bg="white",
    justify="left"
)

details.pack(pady=5)


#studenttable

table_heading = tk.Label(
    right_bottom,
    text="Student Average",
    font=("Arial", 10, "bold"),
    bg="white"
)

table_heading.pack(pady=(8, 3))


for index, row in data.iterrows():

    text = (
        str(row["Name"]) +
        "    " +
        str(round(row["Average"], 2))
    )

    student_label = tk.Label(
        right_bottom,
        text=text,
        font=("Arial", 9),
        bg="white"
    )

    student_label.pack()


#printdata in python shell

print("\nSTUDENT DATA")
print(data)

print("\nCLASS AVERAGE:", round(class_average, 2))
print("TOPPER:", topper_name)
print("TOPPER AVERAGE:", round(topper_average, 2))
print("PASS STUDENTS:", pass_students)
print("FAIL STUDENTS:", fail_students)


window.mainloop()
