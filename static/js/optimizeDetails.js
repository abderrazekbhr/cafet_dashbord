// Function to fetch data and populate the orders table
window.onload = function() {
    fetch('/get-grid-data')
        .then(response => response.json())
        .then(data => {
            populateTable(data);
        });
};

// Function to populate the table with data
function populateTable(data) {
    const tableBody = document.getElementById('orders-body');
    data.forEach(entry => {
        const row = document.createElement('tr');
        // Add data from each entry into a cell
        for (const key in entry) {
            const cell = document.createElement('td');
            cell.textContent = entry[key];
            row.appendChild(cell);
        }
        // Add the row to the table body
        tableBody.appendChild(row);
    });
}