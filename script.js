document.getElementById('tableSearchInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        searchTable();
        e.preventDefault(); // Prevent form submission
    }
});

function searchTable() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("tableSearchInput");
    filter = input.value.toLowerCase();
    table = document.getElementById("contactTable");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        tr[i].style.display = "none";  // Hide all rows initially
        td = tr[i].getElementsByTagName("td")[2];  // Get the "Nome" column (index 2)
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toLowerCase().indexOf(filter) > -1) {
                tr[i].style.display = "";  // Show the row if a match is found in the "Nome" column
            }
        }
    }

    // Set a timer to reset the table after 2 minutes (120000 milliseconds)
    setTimeout(resetTable, 120000);
}

function resetTable() {
    var table, tr, i;
    table = document.getElementById("contactTable");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        tr[i].style.display = "";  // Show all rows
    }
}
