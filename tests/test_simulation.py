"""Testes para simulação em malha fechada."""
import pytest
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from models.simulation import simulate_closed_loop


class TestSimulateClosedLoop:
    def test_returns_arrays(self, simple_model, chr_pid):
        t, r = simulate_closed_loop(simple_model, chr_pid, setpoint=60.0)
        assert isinstance(t, np.ndarray)
        assert isinstance(r, np.ndarray)
        assert len(t) == len(r)

    def test_time_starts_at_zero(self, simple_model, chr_pid):
        t, _ = simulate_closed_loop(simple_model, chr_pid, setpoint=60.0)
        assert t[0] == pytest.approx(0.0, abs=1e-9)

    def test_reaches_setpoint(self, simple_model, chr_pid):
        """Sistema com integrador deve convergir para o setpoint."""
        t, r = simulate_closed_loop(simple_model, chr_pid, setpoint=60.0)
        assert abs(r[-1] - 60.0) / 60.0 < 0.01, f"Valor final {r[-1]:.2f} distante do SP=60"

    def test_reaches_setpoint_cohen_coon(self, simple_model, cc_pid):
        t, r = simulate_closed_loop(simple_model, cc_pid, setpoint=60.0)
        assert abs(r[-1] - 60.0) / 60.0 < 0.01

    def test_auto_duration_longer_than_tau(self, simple_model, chr_pid):
        """Duração automática deve ser >= 10*(tau+theta)."""
        t, _ = simulate_closed_loop(simple_model, chr_pid, setpoint=60.0)
        min_duration = 10.0 * (simple_model.tau + simple_model.theta)
        assert t[-1] >= min_duration

    def test_custom_duration_respected(self, simple_model, chr_pid):
        t, _ = simulate_closed_loop(simple_model, chr_pid, setpoint=60.0, duration=500.0)
        assert abs(t[-1] - 500.0) < 1.0

    def test_custom_samples_respected(self, simple_model, chr_pid):
        _, r = simulate_closed_loop(simple_model, chr_pid, setpoint=60.0, samples=200)
        assert len(r) == 200

    def test_negative_setpoint(self, simple_model, cc_pid):
        """Deve funcionar com setpoint negativo."""
        t, r = simulate_closed_loop(simple_model, cc_pid, setpoint=-30.0)
        assert abs(r[-1] - (-30.0)) / 30.0 < 0.02