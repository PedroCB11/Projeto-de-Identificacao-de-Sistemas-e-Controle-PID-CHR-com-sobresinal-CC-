from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class LoginDialog(QDialog):
    """Tela de login simples — o usuário informa o nome e entra no sistema."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("C213 — Controle PID")
        self.setFixedSize(440, 270)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)

        self.user_name = ""

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(48, 38, 48, 38)

        title = QLabel("Projeto Prático C213")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(15)
        title_font.setBold(True)
        title.setFont(title_font)

        subtitle = QLabel("Identificação de Sistemas e Controle PID")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #555; font-size: 12px;")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Digite seu nome para entrar...")
        self.name_input.setMinimumHeight(38)
        self.name_input.returnPressed.connect(self._on_enter)

        self.enter_button = QPushButton("Entrar")
        self.enter_button.setMinimumHeight(38)
        self.enter_button.setDefault(True)
        self.enter_button.setStyleSheet("""
            QPushButton {
                background-color: #5d7a8a;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #4a6475;
            }
            QPushButton:pressed {
                background-color: #3b5060;
            }
        """)
        self.enter_button.clicked.connect(self._on_enter)

        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("color: #c0392b; font-size: 11px;")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(4)
        layout.addWidget(self.name_input)
        layout.addWidget(self.enter_button)
        layout.addWidget(self.error_label)

    def _on_enter(self):
        name = self.name_input.text().strip()
        if not name:
            self.error_label.setText("Por favor, informe seu nome.")
            self.name_input.setFocus()
            return
        self.user_name = name
        self.accept()