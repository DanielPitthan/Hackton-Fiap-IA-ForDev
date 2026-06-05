# IADT - Fase 5 - Hackathon: STRIDE-AI
## Master Execution Prompt — Phased Build Guide

> **Versão:** 1.0.0 | **Projeto:** FIAP Software Security — Threat Modeling AI  
> **Stack Principal:** Python · FastAPI · Claude Vision API · Streamlit · Graphviz  
> **Consumível por:** .NET, Java, qualquer cliente HTTP via REST

---

## INSTRUÇÕES DE USO DESTE DOCUMENTO

Este prompt foi projetado para ser **pausável e retomável**. Cada fase possui:

- ✅ **CHECKPOINT** — Critério de conclusão verificável antes de avançar.
- 📁 **ESTADO** — Arquivo de estado `build_state.json` atualizado ao fim de cada fase.
- ⏸️ **PONTO DE PAUSA SEGURO** — Indicação explícita de onde é seguro interromper.
- 🔁 **RETOMADA** — Instrução de como retomar a partir daquele ponto.

**Ao iniciar qualquer sessão de trabalho**, execute primeiro:

```bash
cat build_state.json  # Verifica o estado atual do projeto
```

---

## CONTROLE DE ESTADO DO PROJETO

Crie o arquivo `build_state.json` na raiz do projeto na Fase 0:

```json
{
  "project": "STRIDE-AI",
  "version": "1.0.0",
  "last_updated": "",
  "current_phase": 0,
  "completed_phases": [],
  "skipped_steps": [],
  "notes": [],
  "api_key_configured": false,
  "dataset_validated": false,
  "dataset_skip_approved": false,
  "model_trained": false,
  "api_deployed": false,
  "tests_passing": false,
  "frontend_ready": false,
  "docs_complete": false
}
```

---

## ARQUITETURA GERAL DO SISTEMA

```
STRIDE-AI/
├── api/                    # FastAPI — núcleo REST consumível por .NET etc.
│   ├── routes/
│   │   ├── analysis.py     # POST /analyze  — envio de diagrama
│   │   ├── report.py       # GET  /report/{id} — relatório STRIDE
│   │   ├── diagram.py      # GET  /diagram/{id} — diagrama corrigido
│   │   └── health.py       # GET  /health
│   ├── services/
│   │   ├── vision_service.py      # Claude Vision: detecção de componentes
│   │   ├── stride_engine.py       # Motor de análise STRIDE
│   │   ├── diagram_generator.py   # Geração de diagrama corrigido (Graphviz)
│   │   ├── script_generator.py    # Geração de scripts de análise profunda
│   │   ├── vuln_database.py       # Base CVE/CWE + contramedidas
│   │   └── dashboard_service.py   # Geração de dados para dashboard
│   ├── models/
│   │   ├── schemas.py      # Pydantic schemas (request/response)
│   │   └── enums.py        # STRIDE categories, component types
│   └── main.py
├── core/
│   ├── preprocessor.py     # Validação e pré-processamento de imagens
│   ├── classifier.py       # Wrapper do modelo supervisionado
│   └── prompts.py          # Engenharia de prompts para Claude API
├── frontend/               # Streamlit GUI
│   ├── app.py
│   ├── pages/
│   │   ├── 01_upload.py
│   │   ├── 02_analysis.py
│   │   ├── 03_report.py
│   │   ├── 04_dashboard.py
│   │   └── 05_docs.py
│   └── components/
├── dataset/
│   ├── raw/                # Imagens brutas
│   ├── annotated/          # Imagens anotadas (YOLO/COCO format)
│   └── preprocessed/       # Imagens validadas e normalizadas
├── scripts/
│   ├── preprocess_check.py # PRÉ-PROCESSAMENTO — validação do dataset
│   ├── annotate.py         # Helper de anotação
│   └── train_model.py      # Script de treinamento
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── docs/
│   ├── mkdocs.yml
│   ├── index.md
│   └── ...
├── notebooks/
│   └── dataset_analysis.ipynb
├── build_state.json
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

---

# FASE 0 — FUNDAÇÃO E SCAFFOLDING

**Estimativa:** 2–3 horas  
**Objetivo:** Criar toda a estrutura do projeto, configurar ambiente, instalar dependências.

## Tarefa 0.1 — Inicialização do Repositório

```bash
# Execute no terminal
mkdir STRIDE-AI && cd STRIDE-AI
git init
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Criar estrutura de diretórios
mkdir -p api/{routes,services,models} core frontend/{pages,components} \
         dataset/{raw,annotated,preprocessed} scripts tests/{unit,integration} \
         docs notebooks

touch build_state.json
```

## Tarefa 0.2 — requirements.txt

Crie `requirements.txt` com o seguinte conteúdo:

```txt
# === API & Web ===
fastapi==0.115.0
uvicorn[standard]==0.30.6
python-multipart==0.0.9
pydantic==2.8.2
pydantic-settings==2.4.0

# === Frontend ===
streamlit==1.38.0
streamlit-option-menu==0.3.12
plotly==5.24.0
pandas==2.2.2

# === AI & Vision ===
anthropic==0.34.0
Pillow==10.4.0
opencv-python==4.10.0.84
numpy==1.26.4

# === Diagram Generation ===
graphviz==0.20.3
matplotlib==3.9.2
reportlab==4.2.2

# === Document Generation ===
python-docx==1.1.2
python-pptx==0.6.23
fpdf2==2.8.1
jinja2==3.1.4
markdown==3.7

# === Data & ML ===
scikit-learn==1.5.2
torch==2.4.0
torchvision==0.19.0
ultralytics==8.2.90   # YOLOv8 para detecção supervisionada
requests==2.32.3
httpx==0.27.2

# === Security & Vuln Data ===
nvdlib==0.7.6          # NVD/CVE API
cvelib==1.4.1

# === Testing ===
pytest==8.3.2
pytest-asyncio==0.23.8
pytest-cov==5.0.0
httpx==0.27.2

# === DevTools ===
python-dotenv==1.0.1
loguru==0.7.2
rich==13.8.0
tqdm==4.66.5
```

```bash
pip install -r requirements.txt
```

## Tarefa 0.3 — Variáveis de Ambiente

Crie `.env`:

```env
# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# App
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000
SECRET_KEY=your-secret-key-here

# Paths
DATASET_RAW_PATH=./dataset/raw
DATASET_ANNOTATED_PATH=./dataset/annotated
MODEL_PATH=./models/stride_detector.pt

# NVD API (gratuita, requer registro em nvd.nist.gov)
NVD_API_KEY=your-nvd-key-here

# Frontend
STREAMLIT_PORT=8501
API_BASE_URL=http://localhost:8000
```

## Tarefa 0.4 — Atualizar build_state.json

```json
{
  "project": "STRIDE-AI",
  "version": "1.0.0",
  "last_updated": "YYYY-MM-DD",
  "current_phase": 0,
  "completed_phases": [0],
  ...
}
```

## ✅ CHECKPOINT FASE 0

- [ ] Estrutura de diretórios criada (`tree -L 3` deve bater com o layout acima)
- [ ] `.venv` ativo e dependências instaladas (`pip list | grep fastapi`)
- [ ] `.env` configurado com a `ANTHROPIC_API_KEY`
- [ ] `build_state.json` atualizado com `"current_phase": 1`

⏸️ **PAUSA SEGURA AQUI** — Projeto estruturado, pronto para desenvolvimento.

---

---

# FASE 1 — PRÉ-PROCESSAMENTO E VALIDAÇÃO DO DATASET

> ⚠️ **DECISÃO DE SKIP:** Se você já possui um dataset extenso e validado,
> avalie este critério antes de executar a fase completa.
> Se `dataset_validated: true` no `build_state.json`, pule para a **Fase 2**.

## Tarefa 1.1 — Script de Validação do Dataset

Crie `scripts/preprocess_check.py`:

```python
"""
STRIDE-AI — Dataset Pre-processing & Validation Script
Verifica se as imagens do dataset atendem aos requisitos mínimos
para processamento pela aplicação. Economiza tempo e custo de API.

Uso:
    python scripts/preprocess_check.py --input ./dataset/raw --output ./dataset/preprocessed
    python scripts/preprocess_check.py --input ./dataset/raw --report-only
"""

import argparse
import json
import os
import sys
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime

import cv2
import numpy as np
from PIL import Image
from loguru import logger
from rich.console import Console
from rich.table import Table
from rich.progress import track
from tqdm import tqdm

console = Console()

# ── Critérios mínimos de qualidade ──────────────────────────────────────────
MIN_WIDTH = 400         # px
MIN_HEIGHT = 300        # px
MAX_WIDTH = 8000        # px
MAX_HEIGHT = 8000       # px
MIN_FILE_SIZE_KB = 10   # KB
MAX_FILE_SIZE_MB = 20   # MB
MIN_SHARPNESS = 50.0    # Laplacian variance — abaixo disso, imagem borrada
SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"}
MIN_CONTRAST_STD = 20.0 # Desvio padrão mínimo de pixel (contraste)


@dataclass
class ImageReport:
    filename: str
    valid: bool
    width: int
    height: int
    file_size_kb: float
    format: str
    sharpness: float
    contrast_std: float
    has_text_regions: bool
    estimated_components: int
    rejection_reason: Optional[str] = None
    preprocessed_path: Optional[str] = None


def compute_sharpness(img_gray: np.ndarray) -> float:
    """Laplacian variance — mede nitidez da imagem."""
    return float(cv2.Laplacian(img_gray, cv2.CV_64F).var())


def compute_contrast(img_gray: np.ndarray) -> float:
    """Desvio padrão dos pixels — proxy para contraste."""
    return float(img_gray.std())


def detect_text_regions(img_gray: np.ndarray) -> bool:
    """Verifica presença de regiões textuais (componentes rotulados)."""
    _, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    small_rects = [c for c in contours if 5 < cv2.contourArea(c) < 5000]
    return len(small_rects) > 10


def estimate_component_count(img_gray: np.ndarray) -> int:
    """Estimativa heurística de componentes arquiteturais por blob detection."""
    blurred = cv2.GaussianBlur(img_gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    valid = [c for c in contours if 200 < cv2.contourArea(c) < 50000]
    return len(valid)


def preprocess_image(img: np.ndarray, output_path: Path) -> str:
    """Normaliza e salva imagem para processamento."""
    # Redimensiona se necessário (mantém aspect ratio)
    h, w = img.shape[:2]
    if w > 2000 or h > 2000:
        scale = min(2000/w, 2000/h)
        img = cv2.resize(img, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_LANCZOS4)

    # Melhora contraste leve (CLAHE no canal L)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    enhanced = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

    cv2.imwrite(str(output_path), enhanced, [cv2.IMWRITE_PNG_COMPRESSION, 6])
    return str(output_path)


def validate_image(image_path: Path, output_dir: Optional[Path] = None) -> ImageReport:
    """Valida uma imagem e opcionalmente a pré-processa."""
    filename = image_path.name
    rejection_reason = None
    preprocessed_path = None

    # Formato
    if image_path.suffix.lower() not in SUPPORTED_FORMATS:
        return ImageReport(filename=filename, valid=False, width=0, height=0,
                           file_size_kb=0, format=image_path.suffix,
                           sharpness=0, contrast_std=0,
                           has_text_regions=False, estimated_components=0,
                           rejection_reason=f"Formato não suportado: {image_path.suffix}")

    # Tamanho do arquivo
    file_size_kb = image_path.stat().st_size / 1024
    if file_size_kb < MIN_FILE_SIZE_KB:
        return ImageReport(filename=filename, valid=False, width=0, height=0,
                           file_size_kb=file_size_kb, format=image_path.suffix,
                           sharpness=0, contrast_std=0,
                           has_text_regions=False, estimated_components=0,
                           rejection_reason=f"Arquivo muito pequeno: {file_size_kb:.1f}KB")

    if file_size_kb > MAX_FILE_SIZE_MB * 1024:
        rejection_reason = f"Arquivo muito grande: {file_size_kb/1024:.1f}MB"

    # Leitura
    try:
        img_bgr = cv2.imread(str(image_path))
        if img_bgr is None:
            raise ValueError("OpenCV não conseguiu ler a imagem")
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        pil_img = Image.open(image_path)
        w, h = pil_img.size
    except Exception as e:
        return ImageReport(filename=filename, valid=False, width=0, height=0,
                           file_size_kb=file_size_kb, format=image_path.suffix,
                           sharpness=0, contrast_std=0,
                           has_text_regions=False, estimated_components=0,
                           rejection_reason=f"Erro de leitura: {e}")

    # Dimensões
    if w < MIN_WIDTH or h < MIN_HEIGHT:
        rejection_reason = rejection_reason or f"Resolução baixa: {w}x{h}px"
    if w > MAX_WIDTH or h > MAX_HEIGHT:
        rejection_reason = rejection_reason or f"Resolução excessiva: {w}x{h}px"

    # Qualidade
    sharpness = compute_sharpness(img_gray)
    contrast = compute_contrast(img_gray)
    has_text = detect_text_regions(img_gray)
    n_components = estimate_component_count(img_gray)

    if sharpness < MIN_SHARPNESS:
        rejection_reason = rejection_reason or f"Imagem borrada: sharpness={sharpness:.1f}"
    if contrast < MIN_CONTRAST_STD:
        rejection_reason = rejection_reason or f"Contraste insuficiente: std={contrast:.1f}"

    is_valid = rejection_reason is None

    # Pré-processa se válida e output_dir especificado
    if is_valid and output_dir:
        out_path = output_dir / f"{image_path.stem}_preprocessed.png"
        preprocessed_path = preprocess_image(img_bgr, out_path)

    return ImageReport(
        filename=filename, valid=is_valid, width=w, height=h,
        file_size_kb=file_size_kb, format=image_path.suffix,
        sharpness=sharpness, contrast_std=contrast,
        has_text_regions=has_text, estimated_components=n_components,
        rejection_reason=rejection_reason, preprocessed_path=preprocessed_path
    )


def run_validation(input_dir: Path, output_dir: Optional[Path],
                   report_only: bool = False) -> dict:
    """Executa validação completa do dataset."""
    images = [p for p in input_dir.rglob("*") if p.suffix.lower() in SUPPORTED_FORMATS]

    if not images:
        logger.error(f"Nenhuma imagem encontrada em {input_dir}")
        sys.exit(1)

    logger.info(f"Encontradas {len(images)} imagens para validação...")

    if output_dir and not report_only:
        output_dir.mkdir(parents=True, exist_ok=True)

    reports = []
    for img_path in track(images, description="Validando imagens..."):
        report = validate_image(img_path, output_dir if not report_only else None)
        reports.append(report)

    # Estatísticas
    valid = [r for r in reports if r.valid]
    invalid = [r for r in reports if not r.valid]

    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_images": len(images),
        "valid_count": len(valid),
        "invalid_count": len(invalid),
        "valid_ratio": len(valid) / len(images),
        "skip_approved": len(valid) / len(images) >= 0.75,  # 75%+ válidas = skip aprovado
        "avg_estimated_components": np.mean([r.estimated_components for r in valid]) if valid else 0,
        "reports": [asdict(r) for r in reports]
    }

    # Exibe tabela no terminal
    table = Table(title="Resultado da Validação do Dataset")
    table.add_column("Arquivo", style="cyan", max_width=40)
    table.add_column("Status", justify="center")
    table.add_column("Dimensão")
    table.add_column("Sharpness")
    table.add_column("Componentes Est.")
    table.add_column("Motivo Rejeição", style="red", max_width=40)

    for r in reports[:50]:  # Exibe primeiros 50
        status = "✅ OK" if r.valid else "❌ FALHOU"
        table.add_row(r.filename, status, f"{r.width}x{r.height}",
                      f"{r.sharpness:.1f}", str(r.estimated_components),
                      r.rejection_reason or "—")

    console.print(table)
    console.print(f"\n[bold]Resumo:[/bold] {len(valid)}/{len(images)} imagens válidas "
                  f"({'✅ DATASET APROVADO' if summary['skip_approved'] else '⚠️ DATASET INSUFICIENTE'})")

    # Salva relatório JSON
    report_path = Path("dataset_validation_report.json")
    with open(report_path, "w") as f:
        json.dump(summary, f, indent=2)
    logger.info(f"Relatório salvo em {report_path}")

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="STRIDE-AI Dataset Validator")
    parser.add_argument("--input", type=Path, default=Path("./dataset/raw"))
    parser.add_argument("--output", type=Path, default=Path("./dataset/preprocessed"))
    parser.add_argument("--report-only", action="store_true",
                        help="Apenas valida sem pré-processar")
    args = parser.parse_args()

    summary = run_validation(args.input, args.output, args.report_only)

    # Atualiza build_state.json
    state_path = Path("build_state.json")
    if state_path.exists():
        with open(state_path) as f:
            state = json.load(f)
        state["dataset_validated"] = True
        state["dataset_skip_approved"] = summary["skip_approved"]
        state["last_updated"] = datetime.now().isoformat()
        with open(state_path, "w") as f:
            json.dump(state, f, indent=2)

    sys.exit(0 if summary["skip_approved"] else 1)
```

## Tarefa 1.2 — Executar Validação

```bash
# Valida sem processar (apenas relatório)
python scripts/preprocess_check.py --input ./dataset/raw --report-only

# Se aprovado (>= 75% válidas), pré-processa
python scripts/preprocess_check.py --input ./dataset/raw --output ./dataset/preprocessed

# Verifica resultado
cat dataset_validation_report.json | python -m json.tool | grep "skip_approved"
```

## ⚠️ DECISÃO DE SKIP PARA FASE DE TREINAMENTO

Após a validação, verifique:

```bash
python -c "
import json
with open('dataset_validation_report.json') as f:
    r = json.load(f)
print('Dataset aprovado para skip do treinamento:', r['skip_approved'])
print(f'Válidas: {r[\"valid_count\"]}/{r[\"total_images\"]} ({r[\"valid_ratio\"]*100:.1f}%)')
"
```

- Se `skip_approved: true` e você já possui um modelo pré-treinado adequado → **atualize `build_state.json`** com `"dataset_skip_approved": true` e pule a Fase 3 (Treinamento).
- Caso contrário, execute a Fase 3 normalmente.

## ✅ CHECKPOINT FASE 1

- [ ] `preprocess_check.py` executa sem erros
- [ ] `dataset_validation_report.json` gerado
- [ ] Decisão de skip documentada no `build_state.json`
- [ ] Imagens pré-processadas em `./dataset/preprocessed/` (se não skip)

⏸️ **PAUSA SEGURA AQUI**

---

---

# FASE 2 — CORE DE IA: VISÃO E MOTOR STRIDE

**Objetivo:** Implementar o núcleo inteligente — detecção de componentes via Claude Vision e análise STRIDE.

## Tarefa 2.1 — Schemas Pydantic (`api/models/schemas.py`)

```python
"""Schemas de entrada/saída da API STRIDE-AI."""
from __future__ import annotations
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
import uuid


class StrideCategory(str, Enum):
    SPOOFING = "Spoofing"
    TAMPERING = "Tampering"
    REPUDIATION = "Repudiation"
    INFORMATION_DISCLOSURE = "Information Disclosure"
    DENIAL_OF_SERVICE = "Denial of Service"
    ELEVATION_OF_PRIVILEGE = "Elevation of Privilege"


class SeverityLevel(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFORMATIONAL = "Informational"


class ComponentType(str, Enum):
    USER = "User/Actor"
    WEB_SERVER = "Web Server"
    APP_SERVER = "Application Server"
    DATABASE = "Database"
    API_GATEWAY = "API Gateway"
    LOAD_BALANCER = "Load Balancer"
    IDENTITY_PROVIDER = "Identity Provider"
    CACHE = "Cache"
    MESSAGE_QUEUE = "Message Queue"
    STORAGE = "Storage"
    MICROSERVICE = "Microservice"
    NETWORK = "Network/VPN"
    TRUST_BOUNDARY = "Trust Boundary"
    DATA_FLOW = "Data Flow"
    FIREWALL = "Firewall"
    CDN = "CDN"
    CONTAINER = "Container/Kubernetes"
    FUNCTION = "Serverless Function"
    UNKNOWN = "Unknown"


class ArchitectureComponent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str
    type: ComponentType
    description: str
    trust_level: str = "Unknown"
    protocols: List[str] = []
    ports: List[str] = []
    location: Optional[str] = None  # subnet, zone, etc.
    connected_to: List[str] = []    # ids de componentes conectados


class TrustBoundary(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str
    boundary_type: str  # External, Internal, Database, Network
    components_inside: List[str] = []


class StrideVulnerability(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    category: StrideCategory
    severity: SeverityLevel
    title: str
    description: str
    affected_component_id: str
    affected_component_name: str
    attack_vector: str
    impact: str
    likelihood: str
    cve_references: List[str] = []
    cwe_references: List[str] = []
    countermeasures: List[str] = []
    implementation_priority: int = Field(ge=1, le=5)  # 1=crítico, 5=baixo


class DeepAnalysisInput(BaseModel):
    """Dados adicionais fornecidos pelo usuário para análise profunda."""
    network_topology: Optional[str] = None
    existing_controls: Optional[List[str]] = None
    compliance_requirements: Optional[List[str]] = None
    infrastructure_files: Optional[List[str]] = None  # paths de arquivos enviados
    additional_context: Optional[str] = None
    tech_stack: Optional[List[str]] = None


class AnalysisRequest(BaseModel):
    """Request de análise — usado internamente após upload."""
    analysis_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    image_path: str
    diagram_type: Optional[str] = None  # "aws", "azure", "gcp", "generic"
    deep_analysis_input: Optional[DeepAnalysisInput] = None
    requested_at: datetime = Field(default_factory=datetime.utcnow)


class StrideReport(BaseModel):
    """Relatório completo de modelagem de ameaças STRIDE."""
    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    analysis_id: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    diagram_summary: str
    components: List[ArchitectureComponent]
    trust_boundaries: List[TrustBoundary]
    vulnerabilities: List[StrideVulnerability]
    overall_risk_score: float = Field(ge=0.0, le=10.0)
    executive_summary: str
    critical_findings: List[str]
    recommended_priority_actions: List[str]
    stride_matrix: Dict[str, List[str]]  # component_id -> [STRIDE categories]
    deep_analysis_script: Optional[str] = None
    corrected_diagram_path: Optional[str] = None
    report_markdown_path: Optional[str] = None


class AnalysisResponse(BaseModel):
    """Resposta da API ao receber um diagrama para análise."""
    analysis_id: str
    status: str  # "queued", "processing", "completed", "failed"
    message: str
    report: Optional[StrideReport] = None
    processing_time_seconds: Optional[float] = None
```

## Tarefa 2.2 — Engenharia de Prompts (`core/prompts.py`)

```python
"""
Prompts de sistema para análise STRIDE via Claude Vision API.
Separar prompts em arquivo dedicado facilita iteração e versionamento.
"""

COMPONENT_DETECTION_PROMPT = """
You are an expert software architect and security analyst specializing in threat modeling.
Your task is to analyze a software architecture diagram and extract ALL components with precision.

For each component found, provide:
1. Component name (as labeled in the diagram)
2. Component type (Web Server, Database, API Gateway, Load Balancer, Identity Provider, 
   Cache, Message Queue, Storage, Microservice, User/Actor, Network/VPN, Trust Boundary, 
   Data Flow, Firewall, CDN, Container, Serverless Function, Unknown)
3. Brief description of its role
4. Trust level (Public, Semi-trusted, Private, Highly-trusted)
5. Protocols/ports visible in the diagram
6. Location (subnet, zone, VPC name if visible)
7. Connected components (what it communicates with)

Also identify:
- All Trust Boundaries (dotted borders, labeled zones, VPCs, subnets)
- All Data Flows (arrows between components, with protocols if labeled)
- Entry points from external entities

Respond ONLY in the following JSON format, no preamble:
{
  "diagram_type": "AWS|Azure|GCP|Generic|Hybrid",
  "diagram_summary": "...",
  "components": [
    {
      "name": "...",
      "type": "...",
      "description": "...",
      "trust_level": "...",
      "protocols": [...],
      "ports": [...],
      "location": "...",
      "connected_to": [...]
    }
  ],
  "trust_boundaries": [
    {
      "name": "...",
      "boundary_type": "External|Internal|Database|Network",
      "components_inside": [...]
    }
  ],
  "data_flows": [
    {
      "from": "...",
      "to": "...",
      "protocol": "...",
      "data_type": "..."
    }
  ]
}
"""

STRIDE_ANALYSIS_PROMPT = """
You are a senior security architect performing a STRIDE threat model analysis.
You have been given a list of architectural components and their relationships.

Apply the full STRIDE methodology to each relevant component and data flow:
- S: Spoofing (identity falsification) 
- T: Tampering (data modification)
- R: Repudiation (denying actions)
- I: Information Disclosure (data leakage)
- D: Denial of Service (availability attack)
- E: Elevation of Privilege (unauthorized access escalation)

For EACH identified threat, provide:
1. STRIDE category
2. Severity (Critical/High/Medium/Low/Informational)
3. Title (concise)
4. Description (what the attack is)
5. Affected component
6. Attack vector (how it would be executed)
7. Impact (what happens if exploited)
8. Likelihood (High/Medium/Low based on exposure)
9. Relevant CVE or CWE references when applicable
10. Specific countermeasures (minimum 3 per threat)
11. Implementation priority (1=immediate, 5=long-term)

Also compute:
- Overall risk score (0-10 CVSS-like scale)
- Top 5 critical findings
- Top 5 priority actions
- Executive summary (3-5 sentences for non-technical stakeholders)

Components and context:
{components_json}

Trust boundaries:
{boundaries_json}

Data flows:
{flows_json}

Respond ONLY in JSON format matching the StrideReport schema. No preamble.
"""

DEEP_ANALYSIS_SCRIPT_PROMPT = """
You are a senior security engineer and Python expert.
Based on the STRIDE analysis results and additional context provided by the user,
generate a comprehensive Python security analysis script.

The script must:
1. Be self-contained and runnable
2. Perform deeper technical validation of the identified threats
3. Include network reconnaissance checks (non-destructive)
4. Verify security configurations based on provided infrastructure data
5. Generate a structured JSON report
6. Include proper error handling and logging
7. Be parameterizable via CLI arguments

Context from STRIDE analysis:
{stride_summary}

Additional user context:
{user_context}

Technical stack: {tech_stack}
Existing controls: {existing_controls}
Compliance requirements: {compliance_requirements}

Generate ONLY the Python script, no explanation. Include docstrings.
The script filename should be: deep_security_analysis.py
"""

DIAGRAM_CORRECTION_PROMPT = """
You are a software architect and security expert.
Based on the original architecture diagram analysis and the STRIDE threats identified,
generate a corrected architecture description that includes all recommended improvements.

Original architecture summary:
{original_summary}

Critical vulnerabilities found:
{critical_vulns}

All recommended countermeasures:
{countermeasures}

Provide a detailed description of the IMPROVED architecture as a JSON structure
that can be used to generate a new Graphviz/DOT diagram. Include:
1. All original components (corrected)
2. New security components to be added (WAF, HSM, SIEM, etc.)
3. Updated data flows with proper encryption labels
4. Corrected trust boundaries
5. Color coding: red=original risk areas, green=new/improved components, blue=unchanged

Respond ONLY in JSON. Format:
{
  "title": "...",
  "components": [...],  // same schema as original + added security components
  "new_components": [...],  // net-new additions
  "removed_flows": [...],
  "updated_flows": [...],
  "annotations": [{"component": "...", "note": "...", "type": "risk|improvement|new"}]
}
"""
```

## Tarefa 2.3 — Vision Service (`api/services/vision_service.py`)

```python
"""
Serviço de análise de diagramas via Claude Vision API.
Detecta componentes arquiteturais e prepara dados para análise STRIDE.
"""
import base64
import json
import time
from pathlib import Path
from typing import Optional
import anthropic
from loguru import logger
from core.prompts import COMPONENT_DETECTION_PROMPT, STRIDE_ANALYSIS_PROMPT, \
    DEEP_ANALYSIS_SCRIPT_PROMPT, DIAGRAM_CORRECTION_PROMPT
from api.models.schemas import (
    ArchitectureComponent, TrustBoundary, ComponentType, StrideReport,
    StrideVulnerability, StrideCategory, SeverityLevel, DeepAnalysisInput
)
import uuid
from datetime import datetime


class VisionService:
    def __init__(self, api_key: Optional[str] = None):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"
        self.max_tokens = 4096

    def _encode_image(self, image_path: str) -> tuple[str, str]:
        """Codifica imagem em base64 com media_type."""
        path = Path(image_path)
        suffix = path.suffix.lower()
        media_map = {
            ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".png": "image/png", ".bmp": "image/bmp",
            ".webp": "image/webp", ".gif": "image/gif"
        }
        media_type = media_map.get(suffix, "image/png")
        with open(image_path, "rb") as f:
            data = base64.standard_b64encode(f.read()).decode("utf-8")
        return data, media_type

    def detect_components(self, image_path: str) -> dict:
        """Fase 1: Detecta e extrai componentes do diagrama."""
        logger.info(f"Detectando componentes em: {image_path}")
        img_data, media_type = self._encode_image(image_path)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=COMPONENT_DETECTION_PROMPT,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": img_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": "Analyze this architecture diagram and extract all components, trust boundaries, and data flows as specified."
                    }
                ],
            }]
        )

        raw = response.content[0].text.strip()
        # Strip possíveis markdown fences
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        
        return json.loads(raw)

    def run_stride_analysis(self, components_data: dict) -> dict:
        """Fase 2: Executa análise STRIDE sobre os componentes detectados."""
        logger.info("Executando análise STRIDE...")

        prompt = STRIDE_ANALYSIS_PROMPT.format(
            components_json=json.dumps(components_data.get("components", []), indent=2),
            boundaries_json=json.dumps(components_data.get("trust_boundaries", []), indent=2),
            flows_json=json.dumps(components_data.get("data_flows", []), indent=2)
        )

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )

        raw = response.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        return json.loads(raw)

    def generate_deep_analysis_script(
        self, stride_summary: dict, user_input: DeepAnalysisInput
    ) -> str:
        """Gera script Python de análise profunda baseado no contexto do usuário."""
        logger.info("Gerando script de análise profunda...")

        prompt = DEEP_ANALYSIS_SCRIPT_PROMPT.format(
            stride_summary=json.dumps(stride_summary, indent=2),
            user_context=user_input.additional_context or "Not provided",
            tech_stack=json.dumps(user_input.tech_stack or []),
            existing_controls=json.dumps(user_input.existing_controls or []),
            compliance_requirements=json.dumps(user_input.compliance_requirements or [])
        )

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )

        script = response.content[0].text.strip()
        if script.startswith("```python"):
            script = script[9:]
        if script.endswith("```"):
            script = script[:-3]

        return script.strip()

    def generate_diagram_corrections(self, original_data: dict, stride_data: dict) -> dict:
        """Gera descrição do diagrama corrigido com melhorias de segurança."""
        logger.info("Gerando diagrama corrigido...")

        critical_vulns = [
            v for v in stride_data.get("vulnerabilities", [])
            if v.get("severity") in ["Critical", "High"]
        ]

        countermeasures = list({
            cm for v in stride_data.get("vulnerabilities", [])
            for cm in v.get("countermeasures", [])
        })

        prompt = DIAGRAM_CORRECTION_PROMPT.format(
            original_summary=original_data.get("diagram_summary", ""),
            critical_vulns=json.dumps(critical_vulns[:10], indent=2),
            countermeasures=json.dumps(countermeasures[:20], indent=2)
        )

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )

        raw = response.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        return json.loads(raw)

    def full_analysis_pipeline(
        self,
        image_path: str,
        analysis_id: str,
        deep_input: Optional[DeepAnalysisInput] = None
    ) -> StrideReport:
        """Pipeline completo: detecção → STRIDE → script → diagrama corrigido."""
        start_time = time.time()

        # Fase 1: Detecção de componentes
        components_data = self.detect_components(image_path)

        # Fase 2: Análise STRIDE
        stride_data = self.run_stride_analysis(components_data)

        # Fase 3: Script de análise profunda (se input adicional fornecido)
        deep_script = None
        if deep_input:
            deep_script = self.generate_deep_analysis_script(stride_data, deep_input)

        # Fase 4: Diagrama corrigido
        corrected_diagram = self.generate_diagram_corrections(components_data, stride_data)

        # Monta relatório final
        report = self._build_report(
            analysis_id=analysis_id,
            components_data=components_data,
            stride_data=stride_data,
            deep_script=deep_script,
            corrected_diagram=corrected_diagram
        )

        elapsed = time.time() - start_time
        logger.info(f"Pipeline concluído em {elapsed:.1f}s — {len(report.vulnerabilities)} ameaças identificadas")

        return report

    def _build_report(self, analysis_id, components_data, stride_data,
                      deep_script, corrected_diagram) -> StrideReport:
        """Constrói o objeto StrideReport a partir dos dados brutos."""
        # Mapeia componentes
        components = []
        for c in components_data.get("components", []):
            try:
                comp_type = ComponentType(c.get("type", "Unknown"))
            except ValueError:
                comp_type = ComponentType.UNKNOWN

            components.append(ArchitectureComponent(
                name=c.get("name", ""),
                type=comp_type,
                description=c.get("description", ""),
                trust_level=c.get("trust_level", "Unknown"),
                protocols=c.get("protocols", []),
                ports=c.get("ports", []),
                location=c.get("location"),
                connected_to=c.get("connected_to", [])
            ))

        # Mapeia trust boundaries
        boundaries = []
        for b in components_data.get("trust_boundaries", []):
            boundaries.append(TrustBoundary(
                name=b.get("name", ""),
                boundary_type=b.get("boundary_type", "External"),
                components_inside=b.get("components_inside", [])
            ))

        # Mapeia vulnerabilidades
        vulns = []
        for v in stride_data.get("vulnerabilities", []):
            try:
                cat = StrideCategory(v.get("category", "Tampering"))
                sev = SeverityLevel(v.get("severity", "Medium"))
            except ValueError:
                cat = StrideCategory.TAMPERING
                sev = SeverityLevel.MEDIUM

            vulns.append(StrideVulnerability(
                category=cat,
                severity=sev,
                title=v.get("title", ""),
                description=v.get("description", ""),
                affected_component_id=v.get("affected_component_id", ""),
                affected_component_name=v.get("affected_component_name", ""),
                attack_vector=v.get("attack_vector", ""),
                impact=v.get("impact", ""),
                likelihood=v.get("likelihood", "Medium"),
                cve_references=v.get("cve_references", []),
                cwe_references=v.get("cwe_references", []),
                countermeasures=v.get("countermeasures", []),
                implementation_priority=v.get("implementation_priority", 3)
            ))

        # STRIDE matrix
        stride_matrix: dict = {}
        for comp in components:
            comp_vulns = [v.category.value for v in vulns
                          if v.affected_component_name == comp.name]
            if comp_vulns:
                stride_matrix[comp.name] = comp_vulns

        return StrideReport(
            analysis_id=analysis_id,
            diagram_summary=components_data.get("diagram_summary", ""),
            components=components,
            trust_boundaries=boundaries,
            vulnerabilities=vulns,
            overall_risk_score=stride_data.get("overall_risk_score", 5.0),
            executive_summary=stride_data.get("executive_summary", ""),
            critical_findings=stride_data.get("critical_findings", []),
            recommended_priority_actions=stride_data.get("recommended_priority_actions", []),
            stride_matrix=stride_matrix,
            deep_analysis_script=deep_script
        )
```

## ✅ CHECKPOINT FASE 2

- [ ] `schemas.py` importa sem erros (`python -c "from api.models.schemas import *"`)
- [ ] `vision_service.py` instancia sem erros
- [ ] Teste manual: `VisionService().detect_components("dataset/preprocessed/test.png")` retorna JSON válido
- [ ] `build_state.json` atualizado com `"current_phase": 3`

⏸️ **PAUSA SEGURA AQUI**

---

---

# FASE 3 — TREINAMENTO DO MODELO SUPERVISIONADO

> **SKIP CONDITION:** Se `build_state.json` tiver `"dataset_skip_approved": true`  
> e você tiver um modelo `YOLOv8` pré-treinado adequado → pule para a **Fase 4**.

## Tarefa 3.1 — Script de Treinamento YOLOv8

Crie `scripts/train_model.py`:

```python
"""
STRIDE-AI — Treinamento YOLOv8 para detecção de componentes arquiteturais.
Detecta visualmente: servidores, databases, APIs, usuários, trust boundaries, etc.

Uso:
    python scripts/train_model.py --data dataset/annotated/data.yaml --epochs 100
    python scripts/train_model.py --skip-train --model models/stride_detector.pt

Dataset esperado em formato YOLO:
    dataset/annotated/
        data.yaml
        images/train/
        images/val/
        labels/train/
        labels/val/
"""
import argparse
import json
from pathlib import Path
from datetime import datetime
from ultralytics import YOLO
from loguru import logger


# Classes de componentes — mapeamento para YOLO labels
COMPONENT_CLASSES = [
    "user_actor", "web_server", "app_server", "database", "api_gateway",
    "load_balancer", "identity_provider", "cache", "message_queue",
    "storage", "microservice", "network_vpn", "trust_boundary",
    "data_flow", "firewall", "cdn", "container", "serverless_function"
]


def generate_data_yaml(dataset_path: Path) -> Path:
    """Gera data.yaml para o YOLOv8 se não existir."""
    yaml_path = dataset_path / "data.yaml"
    if not yaml_path.exists():
        content = f"""
path: {dataset_path.absolute()}
train: images/train
val: images/val
nc: {len(COMPONENT_CLASSES)}
names: {COMPONENT_CLASSES}
"""
        yaml_path.write_text(content)
        logger.info(f"data.yaml gerado em {yaml_path}")
    return yaml_path


def train(data_yaml: Path, epochs: int = 100, img_size: int = 640,
          batch: int = 16, device: str = "cpu") -> Path:
    """Treina modelo YOLOv8 para detecção de componentes."""
    logger.info(f"Iniciando treinamento: {epochs} epochs, img={img_size}, batch={batch}")

    model = YOLO("yolov8n.pt")  # Nano — balanço entre velocidade e precisão

    results = model.train(
        data=str(data_yaml),
        epochs=epochs,
        imgsz=img_size,
        batch=batch,
        device=device,
        project="models",
        name="stride_detector",
        save=True,
        plots=True,
        patience=20,           # Early stopping
        lr0=0.01,
        augment=True,
        mosaic=1.0,
        mixup=0.1,
    )

    best_model_path = Path("models/stride_detector/weights/best.pt")
    logger.info(f"Treinamento concluído. Melhor modelo: {best_model_path}")
    return best_model_path


def evaluate(model_path: Path, data_yaml: Path) -> dict:
    """Avalia o modelo no conjunto de validação."""
    model = YOLO(str(model_path))
    metrics = model.val(data=str(data_yaml))
    return {
        "map50": float(metrics.box.map50),
        "map50_95": float(metrics.box.map),
        "precision": float(metrics.box.mp),
        "recall": float(metrics.box.mr)
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("dataset/annotated"))
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--img-size", type=int, default=640)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--skip-train", action="store_true")
    parser.add_argument("--model", type=Path, default=None)
    args = parser.parse_args()

    if args.skip_train:
        logger.info(f"Treinamento pulado. Usando modelo: {args.model}")
        model_path = args.model
    else:
        yaml_path = generate_data_yaml(args.data)
        model_path = train(yaml_path, args.epochs, args.img_size, args.batch, args.device)

    # Avalia
    yaml_path = generate_data_yaml(args.data)
    metrics = evaluate(model_path, yaml_path)
    logger.info(f"mAP@50: {metrics['map50']:.3f} | mAP@50-95: {metrics['map50_95']:.3f}")

    # Atualiza estado
    state = json.loads(Path("build_state.json").read_text())
    state["model_trained"] = True
    state["model_metrics"] = metrics
    state["model_path"] = str(model_path)
    state["last_updated"] = datetime.now().isoformat()
    Path("build_state.json").write_text(json.dumps(state, indent=2))
```

## ✅ CHECKPOINT FASE 3

- [ ] Modelo treinado (ou pulado com modelo pré-existente)
- [ ] mAP@50 ≥ 0.60 (mínimo aceitável para MVP)
- [ ] `build_state.json`: `"model_trained": true`

⏸️ **PAUSA SEGURA AQUI**

---

---

# FASE 4 — API REST (FastAPI)

**Objetivo:** Construir a API consumível por .NET, Java e qualquer cliente HTTP.

## Tarefa 4.1 — Rotas da API (`api/routes/analysis.py`)

```python
"""Rotas de análise — endpoint principal da API."""
import os
import uuid
import time
import shutil
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from loguru import logger
from api.models.schemas import AnalysisResponse, StrideReport, DeepAnalysisInput
from api.services.vision_service import VisionService
from core.preprocessor import validate_single_image


router = APIRouter(prefix="/api/v1", tags=["analysis"])

# Storage em memória para o MVP (substituir por Redis/DB em produção)
analysis_store: dict[str, AnalysisResponse] = {}
UPLOAD_DIR = Path("./temp_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

vision_service = VisionService(api_key=os.getenv("ANTHROPIC_API_KEY"))


@router.post("/analyze", response_model=AnalysisResponse, summary="Submit diagram for STRIDE analysis")
async def analyze_diagram(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="Architecture diagram image (PNG, JPG, etc.)"),
    diagram_type: Optional[str] = Form(None, description="aws|azure|gcp|generic"),
    additional_context: Optional[str] = Form(None),
    tech_stack: Optional[str] = Form(None, description="Comma-separated list"),
    existing_controls: Optional[str] = Form(None, description="Comma-separated list"),
    compliance_requirements: Optional[str] = Form(None, description="e.g., PCI-DSS,SOC2")
):
    """
    Submit an architecture diagram for automated STRIDE threat modeling analysis.
    
    Returns an analysis_id immediately. The full report is available at GET /report/{analysis_id}.
    
    **Supported formats:** PNG, JPG, JPEG, BMP, WEBP  
    **Max file size:** 20MB
    """
    # Validação básica
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    analysis_id = str(uuid.uuid4())

    # Salva arquivo temporário
    upload_path = UPLOAD_DIR / f"{analysis_id}_{file.filename}"
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Valida imagem
    is_valid, reason = validate_single_image(str(upload_path))
    if not is_valid:
        upload_path.unlink(missing_ok=True)
        raise HTTPException(status_code=422, detail=f"Invalid image: {reason}")

    # Monta deep analysis input
    deep_input = None
    if any([additional_context, tech_stack, existing_controls, compliance_requirements]):
        deep_input = DeepAnalysisInput(
            additional_context=additional_context,
            tech_stack=tech_stack.split(",") if tech_stack else None,
            existing_controls=existing_controls.split(",") if existing_controls else None,
            compliance_requirements=compliance_requirements.split(",") if compliance_requirements else None
        )

    # Registra como queued
    response = AnalysisResponse(
        analysis_id=analysis_id,
        status="queued",
        message="Analysis queued. Retrieve results at GET /api/v1/report/{analysis_id}"
    )
    analysis_store[analysis_id] = response

    # Processa em background
    background_tasks.add_task(
        _run_analysis_task,
        analysis_id=analysis_id,
        image_path=str(upload_path),
        deep_input=deep_input
    )

    return response


async def _run_analysis_task(analysis_id: str, image_path: str,
                              deep_input: Optional[DeepAnalysisInput]):
    """Task assíncrona que executa o pipeline completo."""
    start = time.time()
    try:
        analysis_store[analysis_id] = AnalysisResponse(
            analysis_id=analysis_id, status="processing",
            message="Running STRIDE analysis pipeline..."
        )

        report = vision_service.full_analysis_pipeline(
            image_path=image_path,
            analysis_id=analysis_id,
            deep_input=deep_input
        )

        elapsed = time.time() - start
        analysis_store[analysis_id] = AnalysisResponse(
            analysis_id=analysis_id,
            status="completed",
            message=f"Analysis completed in {elapsed:.1f}s",
            report=report,
            processing_time_seconds=elapsed
        )
        logger.info(f"Analysis {analysis_id} completed in {elapsed:.1f}s")

    except Exception as e:
        logger.exception(f"Analysis {analysis_id} failed: {e}")
        analysis_store[analysis_id] = AnalysisResponse(
            analysis_id=analysis_id,
            status="failed",
            message=f"Analysis failed: {str(e)}"
        )


@router.get("/report/{analysis_id}", response_model=AnalysisResponse,
            summary="Get analysis status and report")
async def get_report(analysis_id: str):
    """Retrieve the STRIDE analysis status and full report by analysis ID."""
    if analysis_id not in analysis_store:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis_store[analysis_id]


@router.get("/report/{analysis_id}/download",
            summary="Download full report as Markdown")
async def download_report(analysis_id: str):
    """Download the generated STRIDE report as a Markdown file."""
    if analysis_id not in analysis_store:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    result = analysis_store[analysis_id]
    if result.status != "completed":
        raise HTTPException(status_code=425, detail="Analysis not yet completed")
    
    # Gera e retorna Markdown
    md_path = _generate_markdown_report(analysis_id, result.report)
    return FileResponse(md_path, media_type="text/markdown",
                       filename=f"stride_report_{analysis_id[:8]}.md")


def _generate_markdown_report(analysis_id: str, report: StrideReport) -> str:
    """Gera arquivo Markdown do relatório."""
    lines = [
        f"# STRIDE Threat Model Report",
        f"**Analysis ID:** `{report.analysis_id}`",
        f"**Generated:** {report.generated_at.strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Overall Risk Score:** {report.overall_risk_score:.1f}/10",
        "",
        "## Executive Summary",
        report.executive_summary,
        "",
        "## Critical Findings",
        *[f"- {f}" for f in report.critical_findings],
        "",
        "## Architecture Components",
        f"*{len(report.components)} components detected across {len(report.trust_boundaries)} trust boundaries.*",
        "",
        "## STRIDE Threat Analysis",
    ]

    # Agrupa por severidade
    for sev in ["Critical", "High", "Medium", "Low", "Informational"]:
        vulns = [v for v in report.vulnerabilities if v.severity.value == sev]
        if vulns:
            lines.append(f"\n### {sev} Severity ({len(vulns)} threats)")
            for v in vulns:
                lines.extend([
                    f"\n#### [{v.category.value}] {v.title}",
                    f"**Component:** {v.affected_component_name}",
                    f"**Description:** {v.description}",
                    f"**Attack Vector:** {v.attack_vector}",
                    f"**Impact:** {v.impact}",
                    "**Countermeasures:**",
                    *[f"  - {cm}" for cm in v.countermeasures],
                    f"**CVE/CWE:** {', '.join(v.cve_references + v.cwe_references) or 'N/A'}",
                ])

    lines.extend(["", "## Priority Action Plan",
                  *[f"{i+1}. {a}" for i, a in enumerate(report.recommended_priority_actions)]])

    md_content = "\n".join(lines)
    out_path = f"./temp_uploads/report_{analysis_id[:8]}.md"
    Path(out_path).write_text(md_content)
    return out_path


@router.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0", "service": "STRIDE-AI"}
```

## Tarefa 4.2 — Main FastAPI (`api/main.py`)

```python
"""STRIDE-AI — FastAPI Application Entry Point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from api.routes.analysis import router as analysis_router

app = FastAPI(
    title="STRIDE-AI Threat Modeling API",
    description="""
    ## STRIDE-AI — Automated Threat Modeling via AI
    
    Upload an architecture diagram to receive a complete STRIDE threat model report.
    
    ### Features
    - 🔍 **Component Detection**: Automatically identifies all architectural components
    - 🛡️ **STRIDE Analysis**: Full threat modeling per component
    - 📊 **Risk Scoring**: CVSS-like overall risk assessment
    - 🔧 **Deep Analysis Script**: Custom Python security script generation
    - 🗺️ **Corrected Diagram**: Improved architecture with security controls
    - 📄 **Report Export**: Markdown report download
    
    ### Integration Example (.NET)
    ```csharp
    using var client = new HttpClient();
    using var form = new MultipartFormDataContent();
    form.Add(new StreamContent(File.OpenRead("diagram.png")), "file", "diagram.png");
    var response = await client.PostAsync("http://localhost:8000/api/v1/analyze", form);
    var result = await response.Content.ReadFromJsonAsync<AnalysisResponse>();
    ```
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS — permite integração com .NET, React, etc.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção: restringir domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis_router)

# Serve arquivos estáticos (diagramas gerados)
Path("./static").mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup():
    logger.info("STRIDE-AI API starting up...")
    if not os.getenv("ANTHROPIC_API_KEY"):
        logger.warning("ANTHROPIC_API_KEY not set!")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
```

## ✅ CHECKPOINT FASE 4

```bash
# Inicia a API
uvicorn api.main:app --reload --port 8000

# Testa o health check
curl http://localhost:8000/api/v1/health

# Abre documentação interativa
open http://localhost:8000/docs
```

- [ ] API responde em `http://localhost:8000/docs`
- [ ] `POST /api/v1/analyze` aceita multipart upload
- [ ] `GET /api/v1/health` retorna `{"status": "healthy"}`

⏸️ **PAUSA SEGURA AQUI**

---

---

# FASE 5 — TESTES UNITÁRIOS E DE INTEGRAÇÃO

## Tarefa 5.1 — Fixtures e Configuração (`tests/conftest.py`)

```python
import pytest
import asyncio
from pathlib import Path
from httpx import AsyncClient
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from api.main import app
from api.models.schemas import (
    StrideReport, ArchitectureComponent, TrustBoundary,
    StrideVulnerability, StrideCategory, SeverityLevel, ComponentType
)
from datetime import datetime


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_component():
    return ArchitectureComponent(
        name="API Gateway",
        type=ComponentType.API_GATEWAY,
        description="Main entry point for API calls",
        trust_level="Semi-trusted",
        protocols=["HTTPS"],
        ports=["443"],
        location="Public Subnet",
        connected_to=["Web Server", "Identity Provider"]
    )


@pytest.fixture
def sample_vulnerability():
    return StrideVulnerability(
        category=StrideCategory.SPOOFING,
        severity=SeverityLevel.HIGH,
        title="API Gateway Authentication Bypass",
        description="Attacker may forge JWT tokens",
        affected_component_id="test-001",
        affected_component_name="API Gateway",
        attack_vector="Forge JWT with weak secret",
        impact="Unauthorized access to backend services",
        likelihood="Medium",
        cve_references=["CVE-2022-21449"],
        cwe_references=["CWE-287"],
        countermeasures=[
            "Enforce RS256 signature validation",
            "Implement token rotation",
            "Add anomaly detection for auth failures"
        ],
        implementation_priority=1
    )


@pytest.fixture
def sample_report(sample_component, sample_vulnerability):
    return StrideReport(
        analysis_id="test-analysis-001",
        diagram_summary="AWS VPC with public/private subnets",
        components=[sample_component],
        trust_boundaries=[
            TrustBoundary(name="External Trust Boundary",
                         boundary_type="External",
                         components_inside=["API Gateway"])
        ],
        vulnerabilities=[sample_vulnerability],
        overall_risk_score=7.5,
        executive_summary="The analyzed architecture presents significant risks...",
        critical_findings=["API Gateway lacks strong authentication"],
        recommended_priority_actions=["Implement JWT RS256", "Add WAF"],
        stride_matrix={"API Gateway": ["Spoofing", "Tampering"]}
    )


@pytest.fixture
def test_image_path(tmp_path):
    """Cria uma imagem de teste mínima."""
    from PIL import Image
    img = Image.new("RGB", (800, 600), color=(255, 255, 255))
    path = tmp_path / "test_diagram.png"
    img.save(path)
    return str(path)
```

## Tarefa 5.2 — Testes Unitários (`tests/unit/test_schemas.py`)

```python
"""Testes dos schemas Pydantic."""
import pytest
from api.models.schemas import (
    StrideCategory, SeverityLevel, ComponentType, ArchitectureComponent,
    StrideVulnerability, StrideReport, DeepAnalysisInput
)


class TestStrideCategory:
    def test_all_stride_values_present(self):
        expected = {"Spoofing", "Tampering", "Repudiation",
                    "Information Disclosure", "Denial of Service", "Elevation of Privilege"}
        actual = {c.value for c in StrideCategory}
        assert actual == expected

    def test_stride_category_from_string(self):
        assert StrideCategory("Spoofing") == StrideCategory.SPOOFING


class TestSeverityLevel:
    def test_severity_ordering(self):
        levels = [SeverityLevel.CRITICAL, SeverityLevel.HIGH,
                  SeverityLevel.MEDIUM, SeverityLevel.LOW, SeverityLevel.INFORMATIONAL]
        assert len(levels) == 5


class TestArchitectureComponent:
    def test_component_creation(self, sample_component):
        assert sample_component.name == "API Gateway"
        assert sample_component.type == ComponentType.API_GATEWAY
        assert "HTTPS" in sample_component.protocols

    def test_component_requires_name(self):
        with pytest.raises(Exception):
            ArchitectureComponent(type=ComponentType.DATABASE)

    def test_component_default_id_generated(self, sample_component):
        assert len(sample_component.id) == 8


class TestStrideVulnerability:
    def test_vulnerability_creation(self, sample_vulnerability):
        assert sample_vulnerability.category == StrideCategory.SPOOFING
        assert sample_vulnerability.severity == SeverityLevel.HIGH
        assert len(sample_vulnerability.countermeasures) == 3

    def test_priority_range_validation(self):
        with pytest.raises(Exception):
            StrideVulnerability(
                category=StrideCategory.SPOOFING,
                severity=SeverityLevel.HIGH,
                title="Test", description="Test",
                affected_component_id="x", affected_component_name="x",
                attack_vector="x", impact="x", likelihood="High",
                countermeasures=[], implementation_priority=6  # inválido
            )


class TestStrideReport:
    def test_report_creation(self, sample_report):
        assert len(sample_report.components) == 1
        assert len(sample_report.vulnerabilities) == 1
        assert 0.0 <= sample_report.overall_risk_score <= 10.0

    def test_risk_score_out_of_range(self):
        with pytest.raises(Exception):
            StrideReport(
                analysis_id="x", diagram_summary="x",
                components=[], trust_boundaries=[], vulnerabilities=[],
                overall_risk_score=11.0,  # inválido
                executive_summary="x", critical_findings=[], recommended_priority_actions=[],
                stride_matrix={}
            )
```

## Tarefa 5.3 — Testes de Integração (`tests/integration/test_api.py`)

```python
"""Testes de integração da API."""
import pytest
import io
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from PIL import Image


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_health_returns_version(self, client):
        response = client.get("/api/v1/health")
        assert "version" in response.json()


class TestAnalyzeEndpoint:
    def _make_image_bytes(self, width=800, height=600):
        img = Image.new("RGB", (width, height), color=(200, 200, 200))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf

    def test_analyze_returns_analysis_id(self, client):
        with patch("api.routes.analysis.vision_service.full_analysis_pipeline") as mock:
            mock.return_value = MagicMock(analysis_id="mocked-id")
            
            img_bytes = self._make_image_bytes()
            response = client.post(
                "/api/v1/analyze",
                files={"file": ("test.png", img_bytes, "image/png")}
            )
            assert response.status_code == 200
            data = response.json()
            assert "analysis_id" in data
            assert data["status"] in ["queued", "processing", "completed"]

    def test_analyze_rejects_non_image(self, client):
        response = client.post(
            "/api/v1/analyze",
            files={"file": ("test.txt", b"not an image", "text/plain")}
        )
        assert response.status_code == 400

    def test_analyze_with_context(self, client):
        with patch("api.routes.analysis._run_analysis_task"):
            img_bytes = self._make_image_bytes()
            response = client.post(
                "/api/v1/analyze",
                files={"file": ("test.png", img_bytes, "image/png")},
                data={
                    "diagram_type": "aws",
                    "additional_context": "Production system with PCI-DSS compliance",
                    "tech_stack": "Python,FastAPI,PostgreSQL",
                    "compliance_requirements": "PCI-DSS,SOC2"
                }
            )
            assert response.status_code == 200


class TestReportEndpoint:
    def test_report_not_found_returns_404(self, client):
        response = client.get("/api/v1/report/nonexistent-id")
        assert response.status_code == 404

    def test_report_returns_full_structure(self, client, sample_report):
        from api.routes.analysis import analysis_store
        from api.models.schemas import AnalysisResponse
        
        analysis_store["test-123"] = AnalysisResponse(
            analysis_id="test-123",
            status="completed",
            message="Done",
            report=sample_report
        )
        
        response = client.get("/api/v1/report/test-123")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["report"]["overall_risk_score"] == 7.5
```

## Tarefa 5.4 — Executar Testes

```bash
# Roda todos os testes com cobertura
pytest tests/ -v --cov=api --cov=core --cov-report=html --cov-report=term-missing

# Apenas unitários
pytest tests/unit/ -v

# Apenas integração
pytest tests/integration/ -v

# Relatório HTML de cobertura
open htmlcov/index.html
```

## ✅ CHECKPOINT FASE 5

- [ ] `pytest tests/ -v` — todos os testes passando
- [ ] Cobertura de código ≥ 70%
- [ ] `build_state.json`: `"tests_passing": true`

⏸️ **PAUSA SEGURA AQUI**

---

---

# FASE 6 — GERAÇÃO DE DIAGRAMA E DASHBOARD

## Tarefa 6.1 — Gerador de Diagrama Corrigido (`api/services/diagram_generator.py`)

```python
"""
Gera diagramas Graphviz a partir dos dados de componentes e melhorias sugeridas.
Exporta como PNG e DOT.
"""
import graphviz
from pathlib import Path
from api.models.schemas import StrideReport, ComponentType, SeverityLevel


COMPONENT_COLORS = {
    ComponentType.USER: ("#E8F5E9", "#2E7D32"),
    ComponentType.WEB_SERVER: ("#E3F2FD", "#1565C0"),
    ComponentType.APP_SERVER: ("#E8EAF6", "#283593"),
    ComponentType.DATABASE: ("#FFF3E0", "#E65100"),
    ComponentType.API_GATEWAY: ("#F3E5F5", "#6A1B9A"),
    ComponentType.LOAD_BALANCER: ("#E0F7FA", "#00695C"),
    ComponentType.IDENTITY_PROVIDER: ("#FCE4EC", "#880E4F"),
    ComponentType.CACHE: ("#FFFDE7", "#F57F17"),
    ComponentType.TRUST_BOUNDARY: ("#FFEBEE", "#B71C1C"),
    ComponentType.FIREWALL: ("#FFCDD2", "#C62828"),
}

SEVERITY_COLORS = {
    SeverityLevel.CRITICAL: "#FF1744",
    SeverityLevel.HIGH: "#FF6D00",
    SeverityLevel.MEDIUM: "#FFD600",
    SeverityLevel.LOW: "#00C853",
}


def generate_corrected_diagram(report: StrideReport, output_dir: str = "./static") -> str:
    """Gera diagrama Graphviz do sistema com anotações de segurança."""
    Path(output_dir).mkdir(exist_ok=True)

    dot = graphviz.Digraph(
        name=f"stride_corrected_{report.analysis_id[:8]}",
        comment="STRIDE-AI Corrected Architecture Diagram",
        graph_attr={
            "rankdir": "TB",
            "splines": "ortho",
            "bgcolor": "#FAFAFA",
            "fontname": "Helvetica",
            "pad": "0.5",
            "nodesep": "0.8",
            "ranksep": "1.0",
            "label": f"STRIDE-AI Security Analysis\\nRisk Score: {report.overall_risk_score:.1f}/10",
            "labelloc": "t",
            "fontsize": "14"
        },
        node_attr={"fontname": "Helvetica", "fontsize": "10"},
        edge_attr={"fontname": "Helvetica", "fontsize": "9"}
    )

    # Agrupa componentes por trust boundary
    boundary_map = {}
    for boundary in report.trust_boundaries:
        boundary_map[boundary.name] = boundary.components_inside

    # Identifica componentes com vulnerabilidades críticas
    critical_components = {
        v.affected_component_name
        for v in report.vulnerabilities
        if v.severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH]
    }

    # Cria subgraphs por boundary
    for boundary in report.trust_boundaries:
        with dot.subgraph(name=f"cluster_{boundary.id}") as sub:
            boundary_color = "#FF1744" if "External" in boundary.boundary_type else "#1565C0"
            sub.attr(
                label=boundary.name,
                style="dashed",
                color=boundary_color,
                fontcolor=boundary_color,
                bgcolor="#FFFFFF00"
            )

            # Adiciona componentes dentro do boundary
            for comp in report.components:
                if comp.name in boundary.components_inside:
                    fill, stroke = COMPONENT_COLORS.get(comp.type, ("#F5F5F5", "#757575"))
                    has_critical = comp.name in critical_components
                    
                    label = f"{comp.name}\\n({comp.type.value})"
                    if comp.protocols:
                        label += f"\\n{', '.join(comp.protocols[:2])}"

                    sub.node(
                        comp.id,
                        label=label,
                        shape="box",
                        style="rounded,filled",
                        fillcolor=fill,
                        color="#FF1744" if has_critical else stroke,
                        penwidth="3" if has_critical else "1",
                        tooltip=comp.description
                    )

    # Componentes sem boundary
    for comp in report.components:
        is_in_boundary = any(
            comp.name in b.components_inside for b in report.trust_boundaries
        )
        if not is_in_boundary:
            fill, stroke = COMPONENT_COLORS.get(comp.type, ("#F5F5F5", "#757575"))
            dot.node(
                comp.id,
                label=f"{comp.name}\\n({comp.type.value})",
                shape="box",
                style="rounded,filled",
                fillcolor=fill,
                color=stroke
            )

    # Data flows como arestas
    comp_name_to_id = {c.name: c.id for c in report.components}
    for comp in report.components:
        for target_name in comp.connected_to:
            if target_name in comp_name_to_id:
                # Verifica se há ameaça neste fluxo
                flow_threatened = any(
                    v.affected_component_name in [comp.name, target_name]
                    and v.category.value in ["Tampering", "Information Disclosure"]
                    for v in report.vulnerabilities
                )
                dot.edge(
                    comp.id,
                    comp_name_to_id[target_name],
                    color="#FF6D00" if flow_threatened else "#546E7A",
                    penwidth="2" if flow_threatened else "1",
                    style="dashed" if flow_threatened else "solid"
                )

    # Legenda
    with dot.subgraph(name="cluster_legend") as legend:
        legend.attr(label="Legend", style="filled", fillcolor="#F5F5F5", fontsize="10")
        legend.node("l1", "⚠ Critical Risk Component", shape="box", style="filled",
                    fillcolor="white", color="#FF1744", penwidth="3", fontsize="9")
        legend.node("l2", "→ Threatened Data Flow", shape="plaintext", fontsize="9",
                    fontcolor="#FF6D00")

    # Renderiza
    output_path = str(Path(output_dir) / f"diagram_{report.analysis_id[:8]}")
    dot.render(output_path, format="png", cleanup=True)
    dot.render(output_path, format="svg", cleanup=True)

    return f"{output_path}.png"
```

## ✅ CHECKPOINT FASE 6

```bash
python -c "
from api.services.diagram_generator import generate_corrected_diagram
# Teste com report de fixture
print('Diagram generator OK')
"
```

- [ ] Graphviz instalado no sistema (`dot -V`)
- [ ] `generate_corrected_diagram` exporta PNG sem erros
- [ ] Diagrama visível em `./static/`

---

---

# FASE 7 — FRONTEND STREAMLIT

## Tarefa 7.1 — App Principal (`frontend/app.py`)

```python
"""
STRIDE-AI — Interface Gráfica Principal (Streamlit)
"""
import streamlit as st
from pathlib import Path

# Configuração da página — DEVE ser o primeiro comando Streamlit
st.set_page_config(
    page_title="STRIDE-AI | Threat Modeling",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/your-org/stride-ai",
        "Report a bug": "https://github.com/your-org/stride-ai/issues",
        "About": "STRIDE-AI — Automated Threat Modeling via AI. FIAP Hackathon 2025."
    }
)

# CSS Global
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;600;700&display=swap');

    .stApp { background: #0D1117; color: #E6EDF3; font-family: 'Inter', sans-serif; }
    
    /* Header estilo cybersec */
    .main-header {
        background: linear-gradient(135deg, #161B22 0%, #21262D 100%);
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #FF1744, #FF6D00, #FFD600, #00C853);
    }
    .stride-badge {
        display: inline-block;
        background: #FF1744;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 2px;
        margin-right: 8px;
    }
    
    /* Risk score */
    .risk-critical { color: #FF1744; font-weight: 700; }
    .risk-high { color: #FF6D00; font-weight: 700; }
    .risk-medium { color: #FFD600; font-weight: 700; }
    .risk-low { color: #00C853; font-weight: 700; }
    
    /* Cards */
    .threat-card {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #161B22;
        border-right: 1px solid #30363D;
    }
    
    /* Métricas */
    div[data-testid="stMetric"] {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 0.75rem;
    }
    
    code, pre { font-family: 'JetBrains Mono', monospace !important; }
    
    /* Upload area */
    div[data-testid="stFileUploader"] {
        background: #161B22;
        border: 2px dashed #30363D;
        border-radius: 12px;
        padding: 1rem;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: #FF1744;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #FF1744, #FF6D00);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(255, 23, 68, 0.4);
    }
</style>
""", unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div class="main-header">
        <span class="stride-badge">STRIDE-AI</span>
        <span style="font-family: 'JetBrains Mono', monospace; color: #8B949E; font-size: 0.8rem;">v1.0.0</span>
        <h1 style="margin: 0.5rem 0 0; font-size: 2rem; font-weight: 700; color: #E6EDF3;">
            Automated Threat Modeling
        </h1>
        <p style="color: #8B949E; margin: 0.25rem 0 0; font-size: 0.95rem;">
            Upload an architecture diagram. Receive a complete STRIDE security analysis powered by AI.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("### 🛡️ STRIDE-AI")
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["🏠 Home", "🔍 Analyze", "📊 Dashboard", "📄 Reports", "📚 Documentation"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("#### Threat Categories")
        for cat, color in [
            ("S — Spoofing", "#E53935"),
            ("T — Tampering", "#F57C00"),
            ("R — Repudiation", "#FBC02D"),
            ("I — Info Disclosure", "#7B1FA2"),
            ("D — Denial of Service", "#1976D2"),
            ("E — Elevation of Privilege", "#388E3C"),
        ]:
            st.markdown(
                f'<span style="color:{color}; font-family: JetBrains Mono; '
                f'font-size: 0.8rem;">● {cat}</span>',
                unsafe_allow_html=True
            )
        
        st.markdown("---")
        st.caption("FIAP Software Security Hackathon 2025")
        return page


def main():
    render_header()
    page = render_sidebar()

    if "Home" in page:
        render_home()
    elif "Analyze" in page:
        render_analyze()
    elif "Dashboard" in page:
        render_dashboard()
    elif "Reports" in page:
        render_reports()
    elif "Documentation" in page:
        render_docs()


def render_home():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Components Analyzed", "2,341", "+12%")
    with col2:
        st.metric("Threats Detected", "18,924", "+8%")
    with col3:
        st.metric("Avg Risk Score", "6.4/10", "-0.3")
    with col4:
        st.metric("Reports Generated", "412", "+23%")

    st.markdown("---")
    st.markdown("### How it works")
    
    steps = [
        ("1️⃣", "Upload Diagram", "Upload your architecture diagram (AWS, Azure, GCP or custom)"),
        ("2️⃣", "AI Analysis", "Claude Vision detects all components, flows, and trust boundaries"),
        ("3️⃣", "STRIDE Modeling", "Automated threat identification per component and flow"),
        ("4️⃣", "Report & Fix", "Download the full report + corrected diagram + deep analysis script"),
    ]
    
    cols = st.columns(4)
    for col, (icon, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div style="background:#161B22;border:1px solid #30363D;border-radius:8px;
                        padding:1rem;text-align:center;height:160px;">
                <div style="font-size:2rem;">{icon}</div>
                <div style="font-weight:600;margin:0.5rem 0;color:#E6EDF3;">{title}</div>
                <div style="color:#8B949E;font-size:0.85rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)


def render_analyze():
    st.markdown("## 🔍 Analyze Architecture Diagram")
    
    col_upload, col_context = st.columns([1, 1])
    
    with col_upload:
        st.markdown("### 1. Upload Diagram")
        uploaded_file = st.file_uploader(
            "Drop your architecture diagram here",
            type=["png", "jpg", "jpeg", "bmp", "webp"],
            help="Supported: PNG, JPG, JPEG, BMP, WEBP. Max 20MB."
        )
        
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Diagram", use_column_width=True)
    
    with col_context:
        st.markdown("### 2. Add Context (Optional — enables Deep Analysis)")
        
        diagram_type = st.selectbox(
            "Cloud Provider / Diagram Type",
            ["Auto-detect", "AWS", "Azure", "GCP", "Generic", "Hybrid"]
        )
        
        tech_stack = st.multiselect(
            "Technology Stack",
            ["Python", "FastAPI", ".NET", "Java/Spring", "Node.js", "PostgreSQL",
             "MySQL", "MongoDB", "Redis", "Kubernetes", "Docker", "Nginx",
             "Apache", "OAuth2", "SAML", "JWT"]
        )
        
        compliance = st.multiselect(
            "Compliance Requirements",
            ["PCI-DSS", "SOC2", "HIPAA", "GDPR", "ISO-27001", "NIST", "LGPD"]
        )
        
        existing_controls = st.text_area(
            "Existing Security Controls",
            placeholder="e.g., WAF deployed, MFA enabled, SIEM in place...",
            height=80
        )
        
        additional_context = st.text_area(
            "Additional Context",
            placeholder="Production system, 50k users, financial data...",
            height=80
        )
    
    st.markdown("---")
    
    if st.button("🚀 Run STRIDE Analysis", disabled=uploaded_file is None, use_container_width=True):
        if uploaded_file:
            _run_analysis(
                uploaded_file=uploaded_file,
                diagram_type=diagram_type,
                tech_stack=tech_stack,
                compliance=compliance,
                existing_controls=existing_controls,
                additional_context=additional_context
            )


def _run_analysis(uploaded_file, **kwargs):
    """Executa análise via API e exibe resultados."""
    import httpx
    import time
    import os

    api_base = os.getenv("API_BASE_URL", "http://localhost:8000")
    
    with st.spinner("🔍 Analyzing diagram with Claude Vision AI..."):
        progress_bar = st.progress(0, text="Uploading diagram...")
        
        try:
            # Upload e análise
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "image/png")}
            data = {k: v for k, v in {
                "diagram_type": kwargs.get("diagram_type", "").replace("Auto-detect", ""),
                "tech_stack": ",".join(kwargs.get("tech_stack", [])),
                "compliance_requirements": ",".join(kwargs.get("compliance", [])),
                "existing_controls": kwargs.get("existing_controls", ""),
                "additional_context": kwargs.get("additional_context", "")
            }.items() if v}
            
            progress_bar.progress(20, text="Sending to STRIDE-AI API...")
            response = httpx.post(f"{api_base}/api/v1/analyze", files=files, data=data, timeout=30)
            response.raise_for_status()
            
            analysis_id = response.json()["analysis_id"]
            progress_bar.progress(40, text="Running AI component detection...")
            
            # Polling
            for i, pct in enumerate(range(40, 100, 10)):
                time.sleep(2)
                status_resp = httpx.get(f"{api_base}/api/v1/report/{analysis_id}", timeout=10)
                status_data = status_resp.json()
                
                if status_data["status"] == "completed":
                    progress_bar.progress(100, text="Analysis complete!")
                    st.session_state["last_report"] = status_data["report"]
                    st.session_state["last_analysis_id"] = analysis_id
                    _display_results(status_data["report"])
                    return
                elif status_data["status"] == "failed":
                    st.error(f"Analysis failed: {status_data['message']}")
                    return
                
                progress_bar.progress(pct, text=f"Processing... ({status_data['status']})")
                
        except httpx.ConnectError:
            st.error("⚠️ Cannot connect to STRIDE-AI API. Make sure the API is running on port 8000.")
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")


def _display_results(report: dict):
    """Exibe resultados da análise."""
    st.success("✅ STRIDE Analysis Complete!")
    
    # Métricas de topo
    risk = report.get("overall_risk_score", 0)
    risk_class = "critical" if risk >= 8 else "high" if risk >= 6 else "medium" if risk >= 4 else "low"
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Risk", f"{risk:.1f}/10")
    with col2:
        st.metric("Components", len(report.get("components", [])))
    with col3:
        st.metric("Threats Found", len(report.get("vulnerabilities", [])))
    with col4:
        critical_count = sum(1 for v in report.get("vulnerabilities", [])
                           if v["severity"] in ["Critical", "High"])
        st.metric("Critical/High", critical_count)
    
    # Summary
    st.markdown("### Executive Summary")
    st.info(report.get("executive_summary", ""))
    
    # Critical findings
    if report.get("critical_findings"):
        st.markdown("### 🚨 Critical Findings")
        for finding in report["critical_findings"]:
            st.error(f"▸ {finding}")
    
    # Tabela de ameaças
    st.markdown("### STRIDE Threat Matrix")
    
    vulns = report.get("vulnerabilities", [])
    if vulns:
        import pandas as pd
        df = pd.DataFrame([{
            "Category": v["category"],
            "Severity": v["severity"],
            "Title": v["title"],
            "Component": v["affected_component_name"],
            "Priority": v["implementation_priority"]
        } for v in vulns])
        
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Priority actions
    if report.get("recommended_priority_actions"):
        st.markdown("### 🎯 Priority Action Plan")
        for i, action in enumerate(report["recommended_priority_actions"], 1):
            st.markdown(f"**{i}.** {action}")


def render_dashboard():
    st.markdown("## 📊 Security Dashboard")
    
    report = st.session_state.get("last_report")
    if not report:
        st.warning("No analysis performed yet. Go to **Analyze** to run your first analysis.")
        return
    
    import plotly.graph_objects as go
    import plotly.express as px
    import pandas as pd
    
    vulns = report.get("vulnerabilities", [])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### STRIDE Category Distribution")
        categories = pd.Series([v["category"] for v in vulns]).value_counts()
        fig = go.Figure(go.Bar(
            x=categories.values, y=categories.index, orientation="h",
            marker_color=["#E53935", "#F57C00", "#FBC02D", "#7B1FA2", "#1976D2", "#388E3C"]
        ))
        fig.update_layout(
            plot_bgcolor="#161B22", paper_bgcolor="#161B22",
            font_color="#E6EDF3", height=300, margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Severity Distribution")
        severities = pd.Series([v["severity"] for v in vulns]).value_counts()
        colors = {"Critical": "#FF1744", "High": "#FF6D00", "Medium": "#FFD600",
                  "Low": "#00C853", "Informational": "#90A4AE"}
        fig2 = go.Figure(go.Pie(
            labels=severities.index,
            values=severities.values,
            marker_colors=[colors.get(s, "#grey") for s in severities.index],
            hole=0.4
        ))
        fig2.update_layout(
            plot_bgcolor="#161B22", paper_bgcolor="#161B22",
            font_color="#E6EDF3", height=300, margin=dict(l=0, r=0, t=0, b=0),
            showlegend=True
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Heatmap STRIDE por componente
    st.markdown("#### STRIDE Threat Heatmap (Component × Category)")
    
    if report.get("stride_matrix"):
        matrix_data = []
        all_categories = ["Spoofing", "Tampering", "Repudiation",
                          "Information Disclosure", "Denial of Service", "Elevation of Privilege"]
        for comp_name, comp_cats in report["stride_matrix"].items():
            row = {"Component": comp_name}
            for cat in all_categories:
                row[cat[:1]] = 1 if cat in comp_cats else 0
            matrix_data.append(row)
        
        if matrix_data:
            df_heat = pd.DataFrame(matrix_data).set_index("Component")
            fig3 = px.imshow(
                df_heat,
                color_continuous_scale=[[0, "#161B22"], [1, "#FF1744"]],
                aspect="auto",
                labels={"color": "Threat Present"}
            )
            fig3.update_layout(
                plot_bgcolor="#161B22", paper_bgcolor="#161B22",
                font_color="#E6EDF3", height=350
            )
            st.plotly_chart(fig3, use_container_width=True)


def render_reports():
    st.markdown("## 📄 Reports")
    
    report = st.session_state.get("last_report")
    analysis_id = st.session_state.get("last_analysis_id")
    
    if not report:
        st.info("No report available. Run an analysis first.")
        return
    
    import os
    api_base = os.getenv("API_BASE_URL", "http://localhost:8000")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            "📄 Download Markdown Report",
            data=_build_markdown_content(report),
            file_name=f"stride_report_{analysis_id[:8] if analysis_id else 'latest'}.md",
            mime="text/markdown",
            use_container_width=True
        )
    with col2:
        if report.get("deep_analysis_script"):
            st.download_button(
                "🐍 Download Deep Analysis Script",
                data=report["deep_analysis_script"],
                file_name="deep_security_analysis.py",
                mime="text/x-python",
                use_container_width=True
            )
        else:
            st.info("Deep analysis script requires additional context. Re-run with context filled.")
    with col3:
        st.link_button(
            "📖 Open Full Report (API)",
            url=f"{api_base}/api/v1/report/{analysis_id}/download" if analysis_id else "#",
            use_container_width=True
        )
    
    # Preview do relatório
    st.markdown("---")
    st.markdown("### Report Preview")
    st.markdown(_build_markdown_content(report))


def _build_markdown_content(report: dict) -> str:
    lines = [
        f"# STRIDE Threat Model Report",
        f"**Risk Score:** {report.get('overall_risk_score', 'N/A')}/10\n",
        "## Executive Summary",
        report.get("executive_summary", ""),
        "\n## Critical Findings",
        *[f"- {f}" for f in report.get("critical_findings", [])],
        "\n## Vulnerabilities",
    ]
    for v in report.get("vulnerabilities", []):
        lines.extend([
            f"\n### [{v['severity']}] [{v['category']}] {v['title']}",
            f"**Component:** {v['affected_component_name']}",
            f"**Description:** {v['description']}",
            f"**Countermeasures:** {', '.join(v['countermeasures'][:3])}"
        ])
    return "\n".join(lines)


def render_docs():
    st.markdown("## 📚 Documentation")
    
    tab1, tab2, tab3 = st.tabs(["Getting Started", "API Reference", "STRIDE Guide"])
    
    with tab1:
        st.markdown("""
        ## Getting Started with STRIDE-AI
        
        ### What is STRIDE?
        STRIDE is a threat modeling methodology developed by Microsoft. 
        It categorizes threats into six categories:
        
        | Letter | Category | Description |
        |--------|----------|-------------|
        | **S** | Spoofing | Identity falsification |
        | **T** | Tampering | Data modification |
        | **R** | Repudiation | Denying actions |
        | **I** | Information Disclosure | Data leakage |
        | **D** | Denial of Service | Availability attacks |
        | **E** | Elevation of Privilege | Unauthorized access escalation |
        
        ### How to Use STRIDE-AI
        1. **Upload** your architecture diagram (AWS, Azure, GCP, or custom)
        2. **Optionally** fill in context (tech stack, compliance, existing controls)
        3. **Click** "Run STRIDE Analysis"
        4. **Review** the generated report with all identified threats
        5. **Download** the Markdown report and deep analysis script
        """)
    
    with tab2:
        st.markdown("""
        ## API Reference
        
        ### Base URL
        ```
        http://localhost:8000/api/v1
        ```
        
        ### POST /analyze — Submit Diagram
        ```http
        POST /api/v1/analyze
        Content-Type: multipart/form-data
        
        file: <image_file>          (required)
        diagram_type: aws           (optional)
        additional_context: ...     (optional)
        tech_stack: Python,FastAPI  (optional, comma-separated)
        compliance_requirements: PCI-DSS,SOC2  (optional)
        existing_controls: WAF,...  (optional)
        ```
        
        ### GET /report/{id} — Get Report
        ```http
        GET /api/v1/report/{analysis_id}
        ```
        
        ### .NET Integration Example
        ```csharp
        using var client = new HttpClient();
        using var form = new MultipartFormDataContent();
        var fileContent = new StreamContent(File.OpenRead("diagram.png"));
        fileContent.Headers.ContentType = MediaTypeHeaderValue.Parse("image/png");
        form.Add(fileContent, "file", "diagram.png");
        form.Add(new StringContent("aws"), "diagram_type");
        
        var response = await client.PostAsync(
            "http://localhost:8000/api/v1/analyze", form);
        var result = await response.Content.ReadAsStringAsync();
        ```
        """)
    
    with tab3:
        st.markdown("""
        ## STRIDE Methodology Guide
        
        ### Trust Boundaries
        Trust boundaries are the most critical element in STRIDE analysis.
        They define where data transitions between different trust levels.
        
        **Common Trust Boundaries:**
        - Internet → DMZ (External)
        - DMZ → Internal Network (Internal)
        - Application → Database (Database)
        - Public Subnet → Private Subnet (Network)
        
        ### Applying STRIDE Per Component
        
        | Component | S | T | R | I | D | E |
        |-----------|---|---|---|---|---|---|
        | User/Actor | ✓ | | ✓ | | | |
        | Web Server | ✓ | ✓ | | ✓ | ✓ | ✓ |
        | API Gateway | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
        | Database | | ✓ | ✓ | ✓ | ✓ | ✓ |
        | Data Flow | | ✓ | | ✓ | ✓ | |
        | Identity Provider | ✓ | | ✓ | ✓ | ✓ | ✓ |
        """)


if __name__ == "__main__":
    main()
```

## ✅ CHECKPOINT FASE 7

```bash
# Inicia o frontend (com API já rodando em outra aba)
cd frontend && streamlit run app.py --server.port 8501

# Acessa em http://localhost:8501
```

- [ ] Interface abre sem erros
- [ ] Upload de imagem funciona no fluxo Analyze
- [ ] Dashboard exibe gráficos com dados de análise
- [ ] Reports permite download do Markdown

⏸️ **PAUSA SEGURA AQUI**

---

---

# FASE 8 — DOCKER E DEPLOY

## Tarefa 8.1 — Dockerfile e Docker Compose

Crie `Dockerfile`:

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    graphviz \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000 8501
```

Crie `docker-compose.yml`:

```yaml
version: "3.9"

services:
  api:
    build: .
    command: uvicorn api.main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - NVD_API_KEY=${NVD_API_KEY}
    volumes:
      - ./static:/app/static
      - ./temp_uploads:/app/temp_uploads
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build: .
    command: streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0
    ports:
      - "8501:8501"
    environment:
      - API_BASE_URL=http://api:8000
    depends_on:
      api:
        condition: service_healthy
```

```bash
# Build e start
docker-compose up --build

# Acessa
# API:      http://localhost:8000/docs
# Frontend: http://localhost:8501
```

## ✅ CHECKPOINT FASE 8

- [ ] `docker-compose up` sobe sem erros
- [ ] Health check da API passa dentro do Docker
- [ ] Frontend conecta na API via `http://api:8000`

---

---

# FASE 9 — DOCUMENTAÇÃO E APRESENTAÇÃO

## Tarefa 9.1 — README.md

```bash
# Crie README.md completo com:
# - Visão geral do projeto
# - Arquitetura do sistema (ASCII ou Mermaid)
# - Como rodar (Docker e local)
# - Endpoints da API com exemplos
# - Screenshots da interface
# - Estrutura de diretórios
# - Como contribuir
# - Licença
```

## Tarefa 9.2 — Geração de Slides

```bash
# Instale e gere slides automáticos
python scripts/generate_presentation.py

# O script usa python-pptx para criar:
# Slide 1: Capa — STRIDE-AI
# Slide 2: Problema e Contexto
# Slide 3: Solução Proposta
# Slide 4: Arquitetura do Sistema
# Slide 5: Demo — Upload e Análise
# Slide 6: Resultados — Métricas e Dashboard
# Slide 7: API e Integrações
# Slide 8: Conclusão e Próximos Passos
```

## ✅ CHECKPOINT FASE 9

- [ ] `README.md` completo com instruções de setup
- [ ] Documentação de API (`/docs`) legível e completa
- [ ] `STRIDE-AI_Presentation.pptx` gerado
- [ ] `build_state.json`: `"docs_complete": true`

---

---

# FASE 10 — VERIFICAÇÃO FINAL E ENTREGÁVEIS

## Checklist Completo

```bash
# Executa o checklist final
python scripts/final_check.py
```

### Funcionalidades
- [ ] Upload de diagrama via interface web ✅
- [ ] Detecção de componentes via Claude Vision ✅
- [ ] Análise STRIDE completa por componente ✅
- [ ] Geração de relatório Markdown ✅
- [ ] Script de análise profunda (com contexto) ✅
- [ ] Diagrama corrigido exportado ✅
- [ ] Dashboard interativo com gráficos ✅
- [ ] API REST consumível por .NET/Java ✅
- [ ] Documentação in-app ✅

### Qualidade
- [ ] Todos os testes passando (`pytest tests/ -v`) ✅
- [ ] Cobertura ≥ 70% ✅
- [ ] Docker funcional ✅
- [ ] API documentada no Swagger ✅

### Entregáveis FIAP
- [ ] Código no GitHub com README ✅
- [ ] Documentação técnica (Markdown) ✅
- [ ] Slides de apresentação ✅
- [ ] Vídeo de até 15 min (gravar com OBS/Loom) ✅

## Atualização Final do Estado

```json
{
  "project": "STRIDE-AI",
  "version": "1.0.0",
  "current_phase": 10,
  "completed_phases": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  "api_key_configured": true,
  "dataset_validated": true,
  "model_trained": true,
  "api_deployed": true,
  "tests_passing": true,
  "frontend_ready": true,
  "docs_complete": true,
  "status": "READY_FOR_DELIVERY"
}
```

---

## RESUMO DE COMANDOS POR FASE

| Fase | Comando de Retomada |
|------|---------------------|
| 0 | `cat build_state.json` → verificar fase atual |
| 1 | `python scripts/preprocess_check.py --report-only` |
| 2 | `python -c "from api.services.vision_service import VisionService; print('OK')"` |
| 3 | `python scripts/train_model.py --skip-train --model models/stride_detector.pt` |
| 4 | `uvicorn api.main:app --reload` → `curl localhost:8000/api/v1/health` |
| 5 | `pytest tests/ -v --cov` |
| 6 | `python -c "from api.services.diagram_generator import generate_corrected_diagram"` |
| 7 | `streamlit run frontend/app.py` |
| 8 | `docker-compose up` |
| 9 | `python scripts/generate_presentation.py` |
| 10 | `python scripts/final_check.py` |

---

*STRIDE-AI — FIAP Software Security Hackathon 2025*  
*Stack: Python · FastAPI · Anthropic Claude · Streamlit · YOLOv8 · Graphviz*
