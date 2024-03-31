from flask import Flask,render_template,request,redirect,session,jsonify
from flask_session import Session
import csv
from classes_and_functions.functions.login_test import test_login,update_data
from classes_and_functions.functions.read_data_csv import *
from classes_and_functions.functions.write_to_csv import *
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Lasso
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
import pickle
import numpy as np
import pandas as pd
from ml_grid import dicto
from math import sqrt
import subprocess

# Define models for optimization
models = {
    'Lasso': (Lasso(), {'alpha': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000]}),
    'SVR': (SVR(), {'C': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000], 'gamma': ['scale', 'auto', 0.0001, 0.001, 0.01, 0.1, 1, 10, 100]}),
    'KNN': (KNeighborsRegressor(), {'n_neighbors': [1, 3, 5, 7, 10, 15, 20, 25, 30, 35, 40, 45, 50], 'weights': ['uniform', 'distance'], 'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']}),
}

app =Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
@app.route('/', defaults={'path': ''})
@app.route('/',methods=['GET','POST'])
def login():
    if(session.get("token")=="connected"):
        return redirect("/main-salade", code=302)
    if(request.method=='GET'):
        return render_template('/pages/login.html',css_file="login.css",js_file="login.js") 
    else:
        email=request.form.get("email")
        password=request.form.get("password")
        if(test_login(email,password)):
            session["token"]="connected"
            return redirect("/main-salade", code=302)
        return render_template('/pages/login.html',css_file="login.css",js_file="login.js") 

@app.route('/main-salade',methods=['GET'])
def main_salade():
    print(session.get("token"))
    if(session.get("token")=="connected"):
        return render_template('/pages/salade.html',css_file="main.css",js_file="main.js")
    return redirect("/", code=302) 

@app.route('/main-sandwich',methods=['GET'])
def main_sandwich():
    if(session.get("token")=="connected"):
        return render_template('/pages/sandwich.html',css_file="main.css",js_file="main.js")
    return redirect("/", code=302) 

@app.route('/main-viennoiseries',methods=['GET'])
def main_viennoiseries():
    if(session.get("token")=="connected"):
        return render_template('/pages/viennoiseries.html',css_file="main.css",js_file="main.js")
    return redirect("/", code=302) 

@app.route('/correlation',methods=['GET'])
def correlation_page():
    if(session.get("token")=="connected"):
        return render_template('/pages/correlation.html',css_file="main.css",js_file="main.js")
    return redirect("/", code=302) 

@app.route('/get-correlation',methods=['GET'])
def data_correlation():
    return read_data_csv().drop(columns=['Date', 'Jour']).corr().to_json(orient='records')


@app.route('/main-orders-salade',methods=['GET'])
def main_orders_salade():
    if(session.get("token")=="connected"):
        return render_template('/pages/saladeOrders.html',css_file="main.css",js_file="main.js")
    return redirect("/", code=302)
@app.route('/main-orders-sandwich',methods=['GET'])
def main_orders_sandwich():
    if(session.get("token")=="connected"):
        return render_template('/pages/sandwichOrders.html',css_file="main.css",js_file="main.js")
    return redirect("/", code=302)
@app.route('/main-orders-viennoiseries',methods=['GET'])
def main_orders_viennoiseries():
    if(session.get("token")=="connected"):
        return render_template('/pages/viennoiseriesOrders.html',css_file="main.css",js_file="main.js")
    return redirect("/", code=302) 
@app.route('/main-orders-add',methods=['GET'])
def main_orders_add():
    if(session.get("token")=="connected"):
        return render_template('/pages/addOrders.html',css_file="main.css",js_file="main.js")
    return redirect("/", code=302) 

@app.route('/predict', methods=['GET','POST'])
def predict():
    if session.get("token") == "connected":
        if request.method == 'POST':
            data_test = pd.read_csv("static/data_base/Final_Dataset.csv")
            model_name = request.form['model']
            chemin_model="classes_and_functions/pkl/"
            if model_name == 'all':
                products_to_process = ["Pain au chocolat", "Croissant", "Pains suisses",
                                       "Sandwiches poulet crudités", "Sandwiches thon crudits",
                                       "Sandwiches végétarien", "Sandwiches poulet mexicain",
                                       "Sandwiches chèvre miel crudités", "Sandwiches poulet curry",
                                       "Sandwiches saumon", "Panini 4 fromages", "Panini poulet Kebab",
                                       "Salade Thon", "Salade Poulet"]
                for product in products_to_process:
                    chemin_model_final = chemin_model + product + ".pkl"
                    model = pickle.load(open(chemin_model_final, "rb"))
                    prediction = model.predict(data_test[product].iloc[-5:].values.reshape(-1, 1))
                    prediction_rounded = np.array([round(value, 2) for value in prediction])
                    write_to_csv(product, prediction_rounded)
            else:
                chemin_model_final = chemin_model + model_name + ".pkl"
                model = pickle.load(open(chemin_model_final, "rb"))
                prediction = model.predict(data_test[model_name].iloc[-5:].values.reshape(-1, 1))
                prediction_rounded = np.array([round(value, 2) for value in prediction])
                write_to_csv(model_name, prediction_rounded)
                
            return render_template('/pages/ml.html', predictions={model_name: prediction_rounded.tolist()}, css_file="ml.css", js_file="ml.js")
        return render_template('/pages/ml.html', css_file="ml.css", js_file="ml.js")
    return redirect("/", code=302)

@app.route('/optimize', methods=['GET', 'POST'])
def optimize():
    optimized_params = {}
    rmse_scores = {}
    best_model_name = None
    best_rmse = float('inf')
    best_model = None

    # Liste des produits à traiter
    products_to_process = ["Pain au chocolat", "Croissant", "Pains suisses",
                           "Sandwiches poulet crudités", "Sandwiches thon crudités",
                           "Sandwiches végétarien", "Sandwiches poulet mexicain",
                           "Sandwiches chèvre miel crudités", "Sandwiches poulet curry",
                           "Sandwiches saumon", "Panini 4 fromages", "Panini poulet Kebab",
                           "Salade Thon", "Salade Poulet"]

    if request.method == 'POST':
        subprocess.Popen(["python", "ml_grid.py"])
        product = request.form['product']

        # Si le produit est "all", traiter tous les produits de la liste
        if product == "all":
            for product in products_to_process:
                # Traitement pour chaque produit
                X_train = dicto[product]['X_train']
                y_train = dicto[product]['y_train']
                X_test = dicto[product]['X_test']
                y_test = dicto[product]['y_test']
                for model_name, (model, param_grid) in models.items():
                    # Perform grid search for each model
                    grid_search = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_squared_error')
                    grid_search.fit(X_train, y_train)

                    # Get the best parameters for each model
                    optimized_params[model_name] = grid_search.best_params_

                    # Calculate RMSE for each model
                    current_model = grid_search.best_estimator_
                    y_pred = current_model.predict(X_test)
                    rmse = sqrt(mean_squared_error(y_test, y_pred))
                    rmse_scores[model_name] = rmse

                    # Check if this model has the lowest RMSE so far
                    if rmse < best_rmse:
                        best_model_name = model_name
                        best_rmse = rmse
                        best_model = current_model

                # Save the best model to a pickle file with the product name
                if best_model:
                    filename = f"classes_and_functions/pkl/{product}.pkl"
                    with open(filename, 'wb') as f:
                        pickle.dump(best_model, f)

                    # Update the CSV file
                    with open('classes_and_functions/csv/grid.csv', 'r', newline='', encoding='utf-8') as csvfile:
                        reader = csv.reader(csvfile)
                        rows = list(reader)
                        for row in rows:
                            if row and row[0] == product:
                                row[1] = best_model_name
                                row[2] = optimized_params[best_model_name]
                                row[3] = best_rmse
                                break
                        else:
                            rows.append([product, best_model_name, optimized_params[best_model_name], best_rmse])

                    with open('classes_and_functions/csv/grid.csv', 'w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerows(rows)
                best_rmse=999

        else:
            # Traitement pour un produit spécifique
            X_train = dicto[product]['X_train']
            y_train = dicto[product]['y_train']
            X_test = dicto[product]['X_test']
            y_test = dicto[product]['y_test']

            for model_name, (model, param_grid) in models.items():
                # Perform grid search for each model
                grid_search = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_squared_error')
                grid_search.fit(X_train, y_train)

                # Get the best parameters for each model
                optimized_params[model_name] = grid_search.best_params_

                # Calculate RMSE for each model
                current_model = grid_search.best_estimator_
                y_pred = current_model.predict(X_test)
                rmse = sqrt(mean_squared_error(y_test, y_pred))
                rmse_scores[model_name] = rmse

                # Check if this model has the lowest RMSE so far
                if rmse < best_rmse:
                    best_model_name = model_name
                    best_rmse = rmse
                    best_model = current_model

            # Save the best model to a pickle file with the product name
            if best_model:
                filename = f"classes_and_functions/pkl/{product}.pkl"
                with open(filename, 'wb') as f:
                    pickle.dump(best_model, f)

                # Lecture du fichier CSV en spécifiant l'encodage
                with open('classes_and_functions/csv/grid.csv', 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    rows = list(reader)
                    for row in rows:
                        if row and row[0] == product:
                            row[1] = best_model_name
                            row[2] = optimized_params[best_model_name]
                            row[3] = best_rmse
                            break
                    else:
                        rows.append([product, best_model_name, optimized_params[best_model_name], best_rmse])

                # Écriture des lignes mises à jour dans le fichier CSV en spécifiant l'encodage
                with open('classes_and_functions/csv/grid.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    for row in rows:
                        writer.writerow(row)

    return render_template('/pages/optimize.html',css_file="optimize.css",js_file="optimizeDetails.js", optimized_params=optimized_params, rmse_scores=rmse_scores, best_model_name=best_model_name)

@app.route('/get-grid-data', methods=['GET'])
def get_grid_data():
    return get_data_by_column_grid([
        "Nom du produit",
        "Modèle associé",
        "Paramètre du modèle",
        "RMSE"
    ]).to_json(orient='records')
    
@app.route('/get-predicted-data', methods=['GET'])
def get_predicted_data():
    return get_data_by_column_predict([
        "Nom du produit",
        "Lundi",
        "Mardi",
        "Mercredi",
        "Jeudi",
        "Vendredi"
    ]).to_json(orient='records')

@app.route('/logout',methods=['GET'])
def logout():
    session.clear()
    print(session.get("token"))
    return redirect("/", code=302)

# @app.route('/update',methods=['POST'])
# def update():
#     data=request.json
#     update_data(data)
#     session.clear()
#     print(session.get("token"))
#     render_template('/pages/login.html',css_file="login.css",js_file="login.js")


@app.route('/chart-data-salade',methods=['GET'])
def chart_salade():
    return get_data_by_column(["Date","Salade Thon","Salade Poulet"]) .to_json(orient='records') 

@app.route('/chart-data-sandwich',methods=['GET'])
def chart_sandwich():
    return get_data_by_column(["Date","Sandwiches poulet crudités","Sandwiches thon crudités","Sandwiches végétarien","Sandwiches poulet mexicain","Sandwiches chèvre miel crudités","Sandwiches poulet curry","Sandwiches saumon","Panini 4 fromages","Panini poulet Kebab"]) .to_json(orient='records') 
 
@app.route('/chart-data-viennoiseries',methods=['GET'])
def chart_viennoiseries():
    return get_data_by_column(["Date","Pain au chocolat","Croissant","Pains suisses"]) .to_json(orient='records') 


@app.route('/get-saladeOrders-data', methods=['GET'])
def get_saladeOrders_data():
    return get_data_by_column([
        "Date",
        "Salade Thon",
        "Salade Poulet"
    ]).to_json(orient='records')
@app.route('/get-sandwichOrders-data', methods=['GET'])
def get_sandwichOrders_data():
    return get_data_by_column([
        "Date",
        "Sandwiches poulet crudités",
        "Sandwiches thon crudités",
        "Sandwiches végétarien",
        "Sandwiches poulet mexicain",
        "Sandwiches chèvre miel crudités",
        "Sandwiches poulet curry",
        "Sandwiches saumon",
        "Panini 4 fromages",
        "Panini poulet Kebab",
    ]).to_json(orient='records')
@app.route('/get-viennoiseriesOrders-data', methods=['GET'])
def get_viennoiseriesOrders_data():
    return get_data_by_column([
        "Date",
        "Pain au chocolat",
        "Croissant",
        "Pains suisses",
    ]).to_json(orient='records')
@app.route('/update-salade', methods=['POST'])
def update_task():
    data = request.json
    updated_data = {
        'date': data['Date'],
        'saladeThon': data['Salade Thon'],
        'saladePoulet': data['Salade Poulet']
    }
    print(updated_data)
    # Mettre à jour les données du fichier CSV avec les données reçues
    filename = 'static/data_base/Final_Dataset.csv'
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)

        # Trouver l'index de la ligne à mettre à jour
        row_index = 0
        for index, row in enumerate(rows):
            if row[1] == updated_data['date']:
                row_index = index
                break

        # Mettre à jour la ligne dans la liste des lignes
        rows[row_index][14] = updated_data['saladeThon']
        rows[row_index][15] = updated_data['saladePoulet']

    # Écrire les données mises à jour dans le fichier CSV
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    return jsonify({'message': 'Task updated successfully'})

@app.route('/update-sandwich', methods=['POST'])
def update_task1():
    data = request.json
    updated_data = {
        'date': data['Date'],
        'pouletCrudites': data['Sandwiches poulet crudités'],
        'thonCrudites': data['Sandwiches thon crudités'],
        'vegetarien': data['Sandwiches végétarien'],
        'pouletMexicain': data['Sandwiches poulet mexicain'],
        'chevreMielCrudites': data['Sandwiches chèvre miel crudités'],
        'pouletCurry': data['Sandwiches poulet curry'],
        'saumon': data['Sandwiches saumon'],
        'quatreFromages': data['Sandwiches 4 fromages'],
        'pouletKebab': data['Sandwiches poulet Kebab']
    }
    print(updated_data)
    # Mettre à jour les données du fichier CSV avec les données reçues
    filename = 'static/data_base/Final_Dataset.csv'
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)

        # Trouver l'index de la ligne à mettre à jour
        row_index = 0
        for index, row in enumerate(rows):
            if row[1] == updated_data['date']:
                row_index = index
                break

        # Mettre à jour la ligne dans la liste des lignes
        rows[row_index][2] = updated_data['pouletCrudites']
        rows[row_index][3] = updated_data['thonCrudites']
        rows[row_index][4] = updated_data['vegetarien']
        rows[row_index][5] = updated_data['pouletMexicain']
        rows[row_index][6] = updated_data['chevreMielCrudites']
        rows[row_index][7] = updated_data['pouletCurry']
        rows[row_index][8] = updated_data['saumon']
        rows[row_index][9] = updated_data['quatreFromages']
        rows[row_index][10] = updated_data['pouletKebab']

    # Écrire les données mises à jour dans le fichier CSV
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    return jsonify({'message': 'Task updated successfully'})


@app.route('/update-viennoiseries', methods=['POST'])
def update_task2():
    data = request.json
    updated_data = {
        'date': data['Date'],
        'painChocolat': data['Pain au chocolat'],
        'croissant': data['Croissant'],
        'painsSuisses': data['Pains suisses']
    }
    print(updated_data)
    # Mettre à jour les données du fichier CSV avec les données reçues
    filename = 'static/data_base/Final_Dataset.csv'
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)

        # Trouver l'index de la ligne à mettre à jour
        row_index = 0
        for index, row in enumerate(rows):
            if row[1] == updated_data['date']:
                row_index = index
                break

        # Mettre à jour la ligne dans la liste des lignes
        rows[row_index][2] = updated_data['painChocolat']
        rows[row_index][3] = updated_data['croissant']
        rows[row_index][4] = updated_data['painsSuisses']

    # Écrire les données mises à jour dans le fichier CSV
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    return jsonify({'message': 'Task updated successfully'})


@app.route('/add-order', methods=['POST'])
def add_order():
    data = request.json  # Récupérer les données envoyées depuis la requête POST
    # Ajouter la nouvelle commande au fichier CSV en utilisant les données reçues
    with open('static/data_base/Final_Dataset.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            data['jour'],
            data['date'],
            data['saladeThon'],
            data['saladePoulet'],
            data['sandwichesPouletCrudites'],
            data['sandwichesThonCrudites'],
            data['sandwichesVegetarien'],
            data['sandwichesPouletMexicain'],
            data['sandwichesChevreMielCrudites'],
            data['sandwichesPouletCurry'],
            data['sandwichesSaumon'],
            data['panini4Fromages'],
            data['paniniPouletKebab'],
            data['painAuChocolat'],
            data['croissant'],
            data['painsSuisses']
        ])
    return jsonify({'message': 'Order added successfully'})
@app.errorhandler(404) 
def default_url(e):
    return redirect("/", code=302) 
 
if __name__ == '__main__':
    app.run(debug=True)