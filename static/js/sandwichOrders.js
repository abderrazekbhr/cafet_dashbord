// Function to fetch data and populate the orders table
window.onload = function() {
    fetch('/get-sandwichOrders-data')
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

        // Ajoutez les données de chaque entrée dans une cellule
        for (const key in entry) {
            const cell = document.createElement('td');
            cell.textContent = entry[key];
            row.appendChild(cell);
        }

        // Ajoutez les boutons d'action dans une cellule
        const actionsCell = document.createElement('td');
        actionsCell.classList.add('align-middle'); // Pour centrer verticalement le contenu
        
        const editButton = document.createElement('button');
        editButton.innerHTML = '<ion-icon name="pencil-outline" class="modify"></ion-icon>';
        editButton.onclick = function() {
            editTask(row);
        };

        const deleteButton = document.createElement('button');
        deleteButton.innerHTML = '<ion-icon name="trash-outline" class="delete"></ion-icon>';
        deleteButton.onclick = function() {
            deleteTask(row);
        };

        actionsCell.appendChild(editButton);
        actionsCell.appendChild(deleteButton);
        
        row.appendChild(actionsCell);

        // Ajoutez la ligne au corps du tableau
        tableBody.appendChild(row);
    });
}

// Function to edit a task
function editTask(row) {
    // Récupérer le texte de chaque cellule de la ligne
    const cells = row.getElementsByTagName('td');
    const data = [];
    for (let i = 0; i < cells.length - 1; i++) {
        data.push(cells[i].textContent);
    }

    // Demander à l'utilisateur de modifier les données
    const newData = prompt("Modifier les données de cet ordre :", data.join(', '));

    // Mettre à jour les données de la ligne si l'utilisateur a fourni de nouvelles données
    if (newData !== null && newData.trim() !== "") {
        const newDataArray = newData.split(',');
        for (let i = 0; i < newDataArray.length && i < data.length; i++) {
            cells[i].textContent = newDataArray[i].trim();
        }
    }
}

// Function to delete a task
function deleteTask(row) {
    // Demander à l'utilisateur s'il veut vraiment supprimer l'ordre
    const confirmation = confirm("Êtes-vous sûr de vouloir effacer cet ordre ?");

    // Supprimer la ligne uniquement si l'utilisateur confirme
    if (confirmation) {
        const tableBody = row.parentNode;
        tableBody.removeChild(row);
    }
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
