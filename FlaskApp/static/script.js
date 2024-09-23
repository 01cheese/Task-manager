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

    if (!taskName) {
        alert("Task name is required");
        return;
    }

    let formData = new FormData();
    formData.append('task_name', taskName);
    formData.append('due_date', taskDueDate);
    formData.append('category', taskCategory);
    formData.append('priority', taskPriority);

    fetch('/add_task', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            displayTasks();
            document.getElementById("taskForm").reset();  // Очищаем форму после добавления
            modal.style.display = "none";
            showNotification("Task added successfully!");
        } else {
            showNotification("Failed to add task.", true);
        }
    }).catch(() => {
        showNotification("Failed to add task.", true);
    });
});

// Функция отображения уведомлений
function showNotification(message, isError = false) {
    const notification = document.getElementById("notification");
    notification.textContent = message;
    notification.style.backgroundColor = isError ? "#dc3545" : "#28a745"; // Красный для ошибок, зеленый для успеха
    notification.classList.add("show");

    // Через 3 секунды скрываем уведомление
    setTimeout(() => {
        notification.classList.remove("show");
    }, 3000);
}


function displayTasks() {
    fetch('/get_tasks')
    .then(response => response.json())
    .then(tasks => {
        let taskList = document.getElementById("taskList");
        taskList.innerHTML = "";  // Очищаем текущий список задач

        // Получаем значения фильтров и поиска
        let filterCategory = document.getElementById("filterCategory").value;
        let filterPriority = document.getElementById("filterPriority").value;
        let filterStatus = document.getElementById("filterStatus").value;
        let searchQuery = document.getElementById("searchBar").value.toLowerCase();

        // Фильтрация и поиск задач
        tasks.forEach(function(task) {
            let showTask = true;

            // Применяем фильтрацию по категориям, приоритету и статусу
            if (filterCategory && task[2] !== filterCategory) {
                showTask = false;
            }
            if (filterPriority && task[3] !== filterPriority) {
                showTask = false;
            }
            if (filterStatus && task[4] !== filterStatus) {
                showTask = false;
            }

            // Применяем фильтр поиска по названию задачи
            if (searchQuery && !task[1].toLowerCase().includes(searchQuery)) {
                showTask = false;
            }

            // Если задача удовлетворяет всем условиям, добавляем ее в таблицу
            if (showTask) {
                let statusClass = task[4] === "completed" ? "status-completed" : "status-pending";
                let row = document.createElement("tr");
                row.innerHTML = `
                    <td><input type="checkbox" class="select-task" data-id="${task[0]}"></td>
                    <td>${task[1]}</td>
                    <td>${task[2]}</td>
                    <td>${task[3]}</td>
                    <td class="${statusClass}">${task[4]}</td>
                    <td>${task[5]}</td>
                    <td>
                        <button onclick="completeTask(${task[0]})" class="complete">Complete</button>
                        <button onclick="deleteTask(${task[0]})" class="delete">Delete</button>
                    </td>
                `;
                taskList.appendChild(row);
            }
        });
    });
}


window.onload = function() {
    displayTasks();
};

// Завершение задачи
function completeTask(id) {
    fetch(`/complete_task/${id}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'Task completed') {
            displayTasks();  // Обновляем список задач после изменения статуса
            showNotification("Task marked as completed!");
        } else {
            showNotification("Failed to complete task.", true);
        }
    })
    .catch(() => {
        showNotification("Failed to complete task.", true);
    });
}

// Удаление задачи
function deleteTask(id) {
    fetch(`/delete_task/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'Task deleted') {
            displayTasks();  // Обновляем список задач после удаления
            showNotification("Task deleted successfully!");
        } else {
            showNotification("Failed to delete task.", true);
        }
    })
    .catch(() => {
        showNotification("Failed to delete task.", true);
    });
}


// Массовое удаление задач
document.getElementById("deleteSelected").addEventListener("click", function() {
    let selectedTasks = document.querySelectorAll(".select-task:checked");
    if (selectedTasks.length === 0) {
        showNotification("No tasks selected.", true);
        return;
    }

    selectedTasks.forEach(taskCheckbox => {
        let taskId = parseInt(taskCheckbox.getAttribute("data-id"));
        fetch(`/delete_task/${taskId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'Task deleted') {
                displayTasks();  // Обновляем список задач после удаления
            } else {
                showNotification(`Failed to delete task with ID ${taskId}.`, true);
            }
        })
        .catch(() => {
            showNotification(`Failed to delete task with ID ${taskId}.`, true);
        });
    });

    showNotification("Selected tasks deleted successfully!");
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
