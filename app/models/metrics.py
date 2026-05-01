import numpy as np


def calculate_response_metrics(time, response, setpoint, settling_band=0.02):
    """Calcula as métricas de desempenho da resposta em malha fechada.

    Parâmetros
    ----------
    time : array-like
        Vetor de tempo da simulação.
    response : array-like
        Vetor de resposta do sistema.
    setpoint : float
        Valor do setpoint (referência) em degrau.
    settling_band : float
        Fração do setpoint usada como banda de acomodação (padrão: 2%).

    Retorna
    -------
    dict com tr, ts, mp, ess e final_value.
    """
    time = np.asarray(time)
    response = np.asarray(response)
    final_value = float(response[-1])

    if setpoint == 0:
        steady_state_error = -final_value
    else:
        steady_state_error = setpoint - final_value

    peak = float(np.max(response))
    overshoot = 0.0
    if setpoint != 0:
        overshoot = max(0.0, (peak - setpoint) / abs(setpoint) * 100)

    rise_time = _rise_time(time, response, setpoint)
    settling_time = _settling_time(time, response, setpoint, settling_band)

    return {
        "tr": rise_time,
        "ts": settling_time,
        "mp": overshoot,
        "ess": steady_state_error,
        "final_value": final_value,
    }


def _rise_time(time, response, setpoint):
    """Tempo de subida de 10% a 90% do setpoint."""
    if setpoint == 0:
        return 0.0

    lower = 0.1 * setpoint
    upper = 0.9 * setpoint

    try:
        if setpoint > 0:
            t10 = time[np.where(response >= lower)[0][0]]
            t90 = time[np.where(response >= upper)[0][0]]
        else:
            t10 = time[np.where(response <= lower)[0][0]]
            t90 = time[np.where(response <= upper)[0][0]]
        return float(t90 - t10)
    except IndexError:
        return None


def _settling_time(time, response, setpoint, settling_band):
    """Tempo de acomodação usando banda de ±settling_band*|setpoint|.

    A banda é calculada sobre o valor do setpoint (não o valor final),
    garantindo o critério correto de ±2% da referência.
    """
    # Usa o setpoint como referência da banda; fallback para final_value se sp=0
    reference = abs(setpoint) if setpoint != 0 else abs(float(response[-1]))
    band = settling_band * max(reference, 1e-9)
    final_value = float(response[-1])

    outside = np.where(np.abs(response - final_value) > band)[0]
    if len(outside) == 0:
        return 0.0
    last_outside = outside[-1]
    if last_outside + 1 >= len(time):
        return None
    return float(time[last_outside + 1])