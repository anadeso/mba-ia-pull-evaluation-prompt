# 🎯 Desafio de Prompt Engineering - Bug to User Story

Projeto de otimização de prompts para conversão automática de bug reports em User Stories completas e profissionais, atingindo média >= 0.9 em todas as métricas de avaliação.

## 🏆 Status: ✅ APROVADO

**Média geral:** **0.9764** (meta: >= 0.9000)

---

## 📋 Visão Geral

Este projeto implementa e valida um prompt otimizado que transforma bug reports técnicos em User Stories ágeis de alta qualidade, utilizando **6 técnicas avançadas de Prompt Engineering**.

### Características Principais

- ✅ **6 técnicas avançadas** aplicadas e validadas
- ✅ **Média 0.9764** em avaliação de casos críticos
- ✅ **Baixa variabilidade** (desvio padrão: 0.0054)
- ✅ **Alta consistência** entre execuções
- ✅ **Formato estruturado** com Markdown
- ✅ **Critérios testáveis** (Given-When-Then)

---

## 🔬 Técnicas de Prompt Engineering Aplicadas

1. **Role Prompting** - Persona de PM Sênior empático
2. **Emotional Priming** - Ativação de empatia antes da escrita
3. **Chain of Thought** - 6 passos de raciocínio estruturado
4. **Rubric-based Prompting** - 5 dimensões de avaliação explícitas
5. **Few-Shot Learning** - 7 exemplos (4 simples + 3 médios)
6. **Negative Examples** - Contrastes entre boas e más práticas

Ver detalhes completos em [RESULTS.md](RESULTS.md).

---

## 📊 Resultados

### Scores Finais (v4.0)

| Métrica | Score | Status |
|---------|-------|--------|
| F1-Score | **0.9805** | ✅ |
| Clarity | **0.9800** | ✅ |
| Precision | **0.9707** | ✅ |
| Helpfulness | **0.9753** | ✅ |
| Correctness | **0.9756** | ✅ |
| **Média Geral** | **0.9764** | ✅ |

### Evolução

- **v3.1 → v4.0:** +12.5% na média geral
- **F1-Score:** +18.1% (maior melhoria)
- **Correctness:** +14.8%

Ver análise completa em [RESULTS.md](RESULTS.md).

---

## 🚀 Quick Start

### 1. Instalação

```bash
# Criar ambiente
conda create -n prompt-opt python=3.12
conda activate prompt-opt

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configuração

```bash
# Copiar template de configuração
cp .env.example .env

# Editar com suas API keys
# - OPENAI_API_KEY
# - LANGSMITH_API_KEY
```

### 3. Executar Avaliação

```bash
# Avaliação rápida (5 casos críticos x 3 rodadas)
python evaluate_quick.py

# Avaliação completa (10 casos)
python src/evaluate.py

# Diagnóstico focado (comparação linha por linha)
python diagnose_worst_cases.py
```

---

## Estrutura obrigatória do projeto

Faça um fork do repositório base: **[Clique aqui para o template](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt)**

```
desafio-prompt-engineer/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Sua documentação do processo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml       # Prompt inicial (após pull)
│   └── bug_to_user_story_v2.yml # Seu prompt otimizado
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith
│   ├── push_prompts.py       # Push ao LangSmith
│   ├── evaluate.py           # Avaliação automática
│   ├── metrics.py            # 4 métricas implementadas
│   ├── dataset.py            # 15 exemplos de bugs
│   └── utils.py              # Funções auxiliares
│
├── tests/
│   └── test_prompts.py       # Testes de validação
│
```

**O que você vai criar:**

- `prompts/bug_to_user_story_v2.yml` - Seu prompt otimizado
- `tests/test_prompts.py` - Seus testes de validação
- `src/pull_prompt.py` Script de pull do repositório da fullcycle
- `src/push_prompt.py` Script de push para o seu repositório
- `README.md` - Documentação do seu processo de otimização

**O que já vem pronto:**

- Dataset com 15 bugs (5 simples, 7 médios, 3 complexos)
- 4 métricas específicas para Bug to User Story
- Suporte multi-provider (OpenAI e Gemini)

## Repositórios úteis

- [Repositório boilerplate do desafio](https://github.com/devfullcycle/desafio-prompt-engineer/)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## VirtualEnv para Python

Crie e ative um ambiente virtual antes de instalar dependências:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🎯 Exemplo de Uso

### Input (Bug Report)

```
Botão de adicionar ao carrinho não funciona no produto ID 1234.
```

### Output (User Story Gerada)

```markdown
Como um cliente navegando na loja, eu quero adicionar produtos ao meu carrinho 
de compras, para que eu possa continuar comprando e finalizar minha compra depois.

Critérios de Aceitação:
- Dado que estou visualizando um produto
- Quando clico no botão "Adicionar ao Carrinho"
- Então o produto deve ser adicionado ao carrinho
- E devo ver uma confirmação visual
- E o contador do carrinho deve ser atualizado
```

---

## 🔧 Comandos Úteis

| Ação | Comando |
|------|---------|
| Validar estrutura | `pytest tests/test_prompts.py -v` |
| Push para LangSmith | `python src/push_prompts.py` |
| Avaliação completa | `python src/evaluate.py` |
| **Avaliação rápida** | `python evaluate_quick.py` ⚡ |
| **Diagnóstico focado** | `python diagnose_worst_cases.py` 🔬 |
| Todos os testes | `pytest tests/ -v` |

---

## 📚 Documentação

- **[RESULTS.md](RESULTS.md)** - Resultados completos, técnicas e análise detalhada
- **[prompts/bug_to_user_story_v2.yml](prompts/bug_to_user_story_v2.yml)** - Prompt otimizado v4.0
- **[LangSmith Hub](https://smith.langchain.com/prompts/bug_to_user_story_v2/032a9885)** - Prompt público

---

## 💡 Highlights

### O que Torna Este Prompt Especial?

1. **Emotional Priming** - Ativa empatia antes da geração
2. **Chain of Thought** - Raciocínio estruturado em 6 passos
3. **Rubric-based** - Modelo sabe exatamente como será avaliado
4. **Few-Shot Learning** - 7 exemplos cobrindo diferentes complexidades
5. **Negative Examples** - Mostra o que evitar (contrastes)
6. **Anti-Alucinação** - 6 regras explícitas para fidelidade aos dados

### Métricas Chave

- ✅ **98.05%** F1-Score (precisão + completude)
- ✅ **98.00%** Clarity (clareza perfeita em todas rodadas)
- ✅ **0.0054** desvio padrão (alta consistência)
- ✅ **100%** dos casos críticos aprovados

---

## ⚙️ Configuração

### Variáveis de Ambiente (.env)

```bash
# OpenAI (obrigatório)
OPENAI_API_KEY=sk-...

# LangSmith (obrigatório)
LANGSMITH_API_KEY=lsv2_pt_...
LANGCHAIN_PROJECT=prompt-optimization-challenge-resolved

# Configuração de LLM
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
EVAL_MODEL=gpt-4o
```

### Dependências Principais

- `langchain` >= 0.1.0
- `langsmith` >= 0.1.0
- `openai` >= 1.0.0
- `python-dotenv`
- `pyyaml`
- `pytest`

Ver versões exatas em [requirements.txt](requirements.txt).

---

## 📈 Roadmap

### ✅ Concluído

- [x] Implementar 6 técnicas avançadas
- [x] Atingir média >= 0.9
- [x] Validar consistência (múltiplas rodadas)
- [x] Documentar resultados completos
- [x] Criar scripts de diagnóstico


