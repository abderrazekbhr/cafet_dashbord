import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

data=pd.read_csv("static/data_base/Final_Dataset.csv")



data_j = data.iloc[5:,:]
data_j = data_j.reset_index(drop=True).dropna()
data_j_5=data.iloc[:len(data)-5,:]
data_j_5 = data_j_5.reset_index(drop=True).dropna()


# Define an empty dictionary to store X_train and y_train for each product
dicto = {}

for product in ["Pain au chocolat", "Croissant", "Pains suisses","Sandwiches poulet crudités",
                "Sandwiches thon crudités", "Sandwiches végétarien", "Sandwiches poulet mexicain",
                "Sandwiches chèvre miel crudités","Sandwiches poulet curry","Sandwiches saumon",
                "Panini 4 fromages","Panini poulet Kebab", "Salade Thon","Salade Poulet"]:
    
    
    X=np.array(data_j_5[product]).reshape(-1,1)
    #y prend les commandes des produits des jours présents
    y = data_j[product]
    # Séparez les 5 dernières lignes pour les prédictions
    X_test = X[-5:]
    y_test = y[-5:]

    # Les lignes restantes pour l'entraînement
    X_train = X[:-5]
    y_train = y[:-5]
    
    # Store X_train and y_train in the data dictionary
    dicto[product] = {'X_train': X_train, 'y_train': y_train,'X_test': X_test, 'y_test': y_test}
print("yes je me suis bien executé")
