# Projeto de Identificacao de Sistemas e Controle PID

Aplicacao em Python para carregar datasets `.mat`, identificar modelos FOPDT e sintonizar controladores PID.

## Estrutura MVC

```text
app/
  main.py
  requirements.txt
  models/
    dataset.py
    identification.py
    tuning.py
    simulation.py
    metrics.py
  controllers/
    main_controller.py
  views/
    main_window.py
```

## Como rodar

```bash
pip install -r requirements.txt
python main.py
```

## Funcionalidades iniciais

- Carregamento de arquivo `.mat`
- Plotagem dos sinais de entrada e saida
- Identificacao FOPDT por Smith e Sundaresan
- Selecao automatica do modelo com menor EQM
- Sintonia PID por CHR com sobresinal
- Sintonia PID por Cohen-Coon
- Modo manual para parametros PID
- Simulacao de resposta em malha fechada
- Calculo de metricas de desempenho
- Exportacao do grafico controlado
