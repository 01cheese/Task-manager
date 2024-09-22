// Initialize tasks array from localStorage or empty array if not available
let tasks = JSON.parse(localStorage.getItem("tasks")) || [];

// Модальное окно
var modal = document.getElementById("taskModal");
var openModalBtn = document.getElementById("openModalBtn");
var closeModalBtn = document.getElementsByClassName("close")[0];

// Открыть модальное окно
openModalBtn.onclick = function() {
    modal.style.display = "block";
}

// Закрыть модальное окно при нажатии на кнопку "X"
closeModalBtn.onclick = function() {
    modal.style.display = "none";
}

// Закрыть модальное окно при клике вне его
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Форма добавления новой задачи

document.getElementById("addTaskBtn").addEventListener("click", function() {
    let taskName = document.getElementById("taskName").value;
    let taskDueDate = document.getElementById("taskDueDate").value;
    let taskCategory = document.getElementById("taskCategory").value;
    let taskPriority = document.getElementById("taskPriority").value;

    // Проверка на наличие имени задачи
    if (!taskName) {
        alert("Task name is required");
        return;
    }

    let newTask = {
        id: Date.now(),
        task_name: taskName,
        due_date: taskDueDate,
        category: taskCategory,
        priority: taskPriority,
        status: "pending" // Новые задачи по умолчанию "pending"
    };

    tasks.push(newTask);
    localStorage.setItem("tasks", JSON.stringify(tasks));

    displayTasks();  // Обновляем таблицу задач
    document.getElementById("taskForm").reset();  // Очищаем форму после добавления
    modal.style.display = "none";
});


// Функция отображения задач в табличном формате
function displayTasks() {
    let taskList = document.getElementById("taskList");
    taskList.innerHTML = "";  // Очищаем текущий список

    // Получаем значения фильтров и поиска
    let filterCategory = document.getElementById("filterCategory").value;
    let filterPriority = document.getElementById("filterPriority").value;
    let filterStatus = document.getElementById("filterStatus").value;
    let searchQuery = document.getElementById("searchBar").value.toLowerCase();

    tasks.forEach(function(task) {
        let showTask = true;

        // Фильтрация задач по категориям, приоритету, статусу и поисковому запросу
        if (filterCategory && task.category !== filterCategory) {
            showTask = false;
        }
        if (filterPriority && task.priority !== filterPriority) {
            showTask = false;
        }
        if (filterStatus && task.status !== filterStatus) {
            showTask = false;
        }
        if (searchQuery && !task.task_name.toLowerCase().includes(searchQuery)) {
            showTask = false;
        }

        // Если задача проходит фильтры, отображаем ее
        if (showTask) {
            let row = document.createElement("tr");

            // Проверка на статус задачи и добавление соответствующего класса для цветовой индикации
            let statusClass = task.status === "completed" ? "status-completed" : "status-pending";

            row.innerHTML = `
                <td><input type="checkbox" class="select-task" data-id="${task.id}"></td>
                <td>${task.task_name}</td>
                <td>${task.category}</td>
                <td>${task.priority}</td>
                <td class="${statusClass}">${task.status}</td>
                <td>${task.due_date}</td>
                <td>
                    <button onclick="completeTask(${task.id})" class="complete">Complete</button>
                    <button onclick="deleteTask(${task.id})" class="delete">Delete</button>
                </td>
            `;
            taskList.appendChild(row);
        }
    });
}

// Завершение задачи
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

// Удаление задачи
function deleteTask(id) {
    tasks = tasks.filter(task => task.id !== id);
    localStorage.setItem("tasks", JSON.stringify(tasks));
    displayTasks();
}

// Массовое удаление задач
document.getElementById("deleteSelected")?.addEventListener("click", function() {
    let selectedTasks = document.querySelectorAll(".select-task:checked");
    selectedTasks.forEach(taskCheckbox => {
        let taskId = parseInt(taskCheckbox.getAttribute("data-id"));
        tasks = tasks.filter(task => task.id !== taskId);
    });
    localStorage.setItem("tasks", JSON.stringify(tasks));
    displayTasks();
});

// Выбрать все задачи
document.getElementById("selectAll")?.addEventListener("change", function() {
    let checkboxes = document.querySelectorAll(".select-task");
    checkboxes.forEach(checkbox => {
        checkbox.checked = this.checked;
    });
});

// Темная тема
document.getElementById("darkModeToggle")?.addEventListener("click", function() {
    document.body.classList.toggle("dark-mode");
});

// Экспорт задач
document.getElementById("exportTasks")?.addEventListener("click", function() {
    let dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(tasks));
    let downloadAnchor = document.createElement("a");
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", "tasks.json");
    downloadAnchor.click();
});

// Импорт задач
document.getElementById("importTasks")?.addEventListener("click", function() {
    document.getElementById("importTasksFile").click();
});

document.getElementById("importTasksFile")?.addEventListener("change", function(event) {
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
document.getElementById("filterCategory")?.addEventListener("change", displayTasks);
document.getElementById("filterPriority")?.addEventListener("change", displayTasks);
document.getElementById("filterStatus")?.addEventListener("change", displayTasks);
document.getElementById("searchBar")?.addEventListener("input", displayTasks);
