# CHECKLIST — Projeto C213 · Grupo 1

> Arquivo de rastreamento de entregas. Atualizar conforme o progresso do grupo.  
> Última atualização: maio/2026

---

## Métodos obrigatórios do Grupo 1

- [x] **CHR com sobresinal** — implementado em `app/models/tuning.py`
- [x] **Cohen-Coon (CC)** — implementado em `app/models/tuning.py`

---

## Estrutura e Configuração

- [x] Estrutura MVC criada (`app/models/`, `app/views/`, `app/controllers/`)
- [x] Ponto de entrada em `app/main.py`
- [x] Arquivo `app/requirements.txt` com todas as dependências
- [x] Dataset do Grupo 1 na raiz (`Dataset_Grupo1_c213 (1).mat`)
- [x] `.gitignore` criado (exclui `__pycache__`, `.venv`, artefatos gerados)
- [ ] Remover `__pycache__` do histórico Git  
  ```bash
  git rm -r --cached "app/**/__pycache__"
  git commit -m "chore: remove __pycache__ do versionamento"
  ```

---

## Carregamento de Dados

- [x] Carregamento de arquivos `.mat` — `app/models/dataset.py`
- [x] Validação das variáveis `tiempo`, `entrada` e `salida`
- [x] Erro claro se variáveis ausentes ou tamanhos inconsistentes
- [x] Detecção automática do instante do degrau
- [x] Propriedades `input_delta` e `output_delta` calculadas

---

## Identificação FOPDT

- [x] Identificação pelo método de Smith — `app/models/identification.py`
- [x] Identificação pelo método de Sundaresan — `app/models/identification.py`
- [x] Cálculo de EQM para cada modelo
- [x] Ordenação automática por menor EQM
- [x] Simulação da resposta em malha aberta para comparação visual
- [x] **Seleção manual do modelo** via lista suspensa na interface

---

## Interface Gráfica (PyQt5)

- [x] Aba **Identificação**: gráfico + painel de resultados + seletor de modelo
- [x] Aba **Controle PID**: modo método / modo manual, campos PID, SetPoint
- [x] Aba **Gráficos**: resposta em malha fechada com marcadores
- [x] Bloqueio dos campos PID no modo por método
- [x] Botão "Limpar" para parâmetros manuais
- [x] Campo de SetPoint com valor padrão do dataset
- [x] Plotagem dos sinais de entrada e saída na identificação
- [x] Comparação visual Smith × Sundaresan com EQM na legenda

---

## Controle PID

- [x] Sintonia automática — CHR com sobresinal
- [x] Sintonia automática — Cohen-Coon
- [x] Modo manual com validação (campos vazios, Ti ≤ 0, Td < 0)
- [x] Simulação em malha fechada com Padé **ordem 2** (corrigido de ordem 1)
- [x] Duração automática da simulação: `10·(τ + θ)`

---

## Métricas de Desempenho

- [x] Tempo de subida (tr) — 10 % a 90 % do setpoint
- [x] Tempo de acomodação (ts) — banda ±2 % do **setpoint** (corrigido)
- [x] Overshoot (Mp) — `(pico − SP) / |SP| × 100 %`
- [x] Erro em regime permanente (ess) — `SP − valor_final`
- [x] Suporte a setpoint negativo no cálculo de tr

---

## Visualização

- [x] Marcador visual de **tr** (seta anotada no gráfico)
- [x] Marcador visual de **ts** (linha vertical)
- [x] Marcador visual de **Mp** (seta no pico)
- [x] Linha de setpoint (tracejada)
- [x] Grid e legenda nos gráficos
- [x] Exportação do gráfico (.png / .jpg) com `dpi=150`

---

## Documentação

- [x] `README.md` principal — instalação, uso, equações, resultados, comparação
- [x] `CHECKLIST.md` separado para rastreamento de entregas (este arquivo)
- [x] Docstrings em todos os módulos de `models/`
- [x] Equações matemáticas documentadas (Smith, Sundaresan, CHR, CC, Padé)
- [x] Análise comparativa CHR × Cohen-Coon com conclusão
- [x] Seção de limitações e melhorias futuras

---

## Resultados Gerados

- [x] Pasta `assets/` criada com gráficos dos resultados do Grupo 1
- [x] `assets/identificacao_grupo1.png` — comparação Smith × Sundaresan
- [x] `assets/controle_chr_grupo1.png` — resposta CHR com marcadores
- [x] `assets/controle_cc_grupo1.png` — resposta Cohen-Coon com marcadores
- [x] `assets/comparacao_metodos_grupo1.png` — comparação lado a lado
- [ ] Prints da IHM em execução (capturar ao rodar a aplicação e adicionar em `assets/`)

---

## Testes Automatizados

- [x] `tests/conftest.py` — fixtures `simple_model`, `chr_pid`, `cc_pid`, `dataset_path`
- [x] `tests/test_dataset.py` — 8 testes (carregamento, validação, erros)
- [x] `tests/test_identification.py` — 15 testes (Smith, Sundaresan, EQM, parâmetros reais)
- [x] `tests/test_tuning.py` — 18 testes (fórmulas CHR e CC, validações, dispatch)
- [x] `tests/test_simulation.py` — 8 testes (regime permanente, duração, amostras)
- [x] `tests/test_metrics.py` — 9 testes (tr, ts, Mp, ess, banda)
- [x] **58 / 58 testes passando** (`python -m pytest tests/ -v`)

---

## GitHub e Entrega

- [ ] Adicionar `pytest` às dependências de dev (ex: `requirements-dev.txt`)
- [ ] Prints da IHM adicionados em `assets/`
- [ ] Commits significativos de todos os integrantes do grupo
- [ ] Repositório público com código-fonte, README, assets e resultados
- [ ] Preparar demonstração ao vivo para a apresentação

---

## Resumo de Status

| Categoria | Concluído | Pendente |
|-----------|-----------|---------|
| Estrutura / Config | 5 | 1 (limpar `__pycache__` do Git) |
| Dados | 5 | 0 |
| Identificação | 6 | 0 |
| Interface (PyQt5) | 8 | 0 |
| Controle PID | 5 | 0 |
| Métricas | 6 | 0 |
| Visualização | 6 | 0 |
| Documentação | 7 | 0 |
| Resultados / Assets | 4 | 1 (prints da IHM) |
| Testes | 6 | 0 |
| GitHub / Entrega | 0 | 5 |
| **TOTAL** | **58** | **7** |
