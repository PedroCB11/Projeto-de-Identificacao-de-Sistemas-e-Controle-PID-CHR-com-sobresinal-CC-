# Projeto de Identificacao de Sistemas e Controle PID

Checklist geral do projeto do **Grupo 1**, baseado nos requisitos detalhados em
[app/README.md](app/README.md).

Metodos obrigatorios do Grupo 1:

- [x] CHR com sobresinal
- [x] CC - Cohen-Coon

## Feito

- [x] Estrutura MVC criada. Arquivos/pastas: `app/models`, `app/views`, `app/controllers`, `app/main.py`.
- [x] Pasta `app/models` criada para regras de negocio e calculos. Arquivos: `app/models/dataset.py`, `app/models/identification.py`, `app/models/tuning.py`, `app/models/simulation.py`, `app/models/metrics.py`.
- [x] Pasta `app/views` criada para a interface grafica. Arquivo: `app/views/main_window.py`.
- [x] Pasta `app/controllers` criada para conectar interface e modelos. Arquivo: `app/controllers/main_controller.py`.
- [x] Ponto de entrada criado em `app/main.py`. Arquivo: `app/main.py`.
- [x] Arquivo `app/requirements.txt` criado com as dependencias principais. Arquivo: `app/requirements.txt`.
- [x] Dataset do Grupo 1 incluido na raiz do repositorio. Arquivo: `Dataset_Grupo1_c213 (1).mat`.
- [x] Carregamento de arquivos `.mat` implementado. Arquivo: `app/models/dataset.py`.
- [x] Validacao das variaveis `tiempo`, `entrada` e `salida`. Arquivo: `app/models/dataset.py`.
- [x] Deteccao do instante do degrau. Arquivo: `app/models/dataset.py`.
- [x] Plotagem dos sinais de entrada e saida. Arquivo: `app/controllers/main_controller.py`.
- [x] Comparacao visual entre saida experimental e modelos Smith/Sundaresan. Arquivos: `app/controllers/main_controller.py`, `app/models/identification.py`.
- [x] Identificacao FOPDT pelo metodo de Smith. Arquivo: `app/models/identification.py`.
- [x] Identificacao FOPDT pelo metodo de Sundaresan. Arquivo: `app/models/identification.py`.
- [x] Calculo de EQM para os modelos identificados. Arquivo: `app/models/identification.py`.
- [x] Selecao automatica do modelo com menor EQM. Arquivos: `app/models/identification.py`, `app/controllers/main_controller.py`.
- [x] Interface PyQt5 com abas de Identificacao, Controle PID e Graficos. Arquivo: `app/views/main_window.py`.
- [x] Sintonia PID por CHR com sobresinal. Arquivo: `app/models/tuning.py`.
- [x] Sintonia PID por Cohen-Coon. Arquivo: `app/models/tuning.py`.
- [x] Modo manual para informar `Kp`, `Ti` e `Td`. Arquivos: `app/views/main_window.py`, `app/controllers/main_controller.py`.
- [x] Bloqueio dos campos PID no modo por metodo. Arquivo: `app/views/main_window.py`.
- [x] Botao para limpar parametros no modo manual. Arquivo: `app/views/main_window.py`.
- [x] Campo de SetPoint. Arquivos: `app/views/main_window.py`, `app/controllers/main_controller.py`.
- [x] Simulacao de resposta em malha fechada. Arquivo: `app/models/simulation.py`.
- [x] Uso de aproximacao de Pade para atraso na simulacao. Arquivo: `app/models/simulation.py`.
- [x] Calculo de tempo de subida. Arquivo: `app/models/metrics.py`.
- [x] Calculo de tempo de acomodacao. Arquivo: `app/models/metrics.py`.
- [x] Calculo de overshoot. Arquivo: `app/models/metrics.py`.
- [x] Calculo de erro em regime permanente. Arquivo: `app/models/metrics.py`.
- [x] Exportacao do grafico controlado. Arquivo: `app/controllers/main_controller.py`.
- [x] README do app detalhando requisitos, arquitetura e entregaveis. Arquivo: `app/README.md`.

## Parcial

- [ ] Selecao manual do modelo identificado. Hoje o sistema escolhe automaticamente o menor EQM, mas ainda nao ha combo/lista para o usuario escolher outro modelo.
- [ ] Marcadores de metricas no grafico. As metricas sao calculadas, mas ainda nao aparecem como pontos/anotacoes no grafico.
- [ ] Validacao do modo manual. O sistema converte os valores digitados, mas ainda precisa validar melhor estabilidade, valores nulos, negativos ou comportamento inadequado.
- [ ] Documentacao matematica. O README cita os metodos, mas ainda falta detalhar as equacoes usadas em Smith, Sundaresan, CHR com sobresinal e Cohen-Coon.
- [ ] Analise comparativa dos metodos. O codigo executa CHR e Cohen-Coon, mas ainda falta registrar resultados, graficos e conclusoes.

## Falta Fazer

- [ ] Criar `.gitignore`.
- [ ] Remover `__pycache__` do versionamento.
- [ ] Adicionar prints da IHM no repositorio.
- [ ] Exportar e salvar graficos dos resultados do Grupo 1.
- [ ] Criar pasta para resultados, por exemplo `docs/`, `resultados/` ou `assets/`.
- [ ] Melhorar este README principal com descricao completa do projeto.
- [ ] Incluir instrucoes claras de instalacao e execucao na raiz do repositorio.
- [ ] Permitir escolha manual entre Smith e Sundaresan na interface.
- [ ] Adicionar marcadores no grafico controlado: tempo de subida, tempo de acomodacao, pico/overshoot e SetPoint.
- [ ] Permitir configurar tempo total e quantidade de amostras da simulacao.
- [ ] Melhorar mensagens de erro da interface.
- [ ] Revisar metricas para respostas decrescentes ou SetPoint negativo.
- [ ] Adicionar testes automatizados para carregamento do dataset, identificacao, sintonia PID, simulacao e metricas.
- [ ] Criar secao de resultados com parametros identificados, parametros PID, metricas e comparacao final.
- [ ] Criar secao de limitacoes e melhorias futuras.
- [ ] Preparar apresentacao com demonstracao ao vivo.
- [ ] Garantir commits significativos dos integrantes.

## Prioridade Recomendada

1. Criar `.gitignore` e limpar `__pycache__`.
2. Permitir selecionar manualmente o modelo identificado.
3. Adicionar marcadores de metricas nos graficos.
4. Exportar graficos finais e prints da IHM.
5. Completar documentacao matematica e analise comparativa.
6. Criar testes automatizados.
