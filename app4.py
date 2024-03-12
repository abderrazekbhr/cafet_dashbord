from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained models
model1 = pickle.load(open("knn.pkl", "rb"))
model2 = pickle.load(open("svr.pkl", "rb"))
model3 = pickle.load(open("lasso.pkl", "rb"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract input features from the request
    model_name = request.form['model']
    lundi = float(request.form['lundi'])
    mardi = float(request.form['mardi'])
    mercredi = float(request.form['mercredi'])
    jeudi = float(request.form['jeudi'])
    vendredi = float(request.form['vendredi'])
    
    # Create features array
    features = np.array([[lundi], [mardi], [mercredi], [jeudi], [vendredi]])

    # Perform prediction based on selected model
    if model_name == 'knn':
        prediction = model1.predict(features)
    elif model_name == 'svr':
        prediction = model2.predict(features)
    elif model_name == 'lasso':
        prediction = model3.predict(features)
    else:
        return "Invalid model selected"

    # Pass predictions to the template
    return render_template('index.html', predictions={model_name: prediction.tolist()})

if __name__ == '__main__':
    app.run(port=3000, debug=True)
