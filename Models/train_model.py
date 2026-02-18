import pandas as pd
import numpy as np
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Chargement des données

script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "..", "Data", "Dataset_Student_performance.csv")
df = pd.read_csv(data_path)

print("Dataset chargé.")
print(f"Shape : {df.shape}")

# Séparation X / y

X = df.drop("Exam_Score", axis=1)
y = df["Exam_Score"]

# Identification des colonnes

numeric_features = X.select_dtypes(include=["int64", "float64"]).columns
categorical_features = X.select_dtypes(include=["object"]).columns

print(f"Variables numériques : {len(numeric_features)}")
print(f"Variables catégorielles : {len(categorical_features)}")

# Préprocessing

numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])

# Modèle final

model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

# Train / Test split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Entraînement

model.fit(X_train, y_train)

# Évaluation

y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n===== Résultats =====")
print(f"RMSE : {rmse:.4f}")
print(f"R² : {r2:.4f}")

# Sauvegarde

models_dir = script_dir
model_out_path = os.path.join(models_dir, "model.pkl")
rmse_out_path = os.path.join(models_dir, "rmse.pkl")

with open(model_out_path, "wb") as f:
    pickle.dump(model, f)

with open(rmse_out_path, "wb") as f:
    pickle.dump(rmse, f)

print("\nModèle et RMSE sauvegardés avec succès.")
