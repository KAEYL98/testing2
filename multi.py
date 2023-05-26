import multiprocessing
import sys
from presidio_analyzer import AnalyzerEngine, recognizer_result
from timeit import default_timer as timer

# Set up the engine, loads the NLP module (spaCy model by default) and other PII recognizers`b`
analyzer = AnalyzerEngine()

# entities to be detected
entities = [
    "PERSON",
    "PHONE_NUMBER",
    "NRP",
    "EMAIL_ADDRESS",
    "IBAN_CODE",
    "CREDIT_CARD",
    "LOCATION",
    "IP_ADDRESS",
    "URL"
]


text = [
    "My name is Andrew and my phone number is 212-555-5555",
    "I'm located at 71 Makati Avenue",
    "Here is my credit card number 5555-5537-5304-8194"
]

text *= 10000
text = text[:10000]

def format_results(text:str, results:list[recognizer_result.RecognizerResult]):
    for result in results:
        entity = text[result.start: result.end]


def detect_pii(text: str):
    results = analyzer.analyze(text,
                            entities=entities,
                            language='en')
    format_results(text ,results)


if __name__ == "__main__":

    start = timer()
    print(len(sys.argv))

    if len(sys.argv) == 1:
        with multiprocessing.Pool() as pool:
            pool.map(detect_pii, text)
    elif sys.argv[1] == '1':
        for i in text:
            detect_pii(i)
    else:
        with multiprocessing.Pool(int(sys.argv[1])) as pool:
            pool.map(detect_pii, text)
    
    end = timer()

    print("Program finished!")
    print(end-start)