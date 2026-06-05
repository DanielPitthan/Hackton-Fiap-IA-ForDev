"""
segregate_datasets.py
Analisa amostras de datasets em raw/ e os segrega por relevancia para STRIDE.

RELEVANTE:
  - Diagramas de arquitetura reais (AWS/Azure/GCP, DFDs, modelos de ameacas)
  - Modelos STRIDE/PASTA/Attack Tree, Threat Dragon, OWASP
  - Componentes identificaveis: servers, APIs, DBs, trust boundaries

NAO RELEVANTE:
  - Diagramas UML sinteticos com palavras aleatorias (sem semantica de sistema)
  - Conteudo gerado por ferramentas de benchmark sem contexto de seguranca

Saida:
  datasets/data_refined/  <- relevantes para STRIDE
  datasets/data_refused/  <- nao relevantes
"""

import os
import re
import shutil
import random
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
RAW_DIR      = SCRIPT_DIR / "raw"
REFINED_DIR  = SCRIPT_DIR / "data_refined"
REFUSED_DIR  = SCRIPT_DIR / "data_refused"

SAMPLE_SIZE        = 30
MIN_SCORE_TO_ACCEPT = 3
MAX_FILES_TO_SCAN  = 5000

# Termos com word-boundary (nao casam como substring)
SECURITY_TERMS_EXACT = [
    r"\bstride\b", r"\bspoofing\b", r"\btampering\b", r"\brepudiation\b",
    r"\bthreat\b", r"\battack\b", r"\bvulnerabilit", r"\brisk\b",
    r"\bmitigat", r"\bcountermeasure\b", r"\bfirewall\b",
    r"\bvpc\b", r"\bsubnet\b", r"\bgateway\b",
    r"\bauthentication\b", r"\bauthorization\b", r"\bencryption\b",
    r"\biam\b", r"\bacl\b", r"\bwaf\b",
    r"\bdatabase\b", r"\bserver\b", r"\bmicroservice\b", r"\bbroker\b",
    r"\bprocess\b", r"\bdatastore\b",
    r"\bowasp\b", r"\bthreat.dragon\b", r"\biriusrisk\b",
    r"\bdata.flow\b", r"\bdfd\b", r"\btrust.boundary\b",
    r"\battack.tree\b",
    # Cloud - mais especificos para evitar false positives
    r"\baws_\w+", r"\bazure_\w+", r"\bgcp_\w+",
    r"\bamazon\s+\w", r"\belasticache\b", r"\bdynamo\b",
    r"\bec2\b", r"\bs3\b", r"\brds\b",   # exatos com word-boundary
]

# Padroes sinteticos (penalizam o score)
SYNTHETIC_PATTERNS = [
    # PlantUML benchmark: nomes de arquivo com hash numerico
    r"(act|seq)\d{6,}",
    # Conteudo PlantUML sintetico: labels sem sentido
    r":\w+\s+\w+;\s*<<(task|procedure|continuous)>>",
    r"if\s*\([a-z]+ [a-z]+\?",
    # Palavras tipicas dos datasets sinteticos
    r"\b(peroxide|collapses|bamboozled|redundancies|manatees|necromancer"
    r"|stoolie|cupcakes|sabotage|conspiring|systolic|torpedo"
    r"|baited|drowsy|judicial|canyon|crock|singers)\b",
]


def compile_patterns(patterns):
    return [re.compile(p, re.IGNORECASE) for p in patterns]

SECURITY_RE   = compile_patterns(SECURITY_TERMS_EXACT)
SYNTHETIC_RE  = compile_patterns(SYNTHETIC_PATTERNS)


def collect_files_limited(dataset_dir, limit):
    files = []
    for root, dirs, filenames in os.walk(dataset_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fname in filenames:
            if not fname.startswith("."):
                files.append(Path(root) / fname)
                if len(files) >= limit:
                    return files
    return files


def read_text_sample(path, max_bytes=3000):
    try:
        return path.read_bytes()[:max_bytes].decode("utf-8", errors="ignore")
    except Exception:
        return ""


def score_content(text):
    """Score semantico: +1 por termo de seguranca, -2 por indicador sintetico."""
    score  = sum(1 for r in SECURITY_RE  if r.search(text))
    score -= sum(2 for r in SYNTHETIC_RE if r.search(text))
    return score


def analyze_dataset(dataset_dir):
    all_files = collect_files_limited(dataset_dir, MAX_FILES_TO_SCAN)
    total = len(all_files)

    if total == 0:
        return {"total": 0, "sampled": 0, "score": 0, "relevant": False,
                "reason": "Vazio", "extensions": {}, "evidence": []}

    sample = random.sample(all_files, min(SAMPLE_SIZE, total))

    total_score  = 0
    positive_hits = 0
    extensions   = {}
    evidence     = []

    TEXT_EXTS = {".txt", ".json", ".xml", ".plantuml", ".puml",
                 ".py", ".dot", ".svg", ".md"}

    for f in sample:
        ext = f.suffix.lower()
        extensions[ext] = extensions.get(ext, 0) + 1

        # Analisa conteudo textual
        content_score = 0
        if ext in TEXT_EXTS:
            content = read_text_sample(f)
            content_score = score_content(content)
            matched = [r.pattern for r in SECURITY_RE if r.search(content)]
            if matched and content_score > 0:
                evidence.append("{}: {}".format(f.name, matched[:3]))

        # Analisa o path (nome de pastas/arquivo indica contexto)
        path_text = str(f)
        path_score = score_content(path_text)

        file_score = content_score + path_score
        total_score += file_score
        if file_score > 0:
            positive_hits += 1

    relevant = total_score >= MIN_SCORE_TO_ACCEPT
    reason = (
        "Score={}, {}/{} arquivos positivos".format(total_score, positive_hits, len(sample))
        if relevant
        else "Score={}, conteudo nao relacionado a STRIDE/seguranca".format(total_score)
    )

    return {
        "total": total,
        "sampled": len(sample),
        "score": total_score,
        "relevant": relevant,
        "reason": reason,
        "extensions": extensions,
        "evidence": evidence[:5],
    }


def segregate_datasets(dry_run=False):
    print("=" * 65)
    print("  Dataset Segregation -- Metodologia STRIDE")
    print("=" * 65)

    if not RAW_DIR.exists():
        print("[ERRO] Diretorio nao encontrado: {}".format(RAW_DIR))
        return

    if not dry_run:
        REFINED_DIR.mkdir(exist_ok=True)
        REFUSED_DIR.mkdir(exist_ok=True)

    results = {}

    for dataset_path in sorted(RAW_DIR.iterdir()):
        if not dataset_path.is_dir():
            continue

        print("\n" + "-" * 55)
        print("  Analisando: {}".format(dataset_path.name))
        print("-" * 55)

        analysis = analyze_dataset(dataset_path)
        results[dataset_path.name] = analysis

        print("  Arquivos escaneados : {:,}".format(analysis["total"]))
        print("  Amostrados          : {}".format(analysis["sampled"]))
        print("  Score STRIDE        : {}".format(analysis["score"]))
        print("  Extensoes           : {}".format(dict(list(analysis["extensions"].items())[:6])))
        if analysis["evidence"]:
            print("  Evidencias          :")
            for ev in analysis["evidence"]:
                print("    * {}".format(ev))

        label = "[OK] RELEVANTE -> data_refined" if analysis["relevant"] else "[NO] RECUSADO  -> data_refused"
        print("  Decisao             : {}".format(label))
        print("  Motivo              : {}".format(analysis["reason"]))

        if not dry_run:
            dest_base = REFINED_DIR if analysis["relevant"] else REFUSED_DIR
            dest = dest_base / dataset_path.name
            if dest.exists():
                shutil.rmtree(dest)
            print("  Movendo para: {}".format(dest))
            shutil.move(str(dataset_path), str(dest))

    print("\n" + "=" * 65)
    print("  RESUMO FINAL")
    print("=" * 65)

    refined = [k for k, v in results.items() if v["relevant"]]
    refused = [k for k, v in results.items() if not v["relevant"]]

    print("\n  data_refined ({} dataset(s)):".format(len(refined)))
    for name in refined:
        print("    [OK] {}  ({:,} arquivos)".format(name, results[name]["total"]))

    print("\n  data_refused ({} dataset(s)):".format(len(refused)))
    for name in refused:
        print("    [NO] {}  ({:,} arquivos)".format(name, results[name]["total"]))

    status = "[DRY-RUN] Nenhum arquivo foi movido." if dry_run else "Segregacao concluida com sucesso."
    print("\n  " + status)
    print("=" * 65)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Segrega datasets para STRIDE.")
    parser.add_argument("--dry-run", action="store_true", help="Simula sem mover.")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    random.seed(args.seed)
    segregate_datasets(dry_run=args.dry_run)
