# datasets/

Este diretório centraliza todos os dados usados no **Threat Modeling MVP** — um sistema que analisa diagramas de arquitetura de software e gera relatórios de Modelagem de Ameaças pela metodologia **STRIDE**.

---

## Estrutura de pastas

```
datasets/
├── raw/                        ← Datasets brutos (download original)
├── data_refined/               ← Datasets relevantes para STRIDE (pós-segregação)
├── data_refused/               ← Datasets descartados (sem relevância para STRIDE)
├── data_refined_small_sample/  ← Amostra de 20% do data_refined (para experimentos rápidos)
├── segregate_datasets.py       ← Script de análise e segregação automática
└── create_small_sample.py      ← Script para (re)gerar a amostra de 20%
```

---

## Descrição detalhada de cada pasta

### `raw/`
Contém os datasets baixados em sua forma **original, sem nenhuma modificação**. Serve como fonte de verdade e permite reprocessar os dados a qualquer momento.

| Subpasta | Origem | Conteúdo |
|---|---|---|
| `arch_diagram_corpus/` | Figshare + OWASP + Threat Dragon | Imagens de padrões arquiteturais, DFDs, modelos de ameaças OWASP e JSONs do Threat Dragon |
| `kaggle_cloud_dataset/` | Kaggle | Imagens de diagramas de infraestrutura AWS/Azure/GCP com anotações XML (bounding boxes de componentes) |
| `PlantUML_Data_bundle/` | PlantUML Benchmark | Diagramas de sequência e atividade gerados sinteticamente com conteúdo aleatório (sem contexto de segurança) |

**Não modifique os arquivos desta pasta.** Ela é somente leitura para fins de rastreabilidade.

---

### `data_refined/`
Datasets **relevantes para a metodologia STRIDE**, movidos automaticamente pelo script `segregate_datasets.py` após análise de conteúdo.

Um dataset é considerado relevante se seus arquivos contêm elementos úteis para STRIDE:
- Entidades externas, processos, data stores e fluxos de dados (DFD)
- Limites de confiança (trust boundaries), VPCs, subnets
- Modelos de ameaças explícitos (Threat Dragon, IriusRisk, OWASP Threat Cookbook)
- Anotações de componentes cloud reais (AWS, Azure, GCP)

| Subpasta | Tipos de arquivo | Uso no projeto |
|---|---|---|
| `arch_diagram_corpus/` | `.png`, `.jpg`, `.svg`, `.json`, `.py`, `.pdf`, `.plantuml` | Treinamento do modelo de visão para detecção de componentes; exemplos de DFDs e Attack Trees |
| `kaggle_cloud_dataset/` | `.png` (diagramas), `.xml` (anotações PASCAL VOC) | Treinamento de object detection para identificar ícones de serviços cloud em diagramas |

**Subpastas de `arch_diagram_corpus`:**

- `figshare_patterns/ArchPatterns/Broker/` — imagens de diagramas com padrão arquitetural Broker (componentes, conectores, fluxos)
- `owasp_cookbook/Attack Tree/` — arquivos `.plantuml` e `.svg` de árvores de ataque OWASP para sistemas reais (IoT, pagamento, SaaS, etc.)
- `owasp_cookbook/Flow Diagram/` — DFDs gerados com Python/Graphviz para sistemas como e-commerce, IoT, jogos online, etc.
- `owasp_cookbook/IriusRisk/` — modelos de ameaças exportados da ferramenta IriusRisk (3-Tier Web App)
- `threat_dragon_models/ThreatDragonModels/` — modelos JSON do OWASP Threat Dragon com ameaças STRIDE mapeadas

---

### `data_refused/`
Datasets **descartados** por não conterem elementos úteis para a metodologia STRIDE.

| Subpasta | Motivo da rejeição |
|---|---|
| `PlantUML_Data_bundle/` | Diagramas UML sintéticos gerados com palavras e frases aleatórias (sem semântica de sistema real). Score STRIDE = −108 na análise. Úteis apenas para benchmarks de geração de diagramas UML, não para análise de ameaças. |

Os arquivos desta pasta **não são usados** pelo pipeline do MVP. São mantidos aqui para auditoria e rastreabilidade.

---

### `data_refined_small_sample/`
Amostra aleatória de **20% dos arquivos** de `data_refined`, com estrutura de subpastas preservada. Gerada com semente fixa (`seed=42`) para reprodutibilidade.

| Métrica | Valor |
|---|---|
| Origem | `data_refined/` |
| Proporção | 20% (seleção aleatória, seed=42) |
| Estrutura | Idêntica à de `data_refined/` |

**Uso:** desenvolvimento rápido, testes unitários, protótipos e experimentos onde usar o dataset completo seria demorado.

Para regenerar esta pasta, execute na raiz de `datasets/`:
```bash
python create_small_sample.py --force
```

---

## Scripts

### `segregate_datasets.py`
Analisa amostras de cada subpasta em `raw/` usando critérios semânticos (word-boundary regex, pontuação STRIDE) e move automaticamente cada dataset para `data_refined/` ou `data_refused/`.

```bash
# Simular sem mover arquivos
python segregate_datasets.py --dry-run

# Executar a segregação
python segregate_datasets.py --seed 42
```

### `create_small_sample.py`
Cria (ou recria) `data_refined_small_sample/` copiando 20% dos arquivos de `data_refined/` com estrutura preservada.

```bash
# Criar amostra (20%, seed=42)
python create_small_sample.py

# Recriar do zero com percentual diferente
python create_small_sample.py --force --pct 10 --seed 0
```

---

## Fluxo de dados

```
raw/                         (dados brutos, imutáveis)
  └─► segregate_datasets.py
        ├─► data_refined/    (relevantes para STRIDE)
        │     └─► create_small_sample.py
        │               └─► data_refined_small_sample/  (20% para dev/testes)
        └─► data_refused/   (descartados)
```

---

## Critérios de relevância STRIDE

Para ser classificado como relevante, um dataset precisa apresentar elementos dos cinco componentes de um Diagrama de Fluxo de Dados (DFD) necessários para aplicar STRIDE:

| Componente DFD | Ameaças STRIDE associadas | Exemplos no dataset |
|---|---|---|
| Entidades Externas | Spoofing, Repudiation | Usuários, sistemas externos, provedores de identidade |
| Processos | Tampering, Elevation of Privilege, DoS | EC2, API Gateway, Logic Apps, microsserviços |
| Data Stores | Tampering, Information Disclosure, Repudiation | RDS, S3, ElastiCache, sistemas de arquivos |
| Fluxos de Dados | Tampering, Information Disclosure | Setas HTTP/HTTPS, chamadas de API |
| Limites de Confiança | Todos | VPC, subnets públicas/privadas, resource groups |
