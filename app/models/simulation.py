import numpy as np
import control


def simulate_closed_loop(model, pid, setpoint, duration=130.0, samples=600):
    time = np.linspace(0, duration, samples)

    s = control.TransferFunction.s
    controller = pid.kp * (1 + 1 / (pid.ti * s) + pid.td * s)
    plant = control.TransferFunction([model.k], [model.tau, 1])

    if model.theta > 0:
        delay_num, delay_den = control.pade(model.theta, 1)
        plant = control.TransferFunction(delay_num, delay_den) * plant

    closed_loop = control.feedback(controller * plant, 1)
    _, response = control.step_response(closed_loop * setpoint, T=time)
    return time, np.asarray(response)
