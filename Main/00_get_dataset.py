import os, io, zipfile, subprocess, requests
import pandas as pd
from datasets import load_dataset

ROOT = "arch_diagram_corpus"
os.makedirs(ROOT, exist_ok=True)

# 1) Figshare architectural pattern images (CC BY 4.0) -> sample a subset
fig_zip = requests.get("https://ndownloader.figshare.com/files/27948726", timeout=120)
with zipfile.ZipFile(io.BytesIO(fig_zip.content)) as z:
    names = z.namelist()
    # keep ~100 images from threat-relevant patterns
    wanted = [n for n in names if any(p in n.lower() for p in
              ["microservice", "client", "rest", "layered", "broker"])][:100]
    for n in wanted:
        z.extract(n, os.path.join(ROOT, "figshare_patterns"))

# 2) OWASP Threat Model Cookbook (CC-BY 4.0 / Apache-2.0): DFDs + source
subprocess.run(["git", "clone", "--depth", "1",
    "https://github.com/OWASP/threat-model-cookbook.git",
    os.path.join(ROOT, "owasp_cookbook")], check=True)

# 3) OWASP Threat Dragon sample models (JSON annotations)
subprocess.run(["git", "clone", "--depth", "1",
    "https://github.com/jgadsden/owasp-threat-dragon-models.git",
    os.path.join(ROOT, "threat_dragon_models")], check=True)

print("Corpus assembled under", ROOT)

# 1. Hugging Face Datasets
print("Obtendo datasets do Hugging Face...")

# Baixa o DiagramBank, que contém os diagramas científicos e metadados
diagram_bank = load_dataset("zhangt20/DiagramBank")
print("DiagramBank carregado com sucesso!")

# Baixa o UML-Generator-Dataset-DeepSeek-V3.2 focado em prompts para geração de código
uml_deepseek = load_dataset("sequelbox/UML-Generator-Dataset-DeepSeek-V3.2")
print("DeepSeek UML Dataset carregado com sucesso!")
# 2. Kaggle (Software Architecture Dataset focado em nuvem)
print("\nBaixando dataset do Kaggle (Cloud Components)...")
# O comando fará o download da base e extração automática dos arquivos Pascal VOC XML e PNGs
os.system("kaggle datasets download -d carlosrian/software-architecture-dataset -p./kaggle_cloud_dataset --unzip")
print("Dataset do Kaggle baixado com sucesso!")
# 3. Zenodo (Synthetic UML Diagram Dataset - PlantUML)
print("\nBaixando dataset PlantUML do Zenodo (Aviso: O arquivo pesa 12.3 GB e pode demorar)...")
zenodo_url = "https://zenodo.org/records/15103682/files/PlantUML_Data_bundle.zip?download=1"
response = requests.get(zenodo_url, stream=True)

with open("PlantUML_Data_bundle.zip", "wb") as file:
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            file.write(chunk)
print("Pacote PlantUML baixado com sucesso!")
# 4. Leitura tabular via Pandas (XML-based-UML-models-dataset da J. Pecuchova)
print("\nDemonstração de leitura do dataset educacional de UML via Pandas...")
# Assumindo que o arquivo CSV extraído foi salvo no mesmo diretório
try:
    # O arquivo é separado por vírgulas e usa codificação UTF-8 padrão
    student_df = pd.read_csv("student_data25.csv", sep=',')
    print(student_df.head())
except FileNotFoundError:
    print("Arquivo 'student_data25.csv' não encontrado. É preciso baixá-lo do repositório para testar a leitura tabular.")