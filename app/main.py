from PyQt5.QtWidgets import QApplication

from controllers.main_controller import MainController
from views.main_window import MainWindow


def main():
    app = QApplication([])
    window = MainWindow()
    controller = MainController(window)
    window.set_controller(controller)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
