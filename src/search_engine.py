from src.preprocessing import preprocess_text
from src.tfidf_retrieval import TFIDFRetrieval
from src.bm25 import BM25Retrieval

class SearchEngine:
    def __init__(self, csv_path):
        self.tfidf = TFIDFRetrieval(csv_path)
        self.bm25 = BM25Retrieval(csv_path)
        
    def search(self, query, method="TF-IDF + Cosine", top_k=10):
        clean_q = preprocess_text(query)
        if method == "TF-IDF + Cosine":
            results = self.tfidf.search(clean_q, top_k=top_k)
        else:
            results = self.bm25.search(clean_q.split(), top_k=top_k)
        return clean_q, results