"""Testes para carregamento e validação do dataset."""
import pytest
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from models.dataset import load_process_dataset, ProcessDataset


class TestLoadDataset:
    def test_loads_grupo1_dataset(self, dataset_path):
        ds = load_process_dataset(dataset_path)
        assert isinstance(ds, ProcessDataset)

    def test_vectors_same_length(self, dataset_path):
        ds = load_process_dataset(dataset_path)
        assert len(ds.time) == len(ds.input_signal) == len(ds.output_signal)

    def test_time_is_monotonic(self, dataset_path):
        ds = load_process_dataset(dataset_path)
        assert np.all(np.diff(ds.time) > 0), "Vetor de tempo não é monotonicamente crescente."

    def test_step_detected(self, dataset_path):
        ds = load_process_dataset(dataset_path)
        assert ds.step_time > 0, "Instante do degrau deve ser maior que zero."
        assert ds.step_time < ds.time[-1], "Instante do degrau deve estar dentro do vetor de tempo."

    def test_input_delta_nonzero(self, dataset_path):
        ds = load_process_dataset(dataset_path)
        assert ds.input_delta != 0, "Delta da entrada deve ser diferente de zero."

    def test_output_delta_nonzero(self, dataset_path):
        ds = load_process_dataset(dataset_path)
        assert ds.output_delta != 0, "Delta da saída deve ser diferente de zero."

    def test_missing_variable_raises(self, tmp_path):
        """Arquivo .mat sem as variáveis esperadas deve lançar ValueError."""
        from scipy.io import savemat
        mat_file = tmp_path / "bad.mat"
        savemat(str(mat_file), {"x": [1, 2, 3]})
        with pytest.raises(ValueError, match="variaveis esperadas"):
            load_process_dataset(str(mat_file))

    def test_mismatched_lengths_raises(self, tmp_path):
        """Vetores com tamanhos diferentes devem lançar ValueError."""
        from scipy.io import savemat
        mat_file = tmp_path / "bad2.mat"
        savemat(str(mat_file), {
            "tiempo": [0, 1, 2],
            "entrada": [0, 1],       # tamanho diferente
            "salida":  [0, 1, 2],
        })
        with pytest.raises(ValueError, match="mesmo tamanho"):
            load_process_dataset(str(mat_file))