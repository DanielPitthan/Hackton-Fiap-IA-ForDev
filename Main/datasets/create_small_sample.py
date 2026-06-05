"""
create_small_sample.py
──────────────────────
Cria a pasta data_refined_small_sample com 20% dos arquivos de data_refined,
preservando a estrutura de subpastas.

Execute diretamente no Windows para melhor desempenho:
    python create_small_sample.py

Flags opcionais:
    --seed N     Semente aleatória (default: 42, para reprodutibilidade)
    --pct  N     Percentual a copiar (default: 20)
    --force      Recria do zero mesmo que a pasta já exista
"""

import os
import shutil
import random
import argparse
from pathlib import Path

# ── Configuração ─────────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).parent
REFINED_DIR = SCRIPT_DIR / "data_refined"
SAMPLE_DIR  = SCRIPT_DIR / "data_refined_small_sample"


def collect_files(base_dir: Path) -> list[Path]:
    """Coleta todos os arquivos ignorando .git e arquivos ocultos."""
    files = []
    for root, dirs, fnames in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in fnames:
            if not f.startswith("."):
                files.append(Path(root) / f)
    return files


def create_sample(pct: float = 0.20, seed: int = 42, force: bool = False) -> None:
    random.seed(seed)

    if not REFINED_DIR.exists():
        print(f"[ERRO] Pasta não encontrada: {REFINED_DIR}")
        return

    if SAMPLE_DIR.exists() and not force:
        existing = sum(1 for _ in SAMPLE_DIR.rglob("*") if _.is_file())
        print(f"[INFO] {SAMPLE_DIR.name} já existe com {existing:,} arquivos.")
        print("       Use --force para recriar do zero.")
        return

    if SAMPLE_DIR.exists() and force:
        print(f"[INFO] Removendo {SAMPLE_DIR.name}...")
        shutil.rmtree(SAMPLE_DIR)

    SAMPLE_DIR.mkdir()

    print(f"Coletando arquivos de {REFINED_DIR.name}...")
    all_files = collect_files(REFINED_DIR)
    total     = len(all_files)
    sample_n  = max(1, round(total * pct))

    print(f"Total em data_refined   : {total:,}")
    print(f"Percentual              : {pct*100:.0f}%")
    print(f"Arquivos a copiar       : {sample_n:,}")
    print("Copiando...", flush=True)

    sample = random.sample(all_files, sample_n)

    copied  = 0
    errors  = 0
    for i, src in enumerate(sample, 1):
        dest = SAMPLE_DIR / src.relative_to(REFINED_DIR)
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(src, dest)
            copied += 1
        except Exception as e:
            errors += 1
            print(f"  [WARN] {src.name}: {e}")

        if i % 500 == 0:
            print(f"  {i:,}/{sample_n:,} copiados...", flush=True)

    print(f"\nConcluído!")
    print(f"  Copiados  : {copied:,}")
    if errors:
        print(f"  Erros     : {errors:,}")

    # Resumo por subpasta
    print("\nArquivos por subpasta em data_refined_small_sample:")
    for sub in sorted(SAMPLE_DIR.iterdir()):
        if sub.is_dir():
            n = sum(1 for f in sub.rglob("*") if f.is_file())
            print(f"  {sub.name:40s}: {n:,}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cria amostra de 20% do data_refined.")
    parser.add_argument("--seed",  type=int,   default=42,   help="Semente aleatória")
    parser.add_argument("--pct",   type=float, default=20.0, help="Percentual (ex: 20)")
    parser.add_argument("--force", action="store_true",      help="Recriar do zero")
    args = parser.parse_args()

    create_sample(pct=args.pct / 100, seed=args.seed, force=args.force)
