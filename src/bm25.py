import numpy as np
import pandas as pd
from collections import Counter
import math

class BM25Retrieval:
    def __init__(self, csv_path, k1=1.2, b=0.75):
        self.df = pd.read_csv(csv_path)
        
        # 2. Parameter tuning BM25
        self.k1 = k1  # Mengontrol saturasi Term Frequency (TF saturation)
        self.b = b    # Mengontrol tingkat penalti berdasarkan panjang dokumen (length normalization)
        
        # 3. Membentuk korpus dokumen (tokenisasi setiap teks bersih menjadi list kata)
        self.corpus = [str(text).split() for text in self.df['clean_content'].fillna('')]
        
        # 4. Menghitung panjang setiap dokumen (jumlah term) dan rata-rata panjang dokumen korpus (avgdl)
        self.doc_len = [len(doc) for doc in self.corpus]
        self.avgdl = np.mean(self.doc_len) if len(self.doc_len) > 0 else 0
        self.N = len(self.corpus)  # Total jumlah dokumen dalam korpus
        
        # 5. Menghitung Document Frequency (DF) untuk setiap term unik di seluruh korpus
        self.doc_freqs = Counter()
        for doc in self.corpus:
            for word in set(doc):  # set(doc) memastikan term unik dihitung sekali per dokumen
                self.doc_freqs[word] += 1
                
        # 6. Menghitung Inverse Document Frequency (IDF) menggunakan rumus Robertson-Spärck Jones
        self.idf = {}
        for word, freq in self.doc_freqs.items():
            # IDF memberikan bobot lebih tinggi pada kata yang jarang muncul (spesifik)
            self.idf[word] = math.log(1 + (self.N - freq + 0.5) / (freq + 0.5))

    def search(self, query_tokens, top_k=10):
        # Inisialisasi array skor bernilai 0 untuk seluruh dokumen
        scores = np.zeros(self.N)
        
        # Iterasi setiap term/kata di dalam query
        for term in query_tokens:
            if term not in self.idf:
                continue  # Lewati term jika tidak ada di dalam indeks IDF korpus
            
            idf_val = self.idf[term]
            
            # Hitung kontribusi skor term ini terhadap setiap dokumen di korpus
            for idx, doc in enumerate(self.corpus):
                tf = doc.count(term)  # Term Frequency (frekuensi kemunculan term dalam dokumen)
                
                if tf > 0:
                    dl = self.doc_len[idx]  # Panjang dokumen saat ini
                    
                    # Rumus Pembilang: Mengontrol TF Saturation dengan parameter k1
                    numerator = tf * (self.k1 + 1)
                    
                    # Rumus Penyebut: Normalisasi panjang dokumen relatif terhadap rata-rata (avgdl)
                    denominator = tf + self.k1 * (1 - self.b + self.b * (dl / self.avgdl))
                    
                    # Akumulasi skor BM25 untuk dokumen ke-idx
                    scores[idx] += idf_val * (numerator / denominator)
                    
        # Mengurutkan indeks dokumen berdasarkan skor tertinggi ke terendah
        top_indices = scores.argsort()[::-1][:top_k]
        
        # Menyusun daftar hasil pencarian Top-k
        results = []
        for idx in top_indices:
            if scores[idx] > 0:  # Hanya ambil dokumen yang memiliki skor relevansi > 0
                results.append({
                    "doc_id": self.df.iloc[idx].get('doc_id', f"D{idx+1}"),
                    "title": self.df.iloc[idx]['title'],
                    "url": self.df.iloc[idx]['url'],
                    "score": float(scores[idx]),
                    "snippet": str(self.df.iloc[idx]['content'])[:200] + "..."
                })
                
        return results