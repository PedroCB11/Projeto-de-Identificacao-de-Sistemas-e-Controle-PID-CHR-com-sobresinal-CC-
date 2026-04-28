from dataclasses import dataclass

import numpy as np


@dataclass
class FOPDTModel:
    method: str
    k: float
    tau: float
    theta: float
    mse: float


def _time_at_response_level(dataset, level):
    target = dataset.output_initial + level * dataset.output_delta
    time = dataset.time
    output = dataset.output_signal
    start_index = int(np.searchsorted(time, dataset.step_time))

    for index in range(start_index + 1, len(output)):
        y0 = output[index - 1]
        y1 = output[index]
        crossed_up = y0 <= target <= y1
        crossed_down = y0 >= target >= y1
        if crossed_up or crossed_down:
            if y1 == y0:
                return float(time[index])
            ratio = (target - y0) / (y1 - y0)
            return float(time[index - 1] + ratio * (time[index] - time[index - 1]) - dataset.step_time)

    raise ValueError(f"Nao foi possivel localizar o ponto de {level * 100:.1f}% da resposta.")


def identify_smith(dataset):
    if dataset.input_delta == 0:
        raise ValueError("A entrada nao possui degrau valido para identificacao.")

    k = dataset.output_delta / dataset.input_delta
    t28 = _time_at_response_level(dataset, 0.283)
    t63 = _time_at_response_level(dataset, 0.632)
    tau = 1.5 * (t63 - t28)
    theta = max(0.0, t63 - tau)

    simulated = simulate_open_loop(dataset.time, dataset.step_time, dataset.input_delta, dataset.output_initial, k, tau, theta)
    mse = float(np.mean((dataset.output_signal - simulated) ** 2))

    return FOPDTModel(method="Smith", k=float(k), tau=float(tau), theta=float(theta), mse=mse)


def identify_sundaresan(dataset):
    if dataset.input_delta == 0:
        raise ValueError("A entrada nao possui degrau valido para identificacao.")

    k = dataset.output_delta / dataset.input_delta
    t35 = _time_at_response_level(dataset, 0.353)
    t85 = _time_at_response_level(dataset, 0.853)
    tau = 0.67 * (t85 - t35)
    theta = max(0.0, 1.3 * t35 - 0.29 * t85)

    simulated = simulate_open_loop(dataset.time, dataset.step_time, dataset.input_delta, dataset.output_initial, k, tau, theta)
    mse = float(np.mean((dataset.output_signal - simulated) ** 2))

    return FOPDTModel(method="Sundaresan", k=float(k), tau=float(tau), theta=float(theta), mse=mse)


def identify_all(dataset):
    results = [identify_smith(dataset), identify_sundaresan(dataset)]
    return sorted(results, key=lambda item: item.mse)


def simulate_open_loop(time, step_time, input_delta, output_initial, k, tau, theta):
    if tau <= 0:
        raise ValueError("Tau deve ser maior que zero.")

    effective_time = np.asarray(time, dtype=float) - step_time - theta
    response_delta = np.where(
        effective_time >= 0,
        k * input_delta * (1 - np.exp(-effective_time / tau)),
        0.0,
    )
    return response_delta + output_initial
