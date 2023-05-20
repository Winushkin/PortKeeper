import sqlalchemy
import datetime
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Student(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "students"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    login = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)
    avatar = sqlalchemy.Column(sqlalchemy.BLOB, default=None)
    birth_date = sqlalchemy.Column(sqlalchemy.Date)
    created_date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.date.today())
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teachers.id"))
    group = sqlalchemy.Column(sqlalchemy.String)
    teacher = orm.relationship("Teacher")
    portfolio = orm.relationship("Portfolio", back_populates="student")
    exams = orm.relationship("Exam", back_populates="student")


