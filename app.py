from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

app = Flask(__name__)

# SQLite database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False, server_default="password")
    

    def __repr__(self):
        return f"<User {self.username}>"


class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return f"<User {self.name}>"

class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classname = db.Column(db.String(80), nullable=False)
    timing = db.Column(db.String(120), unique=True, nullable=False)
    teacher = db.Column(db.String(120), unique=False, nullable=False)
    enrollment = db.Column(db.String(7), unique=False, nullable=False)
    def __repr__(self):
        return f"<User {self.classname}>"

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return f"<User {self.name}>"

# admin panel
admin = Admin(app, name="Dashboard")
admin.add_view(ModelView(User, db.session))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/users")
def users():
    all_users = User.query.all()
    return render_template("users.html", users=all_users)

if __name__ == "__main__":
    app.run(debug=True)