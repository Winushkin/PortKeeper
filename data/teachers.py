import sqlalchemy
import datetime
from .db_session import SqlAlchemyBase
from sqlalchemy import orm

class Teacher(SqlAlchemyBase):
    __tablename__ = "teachers"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    post = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    avatar = sqlalchemy.Column(sqlalchemy.BLOB, default=None, nullable=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    students = orm.relationship("Student", back_populates="teacher")
    groups = orm.relationship("Group", back_populates="teacher")


