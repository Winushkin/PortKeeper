let rows = document.querySelectorAll(".marks-2 tbody tr");

let tbody = document.querySelector(".marks-2 > tbody");

let headers = document.querySelectorAll(".marks-2 th");


headers.forEach(function(header){
    header.addEventListener("click", function(e){
        let sortedRows = Array.from(rows)
        if (e.target.textContent == 'Уровень') {
            if (e.target.dataset.sort == 'up') {
                sortedRows.sort(function(a, b){
                    return a.cells[0].innerHTML > b.cells[0].innerHTML ? 1 : -1;
                });
                e.target.dataset.sort = 'down'
            } else {
                sortedRows.sort(function(a, b){
                    return a.cells[0].innerHTML < b.cells[0].innerHTML ? 1 : -1;
                });
                e.target.dataset.sort = 'up'
            }

           
            tbody.append(...sortedRows);
        }
        
        if (e.target.textContent == 'Предмет') {
            if (e.target.dataset.sort == 'up') {
            sortedRows.sort(function(a, b){
                return a.cells[1].innerHTML > b.cells[1].innerHTML ? 1 : -1;
            });
            e.target.dataset.sort = "down"
        } else {
            sortedRows.sort(function(a, b){
                return a.cells[1].innerHTML < b.cells[1].innerHTML ? 1 : -1;
            });
            e.target.dataset.sort = 'up'
        }

            tbody.append(...sortedRows);
        }
        if (e.target.textContent == 'Название') {
            if (e.target.dataset.sort == 'up') {
                sortedRows.sort(function(a, b){
                    return a.cells[2].innerHTML > b.cells[2].innerHTML ? 1 : -1;
                });
                e.target.dataset.sort = "down"
            } else {
                sortedRows.sort(function(a, b){
                    return a.cells[2].innerHTML < b.cells[2].innerHTML ? 1 : -1;
                });
                e.target.dataset.sort = 'up'
            }
            
            tbody.append(...sortedRows);
        }
        if (e.target.textContent == 'Дата') {
            if (e.target.dataset.sort == 'up') {
                sortedRows.sort(function(a, b){
                    return new Date(a.cells[3].innerHTML) > new Date(b.cells[3].innerHTML) ? 1 : -1;
                }); 
                e.target.dataset.sort = "down"
            } else {
                sortedRows.sort(function(a, b){
                    return new Date(a.cells[3].innerHTML) < new Date(b.cells[3].innerHTML) ? 1 : -1;
                }); 
                e.target.dataset.sort = 'up'
            } 
            
            tbody.append(...sortedRows);
        }
        if (e.target.textContent == 'Результаты') {
            if (e.target.dataset.sort == 'up') {
                sortedRows.sort(function(a, b){
                    return a.cells[4].innerHTML > b.cells[4].innerHTML ? 1 : -1;
                });
                e.target.dataset.sort = "down"
            } else {
                sortedRows.sort(function(a, b){
                    return a.cells[4].innerHTML < b.cells[4].innerHTML ? 1 : -1;
                });
                e.target.dataset.sort = 'up'
            }
            
            tbody.append(...sortedRows);
        }
    });
});


