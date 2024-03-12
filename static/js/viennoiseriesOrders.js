// Function to fetch data and populate the orders table
window.onload = function() {
    fetch('/get-viennoiseriesOrders-data')
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

        // Add action buttons into a cell
        const actionsCell = document.createElement('td');
        actionsCell.classList.add('align-middle'); // Vertically center content

        const editButton = document.createElement('button');
        editButton.classList.add('btn');
        editButton.classList.add('btn-warning');
        editButton.classList.add('shadow-none');
        editButton.classList.add('mx-2');

        editButton.innerHTML = '<ion-icon name="pencil-outline" class="modify"></ion-icon>';
        editButton.onclick = function() {
            openModalForEdit(row); // Open modal for editing
        };

        const deleteButton = document.createElement('button');
        deleteButton.classList.add('btn');
        deleteButton.classList.add('btn-danger');
        deleteButton.classList.add('shadow-none');
        deleteButton.classList.add('mx-2');
        
        deleteButton.innerHTML = '<ion-icon name="trash-outline" class="delete"></ion-icon>';
        deleteButton.onclick = function() {
            deleteTask(row);
        };

        actionsCell.appendChild(editButton);
        actionsCell.appendChild(deleteButton);

        row.appendChild(actionsCell);

        // Add the row to the table body
        tableBody.appendChild(row);
    });
}

// Function to delete a task
function deleteTask(row) {
    // Ask the user if they really want to delete the task
    const confirmation = confirm("Êtes-vous sûr de vouloir effacer cet ordre ?");

    // Remove the row only if the user confirms
    if (confirmation) {
        const tableBody = row.parentNode;
        tableBody.removeChild(row);
    }
}


// Function to fill the modal with task data for editing
function fillModal(row) {
    const cells = row.getElementsByTagName('td');
    const modalBody = document.querySelector('.modal-body');
    modalBody.innerHTML = ''; // Clear previous modal body content
    
    const columnNames = ['Date', 'Pain au chocolat', 'Croissant', 'Pains suisses'];
    
    for (let i = 0; i < cells.length - 1; i++) {
        const label = document.createElement('label');
        label.textContent = `${columnNames[i]}: `;
        const input = document.createElement('input');
        input.type = 'text';
        input.value = cells[i].textContent;
        input.name = `data${i + 1}`;
        
        // Create a div to contain label and input elements
        const div = document.createElement('div');
        div.appendChild(label);
        div.appendChild(input);
        
        // Append the div to modal body
        modalBody.appendChild(div);
    }
}

// Function to update a task
function updateTask() {
    // Extract the updated data from the modal form
    const updatedData = {};
    // Fill updatedData object with form field values

    // Send updated data to server via POST request
    fetch('/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(updatedData)
    })
    .then(response => {
        // Handle response, e.g., update UI if successful
    })
    .catch(error => {
        console.error('Error updating task:', error);
    });
}

// Function to open the modal with the selected row's data
function openModalForEdit(row) {
    // Your existing code

    // Display the modal using Bootstrap modal method
    $('.modal').modal('show');
    fillModal(row); // Call fillModal function to fill modal with task data
}

// Function to close the modal
function closeModal() {
    // Hide the modal using Bootstrap modal method
    $('.modal').modal('hide');
}

function addNewRow() {
    // Boîte de dialogue pour saisir les données de la nouvelle ligne
    const formData = prompt("Ajouter une nouvelle ligne", "Date, Salade Thon, Salade Poulet");

    if (formData !== null && formData.trim() !== "") {
        // Séparez les données saisies en utilisant une virgule comme séparateur
        const dataArray = formData.split(',');

        // Assurez-vous qu'il y a suffisamment de données pour chaque colonne
        if (dataArray.length >= 3) {
            const tableBody = document.getElementById('orders-body');
            const newRow = document.createElement('tr');

            // Ajoutez les données saisies dans chaque cellule de la nouvelle ligne
            for (let i = 0; i < 3; i++) {
                const cell = document.createElement('td');
                cell.textContent = dataArray[i].trim();
                newRow.appendChild(cell);
            }

            // Ajoutez les boutons d'action dans une cellule
            const actionsCell = document.createElement('td');
            actionsCell.classList.add('align-middle'); // Pour centrer verticalement le contenu

            const editButton = document.createElement('button');
            editButton.innerHTML = '<ion-icon name="pencil-outline" class="modify"></ion-icon>';
            editButton.onclick = function() {
                editTask(newRow);
            };

            const deleteButton = document.createElement('button');
            deleteButton.innerHTML = '<ion-icon name="trash-outline" class="delete"></ion-icon>';
            deleteButton.onclick = function() {
                deleteTask(newRow);
            };

            actionsCell.appendChild(editButton);
            actionsCell.appendChild(deleteButton);

            newRow.appendChild(actionsCell);

            // Ajoutez la nouvelle ligne au tableau
            tableBody.appendChild(newRow);
        } else {
            // Si moins de trois données sont fournies, affichez un message d'erreur
            alert("Veuillez saisir au moins une date, une salade thon et une salade poulet.");
        }
    }
}
