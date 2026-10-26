import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TFIDFRetrieval:
  def __init__(self, csv_path):
    self.df = pd.read_csv(csv_path)

    self.vectorizer = TfidfVectorizer()

    # 3. Membangun Vector Space Model (VSM) untuk seluruh korpus dokumen
    self.doc_vectors = self.vectorizer.fit_transform(
        self.df['clean_content'].fillna('')
    )

  def search(self, query, top_k=10):
    # 4. Mengubah query teks menjadi vektor menggunakan vocabulary yang sama
    query_vector = self.vectorizer.transform([query])

    # 5. Menghitung Cosine Similarity antara vektor query dan semua vektor dokumen
    scores = cosine_similarity(query_vector, self.doc_vectors).flatten()

    # 6. Mengurutkan indeks dokumen berdasarkan skor dari yang terbesar (paling relevan)
    top_indices = scores.argsort()[::-1][:top_k]

    # 7. Menyusun daftar hasil pencarian untuk ditampilkan ke antarmuka
    results = []
    for idx in top_indices:
      # Filter hanya dokumen yang memiliki kemiripan (skor > 0)
      if scores[idx] > 0:
        results.append({
            'doc_id': self.df.iloc[idx].get('doc_id', f'D{idx+1}'),
            'title': self.df.iloc[idx]['title'],
            'url': self.df.iloc[idx]['url'],
            'score': float(scores[idx]),
            'snippet': str(self.df.iloc[idx]['content'])[:200] + '...',
        })

    return results