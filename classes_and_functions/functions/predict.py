from flask import request, render_template
import numpy as np
import pickle as pick

model = pick.load(open("model2.pkl","rb"))

def predict():
    # Extract input features from the request
    lundi = float(request.form['lundi'])
    mardi = float(request.form['mardi'])
    mercredi = float(request.form['mercredi'])
    jeudi = float(request.form['jeudi'])
    vendredi = float(request.form['vendredi'])
    
    #On a 5 features qui representent les donnees de toute une semaine
    features = np.array([[lundi], [mardi], [mercredi], [jeudi], [vendredi]])

    #Prédiction 
    prediction = model.predict(features)
    print(prediction)
    return render_template('index2.html', prediction=prediction.tolist())