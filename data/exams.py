import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Exam(SqlAlchemyBase):
    __tablename__ = "exams"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    subject = sqlalchemy.Column(sqlalchemy.String)
    mark = sqlalchemy.Column(sqlalchemy.Integer)
    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("students.id"))
    student = orm.relationship("Student")

    def to_dict(self):
        dict_obj = {
            "id": self.id,
            'subject': self.subject,
            "mark": self.mark,
            "student_id": self.student_id
        }
        return dict_obj
