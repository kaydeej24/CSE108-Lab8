from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
#from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False, server_default="password")
    role = db.Column(db.String(20), nullable=False, server_default="student")

class Student(db.Model):
    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False, server_default="password")

class Teacher(db.Model):
    __tablename__ = "teacher"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False, server_default="password")
    
 
class Class(db.Model):
    __tablename__ = "class"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    timing = db.Column(db.String(120))

    teacher_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    enrollment = db.Column(db.Integer, nullable=False, server_default=text("0"))
    capacity = db.Column(db.Integer, nullable=False, server_default=text("50"))

    # relationship
    teacher = db.relationship("User", backref="classes_teaching")
    

class Enrollment(db.Model):
    __tablename__ = "enrollment"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    # comment out name variable
    # class_id = 
    # student_id

