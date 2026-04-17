from flask import Flask, render_template, request, redirect, url_for, session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from models import db, Class, Enrollment, Student, Teacher, User

app = Flask(__name__)
app.secret_key = "secret-key"


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

# init db
db.init_app(app)
# migrations
migrate = Migrate(app, db)

# admin
admin = Admin(app, name="Dashboard")
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Class, db.session))
admin.add_view(ModelView(Enrollment, db.session))

# create tables
with app.app_context():
    db.create_all()


# login and register for teachers and students
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form["password"]
        username = request.form.get("username")

        # check if user exists by checking the inputted username against user  
        user = Student.query.filter_by(username=username).first()
        if(Teacher.query.filter_by(username=username).first() != None):
            user = Teacher.query.filter_by(username=username).first()

        if user:
            # LOGIN FLOW
            if user.password == password:
                session["user_id"] = user.id
                return render_template("loginPost.html", textIn="Logged in successfully")
            else:
                return render_template("loginPost.html", textIn="Wrong password")

    return render_template("login.html") #, redirect(url_for("users"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        fullname = request.form["fullname"]
        role = request.form["role"]

        user = User(
            username=username,
            fullname=fullname,
            password=password,
        )

        #db.session.add(user)

        # 🔥 THIS is what populates other tables
        if role == "student":
            student = Student(
                user_id = user.id,
                username = username,
                password = password,
                name = fullname
            )
            db.session.add(student)

        elif role == "teacher":
            teacher = Teacher(
                username = username,
                name = fullname,
                password = password
            )
            db.session.add(teacher)
        
        db.session.flush()  # gets user.id
        db.session.commit()

        return render_template("loginPost.html", textIn="User created ")

    return render_template("register.html")

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

# ---------------- TEACHER DASHBOARD ----------------
@app.route("/teacher")
def teacher_dashboard():
    if session.get("role") != "teacher":
        return redirect(url_for("login"))

    courses = []
    students = []

    for c in course_catalog:
        courses.append({**c, "student_count": count_students(c["id"])})

    for username, data in users.items():
        if data["role"] == "student":
            students.append({
                "username": username,
                "name": data["full_name"],
                "courses": user_courses.get(username, [])
            })

    return render_template(
        "teacher.html",
        courses=courses,
        students=students,
        course_catalog=course_catalog
    )

# ---------------- GRADEBOOK ----------------
@app.route("/teacher/course/<int:course_id>", methods=["GET", "POST"])
def teacher_course(course_id):
    if session.get("role") != "teacher":
        return redirect(url_for("login"))

    if request.method == "POST":
        for key in request.form:
            if key.startswith("grade_"):
                username = key.split("_")[1]
                grades[(username, course_id)] = request.form[key]

    enrolled_students = []

    for username, courses in user_courses.items():
        if course_id in courses:
            enrolled_students.append({
                "username": username,
                "name": users[username]["full_name"],
                "grade": grades.get((username, course_id), "")
            })

    course = next(c for c in course_catalog if c["id"] == course_id)

    return render_template(
        "teacher_course.html",
        course=course,
        students=enrolled_students
    )

# ---------------- ADD / REMOVE ----------------
@app.route("/teacher/add/<username>/<int:course_id>")
def teacher_add(username, course_id):
    user_courses.setdefault(username, [])
    if course_id not in user_courses[username]:
        user_courses[username].append(course_id)
    return redirect(url_for("teacher_dashboard"))

@app.route("/teacher/remove/<username>/<int:course_id>")
def teacher_remove(username, course_id):
    if course_id in user_courses.get(username, []):
        user_courses[username].remove(course_id)
    return redirect(url_for("teacher_dashboard"))

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)