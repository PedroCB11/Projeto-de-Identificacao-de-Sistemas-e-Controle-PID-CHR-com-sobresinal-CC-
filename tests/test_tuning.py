"""Testes para os métodos de sintonia PID."""
import pytest
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from models.tuning import tune_chr_overshoot, tune_cohen_coon, tune_by_method, PIDParameters
from models.identification import FOPDTModel


# Parâmetros de referência calculados manualmente para o modelo do Grupo 1
# k=1.0801, tau=16.9245, theta=3.0367
K, TAU, THETA = 1.0801, 16.9245, 3.0367
R = THETA / TAU   # ≈ 0.1795


class TestCHROvershoot:
    def test_kp_formula(self, simple_model):
        pid = tune_chr_overshoot(simple_model)
        expected = 0.95 * TAU / (K * THETA)
        assert abs(pid.kp - expected) / expected < 1e-6

    def test_ti_formula(self, simple_model):
        pid = tune_chr_overshoot(simple_model)
        expected = 1.40 * TAU
        assert abs(pid.ti - expected) / expected < 1e-6

    def test_td_formula(self, simple_model):
        pid = tune_chr_overshoot(simple_model)
        expected = 0.47 * THETA
        assert abs(pid.td - expected) / expected < 1e-6

    def test_method_name(self, simple_model):
        pid = tune_chr_overshoot(simple_model)
        assert pid.method == "CHR com sobresinal"

    def test_all_params_positive(self, simple_model):
        pid = tune_chr_overshoot(simple_model)
        assert pid.kp > 0 and pid.ti > 0 and pid.td > 0

    def test_zero_gain_raises(self):
        model = FOPDTModel("test", k=0.0, tau=10.0, theta=2.0, mse=0.0)
        with pytest.raises(ValueError, match="Ganho k"):
            tune_chr_overshoot(model)

    def test_zero_tau_raises(self):
        model = FOPDTModel("test", k=1.0, tau=0.0, theta=2.0, mse=0.0)
        with pytest.raises(ValueError, match="Tau deve ser"):
            tune_chr_overshoot(model)

    def test_zero_theta_raises(self):
        model = FOPDTModel("test", k=1.0, tau=10.0, theta=0.0, mse=0.0)
        with pytest.raises(ValueError, match="Theta deve ser"):
            tune_chr_overshoot(model)


class TestCohenCoon:
    def test_kp_formula(self, simple_model):
        pid = tune_cohen_coon(simple_model)
        expected = (1 / K) * (TAU / THETA) * (4/3 + THETA / (4 * TAU))
        assert abs(pid.kp - expected) / expected < 1e-6

    def test_ti_formula(self, simple_model):
        pid = tune_cohen_coon(simple_model)
        expected = THETA * (32 + 6 * R) / (13 + 8 * R)
        assert abs(pid.ti - expected) / expected < 1e-6

    def test_td_formula(self, simple_model):
        pid = tune_cohen_coon(simple_model)
        expected = 4 * THETA / (11 + 2 * R)
        assert abs(pid.td - expected) / expected < 1e-6

    def test_method_name(self, simple_model):
        pid = tune_cohen_coon(simple_model)
        assert pid.method == "Cohen-Coon"

    def test_all_params_positive(self, simple_model):
        pid = tune_cohen_coon(simple_model)
        assert pid.kp > 0 and pid.ti > 0 and pid.td > 0


class TestTuneByMethod:
    def test_chr_dispatch(self, simple_model):
        pid = tune_by_method(simple_model, "CHR com sobresinal")
        assert pid.method == "CHR com sobresinal"

    def test_cc_dispatch(self, simple_model):
        pid = tune_by_method(simple_model, "Cohen-Coon")
        assert pid.method == "Cohen-Coon"

    def test_unknown_method_raises(self, simple_model):
        with pytest.raises(ValueError, match="desconhecido"):
            tune_by_method(simple_model, "Método Inexistente")