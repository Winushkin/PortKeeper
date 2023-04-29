let rows = document.querySelectorAll(".marks-2 tbody tr");

let tbody = document.querySelector(".marks-2 > tbody");

let headers = document.querySelectorAll(".marks-2 th");


headers.forEach(function(header){
    console.log(1)
    header.addEventListener("click", function(e){
        let sortedRows = Array.from(rows)
        if (e.target.textContent == 'Уровень') {
            sortedRows.sort(function(a, b){
                return a.cells[0].innerHTML > b.cells[0].innerHTML ? 1 : -1;
            });
            tbody.append(...sortedRows);
        }
        if (e.target.textContent == 'Предмет') {
            sortedRows.sort(function(a, b){
                return a.cells[1].innerHTML > b.cells[1].innerHTML ? 1 : -1;
            });
            tbody.append(...sortedRows);
        }
        if (e.target.textContent == 'Название') {
            sortedRows.sort(function(a, b){
                return a.cells[2].innerHTML > b.cells[2].innerHTML ? 1 : -1;
            });
            tbody.append(...sortedRows);
        }
        if (e.target.textContent == 'Дата') {
            // .sort()
        }
        if (e.target.textContent == 'Результаты') {
            // .sort()
        }
    });
});
