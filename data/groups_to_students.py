import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm

class GroupToStudent(SqlAlchemyBase):
    __tablename__ = "groups_to_students"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"))
    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("students.id"))
    group = orm.relationship("Group")
    student = orm.relationship("Student")


    # def to_dict(self):
    #     dict_obj = {
    #         "id": self.id,
    #         "name": self.name,
    #         "teacher_id": self.teacher_id
    #     }
    #     return dict_obj