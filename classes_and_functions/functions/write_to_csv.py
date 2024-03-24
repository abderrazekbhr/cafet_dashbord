def write_to_csv(product, prediction):
    csv_file = 'classes_and_functions/csv/prediction.csv'

    # Lire le fichier CSV et stocker les données dans une liste
    try:
        with open(csv_file, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
    except FileNotFoundError:
        rows = []

    # Rechercher le produit dans la liste et le mettre à jour s'il existe
    product_found = False
    for row in rows:
        if row and row[0] == product:
            row[1:] = prediction.tolist()
            product_found = True
            break

    # Si le produit n'a pas été trouvé, ajouter une nouvelle entrée pour le produit
    if not product_found:
        rows.append([product] + prediction.tolist())

    # Écrire la liste mise à jour dans le fichier CSV
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
            