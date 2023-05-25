import sqlalchemy
import datetime
from .db_session import SqlAlchemyBase
from sqlalchemy import orm

class Portfolio(SqlAlchemyBase):
    __tablename__ = "portfolio"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    subject = sqlalchemy.Column(sqlalchemy.String)
    file_uuid = sqlalchemy.Column(sqlalchemy.String)
    level = sqlalchemy.Column(sqlalchemy.String)
    result = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.String)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("students.id"))
    student = orm.relationship("Student")

    def to_dict(self):
        dict_obj = {
            "id": self.id,
            'name': self.name,
            "subject": self.subject,
            "file_uuid": self.file_uuid,
            "level": self.level,
            "result": self.result,
            "date": self.date,
            "created_at": self.created_at,
            "student_id": self.student_id
        }
        return dict_obj