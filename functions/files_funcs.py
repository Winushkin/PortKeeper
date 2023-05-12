import os
from uuid import uuid4
from database import DataBase
import fitz

db = DataBase("database/base.sqlite3")
db.create_tables()


def download_zip():
    portfolio = db.get_portfolio_by_student_id(student_id)
    archive = file_zipping(portfolio)
    zip_sender = send_from_directory(DOWNLOAD_FOLDER, archive, as_attachment=True)
    zip_delete(archive)


