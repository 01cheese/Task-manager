// Инициализация массива задач
let tasks = JSON.parse(localStorage.getItem("tasks")) || [];

// Обработчик формы для добавления задачи
document.getElementById("taskForm").addEventListener("submit", function(event) {
    event.preventDefault();

    let taskName = document.getElementById("taskName").value;
    let taskDescription = document.getElementById("taskDescription").value;
    let taskDueDate = document.getElementById("taskDueDate").value;
    let taskCategory = document.getElementById("taskCategory").value;
    let taskPriority = document.getElementById("taskPriority").value;
    let taskRepeating = document.getElementById("taskRepeating").checked;
    let taskFavorite = document.getElementById("taskFavorite").checked;

    let newTask = {
        id: Date.now(),
        task_name: taskName,
        description: taskDescription,
        due_date: taskDueDate,
        status: "pending",
        category: taskCategory,
        priority: taskPriority,
        is_favorite: taskFavorite,
        is_repeating: taskRepeating
    };

    tasks.push(newTask);
    localStorage.setItem("tasks", JSON.stringify(tasks));

    displayTasks();
    document.getElementById("taskForm").reset(); // Сброс формы после добавления задачи
});

// Функция для отображения задач с учетом фильтров
function displayTasks() {
    let taskList = document.getElementById("taskList");
    taskList.innerHTML = "";

    let filterCategory = document.getElementById("filterCategory").value;
    let filterPriority = document.getElementById("filterPriority").value;
    let filterStatus = document.getElementById("filterStatus").value;
    let searchQuery = document.getElementById("searchBar").value.toLowerCase();

    tasks.forEach(function(task) {
        if ((filterCategory && task.category !== filterCategory) ||
            (filterPriority && task.priority !== filterPriority) ||
            (filterStatus && task.status !== filterStatus) ||
            (searchQuery && !task.task_name.toLowerCase().includes(searchQuery))) {
            return;
        }

        let li = document.createElement("li");
        li.setAttribute("data-id", task.id);
        li.innerHTML = `
            <span class="${task.status === 'completed' ? 'completed' : ''}">
                ${task.task_name} - ${task.due_date} - ${task.category} - ${task.priority}
            </span>
            <div>
                <button onclick="completeTask(${task.id})">Complete</button>
                <button onclick="deleteTask(${task.id})">Delete</button>
            </div>
        `;
        taskList.appendChild(li);
    });
}

// Функция для завершения задачи
function completeTask(id) {
    tasks = tasks.map(task => {
        if (task.id === id) {
            task.status = "completed";
        }
        return task;
    });
    localStorage.setItem("tasks", JSON.stringify(tasks));
    displayTasks();
}

// Функция для удаления задачи
function deleteTask(id) {
    tasks = tasks.filter(task => task.id !== id);
    localStorage.setItem("tasks", JSON.stringify(tasks));
    displayTasks();
}

// Переключение темной темы
document.getElementById("darkModeToggle").addEventListener("click", function() {
    document.body.classList.toggle("dark-mode");
});

// Экспорт задач
document.getElementById("exportTasks").addEventListener("click", function() {
    let dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(tasks));
    let downloadAnchor = document.createElement("a");
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", "tasks.json");
    downloadAnchor.click();
});

// Импорт задач
document.getElementById("importTasks").addEventListener("click", function() {
    document.getElementById("importTasksFile").click();
});

document.getElementById("importTasksFile").addEventListener("change", function(event) {
    let file = event.target.files[0];
    let reader = new FileReader();
    reader.onload = function(e) {
        let importedTasks = JSON.parse(e.target.result);
        tasks = tasks.concat(importedTasks);
        localStorage.setItem("tasks", JSON.stringify(tasks));
        displayTasks();
    };
    reader.readAsText(file);
});

// Загрузка задач при запуске страницы
window.onload = function() {
    displayTasks();
};

// Фильтрация и поиск задач
document.getElementById("filterCategory").addEventListener("change", displayTasks);
document.getElementById("filterPriority").addEventListener("change", displayTasks);
document.getElementById("filterStatus").addEventListener("change", displayTasks);
document.getElementById("searchBar").addEventListener("input", displayTasks);
