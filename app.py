from flask import Flask, render_template, request, render_template, redirect, url_for, session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from models import db, User, Student, Teacher, Class, Enrollment
#from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

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
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Teacher, db.session))
admin.add_view(ModelView(Class, db.session))
admin.add_view(ModelView(Enrollment, db.session))

# create tables
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    #return render_template("index.html")
    return redirect(url_for('login'))

@app.route("/users")
def users():
    all_users = User.query.all()
    return render_template("users.html", users=all_users)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        #email = request.form["email"]
        password = request.form["password"]
        username = request.form.get("username")

        # 1. check if user exists
        user = User.query.filter_by(username=username).first()

        if user:
            # LOGIN FLOW
            if user.password == password:
                session["user_id"] = user.id
                return render_template("loginPost.html", textIn="Logged in successfully")
            else:
                return render_template("loginPost.html", textIn="Wrong password")

        else:
            # REGISTER FLOW (auto-create user)
            new_user = User(
                username=username, #or email.split("@")[0],
                #email=email,
                password=password
            )

            db.session.add(new_user)
            db.session.commit()

            session["user_id"] = new_user.id
            return render_template("loginPost.html", textIn="User created and logged in")

    return render_template("login.html") #, redirect(url_for("users"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        fullname = request.form["first"] + " " + request.form["last"]
        role = request.form["role"]

        user = User(
            username=username,
            password=password,
            role=role
        )

        db.session.add(user)
        db.session.flush()  # gets user.id

        # 🔥 THIS is what populates other tables
        if role == "student":
            student = Student(
                user_id=user.id,
                username=username,
                name=fullname
            )
            db.session.add(student)

        elif role == "teacher":
            teacher = Teacher(
                user_id=user.id,
                username=username,
                name=fullname
            )
            db.session.add(teacher)

        db.session.commit()

        return render_template("loginPost.html", textIn="User created ")

    return render_template("register.html")

"""
@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]

    user = User(
        username=username,
        password=password,
        role=role
    )

    db.session.add(user)
    db.session.flush()  # gets user.id

    # 🔥 THIS is what populates other tables
    if role == "student":
        student = Student(
            user_id=user.id,
            name=username
        )
        db.session.add(student)

    elif role == "teacher":
        teacher = Teacher(
            user_id=user.id,
            name=username
        )
        db.session.add(teacher)

    db.session.commit()

    return "User created"
"""

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    return f"Hello {user.username}"

if __name__ == "__main__":
    app.run(debug=True)