from flask import Flask,render_template,request,redirect,session,jsonify
from flask_session import Session
import csv
from classes_and_functions.functions.login_test import test_login,update_data
from classes_and_functions.functions.read_data_csv import *

import pickle
import numpy as np
import pandas as pd

# Load the trained models
knn = pickle.load(open("classes_and_functions/pkl/knn.pkl", "rb"))
svr = pickle.load(open("classes_and_functions/pkl/svr.pkl", "rb"))
lasso = pickle.load(open("classes_and_functions/pkl/lasso.pkl", "rb"))

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
            model_name = request.form['model']
            lundi = float(request.form['lundi'])
            mardi = float(request.form['mardi'])
            mercredi = float(request.form['mercredi'])
            jeudi = float(request.form['jeudi'])
            vendredi = float(request.form['vendredi'])

            features = np.array([[lundi], [mardi], [mercredi], [jeudi], [vendredi]])

            if model_name == 'knn':
                prediction = knn.predict(features)
            elif model_name == 'svr':
                prediction = svr.predict(features)
            elif model_name == 'lasso':
                prediction = lasso.predict(features)
            else:
                return "Invalid model selected"
            return render_template('/pages/ml.html', predictions={model_name: prediction.tolist()},css_file="main.css", js_file="main.js")
        return render_template('/pages/ml.html', css_file="main.css", js_file="main.js")
    return redirect("/", code=302)

@app.route('/logout',methods=['GET'])
def logout():
    session.clear()
    print(session.get("token"))
    return redirect("/", code=302)

@app.route('/update',methods=['POST'])
def update():
    data=request.json
    update_data(data)
    session.clear()
    print(session.get("token"))
    render_template('/pages/login.html',css_file="login.css",js_file="login.js")


@app.route('/chart-data-salade',methods=['GET'])
def chart_salade():
    return get_data_by_column(["Date","Salade Thon","Salade Poulet"]) .to_json(orient='records') 

@app.route('/chart-data-sandwich',methods=['GET'])
def chart_sandwich():
    return get_data_by_column(["Date","Sandwiches poulet crudités","Sandwiches thon cruditès","Sandwiches végétarien","Sandwiches poulet mexicain","Sandwiches chèvre miel crudités","Sandwiches poulet curry","Sandwiches saumon","Panini 4 fromages","Panini poulet Kebab"]) .to_json(orient='records') 
 
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
        "Sandwiches thon cruditès",
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
@app.route('/update', methods=['POST'])
def update_task():
    data = request.json
    # Update the corresponding row in the CSV file with the new data
    # You need to implement this part based on your CSV file handling logic
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