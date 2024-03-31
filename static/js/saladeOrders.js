// Function to fetch data and populate the orders table
window.onload = function() {
    fetch('/get-saladeOrders-data')
        .then(response => response.json())
        .then(data => {
            populateTable(data.reverse());
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
        actionsCell.classList.add('m-auto');
        
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
    
    const columnNames = ['Date', 'Salade Thon', 'Salade Poulet'];
    
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
    const formData = new FormData(document.getElementById('edit-form')); // Utiliser l'ID du formulaire

    // Parcourir les données du formulaire et les ajouter à l'objet updatedData
    formData.forEach((value, key) => {
        updatedData[key] = value;
    });

    // Send updated data to server via POST request
    fetch('/update-salade', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'  // Assurez-vous que le type de contenu est défini sur JSON
        },
        body: JSON.stringify(updatedData) // Convertir les données en JSON avant de les envoyer
    })
    .then(response => {
        // Gérer la réponse du serveur
    })
    .catch(error => {
        console.error('Erreur lors de la mise à jour de la tâche :', error);
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




