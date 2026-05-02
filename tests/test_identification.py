"""Testes para os métodos de identificação FOPDT."""
import pytest
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from models.identification import (
    FOPDTModel,
    identify_smith,
    identify_sundaresan,
    identify_all,
    simulate_open_loop,
)
from models.dataset import load_process_dataset


# Tolerância relativa de 5% em relação aos parâmetros reais do dataset Grupo 1
# (k=1.08, tau=17.0, theta=3.0)
TOL = 0.05


class TestSmithIdentification:
    def test_returns_fopdt_model(self, dataset_path):
        ds = load_process_dataset(dataset_path)
        result = identify_smith(ds)
        assert isinstance(result, FOPDTModel)
        assert result.method == "Smith"

    def test_gain_within_tolerance(self, dataset_path):
        ds = load_process_dataset(dataset_path)
        result = identify_smith(ds)
        assert abs(result.k - 1.08) / 1.08 < TOL, f"k={result.k:.4f} fora da tolerância de ±5%"

    def test_tau_within_tolerance(self, dataset_path):
        ds = load_process_dataset(dataset_path)
        result = identify_smith(ds)
        assert abs(result.tau - 17.0) / 17.0 < TOL, f"tau={result.tau:.4f} fora da tolerância"

    def test_theta_within_tolerance(self, dataset_path):
        ds = load_process_dataset(dataset_path)
        result = identify_smith(ds)
        assert abs(result.theta - 3.0) / 3.0 < TOL, f"theta={result.theta:.4f} fora da tolerância"

    def test_mse_positive(self, dataset_path):
        ds = load_process_dataset(dataset_path)
        result = identify_smith(ds)
        assert result.mse >= 0

    def test_zero_input_raises(self, dataset_path):
        ds = load_process_dataset(dataset_path)
        ds_bad = type(ds)(
            time=ds.time, input_signal=np.zeros_like(ds.input_signal),
            output_signal=ds.output_signal, step_time=ds.step_time,
            input_initial=0.0, input_final=0.0,
            output_initial=ds.output_initial, output_final=ds.output_final,
        )
        with pytest.raises(ValueError, match="degrau valido"):
            identify_smith(ds_bad)


class TestSundaresanIdentification:
    def test_returns_fopdt_model(self, dataset_path):
        ds = load_process_dataset(dataset_path)
        result = identify_sundaresan(ds)
        assert isinstance(result, FOPDTModel)
        assert result.method == "Sundaresan"

    def test_gain_within_tolerance(self, dataset_path):
        ds = load_process_dataset(dataset_path)
        result = identify_sundaresan(ds)
        assert abs(result.k - 1.08) / 1.08 < TOL

    def test_mse_positive(self, dataset_path):
        ds = load_process_dataset(dataset_path)
        result = identify_sundaresan(ds)
        assert result.mse >= 0


class TestIdentifyAll:
    def test_returns_two_models(self, dataset_path):
        ds = load_process_dataset(dataset_path)
        results = identify_all(ds)
        assert len(results) == 2

    def test_sorted_by_mse(self, dataset_path):
        ds = load_process_dataset(dataset_path)
        results = identify_all(ds)
        assert results[0].mse <= results[1].mse, "Modelos devem estar ordenados por EQM crescente."

    def test_best_is_smith_for_grupo1(self, dataset_path):
        """Para o dataset do Grupo 1, Smith deve ter menor EQM."""
        ds = load_process_dataset(dataset_path)
        results = identify_all(ds)
        assert results[0].method == "Smith"


class TestSimulateOpenLoop:
    def test_starts_at_output_initial(self):
        time = np.linspace(0, 100, 500)
        out = simulate_open_loop(time, step_time=5.0, input_delta=60.0,
                                  output_initial=0.0, k=1.08, tau=17.0, theta=3.0)
        # Antes do degrau+atraso, deve ser output_initial
        assert abs(out[0] - 0.0) < 1e-10

    def test_reaches_steady_state(self):
        time = np.linspace(0, 500, 2000)
        out = simulate_open_loop(time, step_time=5.0, input_delta=60.0,
                                  output_initial=0.0, k=1.08, tau=17.0, theta=3.0)
        expected_final = 1.08 * 60.0
        assert abs(out[-1] - expected_final) / expected_final < 0.01

    def test_tau_zero_raises(self):
        with pytest.raises(ValueError, match="Tau deve ser maior"):
            simulate_open_loop(np.linspace(0, 10), 1.0, 1.0, 0.0, 1.0, 0.0, 0.0)