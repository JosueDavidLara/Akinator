let tree = null;
let currentNode = null;

// Inicializar el juego y seleccionar aleatoriamente un modelo
function initializeGame() {
  const treeFiles = [
    "animal_tree_1.json",
    "animal_tree_2.json",
    "animal_tree_3.json",
  ];

  const randomIndex = Math.floor(Math.random() * treeFiles.length);
  const selectedTree = treeFiles[randomIndex];

  console.log(`Modelo cargado: ${selectedTree}`); // Mostrar el modelo cargado en la consola

  // Cargar el modelo seleccionado
  fetch(selectedTree)
    .then((response) => response.json())
    .then((data) => {
      tree = data;
      currentNode = tree;
      showQuestion();
    })
    .catch((error) => {
      console.error("Error al cargar el árbol:", error);
      document.getElementById("question").textContent =
        "Error al cargar el juego. Por favor, intenta de nuevo más tarde.";
    });
}

// Mostrar la pregunta o predicción
function showQuestion() {
  const questionDiv = document.getElementById("question");
  const resultDiv = document.getElementById("result");
  const yesBtn = document.getElementById("yes");
  const noBtn = document.getElementById("no");
  const playAgainBtn = document.getElementById("playAgain");

  resultDiv.textContent = "";

  if (currentNode.prediction) {
    questionDiv.textContent = `¡Tu animal es: ${currentNode.prediction}!`;
    yesBtn.style.display = "none";
    noBtn.style.display = "none";
    playAgainBtn.style.display = "inline";
  } else {
    questionDiv.textContent = currentNode.question;
    yesBtn.style.display = "inline";
    noBtn.style.display = "inline";
    playAgainBtn.style.display = "none";
  }
}

function answerYes() {
  if (currentNode.yes) {
    currentNode = currentNode.yes;
    showQuestion();
  }
}

function answerNo() {
  if (currentNode.no) {
    currentNode = currentNode.no;
    showQuestion();
  }
}

// Modificar la función playAgain para reiniciar todo
function playAgain() {
  initializeGame();
}

// Cargar el CSV y generar la lista
function loadAnimalData() {
  fetch("dataset_animales.csv")
    .then((response) => response.text())
    .then((csvText) => {
      const parsedData = Papa.parse(csvText, {
        header: true,
        skipEmptyLines: true,
      }).data;
      populateAnimalList(parsedData); // Aquí se asegura que el argumento sea un arreglo.
    })
    .catch((error) => console.error("Error al cargar el CSV:", error));
}

// Crear la lista de animales
function populateAnimalList(animals) {
  const animalList = document.getElementById("animalList");
  animalList.innerHTML = ""; // Limpiar la lista

  animals.forEach((animal) => {
    const listItem = document.createElement("li");
    listItem.innerHTML = `<a href="#" onclick='showAnimalDetails(${JSON.stringify(
      animal
    )})'>${animal.Animal}</a>`;
    animalList.appendChild(listItem);
  });
}

function showAnimalDetails(animal) {
  const domestico = animal.Domestico === "1" ? "Sí" : "No";
  const mitologico = animal.Mitologico === "1" ? "Sí" : "No";

  // Filtrar locomociones válidas (excluir "None")
  const locomociones = [
    animal.Locomocion1,
    animal.Locomocion2,
    animal.Locomocion3,
  ].filter((locomocion) => locomocion && locomocion !== "None");

  // Filtrar características válidas (excluir "None")
  const caracteristicas = [
    animal.Caracteristica,
    animal.Caracteristica2,
    animal.Caracteristica3,
    animal.Caracteristica4,
    animal.Caracteristica5,
  ].filter((caracteristica) => caracteristica && caracteristica !== "None");

  document.getElementById("animalListContainer").style.display = "none";
  document.getElementById("animalDetailsContainer").style.display = "block";

  // Crear la vista detallada con diseño más estético
  const detailsHTML = `
    <div class="animal-details-card">
        <ul class="animal-info">
            <li><strong>Vertebrado:</strong> ${
              animal.Vertebrado === "1" ? "Sí" : "No"
            }</li>
            <li><strong>Clasificación:</strong> ${animal.Clasificacion}</li>
            <li><strong>Locomoción:</strong> ${
              locomociones.join(", ") || "No especificada"
            }</li>
            <li><strong>Tamaño:</strong> ${animal.Tamano}</li>
            <li><strong>Dieta:</strong> ${animal.Dieta}</li>
            <li><strong>Reproducción:</strong> ${animal.Reproduccion}</li>
            <li><strong>Patas:</strong> ${animal.Patas}</li>
            <li><strong>Piel:</strong> ${animal.Piel}</li>
            <li><strong>Doméstico:</strong> ${domestico}</li>
            <li><strong>Mitológico:</strong> ${mitologico}</li>
            <li><strong>Características:</strong> ${
              caracteristicas.length > 0
                ? `<ul class="caracteristicas">${caracteristicas
                    .map((caracteristica) => `<li>${caracteristica}</li>`)
                    .join("")}</ul>`
                : "No especificadas"
            }</li>
        </ul>
    </div>
  `;

  document.getElementById("animalName").textContent = animal.Animal;
  document.getElementById("animalDetails").innerHTML = detailsHTML;
}

function showAnimalList() {
  document.getElementById("animalListContainer").style.display = "block";
  document.getElementById("animalDetailsContainer").style.display = "none";
}

function closeSidebar() {
  const sidebar = document.getElementById("sidebar");
  const menuButton = document.getElementById("menuButton");

  sidebar.classList.remove("open");
  menuButton.classList.remove("hidden"); // Asegúrate de mostrar el botón nuevamente
  showAnimalList(); // Volver a la lista al cerrar la barra lateral
}

function filterList() {
  const search = document.getElementById("search").value.toLowerCase();
  const items = document.querySelectorAll("#animalList li");
  items.forEach((item) => {
    if (item.textContent.toLowerCase().includes(search)) {
      item.style.display = "";
    } else {
      item.style.display = "none";
    }
  });
}

function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  const menuButton = document.getElementById("menuButton");

  if (sidebar.classList.contains("open")) {
    sidebar.classList.remove("open");
    menuButton.classList.remove("hidden"); // Mostrar el botón de menú
  } else {
    sidebar.classList.add("open");
    menuButton.classList.add("hidden"); // Ocultar el botón de menú
  }
}

// Llamar a initializeGame al cargar la página
document.addEventListener("DOMContentLoaded", () => {
  initializeGame();
  loadAnimalData();
});
