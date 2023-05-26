from multiprocessing import Pool
from tqdm import tqdm
import sys
from presidio_analyzer import AnalyzerEngine, recognizer_result
import glob
import os
import csv

CWD = os.getcwd()
FILE_PATH = os.path.join(CWD, "DOCS")
OUT_PATH = os.path.join(CWD, "REFS")
OUT_NER_PATH = os.path.join(OUT_PATH, "ner.csv")
OUT_PROGRESS_PATH = os.path.join(OUT_PATH, "progress.txt")
OUT_ERROR_PATH = os.path.join(OUT_PATH, "error.txt")


# Set up the engine, loads the NLP module (spaCy model by default) and other PII recognizers`b`
analyzer = AnalyzerEngine()

# entities to be detected
entities = [
    "PERSON",
    "PHONE_NUMBER",
    "CRYPTO",
    "NRP",
    "EMAIL_ADDRESS",
    "IBAN_CODE",
    "CREDIT_CARD",
    "LOCATION",
    "IP_ADDRESS",
    "URL"
]

def get_file_paths(root_path:str = FILE_PATH) -> list[str]:
    search = os.path.join(root_path, "*.txt")
    paths = glob.glob(search)
    return paths


def format_results(input_path:str, text:str, results:list[recognizer_result.RecognizerResult]):
    for result in results:
        base_name = os.path.basename(input_path)
        path_id = base_name.removesuffix('.txt')
        entity = text[result.start: result.end]
        entity_type = result.entity_type
        score = result.score
        data = [path_id, entity, entity_type, score]
        with open(OUT_NER_PATH, 'a', encoding='UTF8') as f:
            # write the data
            writer = csv.writer(f)
            writer.writerow(data)   


def read_text(path: str) -> str:
    with open(path, 'r') as f:
        data = f.read()
    
    data = "".join(data.splitlines())
    return data

def detect_pii(path: str):
    try:
        text = read_text(path)
        results = analyzer.analyze(text,
                                entities=entities,
                                language='en')
        format_results(path, text, results)
        with open(OUT_PROGRESS_PATH, 'a') as f:
            f.writelines(path + "\n")
    except Exception:
        with open(OUT_ERROR_PATH, 'a') as f:
            f.writelines(path + "\n")

def read_progress():
    progress = []
    if os.path.exists(OUT_PROGRESS_PATH):
        with open(OUT_PROGRESS_PATH, 'r') as f:
            progress += f.read().splitlines()
    if os.path.exists(OUT_ERROR_PATH):
        with open(OUT_ERROR_PATH, 'r') as f:
            progress += f.read().splitlines()
    return progress

def write_header_file_ref(out_path:str = OUT_NER_PATH) -> None:
    if os.path.exists(out_path):
        return
    header = ['path_id', 'entity', 'entity_type', 'score']
    with open(out_path, 'w', encoding='UTF8') as f:
        # write the header
        writer = csv.writer(f)
        writer.writerow(header)

