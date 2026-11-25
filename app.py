
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database
def connect():
    return sqlite3.connect("data.db")

with connect() as con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            course TEXT
        )
    """)

# Read records
@app.route("/")
def home():
    con = connect()
    records = con.execute("SELECT * FROM students").fetchall()
    con.close()
    return render_template("index.html", records=records)

# Create record
@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    course = request.form["course"]

    con = connect()
    con.execute("INSERT INTO students(name, course) VALUES(?,?)",
                (name, course))
    con.commit()
    con.close()
    return redirect("/")

# Update record
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    con = connect()

    if request.method == "POST":
        name = request.form["name"]
        course = request.form["course"]

        con.execute("UPDATE students SET name=?, course=? WHERE id=?",
                    (name, course, id))
        con.commit()
        con.close()
        return redirect("/")

    record = con.execute("SELECT * FROM students WHERE id=?",
                         (id,)).fetchone()
    con.close()
    return render_template("update.html", record=record)

# Delete record
@app.route("/delete/<int:id>")
def delete(id):
    con = connect()
    con.execute("DELETE FROM students WHERE id=?", (id,))
    con.commit()
    con.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
