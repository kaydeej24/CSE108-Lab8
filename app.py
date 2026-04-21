from flask import Flask, render_template, request, redirect, url_for, session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

from models import db, User, Class, Enrollment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret"

db.init_app(app)
migrate = Migrate(app, db)

admin = Admin(app, name="Dashboard")
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Class, db.session))
admin.add_view(ModelView(Enrollment, db.session))

with app.app_context():
    db.create_all()

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session["user_id"] = user.id
            session["role"] = user.role

            if user.role == "teacher":
                return redirect(url_for("teacher_dashboard"))
            return redirect(url_for("dashboard"))

        return render_template("loginPost.html",
                               textIn="Invalid credentials",
                               text2="Try again")

    return render_template("login.html")

# ---------------- STUDENT DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if session.get("role") != "student":
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    # classes student is enrolled in
    enrolled_classes = [e.course for e in user.enrollments]

    # all classes
    all_classes = Class.query.all()

    # available classes = not enrolled
    available_classes = [c for c in all_classes if c not in enrolled_classes]

    def serialize(c):
        return {
            "id": c.id,
            "name": c.name,
            "teacher": c.teacher.name if c.teacher else "N/A",
            "time": c.timing,
            "student_count": len(c.enrollments),
            "capacity": c.capacity
        }

    return render_template(
        "dashboard.html",
        user=user.name,
        classes=[serialize(c) for c in enrolled_classes],
        course_catalog=[serialize(c) for c in available_classes]
    )

# ---------------- JOIN ----------------
@app.route("/join/<int:course_id>")
def join(course_id):
    if session.get("role") != "student":
        return redirect(url_for("login"))

    user_id = session["user_id"]
    course = Class.query.get(course_id)

    if not course:
        return redirect(url_for("dashboard"))

    # capacity check
    if len(course.enrollments) >= course.capacity:
        return "Class is full", 400

    existing = Enrollment.query.filter_by(
        student_id=user_id,
        class_id=course_id
    ).first()

    if not existing:
        db.session.add(Enrollment(student_id=user_id, class_id=course_id))
        db.session.commit()

    return redirect(url_for("dashboard"))

# ---------------- DELETE ----------------
@app.route("/delete/<int:course_id>")
def delete(course_id):
    if session.get("role") != "student":
        return redirect(url_for("login"))

    enrollment = Enrollment.query.filter_by(
        student_id=session["user_id"],
        class_id=course_id
    ).first()

    if enrollment:
        db.session.delete(enrollment)
        db.session.commit()

    return redirect(url_for("dashboard"))

# ---------------- TEACHER DASHBOARD ----------------
@app.route("/teacher")
def teacher_dashboard():
    if session.get("role") != "teacher":
        return redirect(url_for("login"))

    teacher = User.query.get(session["user_id"])

    courses_data = []

    for c in teacher.classes_teaching:
        courses_data.append({
            "id": c.id,
            "name": c.name,
            "time": c.timing,
            "student_count": len(c.enrollments),
            "capacity": c.capacity,
            "students": [
                {
                    "name": e.student.name,
                    "username": e.student.username
                }
                for e in c.enrollments
            ]
        })

    return render_template("teacher.html", courses=courses_data)

@app.route("/teacher/<int:course_id>")
def teacher_course():
    render_template("teacher_course.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)