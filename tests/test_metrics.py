"""Testes para as métricas de desempenho da resposta."""
import pytest
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from models.metrics import calculate_response_metrics
from models.simulation import simulate_closed_loop


def _make_step_response(final, overshoot_frac=0.0, n=1000):
    """Gera uma resposta ao degrau sintética para testes."""
    t = np.linspace(0, 100, n)
    tau = 10.0
    r = final * (1 - np.exp(-t / tau))
    if overshoot_frac > 0:
        # Adiciona um pico artificial
        peak_t = 15.0
        r += final * overshoot_frac * np.exp(-((t - peak_t) ** 2) / 5)
    return t, r


class TestRiseTime:
    def test_rise_time_positive(self, simple_model, chr_pid):
        t, r = simulate_closed_loop(simple_model, chr_pid, setpoint=60.0)
        m = calculate_response_metrics(t, r, 60.0)
        assert m["tr"] is not None and m["tr"] > 0

    def test_rise_time_less_than_settling(self, simple_model, chr_pid):
        t, r = simulate_closed_loop(simple_model, chr_pid, setpoint=60.0)
        m = calculate_response_metrics(t, r, 60.0)
        if m["tr"] and m["ts"]:
            assert m["tr"] < m["ts"]

    def test_zero_setpoint_returns_zero(self):
        t, r = np.linspace(0, 10, 100), np.zeros(100)
        m = calculate_response_metrics(t, r, setpoint=0.0)
        assert m["tr"] == 0.0


class TestSettlingTime:
    def test_settling_time_positive(self, simple_model, chr_pid):
        t, r = simulate_closed_loop(simple_model, chr_pid, setpoint=60.0)
        m = calculate_response_metrics(t, r, 60.0)
        assert m["ts"] is not None and m["ts"] > 0

    def test_settling_band_based_on_setpoint(self):
        """Banda de acomodação deve ser relativa ao setpoint, não ao valor final."""
        sp = 100.0
        t = np.linspace(0, 200, 2000)
        # Resposta que fica exatamente dentro de ±2% de sp=100 após t=50
        r = sp * (1 - np.exp(-t / 15.0))
        m = calculate_response_metrics(t, r, sp, settling_band=0.02)
        assert m["ts"] is not None
        # Após ts, a resposta deve estar dentro de ±2 (2% de 100)
        ts_idx = np.searchsorted(t, m["ts"])
        assert np.all(np.abs(r[ts_idx:] - r[-1]) <= 2.0 + 1e-6)

    def test_already_settled_returns_zero(self):
        t = np.linspace(0, 100, 500)
        r = np.full(500, 50.0)  # constante: nunca saiu da banda
        m = calculate_response_metrics(t, r, setpoint=50.0)
        assert m["ts"] == 0.0


class TestOvershoot:
    def test_no_overshoot_chr(self, simple_model, chr_pid):
        """CHR com sobresinal do Grupo 1 deve ter overshoot < 25%."""
        t, r = simulate_closed_loop(simple_model, chr_pid, setpoint=60.0)
        m = calculate_response_metrics(t, r, 60.0)
        assert m["mp"] < 25.0, f"Overshoot CHR inesperadamente alto: {m['mp']:.1f}%"

    def test_overshoot_cohen_coon_positive(self, simple_model, cc_pid):
        """Cohen-Coon para este modelo deve apresentar overshoot positivo."""
        t, r = simulate_closed_loop(simple_model, cc_pid, setpoint=60.0)
        m = calculate_response_metrics(t, r, 60.0)
        assert m["mp"] > 0

    def test_zero_overshoot_for_monotonic(self):
        t, r = _make_step_response(final=10.0, overshoot_frac=0.0)
        m = calculate_response_metrics(t, r, setpoint=10.0)
        assert m["mp"] == pytest.approx(0.0, abs=0.1)


class TestSteadyStateError:
    def test_ess_near_zero_with_integrator(self, simple_model, chr_pid):
        """PID com integrador: erro em regime deve ser ≈ 0."""
        t, r = simulate_closed_loop(simple_model, chr_pid, setpoint=60.0)
        m = calculate_response_metrics(t, r, 60.0)
        assert abs(m["ess"]) < 0.1

    def test_ess_sign(self):
        """Se o sistema não atingiu o setpoint, ess deve ser positivo."""
        t = np.linspace(0, 100, 500)
        r = 45.0 * np.ones(500)  # fica em 45 quando SP=50
        m = calculate_response_metrics(t, r, setpoint=50.0)
        assert m["ess"] == pytest.approx(5.0, abs=1e-9)