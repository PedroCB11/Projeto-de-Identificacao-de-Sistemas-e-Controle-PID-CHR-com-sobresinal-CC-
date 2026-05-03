from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PlotCanvas(FigureCanvas):
    def __init__(self):
        self.figure = Figure(figsize=(7, 4), tight_layout=True)
        self.axes = self.figure.add_subplot(111)
        super().__init__(self.figure)

    def clear(self):
        self.axes.clear()
        self.draw()


class MainWindow(QMainWindow):
    def __init__(self, user_name: str = ""):
        super().__init__()
        self.controller = None
        self.user_name = user_name
        self.setWindowTitle("Identificação de Sistemas e Controle PID — Grupo 1")
        self.resize(1200, 750)

        # Widget central com header + abas
        central = QWidget()
        central_layout = QVBoxLayout(central)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        # ── Header ──────────────────────────────────────────────────────
        header = QWidget()
        header.setStyleSheet("background-color: #2c3e50;")
        header.setFixedHeight(48)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 16, 0)

        app_title = QLabel("Projeto Prático C213 — Sistemas Embarcados")
        app_title.setStyleSheet("color: #ecf0f1; font-size: 13px; font-weight: bold;")

        self.user_label = QLabel()
        self.user_label.setStyleSheet("color: #bdc3c7; font-size: 12px;")
        self.user_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        if user_name:
            self.user_label.setText(f"👤  {user_name}")

        header_layout.addWidget(app_title)
        header_layout.addStretch()
        header_layout.addWidget(self.user_label)
        # ────────────────────────────────────────────────────────────────

        self.tabs = QTabWidget()

        central_layout.addWidget(header)
        central_layout.addWidget(self.tabs, stretch=1)
        self.setCentralWidget(central)

        self._build_identification_tab()
        self._build_pid_tab()
        self._build_graphs_tab()

    def set_controller(self, controller):
        self.controller = controller
        self.load_button.clicked.connect(self.controller.load_dataset)
        self.identify_button.clicked.connect(self.controller.identify_dataset)
        self.tune_button.clicked.connect(self.controller.tune_pid)
        self.export_button.clicked.connect(self.controller.export_current_plot)
        self.method_mode_radio.toggled.connect(self._update_pid_mode)
        self.model_selector.currentIndexChanged.connect(self.controller.select_model)
        self._update_pid_mode()

    def _build_identification_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Linha de ações
        actions = QHBoxLayout()
        self.load_button = QPushButton("Carregar .mat")
        self.identify_button = QPushButton("Identificar")
        self.identify_button.setEnabled(False)
        self.dataset_label = QLabel("Nenhum dataset carregado")
        actions.addWidget(self.load_button)
        actions.addWidget(self.identify_button)
        actions.addWidget(self.dataset_label, stretch=1)

        # Seletor manual de modelo
        model_row = QHBoxLayout()
        model_label = QLabel("Modelo identificado:")
        self.model_selector = QComboBox()
        self.model_selector.setEnabled(False)
        self.model_selector.setToolTip(
            "Selecione manualmente entre Smith e Sundaresan. "
            "O padrão é o modelo com menor EQM."
        )
        model_row.addWidget(model_label)
        model_row.addWidget(self.model_selector, stretch=1)

        self.identification_plot = PlotCanvas()
        self.identification_results = QTextEdit()
        self.identification_results.setReadOnly(True)
        self.identification_results.setMaximumHeight(140)

        layout.addLayout(actions)
        layout.addLayout(model_row)
        layout.addWidget(self.identification_plot, stretch=1)
        layout.addWidget(self.identification_results)
        self.tabs.addTab(tab, "Identificação")

    def _build_pid_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)

        mode_group = QGroupBox("Modo de sintonia")
        mode_layout = QVBoxLayout(mode_group)
        self.method_mode_radio = QRadioButton("Método clássico")
        self.manual_mode_radio = QRadioButton("Manual")
        self.method_mode_radio.setChecked(True)
        mode_layout.addWidget(self.method_mode_radio)
        mode_layout.addWidget(self.manual_mode_radio)

        method_group = QGroupBox("Método clássico")
        method_layout = QFormLayout(method_group)
        self.tuning_method_combo = QComboBox()
        self.tuning_method_combo.addItems(["CHR com sobresinal", "Cohen-Coon"])
        method_layout.addRow("Método:", self.tuning_method_combo)

        pid_group = QGroupBox("Parâmetros PID")
        pid_layout = QFormLayout(pid_group)
        self.kp_input = QLineEdit()
        self.kp_input.setPlaceholderText("Kp")
        self.ti_input = QLineEdit()
        self.ti_input.setPlaceholderText("Ti (s)")
        self.td_input = QLineEdit()
        self.td_input.setPlaceholderText("Td (s)")
        self.clear_pid_button = QPushButton("Limpar")
        self.clear_pid_button.clicked.connect(self.clear_pid_inputs)
        pid_layout.addRow("Kp:", self.kp_input)
        pid_layout.addRow("Ti:", self.ti_input)
        pid_layout.addRow("Td:", self.td_input)
        pid_layout.addRow(self.clear_pid_button)

        control_group = QGroupBox("Controle")
        control_layout = QFormLayout(control_group)
        self.setpoint_input = QLineEdit("1.0")
        self.setpoint_input.setToolTip("Valor do setpoint para o degrau unitário")
        self.tune_button = QPushButton("Sintonizar")
        self.tune_button.setEnabled(False)
        self.export_button = QPushButton("Exportar gráfico")
        self.export_button.setEnabled(False)
        control_layout.addRow("SetPoint:", self.setpoint_input)
        control_layout.addRow(self.tune_button)
        control_layout.addRow(self.export_button)

        self.metrics_text = QTextEdit()
        self.metrics_text.setReadOnly(True)

        layout.addWidget(mode_group, 0, 0)
        layout.addWidget(method_group, 1, 0)
        layout.addWidget(pid_group, 2, 0)
        layout.addWidget(control_group, 3, 0)
        layout.addWidget(self.metrics_text, 0, 1, 4, 1)
        layout.setColumnStretch(1, 1)

        self.tabs.addTab(tab, "Controle PID")

    def _build_graphs_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        self.control_plot = PlotCanvas()
        layout.addWidget(self.control_plot)
        self.tabs.addTab(tab, "Gráficos")

    def _update_pid_mode(self):
        method_mode = self.method_mode_radio.isChecked()
        self.tuning_method_combo.setEnabled(method_mode)
        self.kp_input.setReadOnly(method_mode)
        self.ti_input.setReadOnly(method_mode)
        self.td_input.setReadOnly(method_mode)
        self.clear_pid_button.setEnabled(not method_mode)

    # ------------------------------------------------------------------
    # Diálogos
    # ------------------------------------------------------------------

    def select_mat_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Selecionar dataset", "", "MAT files (*.mat)")
        return path

    def select_export_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Exportar gráfico", "", "PNG (*.png);;JPEG (*.jpg)")
        return path

    def clear_pid_inputs(self):
        self.kp_input.clear()
        self.ti_input.clear()
        self.td_input.clear()

    def show_error(self, message):
        QMessageBox.critical(self, "Erro", message)

    def show_info(self, message):
        QMessageBox.information(self, "Informação", message)