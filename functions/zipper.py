from zipfile import ZipFile
import uuid
from flask import url_for
import os


def file_zipping(port_list):
    files = [portfolio.file_uuid for portfolio in port_list]
    archive_name = str(uuid.uuid4()) + ".zip"
    with ZipFile("static/files/" + archive_name, "w") as zf:
         for file in files:
             file_path = url_for("static", filename=f"files/{file}")
             zf.write("." + file_path)
    return archive_name



def zip_delete(archive_name):
    os.remove(f"./static/files/{archive_name}")