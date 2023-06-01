import sqlalchemy
import datetime
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Student(SqlAlchemyBase):
    __tablename__ = "students"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    login = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)
    avatar = sqlalchemy.Column(sqlalchemy.BLOB, default=None)
    birth_date = sqlalchemy.Column(sqlalchemy.Date)
    created_date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.date.today())
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teachers.id"))
    teacher = orm.relationship("Teacher")
    portfolio = orm.relationship("Portfolio", back_populates="student")
    exams = orm.relationship("Exam", back_populates="student")
    groups_to_students = orm.relationship("GroupToStudent", back_populates="student")


    def to_dict(self):
        dict_obj = {
            "id": self.id,
            'name': self.name,
            "login": self.login,
            "password": self.password,
            "birth_date": self.birth_date,
            "created_date": self.created_date,
            "teacher_id": self.teacher_id

        }
        return dict_obj