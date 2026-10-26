import os
import time
from html import escape
from urllib.parse import urlparse

import streamlit as st

from src.search_engine import SearchEngine

DATASET_PATH = "data/dataset_preprocessed.csv"
SNIPPET_MAX_CHARS = 240

# ---------------------------------------------------------------------------
# Konfigurasi halaman
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Mesin Pencari Teknologi",
    page_icon="🔍",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Gaya (mengikuti tema terang/gelap Streamlit lewat warna turunan)
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --accent: #3b6fd8;
    --accent-soft: rgba(59, 111, 216, 0.12);
    --line: rgba(128, 128, 128, 0.28);
    --muted-opacity: 0.68;
}

html, body, [class*="st-"], .stApp {
    font-family: 'Inter', -apple-system, 'Segoe UI', Roboto, sans-serif;
}

/* Rapikan chrome bawaan Streamlit */
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 3rem; padding-bottom: 4rem; max-width: 760px; }

/* Header */
.app-title {
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin: 0 0 0.35rem 0;
    line-height: 1.2;
}
.app-subtitle {
    font-size: 0.95rem;
    opacity: var(--muted-opacity);
    margin: 0 0 1.75rem 0;
    line-height: 1.5;
}

/* Form pencarian */
[data-testid="stForm"] {
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 1.25rem 1.25rem 0.75rem 1.25rem;
}
[data-testid="stForm"] button[kind="primaryFormSubmit"],
[data-testid="stForm"] button[kind="primary"] {
    background-color: var(--accent);
    border-color: var(--accent);
    color: #fff;
    font-weight: 600;
}
[data-testid="stForm"] button[kind="primaryFormSubmit"]:hover,
[data-testid="stForm"] button[kind="primary"]:hover {
    filter: brightness(1.08);
    border-color: var(--accent);
}
input:focus-visible, button:focus-visible, a:focus-visible {
    outline: 2px solid var(--accent) !important;
    outline-offset: 2px;
}

/* Ringkasan hasil */
.summary {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 0.25rem 1rem;
    font-size: 0.875rem;
    margin: 1.75rem 0 1rem 0;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--line);
}
.summary .muted { opacity: var(--muted-opacity); }
.summary code {
    background: var(--accent-soft);
    color: inherit;
    padding: 0.1rem 0.4rem;
    border-radius: 4px;
    font-size: 0.8125rem;
}

/* Kartu hasil */
.result {
    padding: 1rem 0 1.1rem 0;
    border-bottom: 1px solid var(--line);
}
.result:last-child { border-bottom: none; }
.result-url {
    font-size: 0.8125rem;
    opacity: var(--muted-opacity);
    margin-bottom: 0.15rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.result-title {
    display: inline-block;
    font-size: 1.125rem;
    font-weight: 600;
    line-height: 1.35;
    color: var(--accent) !important;
    text-decoration: none !important;
    margin-bottom: 0.3rem;
}
.result-title:hover { text-decoration: underline !important; }
.result-snippet {
    font-size: 0.9rem;
    line-height: 1.6;
    opacity: 0.85;
    margin-bottom: 0.65rem;
    max-width: 68ch;
}
.result-meta {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 0.8125rem;
}
.result-meta .muted { opacity: var(--muted-opacity); }
.score-bar {
    flex: 0 0 96px;
    height: 6px;
    border-radius: 3px;
    background: var(--accent-soft);
    overflow: hidden;
}
.score-bar > span {
    display: block;
    height: 100%;
    background: var(--accent);
    border-radius: 3px;
}
.score-value { font-variant-numeric: tabular-nums; font-weight: 600; }

/* Keadaan kosong */
.empty {
    text-align: center;
    padding: 2.5rem 1rem;
    opacity: var(--muted-opacity);
    font-size: 0.9rem;
    line-height: 1.6;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    '<h1 class="app-title">Mesin Pencari Teknologi</h1>'
    '<p class="app-subtitle">Temukan dokumen berdasarkan kata kunci. '
    "Pilih peringkat TF-IDF dengan Cosine Similarity atau Okapi BM25.</p>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Pemeriksaan dataset
# ---------------------------------------------------------------------------
if not os.path.exists(DATASET_PATH):
    st.error(
        f"File `{DATASET_PATH}` tidak ditemukan. "
        "Jalankan script preprocessing dan indexing dari terminal, lalu muat ulang halaman."
    )
    st.stop()


@st.cache_resource(show_spinner="Memuat indeks pencarian...")
def load_search_engine():
    return SearchEngine(DATASET_PATH)


engine = load_search_engine()

# ---------------------------------------------------------------------------
# Form pencarian (tekan Enter atau klik Cari)
# ---------------------------------------------------------------------------
with st.form("search_form", border=False):
    query = st.text_input(
        "Kata kunci",
        placeholder="Contoh: kecerdasan buatan, keamanan siber, internet of things",
        help="Query diproses otomatis: case folding, penghapusan stopword, dan stemming.",
    )

    col_method, col_topk = st.columns([3, 2], gap="large")
    with col_method:
        method = st.radio(
            "Algoritma peringkat",
            ["TF-IDF + Cosine", "BM25"],
            horizontal=True,
        )
    with col_topk:
        top_k = st.slider("Jumlah hasil", min_value=1, max_value=20, value=10)

    search_clicked = st.form_submit_button(
        "Cari", type="primary", use_container_width=True
    )

# ---------------------------------------------------------------------------
# Proses & tampilan hasil
# ---------------------------------------------------------------------------
if not search_clicked:
    st.markdown(
        '<div class="empty">Masukkan kata kunci di atas untuk mulai mencari.</div>',
        unsafe_allow_html=True,
    )
elif not query.strip():
    st.warning("Kata kunci masih kosong. Ketik minimal satu kata untuk mencari.")
else:
    start = time.perf_counter()
    clean_q, results = engine.search(query, method=method, top_k=top_k)
    elapsed = time.perf_counter() - start

    score_label = "Cosine" if "TF-IDF" in method else "BM25"

    if not results:
        st.markdown(
            f'<div class="empty">Tidak ada dokumen yang cocok dengan '
            f"<b>{escape(query)}</b>.<br>Coba kata kunci lain yang lebih umum.</div>",
            unsafe_allow_html=True,
        )
    else:
        # Ringkasan
        st.markdown(
            '<div class="summary">'
            f'<span><b>{len(results)}</b> hasil dalam {elapsed:.3f} detik</span>'
            f'<span class="muted">Query diproses: <code>{escape(str(clean_q))}</code></span>'
            "</div>",
            unsafe_allow_html=True,
        )

        # Skor tertinggi dipakai sebagai acuan panjang bar
        max_score = max((r["score"] for r in results), default=0) or 1

        cards = []
        for i, res in enumerate(results, 1):
            url = str(res["url"])
            host = urlparse(url).netloc or url
            title = escape(str(res["title"]))
            snippet = str(res["snippet"])
            if len(snippet) > SNIPPET_MAX_CHARS:
                snippet = snippet[:SNIPPET_MAX_CHARS].rsplit(" ", 1)[0] + "..."
            width = max(0.0, min(100.0, res["score"] / max_score * 100))

            cards.append(
                '<div class="result">'
                f'<div class="result-url">{escape(host)}</div>'
                f'<a class="result-title" href="{escape(url, quote=True)}" '
                f'target="_blank" rel="noopener noreferrer">{title}</a>'
                f'<div class="result-snippet">{escape(snippet)}</div>'
                '<div class="result-meta">'
                f'<span class="score-bar"><span style="width:{width:.0f}%"></span></span>'
                f'<span class="score-value">{res["score"]:.4f}</span>'
                f'<span class="muted">Skor {score_label}</span>'
                f'<span class="muted">Dokumen {escape(str(res["doc_id"]))}</span>'
                "</div>"
                "</div>"
            )

        st.markdown("".join(cards), unsafe_allow_html=True)