document.addEventListener("DOMContentLoaded", () => {


    const forms = document.querySelectorAll("form");


    for (let i = 1; i <= 4; i++) { // сюда будем помещать drug-&-drop файлы (4)
        window["uploadDragFiles_"+i] = new Object();
    }


    document.querySelectorAll(".upload-file__wrapper").forEach(function (current_item, index) {


        const inputFile = current_item.querySelector(".upload-file__input");


        // создаём массив файлов
        let fileList = [];


        /////////// Кнопка «Прикрепить файл» ///////////
        let textSelector = current_item.querySelector(".upload-file__text");


        // Событие выбора файла(ов)
        inputFile.addEventListener("change", function () {
            fileList.push(...inputFile.files);
            // console.log(inputFile.files);
            // вызов функции для каждого файла
            fileList.forEach(file => {
                uploadFile(file);
            });
        });


        // Проверяем размер файлов и выводим название
        const uploadFile = (file) => {


            // размер файла <5 Мб
            if (file.size > 5 * 1024 * 1024) {
                alert("Файл должен быть не более 5 МБ.");
                return;
            }


            // Показ загружаемых файлов
            if (file && fileList.length > 1) {
                if (fileList.length <= 4) {
                    textSelector.textContent = `Выбрано ${fileList.length} файла`;
                } else {
                    textSelector.textContent = `Выбрано ${fileList.length} файлов`;
                }
            } else {
                textSelector.textContent = file.name;
            }
            fileList = [];
        }




        /////////// Загрузка файлов при помощи «Drag-and-drop» ///////////
        // const dropZones = document.querySelectorAll(".upload-file__label");
        const dropZone = current_item.querySelector(".upload-file__label");
        const dropZoneText = current_item.querySelector(".upload-file__text");
        const maxFileSize = 5000000; // максимальный размер файла - 5 мб.


        // Проверка поддержки «Drag-and-drop»
        if (typeof (window.FileReader) == "undefined") {
            dropZone.textContent = "Drag&Drop Не поддерживается браузером!";
            dropZone.classList.add("error");
        }
        // Событие - перетаскивания файла
        dropZone.ondragover = function () {
            this.classList.add("hover");
            return false;
        };
        // Событие - отмена перетаскивания файла
        dropZone.ondragleave = function () {
            this.classList.remove("hover");
            return false;
        };
        // Событие - файл перетащили
        dropZone.addEventListener("drop", function (e) {
            e.preventDefault();
            this.classList.remove("hover");
            this.classList.add("drop");


            uploadDragFiles = e.dataTransfer.files[0]; // один файл


            // Проверка размера файла
            if (uploadDragFiles.size > maxFileSize) {
                dropZoneText.textContent = "Размер превышает допустимое значение!";
                this.addClass("error");
                return false;
            }


            // Показ загружаемых файлов
            if (uploadDragFiles.length > 1) {
                if (uploadDragFiles.length <= 4) {
                    dropZoneText.textContent = `Выбрано ${uploadDragFiles.length} файла`;
                } else {
                    dropZoneText.textContent = `Выбрано ${uploadDragFiles.length} файлов`;
                }
            } else {
                dropZoneText.textContent = e.dataTransfer.files[0].name;
            }


            // добавляем файл в объект "uploadDragFiles_i"
            window["uploadDragFiles_"+index] = uploadDragFiles;
        });


    });



    //
    // // Отправка формы на сервер
    // const postData = async (url, fData) => { // имеет асинхронные операции
    //
    //
    //     // начало отправки
    //     // здесь можно сообщить пользователю о начале отправки
    //
    //
    //     // ждём ответ, только тогда наш код пойдёт дальше
    //     let fetchResponse = await fetch(url, {
    //         method: "POST",
    //         body: fData
    //     });
    //
    //
    //     // ждём окончания операции
    //     return await fetchResponse.text();
    // };
    //
    //
    // if (forms) {
    //     forms.forEach(el => {
    //         el.addEventListener("submit", function (e) {
    //             e.preventDefault();
    //
    //
    //             // создание объекта FormData
    //             let fData = new FormData(this);
    //
    //
    //             // Добавление файлов input type file
    //             el.querySelectorAll(".upload-file__input").forEach((one_file, index) => {
    //                 for (let i = 0; i < (one_file.files.length); i++) {
    //                     fData.append("files[]", one_file.files[i]); // добавляем файлы, добавленные кнопкой
    //                 }
    //                 fData.append("files[]", window["uploadDragFiles_"+index]); // добавляем drug-&-drop файлы
    //             });
    //
    //
    //             // Отправка на сервер
    //             postData("./mail-files.php", fData)
    //                 .then(fetchResponse => {
    //                     swal({
    //                         title: "Спасибо!",
    //                         text: "Данные отправлены.",
    //                         icon: "success",
    //                         button: "Ok"
    //                     });
    //                     // console.table("Данные успешно отправлены!", fetchResponse);
    //                     el.reset(); // Очистка полей формы
    //                     document.querySelectorAll(".upload-file__text").forEach(this_text => {
    //                         this_text.textContent = "Выберите файл или перетащите в поле";
    //                     });
    //                 })
    //                 .catch(function (error) {
    //                     swal({
    //                         title: error,
    //                         icon: "error",
    //                         button: "Ok"
    //                     });
    //                     // console.table("Ошибка!", error);
    //                 });
    //         });
    //     });
    // };
    //

});
