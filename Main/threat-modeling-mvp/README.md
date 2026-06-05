# Threat Modeling MVP

MVP em Python para análise automática de diagramas de arquitetura de software usando a metodologia **STRIDE**.

## Visão Geral

A aplicação recebe uma imagem de diagrama de arquitetura, identifica os componentes (usuários, servidores, bancos de dados, APIs, microsserviços, limites de confiança e fluxos de dados) e aplica o STRIDE para gerar um relatório estruturado de ameaças com contramedidas sugeridas.

### Metodologia STRIDE

| Letra | Ameaça | Elemento DFD afetado |
|-------|--------|----------------------|
| **S** | Spoofing (Falsificação de Identidade) | Entidades Externas |
| **T** | Tampering (Adulteração) | Fluxos de Dados, Data Stores |
| **R** | Repudiation (Repúdio) | Processos, Data Stores |
| **I** | Information Disclosure (Vazamento) | Fluxos de Dados, Data Stores |
| **D** | Denial of Service (Negação de Serviço) | Processos, Data Stores |
| **E** | Elevation of Privilege (Elevação de Privilégio) | Processos |

---

## Estrutura do Projeto

```
threat-modeling-mvp/
├── app/
│   ├── core/           # Configurações e settings
│   ├── models/         # Modelos Pydantic / ORM
│   ├── services/       # Lógica de negócio (análise STRIDE, visão, relatórios)
│   ├── routers/        # Endpoints FastAPI
│   ├── utils/          # Helpers gerais
│   └── main.py         # Entry point da aplicação
├── data/
│   ├── raw/            # Imagens enviadas pelos usuários
│   ├── processed/      # Imagens pré-processadas
│   └── annotations/    # Anotações e metadados extraídos
├── models/             # Modelos de ML/visão locais (opcional)
├── reports/            # Relatórios gerados
├── tests/              # Testes unitários e de integração
├── requirements.txt
├── .env.example
└── README.md
```

---

## Instalação

```bash
# 1. Clone o repositório
git clone <repo-url>
cd threat-modeling-mvp

# 2. Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite .env com suas chaves de API
```

## Execução

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse a documentação interativa em: http://localhost:8000/docs

---

## Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `VISION_MODEL_PROVIDER` | Provider do modelo de visão (`openai`, `anthropic`, `google`) | `anthropic` |
| `VISION_MODEL_NAME` | Nome do modelo | `claude-3-5-sonnet-20241022` |
| `DATABASE_URL` | URL do banco de dados | SQLite local |
| `UPLOAD_DIR` | Diretório para uploads | `./data/raw` |

Veja `.env.example` para a lista completa.

---

## Endpoints Principais

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/api/v1/analysis/` | Submete diagrama para análise STRIDE |
| `GET` | `/api/v1/analysis/{id}` | Consulta resultado da análise |
| `GET` | `/api/v1/reports/{id}/pdf` | Download do relatório em PDF |
| `GET` | `/api/v1/reports/{id}/json` | Relatório estruturado em JSON |
| `GET` | `/health` | Health check |

---

## Tecnologias

- **Python 3.10+**
- **FastAPI** — framework web
- **Pillow / OpenCV** — pré-processamento de imagens
- **Anthropic / OpenAI / Google** — modelos de visão
- **SQLAlchemy + Aiosqlite** — persistência
- **ReportLab / WeasyPrint** — geração de PDFs
