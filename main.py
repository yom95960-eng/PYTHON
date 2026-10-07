import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error


DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "MYSQL2026"
DB_NAME = "student_performance_db"


# DBCONNECTIONS
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


#CALCULATION
def valid_mark(value, field_name, maximum=100):
    try:
        number = float(value)
        if number < 0 or number > maximum:
            raise ValueError
        return number
    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            f"{field_name} must be a number between 0 and {maximum}."
        )
        return None


def calculate_result(marks):
    total = sum(marks)
    percentage = total / len(marks)

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    elif percentage >= 40:
        grade = "E"
    else:
        grade = "F"

    result = "PASS" if percentage >= 40 and all(m >= 35 for m in marks) else "FAIL"
    return total, percentage, grade, result


#LOGINWINDOW
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Performance Tracking System - Login")
        self.root.geometry("430x300")
        self.root.resizable(False, False)

        frame = ttk.Frame(root, padding=30)
        frame.pack(expand=True, fill="both")

        ttk.Label(
            frame,
            text="Student Performance Tracking System",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 25))

        ttk.Label(frame, text="Username").pack(anchor="w")
        self.username_entry = ttk.Entry(frame, width=35)
        self.username_entry.pack(pady=(3, 12))

        ttk.Label(frame, text="Password").pack(anchor="w")
        self.password_entry = ttk.Entry(frame, width=35, show="*")
        self.password_entry.pack(pady=(3, 18))

        ttk.Button(
            frame,
            text="Login",
            command=self.login
        ).pack(fill="x")

        ttk.Label(
            frame,
            text="Demo login: admin / admin123",
            foreground="gray"
        ).pack(pady=15)

        self.root.bind("<Return>", lambda event: self.login())
        self.username_entry.focus()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning(
                "Login Required",
                "Please enter username and password."
            )
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM users WHERE username=%s AND password=%s",
                (username, password)
            )
            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if user:
                self.root.destroy()
                dashboard = tk.Tk()
                StudentApp(dashboard, username)
                dashboard.mainloop()
            else:
                messagebox.showerror(
                    "Login Failed",
                    "Invalid username or password."
                )

        except Error as e:
            messagebox.showerror(
                "Database Error",
                f"Could not connect to MySQL.\n\n{e}"
            )


#APPLICATION
class StudentApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.selected_id = None

        self.root.title("Student Performance Tracking and Management System")
        self.root.geometry("1400x800")
        self.root.minsize(1100, 700)

        self.create_variables()
        self.create_interface()
        self.load_records()
        self.update_statistics()

        self.root.protocol("WM_DELETE_WINDOW", self.logout)

 #VARIABLES
    def create_variables(self):
        self.roll_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.class_var = tk.StringVar()
        self.division_var = tk.StringVar()

        self.subject1_var = tk.StringVar(value="Mathematics")
        self.subject2_var = tk.StringVar(value="Physics")
        self.subject3_var = tk.StringVar(value="Chemistry")
        self.subject4_var = tk.StringVar(value="English")
        self.subject5_var = tk.StringVar(value="Computer")

        self.marks1_var = tk.StringVar()
        self.marks2_var = tk.StringVar()
        self.marks3_var = tk.StringVar()
        self.marks4_var = tk.StringVar()
        self.marks5_var = tk.StringVar()

        self.attendance_var = tk.StringVar()
        self.assignment_var = tk.StringVar()
        self.internal_var = tk.StringVar()

        self.search_var = tk.StringVar()

  #INTERFACE
    def create_interface(self):
        header = ttk.Frame(self.root, padding=12)
        header.pack(fill="x")

        ttk.Label(
            header,
            text="Student Performance Tracking and Management System",
            font=("Arial", 20, "bold")
        ).pack(side="left")

        ttk.Button(
            header,
            text=f"Logout ({self.username})",
            command=self.logout
        ).pack(side="right")

        stats = ttk.Frame(self.root, padding=(12, 0, 12, 8))
        stats.pack(fill="x")

        self.total_students_label = ttk.Label(
            stats, text="Total Students: 0",
            font=("Arial", 11, "bold")
        )
        self.total_students_label.pack(side="left", padx=10)

        self.pass_label = ttk.Label(
            stats, text="Passed: 0",
            font=("Arial", 11, "bold")
        )
        self.pass_label.pack(side="left", padx=25)

        self.fail_label = ttk.Label(
            stats, text="Failed: 0",
            font=("Arial", 11, "bold")
        )
        self.fail_label.pack(side="left", padx=25)

        # Search area
        search_frame = ttk.Frame(self.root, padding=10)
        search_frame.pack(fill="x")

        ttk.Label(search_frame, text="Search by Roll No / Name:").pack(side="left")
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=35
        )
        search_entry.pack(side="left", padx=8)

        ttk.Button(
            search_frame,
            text="Search",
            command=self.search_records
        ).pack(side="left", padx=4)

        ttk.Button(
            search_frame,
            text="Show All",
            command=self.load_records
        ).pack(side="left", padx=4)

        # Notebook gives separate Add/Manage pages
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=12, pady=5)

        self.form_tab = ttk.Frame(notebook, padding=12)
        self.records_tab = ttk.Frame(notebook, padding=12)

        notebook.add(self.form_tab, text="Add / Update Record")
        notebook.add(self.records_tab, text="View Records")

        self.create_form()
        self.create_records_table()

    def create_form(self):
        personal = ttk.LabelFrame(
            self.form_tab,
            text="Student Details",
            padding=10
        )
        personal.pack(fill="x", pady=5)

        ttk.Label(personal, text="Roll No *").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(personal, textvariable=self.roll_var, width=22).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(personal, text="Name *").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        ttk.Entry(personal, textvariable=self.name_var, width=25).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(personal, text="Class *").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(personal, textvariable=self.class_var, width=22).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(personal, text="Division *").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        ttk.Combobox(
            personal,
            textvariable=self.division_var,
            values=["A", "B", "C", "D"],
            state="readonly",
            width=22
        ).grid(row=1, column=3, padx=5, pady=5)

        subjects = ttk.LabelFrame(
            self.form_tab,
            text="Subject-wise Marks (0-100)",
            padding=10
        )
        subjects.pack(fill="x", pady=5)

        subject_vars = [
            (self.subject1_var, self.marks1_var),
            (self.subject2_var, self.marks2_var),
            (self.subject3_var, self.marks3_var),
            (self.subject4_var, self.marks4_var),
            (self.subject5_var, self.marks5_var),
        ]

        for i, (subject, mark) in enumerate(subject_vars):
            ttk.Label(subjects, text=f"Subject {i+1}").grid(
                row=0, column=i, padx=5, pady=3
            )
            ttk.Entry(subjects, textvariable=subject, width=18).grid(
                row=1, column=i, padx=5, pady=3
            )
            ttk.Entry(subjects, textvariable=mark, width=18).grid(
                row=2, column=i, padx=5, pady=3
            )

        extra = ttk.LabelFrame(
            self.form_tab,
            text="Additional Performance Data",
            padding=10
        )
        extra.pack(fill="x", pady=5)

        ttk.Label(extra, text="Attendance % *").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(extra, textvariable=self.attendance_var, width=18).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(extra, text="Assignment Marks *").grid(row=0, column=2, padx=5, pady=5)
        ttk.Entry(extra, textvariable=self.assignment_var, width=18).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(extra, text="Internal Marks *").grid(row=0, column=4, padx=5, pady=5)
        ttk.Entry(extra, textvariable=self.internal_var, width=18).grid(row=0, column=5, padx=5, pady=5)

        buttons = ttk.Frame(self.form_tab, padding=10)
        buttons.pack(fill="x")

        ttk.Button(
            buttons,
            text="Add Record",
            command=self.add_record
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons,
            text="Update Selected",
            command=self.update_record
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons,
            text="Delete Selected",
            command=self.delete_record
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons,
            text="Clear / Reset",
            command=self.clear_form
        ).pack(side="left", padx=5)

        ttk.Label(
            self.form_tab,
            text="Select a row from View Records to edit or delete it.",
            foreground="gray"
        ).pack(anchor="w", padx=10)

    # RECORDTABLE
    def create_records_table(self):
        columns = (
            "id", "roll", "name", "class", "div",
            "s1", "m1", "s2", "m2", "s3", "m3",
            "s4", "m4", "s5", "m5",
            "attendance", "assignment", "internal",
            "total", "percentage", "grade", "result"
        )

        container = ttk.Frame(self.records_tab)
        container.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            container,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "roll": "Roll No",
            "name": "Name",
            "class": "Class",
            "div": "Div",
            "s1": "Subject 1",
            "m1": "Marks 1",
            "s2": "Subject 2",
            "m2": "Marks 2",
            "s3": "Subject 3",
            "m3": "Marks 3",
            "s4": "Subject 4",
            "m4": "Marks 4",
            "s5": "Subject 5",
            "m5": "Marks 5",
            "attendance": "Attendance",
            "assignment": "Assignment",
            "internal": "Internal",
            "total": "Total",
            "percentage": "%",
            "grade": "Grade",
            "result": "Result"
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=90, anchor="center")

        self.tree.column("id", width=45)
        self.tree.column("name", width=130)
        self.tree.column("roll", width=80)

        y_scroll = ttk.Scrollbar(
            container,
            orient="vertical",
            command=self.tree.yview
        )
        x_scroll = ttk.Scrollbar(
            container,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self.select_record)

    
    def get_form_data(self):
        roll = self.roll_var.get().strip()
        name = self.name_var.get().strip()
        class_name = self.class_var.get().strip()
        division = self.division_var.get().strip()

        if not roll or not name or not class_name or not division:
            messagebox.showwarning(
                "Required Fields",
                "Roll No, Name, Class and Division are required."
            )
            return None

        subject_names = [
            self.subject1_var.get().strip(),
            self.subject2_var.get().strip(),
            self.subject3_var.get().strip(),
            self.subject4_var.get().strip(),
            self.subject5_var.get().strip()
        ]

        if any(not subject for subject in subject_names):
            messagebox.showwarning(
                "Required Fields",
                "All five subject names are required."
            )
            return None

        mark_vars = [
            (self.marks1_var.get(), "Subject 1 Marks"),
            (self.marks2_var.get(), "Subject 2 Marks"),
            (self.marks3_var.get(), "Subject 3 Marks"),
            (self.marks4_var.get(), "Subject 4 Marks"),
            (self.marks5_var.get(), "Subject 5 Marks")
        ]

        marks = []
        for value, label in mark_vars:
            number = valid_mark(value, label)
            if number is None:
                return None
            marks.append(number)

        attendance = valid_mark(
            self.attendance_var.get(),
            "Attendance",
            100
        )
        assignment = valid_mark(
            self.assignment_var.get(),
            "Assignment Marks",
            100
        )
        internal = valid_mark(
            self.internal_var.get(),
            "Internal Marks",
            100
        )

        if attendance is None or assignment is None or internal is None:
            return None

        total, percentage, grade, result = calculate_result(marks)

        return {
            "roll": roll,
            "name": name,
            "class_name": class_name,
            "division": division,
            "subject1": subject_names[0],
            "marks1": marks[0],
            "subject2": subject_names[1],
            "marks2": marks[1],
            "subject3": subject_names[2],
            "marks3": marks[2],
            "subject4": subject_names[3],
            "marks4": marks[3],
            "subject5": subject_names[4],
            "marks5": marks[4],
            "attendance": attendance,
            "assignment": assignment,
            "internal": internal,
            "total": total,
            "percentage": percentage,
            "grade": grade,
            "result": result
        }

    #ADD OPERATION
    def add_record(self):
        data = self.get_form_data()
        if data is None:
            return

        query = """
            INSERT INTO students (
                roll_no, name, class_name, division,
                subject1, marks1, subject2, marks2,
                subject3, marks3, subject4, marks4,
                subject5, marks5, attendance,
                assignment_marks, internal_marks,
                total_marks, percentage, grade, result
            )
            VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s
            )
        """

        values = (
            data["roll"], data["name"], data["class_name"], data["division"],
            data["subject1"], data["marks1"],
            data["subject2"], data["marks2"],
            data["subject3"], data["marks3"],
            data["subject4"], data["marks4"],
            data["subject5"], data["marks5"],
            data["attendance"], data["assignment"], data["internal"],
            data["total"], data["percentage"], data["grade"], data["result"]
        )

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Student record added successfully.")
            self.clear_form()
            self.load_records()
            self.update_statistics()

        except Error as e:
            if "Duplicate entry" in str(e):
                messagebox.showerror(
                    "Duplicate Roll No",
                    "A student with this Roll No already exists."
                )
            else:
                messagebox.showerror("Database Error", str(e))

    # VIEWWOPERATIONS
    def load_records(self):
        self.search_var.set("")

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, roll_no, name, class_name, division,
                       subject1, marks1, subject2, marks2,
                       subject3, marks3, subject4, marks4,
                       subject5, marks5, attendance,
                       assignment_marks, internal_marks,
                       total_marks, percentage, grade, result
                FROM students
                ORDER BY id DESC
            """)

            records = cursor.fetchall()

            for row in records:
                self.tree.insert("", "end", values=row)

            cursor.close()
            conn.close()

        except Error as e:
            messagebox.showerror("Database Error", str(e))

        self.update_statistics()

    # SEARCHOPERATIONS
    def search_records(self):
        keyword = self.search_var.get().strip()

        if not keyword:
            self.load_records()
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
                SELECT id, roll_no, name, class_name, division,
                       subject1, marks1, subject2, marks2,
                       subject3, marks3, subject4, marks4,
                       subject5, marks5, attendance,
                       assignment_marks, internal_marks,
                       total_marks, percentage, grade, result
                FROM students
                WHERE roll_no LIKE %s
                   OR name LIKE %s
                   OR class_name LIKE %s
                   OR division LIKE %s
                ORDER BY id DESC
            """

            value = f"%{keyword}%"
            cursor.execute(query, (value, value, value, value))

            records = cursor.fetchall()

            for row in records:
                self.tree.insert("", "end", values=row)

            cursor.close()
            conn.close()

        except Error as e:
            messagebox.showerror("Database Error", str(e))

    # RECORD
    def select_record(self, event=None):
        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(selected[0], "values")

        if not values:
            return

        self.selected_id = values[0]

        self.roll_var.set(values[1])
        self.name_var.set(values[2])
        self.class_var.set(values[3])
        self.division_var.set(values[4])

        self.subject1_var.set(values[5])
        self.marks1_var.set(values[6])
        self.subject2_var.set(values[7])
        self.marks2_var.set(values[8])
        self.subject3_var.set(values[9])
        self.marks3_var.set(values[10])
        self.subject4_var.set(values[11])
        self.marks4_var.set(values[12])
        self.subject5_var.set(values[13])
        self.marks5_var.set(values[14])

        self.attendance_var.set(values[15])
        self.assignment_var.set(values[16])
        self.internal_var.set(values[17])

    #UPDATE
    def update_record(self):
        if not self.selected_id:
            messagebox.showwarning(
                "No Selection",
                "Select a record from the table first."
            )
            return

        data = self.get_form_data()
        if data is None:
            return

        query = """
            UPDATE students SET
                roll_no=%s,
                name=%s,
                class_name=%s,
                division=%s,
                subject1=%s,
                marks1=%s,
                subject2=%s,
                marks2=%s,
                subject3=%s,
                marks3=%s,
                subject4=%s,
                marks4=%s,
                subject5=%s,
                marks5=%s,
                attendance=%s,
                assignment_marks=%s,
                internal_marks=%s,
                total_marks=%s,
                percentage=%s,
                grade=%s,
                result=%s
            WHERE id=%s
        """

        values = (
            data["roll"], data["name"], data["class_name"], data["division"],
            data["subject1"], data["marks1"],
            data["subject2"], data["marks2"],
            data["subject3"], data["marks3"],
            data["subject4"], data["marks4"],
            data["subject5"], data["marks5"],
            data["attendance"], data["assignment"], data["internal"],
            data["total"], data["percentage"], data["grade"], data["result"],
            self.selected_id
        )

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Record updated successfully.")
            self.clear_form()
            self.load_records()
            self.update_statistics()

        except Error as e:
            messagebox.showerror("Database Error", str(e))

    # DELETE
    def delete_record(self):
        if not self.selected_id:
            messagebox.showwarning(
                "No Selection",
                "Select a record from the table first."
            )
            return

        selected = self.tree.selection()
        name = ""

        if selected:
            values = self.tree.item(selected[0], "values")
            if values:
                name = values[2]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete {name}'s record?"
        )

        if not confirm:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM students WHERE id=%s",
                (self.selected_id,)
            )
            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo("Deleted", "Record deleted successfully.")
            self.clear_form()
            self.load_records()
            self.update_statistics()

        except Error as e:
            messagebox.showerror("Database Error", str(e))

    # CLEAR
    def clear_form(self):
        self.selected_id = None

        self.roll_var.set("")
        self.name_var.set("")
        self.class_var.set("")
        self.division_var.set("")

        self.subject1_var.set("Mathematics")
        self.subject2_var.set("Physics")
        self.subject3_var.set("Chemistry")
        self.subject4_var.set("English")
        self.subject5_var.set("Computer")

        self.marks1_var.set("")
        self.marks2_var.set("")
        self.marks3_var.set("")
        self.marks4_var.set("")
        self.marks5_var.set("")

        self.attendance_var.set("")
        self.assignment_var.set("")
        self.internal_var.set("")

        for item in self.tree.selection():
            self.tree.selection_remove(item)

    # STATISTICS
    def update_statistics(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM students")
            total = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM students WHERE result='PASS'"
            )
            passed = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM students WHERE result='FAIL'"
            )
            failed = cursor.fetchone()[0]

            cursor.close()
            conn.close()

            self.total_students_label.config(
                text=f"Total Students: {total}"
            )
            self.pass_label.config(
                text=f"Passed: {passed}"
            )
            self.fail_label.config(
                text=f"Failed: {failed}"
            )

        except Error:
            pass

    # LOGOUT
    def logout(self):
        if messagebox.askyesno("Logout", "Do you want to logout?"):
            self.root.destroy()
            login_root = tk.Tk()
            LoginWindow(login_root)
            login_root.mainloop()


#START
if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
