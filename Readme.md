# Mesin Pencari Sederhana (Information Retrieval System)

**Mata Kuliah:** Temu Kembali Informasi — Tugas 2

## 📖 Deskripsi Proyek

Proyek ini merupakan implementasi sistem *Classical Information Retrieval* (IR) menggunakan Python. Sistem dirancang untuk mencari dan menentukan peringkat dokumen berdasarkan relevansi terhadap query pengguna.

Metode dan fitur yang diimplementasikan meliputi:

- **Text Preprocessing:** *Case folding*, pembersihan karakter, *stopword removal*, dan *stemming* menggunakan Sastrawi.
- **Inverted Index:** Struktur indeks yang memetakan setiap term ke daftar dokumen beserta nilai *Term Frequency* (TF).
- **Boolean Retrieval:** Pencarian dokumen menggunakan operator Boolean.
- **TF-IDF + Cosine Similarity:** Pembobotan term dan pengukuran kemiripan antara query dengan dokumen.
- **BM25:** Pemeringkatan dokumen menggunakan algoritma Okapi BM25.
- **Evaluation:** Pengujian relevansi hasil pencarian menggunakan Precision, Recall, dan F1-score.
- **User Interface:** Antarmuka pencarian interaktif menggunakan Streamlit.

## 📁 Struktur Folder Proyek

```text
tugas2_ir/
├── data/
│   ├── dataset_teknologi.csv
│   └── dataset_preprocessed.csv
├── index/
│   └── inverted_index.json
├── src/
│   ├── preprocessing.py
│   ├── indexing.py
│   ├── boolean_retrieval.py
│   ├── tfidf_retrieval.py
│   ├── bm25.py
│   └── search_engine.py
├── evaluation/
│   └── queries.csv
├── app.py
└── README.md
```

### Penjelasan Struktur Folder

| File/Folder | Fungsi |
|---|---|
| `data/dataset_teknologi.csv` | Dataset dokumen teknologi mentah. |
| `data/dataset_preprocessed.csv` | Dataset setelah melalui tahap preprocessing. |
| `index/inverted_index.json` | Penyimpanan inverted index dalam format JSON. |
| `src/preprocessing.py` | Modul pembersihan dan preprocessing teks. |
| `src/indexing.py` | Modul pembentukan inverted index dan TF. |
| `src/boolean_retrieval.py` | Modul pencarian dengan operator Boolean. |
| `src/tfidf_retrieval.py` | Modul TF-IDF dan Cosine Similarity. |
| `src/bm25.py` | Modul pemeringkatan menggunakan Okapi BM25. |
| `src/search_engine.py` | Modul penggabung atau pengelola fungsi pencarian. |
| `evaluation/queries.csv` | Kumpulan query dan label dokumen relevan untuk evaluasi. |
| `app.py` | Antarmuka web menggunakan Streamlit. |
| `README.md` | Dokumentasi proyek. |

## ⚙️ Persyaratan Sistem

Pastikan perangkat telah memiliki:

- Python 3.9 atau versi yang kompatibel dengan seluruh dependensi.
- pip untuk menginstal pustaka Python.
- Terminal atau Command Prompt.
- Browser untuk membuka aplikasi Streamlit.

## 🚀 Panduan Menjalankan Program

Jalankan seluruh tahapan berikut secara berurutan dari direktori utama proyek.

### 1. Preprocessing

Tahap ini bertujuan membersihkan dan menormalisasi teks dokumen sebelum proses pencarian.

Jalankan:

```bash
python src/preprocessing.py
```

Tahapan preprocessing dapat meliputi:

1. Penanganan nilai kosong dan duplikat.
2. *Case folding* untuk mengubah huruf menjadi huruf kecil.
3. Pembersihan URL, angka, dan karakter khusus sesuai aturan yang digunakan.
4. Normalisasi spasi.
5. *Stopword removal* untuk menghapus kata umum yang tidak diperlukan.
6. *Stemming* untuk mengubah kata ke bentuk dasarnya menggunakan Sastrawi.

Output:

```text
data/dataset_preprocessed.csv
```

File tersebut menyimpan teks asli dan hasil preprocessing, misalnya pada kolom `content` dan `clean_content`.

### 2. Pembuatan Inverted Index

Setelah preprocessing selesai, jalankan:

```bash
python src/indexing.py
```

Tahap ini memetakan setiap term ke dokumen yang mengandung term tersebut beserta frekuensi kemunculannya.

Contoh struktur inverted index:

```json
{
    "cerdas": [
        {
            "doc_id": "D1",
            "tf": 3
        },
        {
            "doc_id": "D2",
            "tf": 1
        }
    ]
}
```

Keterangan:

- `cerdas` adalah term yang diindeks.
- `doc_id` adalah identitas dokumen.
- `tf` adalah jumlah kemunculan term di dalam dokumen.

Output:

```text
index/inverted_index.json
```

### 3. Menjalankan Aplikasi Streamlit

Setelah preprocessing dan indexing selesai, jalankan:

```bash
streamlit run app.py
```

Streamlit akan menampilkan alamat lokal pada terminal. Biasanya aplikasi dapat dibuka melalui:

```text
http://localhost:8501
```

Buka alamat tersebut di browser untuk menggunakan antarmuka mesin pencari.

Pengguna dapat memasukkan query dan melihat hasil pencarian berdasarkan metode retrieval yang tersedia pada implementasi aplikasi.

## 👤 Informasi Proyek

**Nama Proyek:** Mesin Pencari Sederhana (Information Retrieval System)  
**Mata Kuliah:** Temu Kembali Informasi  
**Tugas:** Tugas 2  
**Bahasa Pemrograman:** Python  
**Antarmuka:** Streamlit