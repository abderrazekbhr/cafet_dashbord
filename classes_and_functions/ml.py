import pandas as pd
import numpy as np
import pickle
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.linear_model import Lasso

data = pd.read_csv("../static/data_base/Final_Dataset.csv")

# Definitions
data_j = data.loc[5:, :].reset_index(drop=True)
data_j_1 = data.loc[:len(data)-2, :].reset_index(drop=True)
data_j_5 = data.loc[:len(data)-6, :]

# Function for model training with imputation
def train_model_with_imputation(model, X_train, y_train, X_test):
    # Impute missing values using mean strategy (you can choose another strategy)
    imputer = SimpleImputer(strategy='mean')

    # Replace missing values in X_train and X_test
    X_train_imputed = imputer.fit_transform(X_train)
    X_test_imputed = imputer.transform(X_test)

    # Check and handle NaN values in the target variable
    y_train_imputed = imputer.fit_transform(y_train.to_numpy().reshape(-1, 1))
    y_train_imputed = y_train_imputed.flatten()

    # Fit the model on the imputed data
    model.fit(X_train_imputed, y_train_imputed)

    return model, X_test_imputed

# KNN
X_knn = np.column_stack((data_j_1["Sandwiches poulet crudités"]))
X1_knn = np.array(data_j_5["Sandwiches poulet crudités"]).reshape(-1, 1)
y_knn = data_j["Sandwiches poulet crudités"]

# Check and handle NaN values in the target variable
y_knn = y_knn.dropna()
X1_knn = X1_knn[:len(y_knn)]

X_train_knn, X_test_knn, y_train_knn, y_test_knn = train_test_split(X1_knn, y_knn, train_size=0.8, shuffle=False)
knn = KNeighborsRegressor(n_neighbors=20)
knn, X_test_knn_imputed = train_model_with_imputation(knn, X_train_knn, y_train_knn, X_test_knn)
pickle.dump(knn, open("pkl/knn.pkl", "wb"))

# SVR
X_svr = np.column_stack((data_j_1["Panini 4 fromages"]))
X1_svr = np.array(data_j_5["Panini 4 fromages"]).reshape(-1, 1)
y_svr = data_j["Panini 4 fromages"]

# Check and handle NaN values in the target variable
y_svr = y_svr.dropna()
X1_svr = X1_svr[:len(y_svr)]

X_train_svr, X_test_svr, y_train_svr, y_test_svr = train_test_split(X1_svr, y_svr, train_size=0.8, shuffle=False)
svr = SVR()
svr, X_test_svr_imputed = train_model_with_imputation(svr, X_train_svr, y_train_svr, X_test_svr)
pickle.dump(svr, open("pkl/svr.pkl", "wb"))

# Lasso
X_lasso = np.column_stack((data_j_1["Sandwiches thon cruditès"]))
X1_lasso = np.array(data_j_5["Sandwiches thon cruditès"]).reshape(-1, 1)
y_lasso = data_j["Sandwiches thon cruditès"]

# Check and handle NaN values in the target variable
y_lasso = y_lasso.dropna()
X1_lasso = X1_lasso[:len(y_lasso)]

X_train_lasso, X_test_lasso, y_train_lasso, y_test_lasso = train_test_split(X1_lasso, y_lasso, train_size=0.8, shuffle=False)
lasso = Lasso()
lasso, X_test_lasso_imputed = train_model_with_imputation(lasso, X_train_lasso, y_train_lasso, X_test_lasso)
pickle.dump(lasso, open("pkl/lasso.pkl", "wb"))
