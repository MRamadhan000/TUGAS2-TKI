import pandas as pd
import json
import os
from collections import defaultdict

def build_inverted_index(csv_path, output_json_path):
    df = pd.read_csv(csv_path)
    inverted_index = defaultdict(list)
    
    for idx, row in df.iterrows():
        doc_id = row['doc_id'] if 'doc_id' in df.columns else f"D{idx+1}"
        content = str(row['clean_content'])
        tokens = content.split()
        
        term_freqs = defaultdict(int)
        for token in tokens:
            term_freqs[token] += 1
            
        for term, freq in term_freqs.items():
            inverted_index[term].append({
                "doc_id": doc_id,
                "tf": freq
            })
            
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(inverted_index, f, ensure_ascii=False, indent=4)
        
    print(f"Inverted index berhasil dibuat dan disimpan di {output_json_path}")
    return inverted_index

if __name__ == "__main__":
    build_inverted_index("data/dataset_preprocessed.csv", "index/inverted_index.json")