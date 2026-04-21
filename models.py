from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # "student" or "teacher"

    # relationships
    enrollments = db.relationship("Enrollment", back_populates="student", cascade="all, delete")
    classes_teaching = db.relationship("Class", back_populates="teacher")


class Class(db.Model):
    __tablename__ = "class"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    timing = db.Column(db.String(120))

    teacher_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    capacity = db.Column(db.Integer, nullable=False, default=50)

    # relationships
    teacher = db.relationship("User", back_populates="classes_teaching")
    enrollments = db.relationship("Enrollment", back_populates="course", cascade="all, delete")


class Enrollment(db.Model):
    __tablename__ = "enrollment"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    class_id = db.Column(db.Integer, db.ForeignKey("class.id"))

    grade = db.Column(db.String(10), nullable=True) 

    # prevent duplicates
    __table_args__ = (
        UniqueConstraint("student_id", "class_id", name="unique_enrollment"),
    )

    # relationships
    student = db.relationship("User", back_populates="enrollments")
    course = db.relationship("Class", back_populates="enrollments")