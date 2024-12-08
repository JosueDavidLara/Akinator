# Akinator de Animales
Este proyecto implementa un Akinator de animales utilizando machine learning. El sistema está diseñado para adivinar el animal que el usuario tiene en mente respondiendo preguntas relacionadas. El dataset utilizado fue creado combinando información de diversas fuentes para garantizar una amplia variedad de animales y características.

La aplicación incluye una interfaz web amigable que permite interactuar con el modelo y, además, ofrece una barra lateral con una lista de animales para consultar información adicional en caso de dudas.

## Estructura del Proyecto
El proyecto está organizado de la siguiente manera:

#### modelo.py
Contiene el código para cargar y utilizar el modelo de machine learning basado en un árbol de decisión.

#### Diccionario beta
También incluye un diccionario que relaciona las preguntas con las características clave de los animales.

#### dataset_animales.csv
Contiene el dataset utilizado para entrenar el modelo. Este dataset incluye características detalladas de cada animal.

#### images/
Carpeta que contiene todas las imagenes de la interfaz web:
- favicon.png
- genio.png
- wallpaper.jpg

#### index.html: 
La página principal del proyecto, donde el usuario interactúa con el Akinator.
#### styles.css 
Contiene los archivos CSS para estilizar la interfaz.
#### script.js:
Contiene los archivos JavaScript para manejar la lógica de la página y conectar el modelo con la interfaz.

## Cómo Probar el Proyecto

#### 1. Clonar el Repositorio

```bash
git clone https://github.com/JosueDavidLara/Akinator.git
```

#### 2. Navegar a la Carpeta del Proyecto

```bash
cd Akinator
```

#### 3. Ejecutar el modelo.py
Ejecutar en la consola el modelo.py para generar nuevos modelos si los deseas, asegurese de que los modelos se exportan con el 100% de precisión.

```bash
modelo.py
```

#### 4. Iniciar un Servidor Local
Ejecutar el siguiente comando para iniciar un servidor web local:

```bash
python -m http.server
```

#### 5. Abrir en el Navegador
Abrir el navegador y acceder a http://localhost:8000.

¡Y listo! Ahora puedes interactuar con el Akinator de animales y probar la funcionalidad de adivinación.
