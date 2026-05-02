"""Fixtures compartilhadas entre os testes."""
import sys
import os
import pytest
import numpy as np

# Adiciona app/ ao path para importar os módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from models.identification import FOPDTModel
from models.tuning import PIDParameters


@pytest.fixture
def simple_model():
    """Modelo FOPDT com valores simples para testes determinísticos."""
    return FOPDTModel(method="Smith", k=1.0801, tau=16.9245, theta=3.0367, mse=0.003713)


@pytest.fixture
def chr_pid(simple_model):
    from models.tuning import tune_chr_overshoot
    return tune_chr_overshoot(simple_model)


@pytest.fixture
def cc_pid(simple_model):
    from models.tuning import tune_cohen_coon
    return tune_cohen_coon(simple_model)


@pytest.fixture
def dataset_path():
    base = os.path.join(os.path.dirname(__file__), "..")
    path = os.path.join(base, "Dataset_Grupo1_c213 (1).mat")
    if not os.path.exists(path):
        pytest.skip("Dataset do Grupo 1 não encontrado.")
    return path