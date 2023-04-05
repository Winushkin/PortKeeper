import datetime
import sqlite3
from password_generator import PasswordGenerator


class DataBase:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def db_close(self):
        self.connection.close()

    def create_tables(self):
        sql = """
        CREATE TABLE IF NOT EXISTS students ( 
            student_id           INTEGER NOT NULL  PRIMARY KEY  AUTOINCREMENT ,
            name                 TEXT NOT NULL                                ,
            password             TEXT NOT NULL                                ,
            avatar               BLOB                                         ,
            birth_date           DATE                                         ,
            created_at           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP  ,
            class                TEXT NOT NULL                                ,
            teacher_id           INTEGER NOT NULL                             ,
            event_time           TEXT NOT NULL                                ,
            FOREIGN KEY ( teacher_id ) REFERENCES teachers( teacher_id ) ON DELETE CASCADE ON UPDATE CASCADE
        );
        """
        self.cursor.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS teachers ( 
            teacher_id           INTEGER NOT NULL  PRIMARY KEY  AUTOINCREMENT,
            name                 TEXT NOT NULL    ,
            password             TEXT NOT NULL    ,
            avatar               BLOB     ,
            created_at           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP   
        );
        """
        self.cursor.execute(sql)
        sql = """CREATE TABLE IF NOT EXISTS portfolio  ( 
            portfolio_id         INTEGER NOT NULL  PRIMARY KEY  AUTOINCREMENT,
            event_name           TEXT NOT NULL    ,
            event_type           TEXT NOT NULL    ,
            student_id           INTEGER NOT NULL    ,
            created_at           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
            event_file_uuid      TEXT     ,
            event_level          TEXT     ,
            event_result         TEXT     ,
            FOREIGN KEY ( student_id ) REFERENCES students( student_id ) ON DELETE CASCADE ON UPDATE CASCADE
        );"""
        self.cursor.execute(sql)
        sql = """CREATE TABLE IF NOT EXISTS exams ( 
                    exam_id           INTEGER NOT NULL  PRIMARY KEY  AUTOINCREMENT,
                    subject           TEXT,
                    mark              INTEGER,
                    student_id        INTEGER NOT NULL,
                    created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY ( student_id ) REFERENCES students( student_id ) ON DELETE CASCADE ON UPDATE CASCADE
 
                );
                """
        self.cursor.execute(sql)
        self.connection.commit()

    def get_portfolio_by_student_id(self, student_id):
        sql = """SELECT * FROM portfolio WHERE student_id = ?"""
        self.cursor.execute(sql, (student_id,))
        return self.cursor.fetchall()


    def get_exams_by_student_id(self, student_id):
        sql = """SELECT * FROM exams WHERE student_id = ?"""
        self.cursor.execute(sql, (student_id,))
        return self.cursor.fetchall()


    def get_students_by_teacher_id(self, teacher_id):
        sql = """SELECT * FROM students WHERE teacher_id = ?"""
        self.cursor.execute(sql, (teacher_id,))
        return self.cursor.fetchall()

    def get_teacher(self, name, password):
        sql = """SELECT * FROM teachers WHERE password = ? AND name = ?"""
        self.cursor.execute(sql, (password, name))
        result = self.cursor.fetchone()
        if not result:
            return None
        return result

    def get_student(self, name, password):
        sql = """SELECT * FROM students WHERE password = ? AND name = ?"""
        self.cursor.execute(sql, (password, name))
        result = self.cursor.fetchone()
        if not result:
            return None
        return result


    def get_student_by_student_id(self, student_id):
        sql = """SELECT * FROM students WHERE student_id = ?"""
        self.cursor.execute(sql, (student_id, ))
        result = self.cursor.fetchone()
        if not result:
            return None
        return result



    def insert_student(self, name, password, teacher_id, learn_class):
        sql = f"""INSERT INTO students (name, password, teacher_id, class) VALUES (?, ? ,?, ?)"""
        self.cursor.execute(sql, (name, password, teacher_id, learn_class))
        self.connection.commit()

    def insert_teacher(self, name):
        password = self.generate_password_for_user()
        sql = """INSERT INTO teachers (name, password) VALUES (?, ?)"""
        self.cursor.execute(sql, (name, password))
        self.connection.commit()

    def insert_portfolio(self, event_name, event_type, student_id, event_file_uuid ,event_level, event_result, event_date):
        sql = """INSERT INTO portfolio (event_name, event_type, student_id, 
        event_file_uuid ,event_level, event_result, event_date) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql, (event_name, event_type, student_id, event_file_uuid ,event_level, event_result, event_date))
        self.connection.commit()


    def insert_exams(self, subject, mark, student_id):
        sql = """INSERT INTO exams (subject, mark, student_id)
                 VALUES (?, ?, ?)"""
        self.cursor.execute(sql, (subject, mark, student_id))
        self.connection.commit()

    def delete_exams(self, student_id):
        sql ="""DELETE FROM exams
                WHERE student_id = ?"""
        self.cursor.execute(sql, (student_id, ))
        self.connection.commit()

    @staticmethod
    def generate_password_for_user():
        pwo = PasswordGenerator()
        pwo.minlen = 8
        pwo.maxlen = 8
        pwo.minuchars = 2
        pwo.minlchars = 2
        pwo.minnumbers = 2
        pwo.minschars = 2
        return pwo.generate()


if __name__ == '__main__':
    db = DataBase("base.sqlite3")
    db.create_tables()