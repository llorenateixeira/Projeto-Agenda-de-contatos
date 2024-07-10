document.getElementById('tableSearchInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        searchTable();
        e.preventDefault(); // Prevent form submission
    }
});

function searchTable() {
    var input, filter, table, tr, td, i, j, txtValue;
    input = document.getElementById("tableSearchInput");
    filter = input.value.toLowerCase();
    table = document.getElementById("contactTable");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        tr[i].style.display = "none";  // Hide all rows initially
        td = tr[i].getElementsByTagName("td");
        for (j = 0; j < td.length; j++) {
            if (td[j]) {
                txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toLowerCase() === filter) {
                    tr[i].style.display = "";  // Show the row if an exact match is found
                    tr[i].classList.add("highlight");  // Highlight the matching row
                    break;  // Stop checking other cells in this row
                } else {
                    tr[i].classList.remove("highlight");  // Remove highlight if no match
                }
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
        tr[i].classList.remove("highlight");  // Remove highlight
    }
}
