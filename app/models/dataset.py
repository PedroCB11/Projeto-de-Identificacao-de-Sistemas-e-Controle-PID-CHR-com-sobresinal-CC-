from dataclasses import dataclass

import numpy as np
from scipy.io import loadmat


@dataclass
class ProcessDataset:
    time: np.ndarray
    input_signal: np.ndarray
    output_signal: np.ndarray
    step_time: float
    input_initial: float
    input_final: float
    output_initial: float
    output_final: float

    @property
    def input_delta(self):
        return self.input_final - self.input_initial

    @property
    def output_delta(self):
        return self.output_final - self.output_initial


def _as_vector(value):
    return np.asarray(value, dtype=float).reshape(-1)


def load_process_dataset(path):
    raw = loadmat(path, squeeze_me=True, struct_as_record=False)

    try:
        time = _as_vector(raw["tiempo"])
        input_signal = _as_vector(raw["entrada"])
        output_signal = _as_vector(raw["salida"])
    except KeyError as exc:
        raise ValueError("Arquivo .mat nao contem as variaveis esperadas: tiempo, entrada e salida.") from exc

    if not (len(time) == len(input_signal) == len(output_signal)):
        raise ValueError("Vetores de tempo, entrada e saida devem ter o mesmo tamanho.")

    input_initial = float(input_signal[0])
    input_final = float(input_signal[-1])
    output_initial = float(output_signal[0])
    output_final = float(output_signal[-1])

    input_change = np.abs(np.diff(input_signal))
    if np.any(input_change > 0):
        step_index = int(np.argmax(input_change) + 1)
        step_time = float(time[step_index])
    else:
        step_time = float(time[0])

    return ProcessDataset(
        time=time,
        input_signal=input_signal,
        output_signal=output_signal,
        step_time=step_time,
        input_initial=input_initial,
        input_final=input_final,
        output_initial=output_initial,
        output_final=output_final,
    )
