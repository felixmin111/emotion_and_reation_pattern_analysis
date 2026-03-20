import spacy
from sentence_transformers import SentenceTransformer

nlp = spacy.load("en_core_web_sm")
embedder = SentenceTransformer("all-MiniLM-L6-v2")