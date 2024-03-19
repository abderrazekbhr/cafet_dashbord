// Function to fetch data and populate the orders table
window.onload = function() {
    fetch('/add-order')
        .then(response => response.json())
        .then(data => {
            populateTable(data);
        });
};


function addNewRow() {
     // Get the current date in "dd/mm/yyyy" format
     const currentDate = new Date();
     const day = String(currentDate.getDate()).padStart(2, '0');
     const month = String(currentDate.getMonth() + 1).padStart(2, '0'); // Month is zero-based
     const year = currentDate.getFullYear();
     const formattedDate = `${day}/${month}/${year}`;
 
     // Update the date field value in the form
     $('input[type="date"]').val(formattedDate);

     // Default day
    const defaultDay = "Mardi"; // Change this to whatever default day you want
    
    // Obtenez les valeurs des champs du formulaire
    const formData = {
        jour: defaultDay,
        date: formattedDate,
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




