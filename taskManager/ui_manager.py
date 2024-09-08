from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QProgressBar, QGroupBox, \
    QListWidget, QLineEdit, QInputDialog, QMessageBox, QStackedWidget
from db_manager import DBManager
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QProgressBar, QGroupBox, QListWidget, QLineEdit, QInputDialog, QMessageBox, QStackedWidget
from db_manager import DBManager

class TaskCard(QGroupBox):
    def __init__(self, task_id, title, description, progress):
        super().__init__()
        self.task_id = task_id
        layout = QVBoxLayout()

        self.title_label = QLabel(f"<b>{title}</b>")
        self.description_label = QLabel(description)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(progress)

        layout.addWidget(self.title_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)


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
        menu_layout.addStretch()  # Добавляем пространство внизу

        # Центральный виджет, который будет переключать страницы
        self.stacked_widget = QStackedWidget()

        # Создаём страницы для разных секций
        task_page = QLabel("Tasks Page")
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

    def load_tasks(self):
        tasks = self.db.get_tasks()

    def add_task(self, status):
        title, ok = QInputDialog.getText(self, 'New Task', 'Enter task title:')
        if ok and title:
            description, ok = QInputDialog.getText(self, 'New Task', 'Enter task description:')
            if ok:
                self.db.add_task(title, description, status, 0)
                self.load_tasks()

    def edit_task(self):
        pass

    def delete_task(self):
        pass