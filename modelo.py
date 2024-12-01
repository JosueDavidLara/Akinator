# ----------------------------------IMPORTACION DE LIBRERIAS----------------------------------
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree, _tree
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# ----------------------------------CREACION DEL MODELO----------------------------------

# Cargar los datos
data = pd.read_csv("./dataset_animales.csv")

# Seleccionar las columnas con variables categóricas para convertirlas en variables dummy
categorical_columns = [
    "Clasificacion",
    "Locomocion",
    "Reproduccion",
    "Tamano",
    "Dieta",
    "Patas",
    "Piel",
    "Caracteristica",
]

# Usar pd.get_dummies para convertir las columnas categóricas en variables dummy
data = pd.get_dummies(
    data, columns=categorical_columns, drop_first=True, prefix="", prefix_sep=""
)

# Mostrar el dataframe procesado
# print(data.info())

# Separar las características (X) y la etiqueta (y)
X = data.drop(columns=["Animal"])
y = data["Animal"]

# Dividir en conjunto de entrenamiento y conjunto de prueba aunque el entrenamiento será con el 100% de los datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.7)

# Crear y entrenar el modelo de árbol de decisión
model = DecisionTreeClassifier(max_depth=34)
model.fit(X, y)

# ----------------------------------EVALUACION DEL MODELO----------------------------------

# Hacer predicciones (testear el modelo)
pred = model.predict(X_test)
comparativa = {"predicciones": pred, "valor real": y_test}
result = pd.DataFrame(comparativa)
print(result)
print(f"Precisión del modelo: {(model.score(X_test, y_test)*100):.2f}%")

# Visualizar el árbol de decisión (opcional)
# plt.figure(figsize=(20, 10))
# plot_tree(
#     model,
#     filled=True,
#     feature_names=X.columns,
#     class_names=y.unique(),
#     rounded=True,
#     fontsize=10,
# )
# plt.show()