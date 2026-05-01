from dataclasses import dataclass


@dataclass
class PIDParameters:
    kp: float
    ti: float
    td: float
    method: str


def tune_chr_overshoot(model):
    """Sintonia PID pelo método CHR com 20% de sobresinal.

    Fórmulas de Chien, Hrones e Reswick (1952) para seguimento de setpoint
    com 20% de sobresinal (overshoot), usando modelo FOPDT:

        Kp = 0.95 * tau / (k * theta)
        Ti = 1.40 * tau
        Td = 0.47 * theta

    Referência: Chien, K.L., Hrones, J.A., Reswick, J.B. (1952).
    """
    _validate_model(model)
    return PIDParameters(
        kp=0.95 * model.tau / (model.k * model.theta),
        ti=1.40 * model.tau,
        td=0.47 * model.theta,
        method="CHR com sobresinal",
    )


def tune_cohen_coon(model):
    """Sintonia PID pelo método de Cohen-Coon.

    Fórmulas de Cohen e Coon (1953) para rejeição de perturbação com
    modelo FOPDT, onde r = theta/tau:

        Kp = (1/k) * (tau/theta) * (4/3 + r/4)
        Ti = theta * (32 + 6*r) / (13 + 8*r)
        Td = 4*theta / (11 + 2*r)

    Referência: Cohen, G.H., Coon, G.A. (1953).
    """
    _validate_model(model)
    r = model.theta / model.tau
    return PIDParameters(
        kp=(1 / model.k) * (model.tau / model.theta) * (4 / 3 + model.theta / (4 * model.tau)),
        ti=model.theta * (32 + 6 * r) / (13 + 8 * r),
        td=4 * model.theta / (11 + 2 * r),
        method="Cohen-Coon",
    )


def tune_by_method(model, method):
    """Seleciona e executa o método de sintonia pelo nome."""
    if method == "CHR com sobresinal":
        return tune_chr_overshoot(model)
    if method == "Cohen-Coon":
        return tune_cohen_coon(model)
    raise ValueError(f"Método de sintonia desconhecido: {method}")


def _validate_model(model):
    if model.k == 0:
        raise ValueError("Ganho k não pode ser zero.")
    if model.tau <= 0:
        raise ValueError("Tau deve ser maior que zero.")
    if model.theta <= 0:
        raise ValueError("Theta deve ser maior que zero para sintonia PID clássica.")