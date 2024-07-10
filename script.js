document.getElementById('tableSearchInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        searchTable();
        e.preventDefault(); // Prevenir o envio do formulário
    }
});

document.getElementById('tableSearchInput').addEventListener('input', function () {
    if (this.value === '') {
        resetTable(); // Resetar a tabela se o campo de pesquisa estiver vazio
    }
});

function searchTable() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("tableSearchInput");
    filter = input.value.toLowerCase();
    table = document.getElementById("contactTable");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        tr[i].style.display = "none";  // Esconder todas as linhas inicialmente
        td = tr[i].getElementsByTagName("td")[2];  // Obter a coluna "Nome" (índice 2)
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toLowerCase().indexOf(filter) > -1) {
                tr[i].style.display = "";  
            }
        }
    }

    // Definir um temporizador para resetar a tabela após 2 minutos (120000 milissegundos)
    setTimeout(resetTable, 120000);
}

function resetTable() {
    var table, tr, i;
    table = document.getElementById("contactTable");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        tr[i].style.display = "";  // Mostrar todas as linhas
    }
}
