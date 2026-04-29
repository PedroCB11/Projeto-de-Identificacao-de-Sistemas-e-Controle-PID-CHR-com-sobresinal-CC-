import os

from models.dataset import load_process_dataset
from models.identification import identify_all, simulate_open_loop
from models.metrics import calculate_response_metrics
from models.simulation import simulate_closed_loop
from models.tuning import PIDParameters, tune_by_method


class MainController:
    def __init__(self, view):
        self.view = view
        self.dataset = None
        self.identification_results = []
        self.selected_model = None
        self.current_pid = None

    def load_dataset(self):
        path = self.view.select_mat_file()
        if not path:
            return

        try:
            self.dataset = load_process_dataset(path)
        except Exception as exc:
            self.view.show_error(str(exc))
            return

        self.view.dataset_label.setText(os.path.basename(path))
        self.view.identify_button.setEnabled(True)
        self.view.tune_button.setEnabled(False)
        self.view.identification_results.setPlainText("Dataset carregado. Clique em Identificar.")
        self._plot_dataset()

        default_setpoint = self.dataset.input_delta if self.dataset.input_delta != 0 else self.dataset.input_final
        self.view.setpoint_input.setText(f"{default_setpoint:.4g}")

    def identify_dataset(self):
        if self.dataset is None:
            self.view.show_error("Carregue um dataset antes de identificar.")
            return

        try:
            self.identification_results = identify_all(self.dataset)
        except Exception as exc:
            self.view.show_error(str(exc))
            return

        self.selected_model = self.identification_results[0]
        self.view.tune_button.setEnabled(True)
        self._plot_dataset(include_models=True)
        self._show_identification_results()

    def tune_pid(self):
        if self.selected_model is None:
            self.view.show_error("Identifique o sistema antes de sintonizar o PID.")
            return

        try:
            setpoint = float(self.view.setpoint_input.text().replace(",", "."))

            if self.view.method_mode_radio.isChecked():
                method = self.view.tuning_method_combo.currentText()
                pid = tune_by_method(self.selected_model, method)
                self._fill_pid_inputs(pid)
            else:
                pid = PIDParameters(
                    kp=float(self.view.kp_input.text().replace(",", ".")),
                    ti=float(self.view.ti_input.text().replace(",", ".")),
                    td=float(self.view.td_input.text().replace(",", ".")),
                    method="Manual",
                )

            time, response = simulate_closed_loop(self.selected_model, pid, setpoint)
            metrics = calculate_response_metrics(time, response, setpoint)
        except Exception as exc:
            self.view.show_error(str(exc))
            return

        self.current_pid = pid
        self._plot_control_response(time, response, setpoint)
        self._show_metrics(pid, metrics)
        self.view.export_button.setEnabled(True)
        self.view.tabs.setCurrentIndex(2)

    def export_current_plot(self):
        path = self.view.select_export_file()
        if not path:
            return

        self.view.control_plot.figure.savefig(path, dpi=150)
        self.view.show_info("Grafico exportado com sucesso.")

    def _plot_dataset(self, include_models=False):
        axes = self.view.identification_plot.axes
        axes.clear()
        axes.plot(self.dataset.time, self.dataset.input_signal, label="Entrada")
        axes.plot(self.dataset.time, self.dataset.output_signal, label="Saida experimental", linewidth=2)

        if include_models:
            for result in self.identification_results:
                simulated = simulate_open_loop(
                    self.dataset.time,
                    self.dataset.step_time,
                    self.dataset.input_delta,
                    self.dataset.output_initial,
                    result.k,
                    result.tau,
                    result.theta,
                )
                label = f"Modelo {result.method} (EQM={result.mse:.4g})"
                axes.plot(self.dataset.time, simulated, linestyle="--", label=label)

        axes.axvline(self.dataset.step_time, color="gray", linestyle="--", label="Degrau")
        title = "Comparacao entre dados experimentais e modelos identificados" if include_models else "Dados experimentais"
        axes.set_title(title)
        axes.set_xlabel("Tempo (s)")
        axes.set_ylabel("Amplitude")
        axes.grid(True)
        axes.legend()
        self.view.identification_plot.draw()

    def _show_identification_results(self):
        lines = ["Resultados de identificacao:"]
        for result in self.identification_results:
            lines.append(
                f"{result.method}: k={result.k:.4f}, tau={result.tau:.4f}, "
                f"theta={result.theta:.4f}, EQM={result.mse:.6f}"
            )
        lines.append("")
        lines.append(f"Modelo selecionado: {self.selected_model.method} (menor EQM)")
        self.view.identification_results.setPlainText("\n".join(lines))

    def _fill_pid_inputs(self, pid):
        self.view.kp_input.setText(f"{pid.kp:.6g}")
        self.view.ti_input.setText(f"{pid.ti:.6g}")
        self.view.td_input.setText(f"{pid.td:.6g}")

    def _plot_control_response(self, time, response, setpoint):
        axes = self.view.control_plot.axes
        axes.clear()
        axes.plot(time, response, label="Resposta controlada")
        axes.axhline(setpoint, color="gray", linestyle="--", label="SetPoint")
        axes.set_title("Resposta em malha fechada")
        axes.set_xlabel("Tempo (s)")
        axes.set_ylabel("Saida")
        axes.grid(True)
        axes.legend()
        self.view.control_plot.draw()

    def _show_metrics(self, pid, metrics):
        def fmt(value):
            return "N/A" if value is None else f"{value:.4f}"

        text = "\n".join(
            [
                f"Metodo: {pid.method}",
                f"Kp: {pid.kp:.6g}",
                f"Ti: {pid.ti:.6g}",
                f"Td: {pid.td:.6g}",
                "",
                f"Tempo de subida (tr): {fmt(metrics['tr'])} s",
                f"Tempo de acomodacao (ts): {fmt(metrics['ts'])} s",
                f"Overshoot (Mp): {metrics['mp']:.4f} %",
                f"Erro em regime permanente (ess): {metrics['ess']:.6g}",
            ]
        )
        self.view.metrics_text.setPlainText(text)
