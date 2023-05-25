import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm

class Group(SqlAlchemyBase):
    __tablename__ = "groups"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teachers.id"))
    teacher = orm.relationship("Teacher")
    groups_to_students = orm.relationship("GroupToStudent", back_populates="group")


    def to_dict(self):
        dict_obj = {
            "id": self.id,
            "name": self.name,
            "teacher_id": self.teacher_id
        }
        return dict_obj