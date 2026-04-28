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
    def __init__(self):
        super().__init__()
        self.controller = None
        self.setWindowTitle("Identificacao de Sistemas e Controle PID")
        self.resize(1100, 720)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

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
        self._update_pid_mode()

    def _build_identification_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        actions = QHBoxLayout()
        self.load_button = QPushButton("Carregar .mat")
        self.identify_button = QPushButton("Identificar")
        self.identify_button.setEnabled(False)
        self.dataset_label = QLabel("Nenhum dataset carregado")
        actions.addWidget(self.load_button)
        actions.addWidget(self.identify_button)
        actions.addWidget(self.dataset_label, stretch=1)

        self.identification_plot = PlotCanvas()
        self.identification_results = QTextEdit()
        self.identification_results.setReadOnly(True)
        self.identification_results.setMaximumHeight(150)

        layout.addLayout(actions)
        layout.addWidget(self.identification_plot, stretch=1)
        layout.addWidget(self.identification_results)
        self.tabs.addTab(tab, "Identificacao")

    def _build_pid_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)

        mode_group = QGroupBox("Modo de sintonia")
        mode_layout = QVBoxLayout(mode_group)
        self.method_mode_radio = QRadioButton("Metodo")
        self.manual_mode_radio = QRadioButton("Manual")
        self.method_mode_radio.setChecked(True)
        mode_layout.addWidget(self.method_mode_radio)
        mode_layout.addWidget(self.manual_mode_radio)

        method_group = QGroupBox("Metodo classico")
        method_layout = QFormLayout(method_group)
        self.tuning_method_combo = QComboBox()
        self.tuning_method_combo.addItems(["CHR com sobresinal", "Cohen-Coon"])
        method_layout.addRow("Metodo:", self.tuning_method_combo)

        pid_group = QGroupBox("Parametros PID")
        pid_layout = QFormLayout(pid_group)
        self.kp_input = QLineEdit()
        self.ti_input = QLineEdit()
        self.td_input = QLineEdit()
        self.clear_pid_button = QPushButton("Limpar")
        self.clear_pid_button.clicked.connect(self.clear_pid_inputs)
        pid_layout.addRow("Kp:", self.kp_input)
        pid_layout.addRow("Ti:", self.ti_input)
        pid_layout.addRow("Td:", self.td_input)
        pid_layout.addRow(self.clear_pid_button)

        control_group = QGroupBox("Controle")
        control_layout = QFormLayout(control_group)
        self.setpoint_input = QLineEdit("1.0")
        self.tune_button = QPushButton("Sintonizar")
        self.tune_button.setEnabled(False)
        self.export_button = QPushButton("Exportar grafico")
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
        self.tabs.addTab(tab, "Graficos")

    def _update_pid_mode(self):
        method_mode = self.method_mode_radio.isChecked()
        self.tuning_method_combo.setEnabled(method_mode)
        self.kp_input.setReadOnly(method_mode)
        self.ti_input.setReadOnly(method_mode)
        self.td_input.setReadOnly(method_mode)
        self.clear_pid_button.setEnabled(not method_mode)

    def select_mat_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Selecionar dataset", "", "MAT files (*.mat)")
        return path

    def select_export_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Exportar grafico", "", "PNG (*.png);;JPEG (*.jpg)")
        return path

    def clear_pid_inputs(self):
        self.kp_input.clear()
        self.ti_input.clear()
        self.td_input.clear()

    def show_error(self, message):
        QMessageBox.critical(self, "Erro", message)

    def show_info(self, message):
        QMessageBox.information(self, "Informacao", message)
