# analyzer.py
import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

nlp = spacy.load("en_core_web_sm")

def summarize_text(text, sentence_count=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)

def extract_entities(text):
    doc = nlp(text)
    entities = {"PERSON": set(), "ORG": set(), "GPE": set(), "DATE": set()}
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].add(ent.text)
    # Convert sets to lists for JSON compatibility
    return {k: list(v) for k, v in entities.items()}

def analyze_text(text):
    return {
        "summary": summarize_text(text),
        "important_entities": extract_entities(text)
    }
from pdf_reader import extract_text_from_pdf

if __name__ == "__main__":
    pdf_path = r"C:\Users\HP\smart-text-analyzer\docs\sample.pdf"  # make sure you have a sample PDF here
    text = extract_text_from_pdf(pdf_path)
    result = analyze_text(text)
    print("Summary:\n", result["summary"])
    print("\nEntities:\n", result["important_entities"])