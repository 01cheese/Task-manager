from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QProgressBar, QGroupBox, QListWidget, QLineEdit, QDialog, QDialogButtonBox, QFormLayout, QCheckBox, QMessageBox, QInputDialog, QListWidgetItem, QStackedWidget
from PyQt5.QtCore import Qt
from db_manager import DBManager

class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Добавить задачу")
        self.setFixedSize(300, 200)

        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.title_input = QLineEdit()
        self.description_input = QLineEdit()

        self.form_layout.addRow("Название задачи:", self.title_input)
        self.form_layout.addRow("Описание задачи:", self.description_input)

        self.layout.addLayout(self.form_layout)

        # Выбор типа задачи (большая или малая)
        self.is_large_task = False
        self.large_task_checkbox = QCheckBox("Большая задача")
        self.large_task_checkbox.stateChanged.connect(self.on_large_task_checked)
        self.layout.addWidget(self.large_task_checkbox)

        # Кнопки "ОК" и "Отмена"
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def on_large_task_checked(self):
        self.is_large_task = self.large_task_checkbox.isChecked()

    def get_task_data(self):
        return self.title_input.text(), self.description_input.text(), self.is_large_task

class AddSubtasksDialog(QDialog):
    def __init__(self, num_subtasks, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Добавить подпункты")
        self.subtasks = []
        self.layout = QVBoxLayout()

        for i in range(num_subtasks):
            subtask_input = QLineEdit(self)
            subtask_input.setPlaceholderText(f"Подпункт {i + 1}")
            self.layout.addWidget(subtask_input)
            self.subtasks.append(subtask_input)

        # Кнопки "ОК" и "Отмена"
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def get_subtasks(self):
        return [subtask.text() for subtask in self.subtasks if subtask.text()]

class SubTaskGroup(QWidget):
    def __init__(self, subtasks):
        super().__init__()
        self.layout = QVBoxLayout()
        self.subtasks = []
        self.completed_count = 0

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        # Добавляем подпункты с чекбоксами
        for subtask in subtasks:
            subtask_checkbox = QCheckBox(subtask)
            subtask_checkbox.stateChanged.connect(self.update_progress)
            self.layout.addWidget(subtask_checkbox)
            self.subtasks.append(subtask_checkbox)

        self.setLayout(self.layout)
        self.update_progress()

    def update_progress(self):
        completed = sum(1 for subtask in self.subtasks if subtask.isChecked())
        total = len(self.subtasks)
        self.progress_bar.setValue(int((completed / total) * 100))

class TaskManagerUI(QWidget):
    def __init__(self):
        super().__init__()

        self.db = DBManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Task Manager with Sidebar Menu")

        # Главный layout
        main_layout = QHBoxLayout()

        # Создаём боковое меню
        menu_layout = QVBoxLayout()

        # Кнопки для бокового меню
        task_button = QPushButton("Tasks")
        message_button = QPushButton("Messages")
        calendar_button = QPushButton("Calendar")
        completed_button = QPushButton("Completed Tasks")
        charts_button = QPushButton("Charts")
        settings_button = QPushButton("Settings")

        # Добавляем кнопки в меню
        menu_layout.addWidget(task_button)
        menu_layout.addWidget(message_button)
        menu_layout.addWidget(calendar_button)
        menu_layout.addWidget(completed_button)
        menu_layout.addWidget(charts_button)
        menu_layout.addWidget(settings_button)
        menu_layout.addStretch()

        # Центральный виджет, который будет переключать страницы
        self.stacked_widget = QStackedWidget()

        # Страница задач (Tasks Page)
        task_page = self.create_tasks_page()

        # Другие страницы
        message_page = QLabel("Messages Page")
        calendar_page = QLabel("Calendar Page")
        completed_page = QLabel("Completed Tasks Page")
        charts_page = QLabel("Charts Page")
        settings_page = QLabel("Settings Page")

        # Добавляем страницы в stacked widget
        self.stacked_widget.addWidget(task_page)       # 0
        self.stacked_widget.addWidget(message_page)    # 1
        self.stacked_widget.addWidget(calendar_page)   # 2
        self.stacked_widget.addWidget(completed_page)  # 3
        self.stacked_widget.addWidget(charts_page)     # 4
        self.stacked_widget.addWidget(settings_page)   # 5

        # Связываем кнопки меню с переключением страниц
        task_button.clicked.connect(lambda: self.switch_page(0))
        message_button.clicked.connect(lambda: self.switch_page(1))
        calendar_button.clicked.connect(lambda: self.switch_page(2))
        completed_button.clicked.connect(lambda: self.switch_page(3))
        charts_button.clicked.connect(lambda: self.switch_page(4))
        settings_button.clicked.connect(lambda: self.switch_page(5))

        # Добавляем меню и центральный виджет в главный layout
        main_layout.addLayout(menu_layout)
        main_layout.addWidget(self.stacked_widget)

        # Устанавливаем главный layout для окна
        self.setLayout(main_layout)

    def switch_page(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def create_tasks_page(self):
        tasks_layout = QVBoxLayout()

        # Создаём три колонки (Начало, В процессе, Выполнено)
        task_columns_layout = QHBoxLayout()

        # Колонка "Начало"
        start_column = QVBoxLayout()
        start_label = QLabel("Начало")
        start_column.addWidget(start_label)
        self.start_task_list = QListWidget()
        start_column.addWidget(self.start_task_list)
        add_start_button = QPushButton("Добавить задачу в Начало")
        add_start_button.clicked.connect(lambda: self.open_add_task_dialog("Начало"))
        start_column.addWidget(add_start_button)

        # Колонка "В процессе"
        progress_column = QVBoxLayout()
        progress_label = QLabel("В процессе")
        progress_column.addWidget(progress_label)
        self.progress_task_list = QListWidget()
        progress_column.addWidget(self.progress_task_list)

        # Колонка "Выполнено"
        done_column = QVBoxLayout()
        done_label = QLabel("Выполнено")
        done_column.addWidget(done_label)
        self.done_task_list = QListWidget()
        done_column.addWidget(self.done_task_list)

        # Добавляем колонки в основной layout
        task_columns_layout.addLayout(start_column)
        task_columns_layout.addLayout(progress_column)
        task_columns_layout.addLayout(done_column)

        tasks_layout.addLayout(task_columns_layout)

        # Создаём виджет для страницы задач
        task_page_widget = QWidget()
        task_page_widget.setLayout(tasks_layout)

        return task_page_widget

    def open_add_task_dialog(self, status):
        dialog = AddTaskDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            title, description, is_large_task = dialog.get_task_data()

            if title:
                if is_large_task:
                    # Запрашиваем количество подпунктов для большой задачи
                    num_subtasks, ok = QInputDialog.getInt(self, 'Количество подпунктов', 'Введите количество подпунктов:')
                    if ok and num_subtasks > 0:
                        subtask_dialog = AddSubtasksDialog(num_subtasks, self)
                        if subtask_dialog.exec_() == QDialog.Accepted:
                            subtasks = subtask_dialog.get_subtasks()
                            if subtasks:
                                task_item = QListWidgetItem(f"{title} - {description}")
                                subtask_group = SubTaskGroup(subtasks)
                                self.progress_task_list.addItem(task_item)
                                self.progress_task_list.setItemWidget(task_item, subtask_group)
                else:
                    # Малые задачи сразу добавляются в колонку "Начало"
                    self.db.add_task(title, description, status, 0)
                    self.load_tasks()

    def load_tasks(self):
        self.start_task_list.clear()
        self.progress_task_list.clear()
        self.done_task_list.clear()

        tasks = self.db.get_tasks()
        for task in tasks:
            task_id, title, description, status, progress = task
            task_card = QListWidgetItem(f"{title}: {description} ({progress}%)")

            if status == "Начало":
                self.start_task_list.addItem(task_card)
            elif status == "В процессе":
                self.progress_task_list.addItem(task_card)
            elif status == "Выполнено":
                self.done_task_list.addItem(task_card)

    def edit_task(self):
        pass

    def delete_task(self):
        pass
