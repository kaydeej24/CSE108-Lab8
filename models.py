from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False, server_default="password")
    role = db.Column(db.String(20), nullable=False, server_default="student")
    name = db.Column(db.String(80), nullable=False)



"""
class Teacher(db.Model):
    __tablename__ = "teacher"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, server_default="defaultTeach")
    name = db.Column(db.String(80), nullable=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", name="fk_teacher_user_id")
    )

    __table_args__ = (
        db.UniqueConstraint("user_id", name="uq_teacher_user_id"),
    )

    user = db.relationship("User", backref="teacher_profile")

    
class Student(db.Model):
    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    __table_args__ = (
        db.UniqueConstraint("user_id", name="uq_student_user_id"),
    )

    username = db.Column(db.String(80), nullable=False, server_default="defaultStudent")
    name = db.Column(db.String(80), nullable=False)

    user = db.relationship("User", backref="student_profile")
"""
    
class Class(db.Model):
    __tablename__ = "class"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    timing = db.Column(db.String(120))

    #teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"))

    enrollment = db.Column(db.Integer, nullable=False, server_default=text("0"))
    capacity = db.Column(db.Integer, nullable=False, server_default=text("50"))
    

class Enrollment(db.Model):
    __tablename__ = "enrollment"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
