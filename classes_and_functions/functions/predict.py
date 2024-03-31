from flask import request, render_template
import numpy as np
import pickle as pick

model = pick.load(open("../pkl/knn.pkl","rb"))

def predict():
    prediction = model.predict()
    print(prediction)
    return render_template('index2.html', prediction=prediction.tolist())