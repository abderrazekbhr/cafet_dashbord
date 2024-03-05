// Function to fetch data and populate the orders table
window.onload = function() {
    fetch('/add-order')
        .then(response => response.json())
        .then(data => {
            populateTable(data);
        });
};


function addNewRow() {
    

    if (formData !== null && formData.trim() !== "") {
        // Séparez les données saisies en utilisant une virgule comme séparateur
        const dataArray = formData.split(',');

        // Assurez-vous qu'il y a suffisamment de données pour chaque colonne
        if (dataArray.length >= 15) { // Mettez à jour le nombre de données en fonction de votre formulaire HTML
            // Créez un objet pour contenir les données à envoyer
            const newData = {
                date: dataArray[0].trim(),
                saladeThon: dataArray[1].trim(),
                saladePoulet: dataArray[2].trim(),
                // Ajoutez d'autres colonnes de données selon votre structure de données
                sandwichesPouletCrudites: dataArray[3].trim(),
                sandwichesThonCrudites: dataArray[4].trim(),
                sandwichesVegetarien: dataArray[5].trim(),
                sandwichesPouletMexicain: dataArray[6].trim(),
                sandwichesChevreMielCrudites: dataArray[7].trim(),
                sandwichesPouletCurry: dataArray[8].trim(),
                sandwichesSaumon: dataArray[9].trim(),
                panini4Fromages: dataArray[10].trim(),
                paniniPouletKebab: dataArray[11].trim(),
                painAuChocolat: dataArray[12].trim(),
                croissant: dataArray[13].trim(),
                painsSuisses: dataArray[14].trim(),
            };

            // Effectuez une requête POST vers l'endpoint Flask pour ajouter la commande
            fetch('/add-order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newData)
            })
            .then(response => response.json())
            .then(data => {
                // Traitez la réponse si nécessaire
                console.log(data);
            })
            .catch(error => {
                console.error('Error adding order:', error);
            });
        } else {
            // Si moins de données sont fournies, affichez un message d'erreur
            alert("Veuillez saisir toutes les données nécessaires.");
        }
    }
}




