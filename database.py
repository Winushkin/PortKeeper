import datetime
import sqlite3

class DataBase:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
#        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def db_close(self):
        self.connection.close()

    def create_tables(self):
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
        self.cursor.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS teachers ( 
            teacher_id           INTEGER NOT NULL  PRIMARY KEY  AUTOINCREMENT,
            name                 TEXT NOT NULL  ,
            login                TEXT NOT NULL  ,
            password             TEXT NOT NULL  ,
            post                 TEXT NOT NULL  ,
            avatar               BLOB           ,
            created_at           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP   
        );
        """
        self.cursor.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS portfolio  ( 
            portfolio_id         INTEGER NOT NULL  PRIMARY KEY  AUTOINCREMENT   ,
            event_name           TEXT NOT NULL                                  ,
            event_type           TEXT NOT NULL                                  ,
            student_id           INTEGER NOT NULL                               ,
            created_at           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP    ,
            file_uuid            BLOB                                           ,
            event_level          TEXT                                           ,
            event_result         TEXT                                           ,
            event_date           TEXT                                           ,
            event_date           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
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


#__________________________________________________________TEACHERS_____________________________________________________
    def get_teacher(self, login, password):
        sql = """SELECT * FROM teachers WHERE login = ? AND password = ?"""
        self.cursor.execute(sql, (login, password))
        result = self.cursor.fetchone()
        if not result:
            return None
        return result


    def get_teacher_by_teacher_id(self, teacher_id):
        sql = """SELECT * FROM teachers WHERE teacher_id =?"""
        self.cursor.execute(sql, (teacher_id,))
        result = self.cursor.fetchone()
        if not result:
            return None
        return result

    def insert_teachers_avatar(self, avatar, teacher_id):
        sql = """UPDATE teachers 
                 SET avatar = ?
                 WHERE teacher_id = ?"""
        self.cursor.execute(sql, (avatar, teacher_id))
        self.connection.commit()


    def insert_teacher(self, name):
        password = self.generate_password_for_user()
        sql = """INSERT INTO teachers (name, password) VALUES (?, ?)"""
        self.cursor.execute(sql, (name, password))
        self.connection.commit()




#_______________________________________________________STUDENTS________________________________________________________

    def get_students_by_teacher_id(self, teacher_id):
        sql = """SELECT * FROM students WHERE teacher_id = ?"""
        self.cursor.execute(sql, (teacher_id,))
        return self.cursor.fetchall()


    def get_student(self, login, password):
        sql = """SELECT * FROM students WHERE password = ? AND login = ?"""
        self.cursor.execute(sql, (password, login))
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

    def insert_student(self, name, login, password, teacher_id, class_num, old):
        sql = """INSERT INTO students (name, login, password, teacher_id, class, old) 
                 VALUES (?, ?, ? ,?, ?, ?)"""
        self.cursor.execute(sql, (name, login, password, teacher_id, class_num, old))
        self.connection.commit()

    def update_students_novelty(self, student_id):
        sql = """UPDATE students
                 SET old = 1
                 WHERE student_id = ?"""
        self.cursor.execute(sql, (student_id,))
        self.connection.commit()

    def insert_student_avatar(self, avatar, student_id):
        sql = """UPDATE students 
                 SET avatar = ?
                 WHERE student_id = ?"""
        self.cursor.execute(sql, (avatar, student_id))
        self.connection.commit()

#_______________________________________________________PORTFOLIO_______________________________________________________


    def get_portfolio_by_student_id(self, student_id):
        sql = """SELECT * FROM portfolio WHERE student_id = ?"""
        self.cursor.execute(sql, (student_id,))
        return self.cursor.fetchall()


    def insert_portfolio(self, event_name, event_type, student_id, event_level, file_uuid, event_result, event_date):
        sql = """INSERT INTO portfolio (event_name, event_type, student_id, event_level, file_uuid, event_result, event_date)
                 VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql,
                            (event_name, event_type, student_id ,event_level, file_uuid, event_result, event_date))
        self.connection.commit()


#________________________________________________________EXAMS__________________________________________________________


    def get_exams_by_student_id(self, student_id):
        sql = """SELECT * FROM exams WHERE student_id = ?"""
        self.cursor.execute(sql, (student_id,))
        return self.cursor.fetchall()


    def insert_exams(self, subject, mark, student_id):
        sql = """INSERT INTO exams (subject, mark, student_id)
                  VALUES (?, ?, ?)"""
        self.cursor.execute(sql, (subject, mark, student_id))
        self.connection.commit()


    def delete_exams(self, student_id):
        sql = """DELETE FROM exams
                 WHERE student_id = ?"""
        self.cursor.execute(sql, (student_id,))
        self.connection.commit()

#________________________________________________________GENERAL________________________________________________________

    def check_uniq_login(self, login):
        sql = """SELECT * FROM students
                 WHERE login = ?"""
        self.cursor.execute(sql, (login, ))
        self.connection.commit()



if __name__ == '__main__':
    db = DataBase("database/base.sqlite3")
    db.create_tables()
