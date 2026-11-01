from flask import Flask, request, render_template_string
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="internship_db"
)

cursor = db.cursor()

# Home page
@app.route("/")
def home():
    with open("index.html", "r") as file:
        return file.read()


# Submit internship application
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    student_id = request.form["student_id"]
    company = request.form["company"]
    internship = request.form["internship"]

    sql = """
    INSERT INTO applications
    (student_name, student_id, company, internship)
    VALUES (%s, %s, %s, %s)
    """

    values = (name, student_id, company, internship)

    cursor.execute(sql, values)
    db.commit()

    return "Application Submitted Successfully! <br><a href='/'>Go Back</a>"


# Show all applications
@app.route("/show")
def show():
    cursor.execute("SELECT * FROM applications")
    records = cursor.fetchall()

    with open("show.html", "r") as file:
        page = file.read()

    rows = ""

    for record in records:
        rows = rows + "<tr>"
        for item in record:
            rows = rows + "<td>" + str(item) + "</td>"
        rows = rows + "</tr>"

    page = page.replace("RECORDS", rows)

    return page


if __name__ == "__main__":
    app.run(debug=True)