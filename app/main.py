import sys

from PyQt5.QtWidgets import QApplication

from controllers.main_controller import MainController
from views.login_dialog import LoginDialog
from views.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # ── Tela de login ────────────────────────────────────────────────
    login = LoginDialog()
    if login.exec_() != LoginDialog.Accepted:
        # Usuário fechou a janela de login sem entrar
        sys.exit(0)

    user_name = login.user_name
    # ─────────────────────────────────────────────────────────────────

    window = MainWindow(user_name=user_name)
    controller = MainController(window)
    window.set_controller(controller)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()