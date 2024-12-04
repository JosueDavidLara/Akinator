# ----------------------------------IMPORTACION DE LIBRERIAS----------------------------------
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree, _tree
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import json

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
]

#  Consolidar las columnas de características múltiples en una sola
characteristic_columns = ["Caracteristica", "Caracteristica2"]
data["CaracteristicasUnicas"] = data[characteristic_columns].apply(
    lambda row: ";".join([str(x) for x in row if pd.notnull(x)]), axis=1
)

# Crear dummies para las características únicas
dummies = data["CaracteristicasUnicas"].str.get_dummies(sep=";")

# Añadir las columnas dummy de CaracteristicasUnicas al dataframe original
data = pd.concat([data, dummies], axis=1)

# Convertir las demás columnas categóricas en variables dummy
data = pd.get_dummies(
    data, columns=categorical_columns, drop_first=True, prefix="", prefix_sep=""
)

# Eliminar columnas innecesarias
data = data.drop(columns=["Caracteristica", "Caracteristica2", "CaracteristicasUnicas"])

# Mostrar el dataframe procesado
column_list = data.drop(columns=["Animal"]).columns.tolist()
print(column_list, len(column_list))
print(data[data["Animal"] == "Cabra"][["Cuernos"]])

# Separar las características (X) y la etiqueta (y)
X = data.drop(columns=["Animal"])
y = data["Animal"]

# Dividir en conjunto de entrenamiento y conjunto de prueba aunque el entrenamiento será con el 100% de los datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.99)

# Crear y entrenar el modelo de árbol de decisión
model = DecisionTreeClassifier(max_depth=45)
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

# ----------------------------------GENERACION DE PREGUNTAS DINAMICAS----------------------------------

# Cargar el diccionario
df = pd.read_csv("./Diccionario alpha.csv")
criteria_dict = dict(zip(df["Criterio"], df["Puente"]))


# Función para generar preguntas dinámicas
def generate_questions(Features, criteria_dict):
    questions = []
    for feature in Features:
        # Verificar si la característica esta en el diccionario
        if feature in criteria_dict:
            puente = criteria_dict[feature]
        else:
            puente = f"es {feature.lower()}"

        # Generar la pregunta en el formato "¿Tu animal [puente] [columna]?"
        new_brige = puente.replace("[columna_criterio]", feature.lower())
        question = f"¿Tu animal {new_brige}?"
        questions.append(question)
    return questions


# Generar preguntas
questions = generate_questions(X.columns, criteria_dict)

# ----------------------------------EXPORTACION DEL MODELO----------------------------------


# Función para convertir el árbol de decisión en JSON
def tree_to_json(tree, feature_names, class_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    def recurse(node):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            # Nodo interno: incluye la característica y los hijos
            return {
                "question": feature_name[node],
                "threshold": tree_.threshold[node],
                "yes": recurse(tree_.children_right[node]),
                "no": recurse(tree_.children_left[node]),
            }
        else:
            # Nodo hoja: incluye la predicción
            predicted_class_index = tree_.value[node].argmax()
            predicted_class = class_names[predicted_class_index]
            return {"prediction": predicted_class}

    return recurse(0)


# Exportar el árbol como JSON
tree_json = tree_to_json(model, questions, model.classes_)
with open("animal_tree.json", "w") as f:
    json.dump(tree_json, f, indent=2)
