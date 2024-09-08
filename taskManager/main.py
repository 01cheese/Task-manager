import sys
from PyQt5.QtWidgets import QApplication
from ui_manager import TaskManagerUI

def main():
    app = QApplication(sys.argv)

    # Подключение стилей
    with open("assets/styles.qss", "r") as style_file:
        app.setStyleSheet(style_file.read())

    window = TaskManagerUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
