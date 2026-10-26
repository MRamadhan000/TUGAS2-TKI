import json
import pandas as pd

class BooleanRetrieval:
    def __init__(self, index_path, csv_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            self.index = json.load(f)
        self.df = pd.read_csv(csv_path)
        
    def search_term(self, term):
        term = term.lower().strip()
        if term in self.index:
            return [item['doc_id'] for item in self.index[term]]
        return []