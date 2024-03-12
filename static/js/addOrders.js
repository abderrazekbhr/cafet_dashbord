// Function to fetch data and populate the orders table
window.onload = function() {
    fetch('/add-order')
        .then(response => response.json())
        .then(data => {
            populateTable(data);
        });
};


function addNewRow() {
    // Obtenez les valeurs des champs du formulaire
    const formData = {
        date: $('input[type="date"]').val(),
        saladeThon: $('input[name="saladeThon"]').val(),
        saladePoulet: $('input[name="saladePoulet"]').val(),
        sandwichesPouletCrudites: $('input[name="sandwichesPouletCrudites"]').val(),
        sandwichesThonCrudites: $('input[name="sandwichesThonCrudites"]').val(),
        sandwichesVegetarien: $('input[name="sandwichesVegetarien"]').val(),
        sandwichesPouletMexicain: $('input[name="sandwichesPouletMexicain"]').val(),
        sandwichesChevreMielCrudites: $('input[name="sandwichesChevreMielCrudites"]').val(),
        sandwichesPouletCurry: $('input[name="sandwichesPouletCurry"]').val(),
        sandwichesSaumon: $('input[name="sandwichesSaumon"]').val(),
        panini4Fromages: $('input[name="panini4Fromages"]').val(),
        paniniPouletKebab: $('input[name="paniniPouletKebab"]').val(),
        painAuChocolat: $('input[name="painAuChocolat"]').val(),
        croissant: $('input[name="croissant"]').val(),
        painsSuisses: $('input[name="painsSuisses"]').val(),
    };

    // Effectuez une requête POST vers l'endpoint Flask pour ajouter la commande
    fetch('/add-order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData) // Envoyez les données sérialisées au backend
    })
    .then(response => response.json())
    .then(data => {
        // Affichez une alerte lorsque la commande est ajoutée avec succès
        alert(data.message);
    })
    .catch(error => {
        console.error('Error adding order:', error);
    });
}




