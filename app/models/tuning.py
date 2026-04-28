from dataclasses import dataclass


@dataclass
class PIDParameters:
    kp: float
    ti: float
    td: float
    method: str


def tune_chr_overshoot(model):
    _validate_model(model)
    return PIDParameters(
        kp=0.95 * model.tau / (model.k * model.theta),
        ti=1.4 * model.tau,
        td=0.47 * model.theta,
        method="CHR com sobresinal",
    )


def tune_cohen_coon(model):
    _validate_model(model)
    r = model.theta / model.tau
    return PIDParameters(
        kp=(1 / model.k) * (model.tau / model.theta) * (4 / 3 + model.theta / (4 * model.tau)),
        ti=model.theta * (32 + 6 * r) / (13 + 8 * r),
        td=model.theta * 4 / (11 + 2 * r),
        method="Cohen-Coon",
    )


def tune_by_method(model, method):
    if method == "CHR com sobresinal":
        return tune_chr_overshoot(model)
    if method == "Cohen-Coon":
        return tune_cohen_coon(model)
    raise ValueError(f"Metodo de sintonia desconhecido: {method}")


def _validate_model(model):
    if model.k == 0:
        raise ValueError("Ganho k nao pode ser zero.")
    if model.tau <= 0:
        raise ValueError("Tau deve ser maior que zero.")
    if model.theta <= 0:
        raise ValueError("Theta deve ser maior que zero para sintonia PID classica.")
