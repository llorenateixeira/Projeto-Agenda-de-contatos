document.getElementById('tableSearchInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        searchTable();
        e.preventDefault(); // Prevent form submission
    }
});

function searchTable() {
    var input, filter, table, tr, td, i, j, txtValue, firstMatch;
    input = document.getElementById("tableSearchInput");
    filter = input.value.toLowerCase();
    table = document.getElementById("contactTable");
    tr = table.getElementsByTagName("tr");
    firstMatch = null;

    for (i = 0; i < tr.length; i++) {
        tr[i].classList.remove("highlight");  // Remove previous highlights
        td = tr[i].getElementsByTagName("td");
        for (j = 0; j < td.length; j++) {
            if (td[j]) {
                txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toLowerCase().indexOf(filter) > -1) {
                    tr[i].classList.add("highlight");  // Highlight matching row
                    if (!firstMatch) {
                        firstMatch = tr[i];
                    }
                    break;  // Stop checking other cells in this row
                }
            }
        }
    }

    // Scroll to the first match
    if (firstMatch) {
        firstMatch.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}
