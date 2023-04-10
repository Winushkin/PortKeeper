from zipfile import ZipFile
import uuid
from flask import url_for


def file_zipping(port_list):
    files = [portfolio[5] for portfolio in port_list]
    archive_name = str(uuid.uuid4()) + ".zip"
    with ZipFile("static/files/" + archive_name, "w") as zf:
         for file in files:
             file_path = url_for("static", filename=f"files/{file}")
             zf.write("." + file_path)
    return archive_name


# file_zipping([(22, 'Олимпиада Яндекс Учебник', 'Информатика', 10, '2023-04-05 22:55:09', '39f78937-7f19-4f1a-9598-e2cc60111d85.pdf', 'Международный', 'Победа', '09.03.2023'), (23, 'Олимпиада Яндекс Учебник', 'инфа', 10, '2023-04-06 09:19:14', 'f3a22ded-1bbe-4129-9e99-96f3c5d10088.pdf', 'Всероссийский', 'Победа', '09.03.2023'), (24, 'Олимпиада Яндекс Учебник', 'Информатика', 10, '2023-04-06 09:19:32', 'a2dd89e4-dcd7-4306-a74f-ef4cfe0a98ec.jpg', 'Региональный', 'Победа', '09.03.2023')]
# )