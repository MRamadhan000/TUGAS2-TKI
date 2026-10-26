import pandas as pd
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Inisialisasi satu kali agar lebih efisien
stemmer = StemmerFactory().create_stemmer()
stopword_remover = StopWordRemoverFactory().create_stop_word_remover()

def preprocess_text_with_steps(text):
    """
    Melakukan preprocessing dan mencatat setiap tahap perubahan 
    khusus untuk sampel dokumen debugging.
    """
    steps = {}
    if pd.isna(text):
        return "", {}
    
    original = str(text)
    steps['1. Raw / Original'] = original
    
    # 1. Case folding
    text_lower = original.lower()
    steps['2. Case Folding'] = text_lower
    
    # 2-5. Menghapus URL, email, mention, hashtag
    t = re.sub(r'https?://\S+|www\.\S+', ' ', text_lower)
    t = re.sub(r'\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b', ' ', t)
    t = re.sub(r'@\w+', ' ', t)
    t = re.sub(r'#(\w+)', r'\1', t)
    steps['3. Bersih URL/Mention'] = t
    
    # 6. Menghapus angka dan karakter selain huruf
    t_alpha = re.sub(r'[^a-z\s]', ' ', t)
    steps['4. Hapus Simbol & Angka'] = t_alpha
    
    # 7. Menghapus spasi berlebih
    t_space = re.sub(r'\s+', ' ', t_alpha).strip()
    steps['5. Normalisasi Spasi Awal'] = t_space
    
    if not t_space:
        return "", steps
    
    # 8. Stopword removal
    t_stop = stopword_remover.remove(t_space)
    steps['6. Stopword Removal'] = t_stop
    
    # 9. Stemming bahasa Indonesia
    t_stem = stemmer.stem(t_stop)
    steps['7. Stemming'] = t_stem
    
    # 10. Normalisasi spasi akhir
    final_text = re.sub(r'\s+', ' ', t_stem).strip()
    steps['8. Final Clean'] = final_text
    
    return final_text, steps

def preprocess_text(text):
    """Fungsi utama untuk processing massal ke dataframe."""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    text = re.sub(r'\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b', ' ', text)
    text = re.sub(r'@\w+', ' ', text)
    text = re.sub(r'#(\w+)', r'\1', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    if not text:
        return ""
    text = stopword_remover.remove(text)
    text = stemmer.stem(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_dataset(input_path, output_path, limit=None):
    print(f"Membaca dataset dari {input_path}...")
    df = pd.read_csv(input_path)
    
    if 'content' not in df.columns:
        raise ValueError("Kolom 'content' tidak ditemukan dalam dataset.")
        
    df = df.dropna(subset=['content']).copy()
    df['content'] = df['content'].astype(str)
    df = df.drop_duplicates(subset=['content']).copy()
    df = df[df['content'].str.strip() != ''].copy()
    
    if limit is not None and limit > 0:
        df = df.head(limit).copy()
        print(f"[INFO] Limit aktif: {len(df)} dokumen akan diproses.")
        
    total_docs = len(df)
    if total_docs == 0:
        print("Dataset kosong. Tidak ada dokumen untuk diproses.")
        df['clean_content'] = pd.Series(dtype='object')
        df.to_csv(output_path, index=False)
        return df

    # Ambil 1 sampel teks mentah pertama dan ambil kalimat pertamanya saja agar rapi
    raw_sample_full = df['content'].iloc[0]
    # Ambil kalimat pertama (berdasarkan tanda titik atau batasan 150 karakter)
    sample_sentence = raw_sample_full.split('.')[0] if '.' in raw_sample_full else raw_sample_full[:150]

    print(f"\nMenjalankan prapemrosesan bertahap pada 1 sampel kalimat:\n> \"{sample_sentence}\"\n")
    
    # Jalankan simulasi step-by-step untuk sampel
    _, sample_steps = preprocess_text_with_steps(sample_sentence)
    
    # Tampilkan dalam bentuk tabel rapi di terminal menggunakan Pandas DataFrame
    table_data = [{"Tahap Preprocessing": tahap, "Hasil Teks": hasil} for tahap, hasil in sample_steps.items()]
    df_table = pd.DataFrame(table_data)
    
    print("=" * 80)
    print(" TABEL DEBUGGING TAHAPAN PREPROCESSING (1 KALIMAT SAMPEL)")
    print("=" * 80)
    print(df_table.to_string(index=False))
    print("=" * 80)

    print(f"\nMemproses seluruh {total_docs} dokumen...")
    print("-" * 50)
    
    clean_contents = []
    for idx, row in enumerate(df.itertuples(index=False), start=1):
        cleaned_text = preprocess_text(row[df.columns.get_loc('content')])
        clean_contents.append(cleaned_text)
        doc_id = getattr(row, 'doc_id', 'N/A')
        print(f"[{idx}/{total_docs}] Selesai memproses dokumen ID: {doc_id}")
        
    df['clean_content'] = clean_contents
    
    df.to_csv(output_path, index=False)
    print(f"\nDataset berhasil disimpan ke: {output_path}")
    print(f"Total dokumen diproses: {total_docs}")
    
    return df

if __name__ == "__main__":
    LIMIT_DOCS = None  # Diatur kecil dulu agar tabel debug sampel langsung terlihat jelas
    process_dataset(
        input_path="data/dataset_teknologi.csv",
        output_path="data/dataset_preprocessed.csv",
        limit=LIMIT_DOCS
    )