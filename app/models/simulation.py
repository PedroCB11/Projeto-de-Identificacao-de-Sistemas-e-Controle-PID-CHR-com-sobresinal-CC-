import numpy as np
import control


def simulate_closed_loop(model, pid, setpoint, duration=None, samples=1000):
    """Simula a resposta em malha fechada com controlador PID e modelo FOPDT.

    A aproximação de Padé de ordem 2 é usada para o atraso de transporte,
    pois oferece melhor acurácia que a ordem 1, reduzindo o artefato de
    pico negativo inicial típico das aproximações racionais de e^(-s*theta).

    A duração padrão é calculada automaticamente como 10*(tau+theta) para
    garantir que o regime permanente fique visível na simulação.
    """
    if duration is None:
        duration = 10.0 * (model.tau + model.theta)

    time = np.linspace(0, duration, samples)

    s = control.TransferFunction.s

    # Controlador PID paralelo: Kp * (1 + 1/(Ti*s) + Td*s)
    controller = pid.kp * (1 + 1 / (pid.ti * s) + pid.td * s)

    # Planta FOPDT: k / (tau*s + 1)
    plant = control.TransferFunction([model.k], [model.tau, 1])

    # Atraso de transporte aproximado por Padé de ordem 2
    if model.theta > 0:
        delay_num, delay_den = control.pade(model.theta, 2)
        plant = control.TransferFunction(delay_num, delay_den) * plant

    # Sistema em malha fechada unitária
    closed_loop = control.feedback(controller * plant, 1)

    # Resposta ao degrau escalada pelo setpoint
    _, response = control.step_response(closed_loop * setpoint, T=time)
    return time, np.asarray(response)