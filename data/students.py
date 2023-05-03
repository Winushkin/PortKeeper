import sqlalchemy
import datetime
from .db_session import SqlAlchemyBase


sql = """
        CREATE TABLE IF NOT EXISTS students ( 
            student_id           INTEGER NOT NULL  PRIMARY KEY  AUTOINCREMENT ,
            name                 TEXT NOT NULL                                ,
            login                TEXT NOT NULL                                ,
            password             TEXT NOT NULL                                ,
            avatar               BLOB                                         ,
            birth_date           DATE                                         ,
            created_at           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP  ,
            class                TEXT NOT NULL                                ,
            teacher_id           INTEGER NOT NULL                             ,
            event_time           TEXT NOT NULL                                ,
            old                  INTEGER NOT NULL                             ,
            FOREIGN KEY ( teacher_id ) REFERENCES teachers( teacher_id ) ON DELETE CASCADE ON UPDATE CASCADE
        );
        """




class Students(SqlAlchemyBase):
    __tablename__ = "students"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    login = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)
    avatar = sqlalchemy.Column(sqlalchemy.BLOB, default=None)
    birth_date = sqlalchemy.Column(sqlalchemy.Date)
    created_date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.date.today())
    level = sqlalchemy.Column(sqlalchemy.String)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer)
