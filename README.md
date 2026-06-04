# Agentix Framework Lab Demos

Colecao de 8 projetos Python independentes para comparar frameworks de agentes de IA no contexto Agentix.

## Objetivo

Cada projeto implementa o mesmo cenario didatico:

- dominio: Data/SQL governance
- cenario: `sql-lineage-triage`
- entrada: uma mudanca SQL com impacto potencial em lineage, contratos e promocao
- saida esperada:
  - `lineage`
  - `risks`
  - `recommendation`
  - `next_steps`

Os frameworks incluidos sao:

1. LangChain
2. LangGraph
3. CrewAI
4. Agno
5. SmolAgents
6. Microsoft AutoGen
7. OpenAI Agents SDK
8. PydanticAI

## Estrutura

```text
frameworks/                Projetos independentes por framework
shared/agentix_framework_demos/
  scenario.py              Catalogo, prompt e estruturas comuns
  runtime.py               Runners reais para os 8 frameworks
tests/                     Testes leves do catalogo compartilhado
requirements-common.txt    Dependencias comuns
```

## Rodar um demo

Exemplo com OpenAI Agents SDK:

```bash
cd frameworks/openai-agents
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Com provider compativel OpenAI:

```bash
export OPENAI_API_KEY=...
export OPENAI_MODEL=gpt-4o-mini
python frameworks/langgraph/main.py
```

Com OpenRouter:

```bash
export OPENAI_API_KEY=...
export OPENAI_MODEL=openrouter/auto
export OPENAI_API_BASE=https://openrouter.ai/api/v1
python frameworks/pydanticai/main.py
```

## Comandos uteis

```bash
pytest
python scripts/list_frameworks.py
```

## Observacoes

- Os 8 demos compartilham o mesmo contrato de comparacao para facilitar analise lado a lado.
- O foco aqui e clareza didatica e equivalencia de cenario, nao esconder as diferencas entre frameworks.
- Trate cada pasta em `frameworks/` como um projeto com ambiente proprio. Instalar todos os frameworks no mesmo `.venv` tende a gerar resolucao de dependencias lenta e fragil.
- Algumas dependencias de frameworks mudam rapido. Se um demo exigir ajuste fino de versao, mantenha o README daquele framework como fonte de verdade local.
