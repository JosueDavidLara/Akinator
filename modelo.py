# ----------------------------------IMPORTACION DE LIBRERIAS----------------------------------
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree, _tree
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import json

# ----------------------------------TRATAMIENTO DE DATOS----------------------------------

# Cargar los datos
data = pd.read_csv("./dataset_animales.csv")

# Seleccionar las columnas con variables categóricas para convertirlas en variables dummy
categorical_columns = [
    "Clasificacion",
    "Reproduccion",
    "Tamano",
    "Dieta",
    "Patas",
    "Piel",
]

# Consolidar las columnas de locomoción en una sola columna "LocomocionUnica"
locomotion_columns = ["Locomocion1", "Locomocion2", "Locomocion3"]
data["LocomocionUnica"] = data[locomotion_columns].apply(
    lambda row: ";".join([str(x) for x in row if pd.notnull(x) and x != "None"]),
    axis=1,
)

# Crear dummies para la columna "LocomocionUnica"
locomotion_dummies = data["LocomocionUnica"].str.get_dummies(sep=";")

# Consolidar las columnas de características múltiples en una sola columna "CaracteristicasUnicas"
characteristic_columns = [
    "Caracteristica",
    "Caracteristica2",
    "Caracteristica3",
    "Caracteristica4",
    "Caracteristica5",
]
data["CaracteristicasUnicas"] = data[characteristic_columns].apply(
    lambda row: ";".join([str(x) for x in row if pd.notnull(x) and x != "None"]),
    axis=1,
)

# Crear dummies para la columna "CaracteristicasUnicas"
characteristic_dummies = data["CaracteristicasUnicas"].str.get_dummies(sep=";")

# Añadir las columnas dummy de LocomocionUnica y CaracteristicasUnicas al dataframe original
data = pd.concat([data, locomotion_dummies, characteristic_dummies], axis=1)

# Convertir las demás columnas categóricas en variables dummy
data = pd.get_dummies(
    data, columns=categorical_columns, drop_first=True, prefix="", prefix_sep=""
)

# Eliminar columnas innecesarias
columns_to_drop = (
    locomotion_columns
    + characteristic_columns
    + [
        "LocomocionUnica",
        "CaracteristicasUnicas",
    ]
)
data = data.drop(columns=columns_to_drop)

# Mostrar el dataframe procesado
column_list = data.drop(columns=["Animal"]).columns.tolist()
# print(column_list, len(column_list))

# Separar las características (X) y la etiqueta (y)
X = data.drop(columns=["Animal"])
y = data["Animal"]

# ----------------------------------GENERACION DE PREGUNTAS DINAMICAS----------------------------------

# Cargar el diccionario
df = pd.read_csv("./Diccionario beta.csv")
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

# ----------------------------------EXPORTACION DE MULTIPLES MODELO----------------------------------

models = [
    {"name": "animal_tree_1.json", "max_depth": 37},
    {"name": "animal_tree_2.json", "max_depth": 36},
    {"name": "animal_tree_3.json", "max_depth": 40},
]


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


# Función para entrenar y exportar un modelo
def train_and_export_tree(config, X, y, questions):
    # Crear y entrenar el modelo con la configuración actual
    model = DecisionTreeClassifier(max_depth=config["max_depth"])
    model.fit(X, y)

    # Exportar el árbol a JSON
    tree_json = tree_to_json(model, questions, model.classes_)
    with open(config["name"], "w") as f:
        json.dump(tree_json, f, indent=2)

    # Mostrar el mensaje de exportación con precisión
    print(
        f"Modelo exportado: {config['name']} - Precisión: {model.score(X, y) * 100:.2f}%"
    )


# Entrenar y exportar cada modelo
for config in models:
    train_and_export_tree(config, X, y, questions)
