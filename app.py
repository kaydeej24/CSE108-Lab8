from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret-key"

# ---------------- USERS ----------------
users = {
    "jsmith": {"password": "password", "role": "student", "full_name": "James Smith"},
    "mgarcia": {"password": "password", "role": "student", "full_name": "Maria Garcia"},
    "ajohnson": {"password": "password", "role": "student", "full_name": "Alex Johnson"},
    "edavis": {"password": "password", "role": "student", "full_name": "Emily Davis"},
    "mbrown": {"password": "password", "role": "student", "full_name": "Michael Brown"},
    "swilson": {"password": "password", "role": "student", "full_name": "Sarah Wilson"},
    "dlee": {"password": "password", "role": "student", "full_name": "David Lee"},
    "jtaylor": {"password": "password", "role": "student", "full_name": "Jessica Taylor"},
    "dmartinez": {"password": "password", "role": "student", "full_name": "Daniel Martinez"},
    "sanderson": {"password": "password", "role": "student", "full_name": "Sophia Anderson"},
    "teacher": {"password": "password", "role": "teacher", "full_name": "Teacher"}
}

# ---------------- COURSES ----------------
course_catalog = [
    {"id": 101, "name": "Calculus I", "teacher": "Dr. Newton", "time": "MWF 9-10"},
    {"id": 102, "name": "Chemistry 101", "teacher": "Dr. Curie", "time": "TR 10-11"},
    {"id": 103, "name": "Biology 101", "teacher": "Dr. Darwin", "time": "MWF 1-2"},
    {"id": 104, "name": "English Composition", "teacher": "Dr. Austen", "time": "TR 12-1"},
    {"id": 105, "name": "US History", "teacher": "Dr. Lincoln", "time": "MWF 2-3"},
    {"id": 106, "name": "Psychology 101", "teacher": "Dr. Freud", "time": "TR 3-4"},
    {"id": 107, "name": "Philosophy 101", "teacher": "Dr. Socrates", "time": "MWF 11-12"},
    {"id": 108, "name": "Computer Science 101", "teacher": "Dr. Turing", "time": "TR 1-2"}
]

# ---------------- ENROLLMENTS ----------------
user_courses = {
    "jsmith": [101, 103],
    "mgarcia": [102],
    "ajohnson": [105],
    "edavis": [],
    "mbrown": [],
    "swilson": [],
    "dlee": [],
    "jtaylor": [],
    "dmartinez": [],
    "sanderson": []
}

# ---------------- HELPERS ----------------
def count_students(course_id):
    return sum(course_id in courses for courses in user_courses.values())

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            session["user"] = username
            session["role"] = users[username]["role"]
            user_courses.setdefault(username, [])

            if session["role"] == "teacher":
                return redirect(url_for("teacher_dashboard"))
            else:
                return redirect(url_for("dashboard"))

        return "Invalid credentials"

    return render_template("login.html")

# ---------------- STUDENT DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    user = session["user"]
    enrolled = user_courses.get(user, [])

    my_courses = []
    available = []

    for c in course_catalog:
        c2 = {**c, "student_count": count_students(c["id"])}

        if c["id"] in enrolled:
            my_courses.append(c2)
        else:
            available.append(c2)

    return render_template(
        "dashboard.html",
        user=user,
        classes=my_courses,
        course_catalog=available
    )

# ---------------- JOIN / DELETE ----------------
@app.route("/join/<int:course_id>")
def join(course_id):
    user = session["user"]
    user_courses.setdefault(user, [])

    if course_id not in user_courses[user]:
        user_courses[user].append(course_id)

    return redirect(url_for("dashboard"))

@app.route("/delete/<int:course_id>")
def delete(course_id):
    user = session["user"]

    if course_id in user_courses[user]:
        user_courses[user].remove(course_id)

    return redirect(url_for("dashboard"))

# ---------------- TEACHER DASHBOARD (RESTORED TABS STYLE) ----------------
@app.route("/teacher")
def teacher_dashboard():
    if session.get("role") != "teacher":
        return redirect(url_for("login"))

    courses_with_counts = []
    students = []

    for c in course_catalog:
        courses_with_counts.append({
            **c,
            "student_count": count_students(c["id"])
        })

    for username, data in users.items():
        if data["role"] == "student":
            students.append({
                "username": username,
                "name": data["full_name"],
                "courses": user_courses.get(username, [])
            })

    return render_template(
        "teacher.html",
        courses=courses_with_counts,
        students=students,
        course_catalog=course_catalog,
        user_courses=user_courses
    )

# ---------------- TEACHER ADD/REMOVE ----------------
@app.route("/teacher/add/<username>/<int:course_id>")
def teacher_add(username, course_id):
    user_courses.setdefault(username, [])

    if course_id not in user_courses[username]:
        user_courses[username].append(course_id)

    return redirect(url_for("teacher_dashboard"))

@app.route("/teacher/remove/<username>/<int:course_id>")
def teacher_remove(username, course_id):
    if username in user_courses and course_id in user_courses[username]:
        user_courses[username].remove(course_id)

    return redirect(url_for("teacher_dashboard"))

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)