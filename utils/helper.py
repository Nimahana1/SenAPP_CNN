"""
helper.py

Utility umum aplikasi SenAPP
"""

from __future__ import annotations

import random
from pathlib import Path

import streamlit as st
import pandas as pd

from utils.interpret import CATEGORY_KEYWORDS, WORDCLOUD_EXTRA_KEYWORDS


# ======================================================
# CSS
# ======================================================

def load_css(css_file: str | Path) -> None:
    """
    Memuat file CSS.
    """

    css_path = Path(css_file)

    if css_path.exists():

        with open(css_path, encoding="utf-8") as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True,
            )


# ======================================================
# Number
# ======================================================

def format_number(number: int) -> str:
    """
    Format angka ribuan.

    Contoh
    -------
    10000 -> 10.000
    """

    return f"{number:,}".replace(",", ".")


# ======================================================
# Percentage
# ======================================================

def calculate_percentage(value: int, total: int) -> float:
    """
    Menghitung persentase.
    """

    if total == 0:

        return 0.0

    return round((value / total) * 100, 2)


# ======================================================
# Random Review
# ======================================================

def random_reviews(
    dataframe: pd.DataFrame,
    label_column: str,
    label_value: str,
    n: int = 5,
) -> pd.DataFrame:
    """
    Mengambil review acak.
    """

    sample = dataframe[
        dataframe[label_column] == label_value
    ]

    if len(sample) <= n:

        return sample

    return sample.sample(
        n=n,
        random_state=random.randint(1, 9999),
    )


# ======================================================
# Session State
# ======================================================

def initialize_session_state() -> None:
    """
    Inisialisasi Session State.
    """

    defaults = {

        # Halaman aktif
        "selected_page": "Dashboard",

        # Hasil prediksi
        "prediction_result": None,

        # Confidence prediksi
        "confidence": None,

        # Input pengguna
        "user_input": "",

        # Seed untuk memilih contoh ulasan secara acak
        "review_seed": 42,

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value

def image_to_base64(image_path: Path) -> str:
    """
    Mengubah gambar menjadi Base64 agar dapat
    ditampilkan melalui HTML.
    """
    import base64

    with open(image_path, "rb") as image:
        return base64.b64encode(image.read()).decode()
    
def get_sentiment_statistics(
    dataframe: pd.DataFrame,
    label_column: str = "Sentimen",
) -> dict:
    """
    Menghasilkan statistik utama dashboard.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Dataset hasil labeling.

    label_column : str
        Nama kolom sentimen.

    Returns
    -------
    dict
        Statistik jumlah ulasan.
    """

    sentiment = dataframe[label_column].value_counts()

    return {
        "total": len(dataframe),
        "positive": sentiment.get("Positive", 0),
        "negative": sentiment.get("Negative", 0),
    }

def get_sample_reviews(
    labeling_df: pd.DataFrame,
    seed: int = 42,
    n: int = 5,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Mengambil contoh ulasan positif dan negatif secara acak.

    NOTE: Sebelumnya fungsi ini menerima `reviews_df` terpisah
    lalu menempelkan kolom "Sentimen" dari `labeling_df` secara
    POSISIONAL (`dataframe["Sentimen"] = labeling_df["Sentimen"]`).
    Ini hanya valid jika kedua dataframe punya urutan baris yang
    identik persis - begitu jumlah/urutan baris sedikit berbeda
    (mis. ada baris yang ter-drop saat preprocessing/labeling),
    kolom Sentimen jadi salah pasang dengan ulasan yang salah.

    labeling_df sendiri sudah memiliki kolom "Review Text" dan
    "Sentimen" yang berpasangan dengan benar pada baris yang sama,
    jadi tidak perlu lagi digabung dengan dataset lain.
    """

    positive = labeling_df[labeling_df["Sentimen"] == "Positive"]

    negative = labeling_df[labeling_df["Sentimen"] == "Negative"]

    positive_sample = positive.sample(
        n=min(n, len(positive)),
        random_state=seed,
    )

    negative_sample = negative.sample(
        n=min(n, len(negative)),
        random_state=seed,
    )

    return positive_sample, negative_sample


# ======================================================
# Category Keyword Filter (untuk WordCloud Insight)
# ======================================================

def get_category_keyword_set(sentiment: str) -> set[str]:
    """
    Menggabungkan seluruh keyword dari semua kategori
    insight (Grafis, Gameplay, Musik, dst) milik satu
    sentimen, DITAMBAH kata tambahan khusus WordCloud
    (WORDCLOUD_EXTRA_KEYWORDS), menjadi satu set kata
    tunggal.

    Kata tambahan ini sengaja tidak dipakai pada
    detect_category() (klasifikasi kategori di halaman
    Prediksi Sentimen) agar akurasi klasifikasi tidak
    terpengaruh oleh kata-kata generik. Di sini aman
    karena hanya untuk memperkaya tampilan WordCloud.

    Frasa multi-kata seperti "tidak nyaman" atau
    "gak dapet" dipecah menjadi kata-kata terpisah
    agar bisa dicocokkan per token hasil stemming.
    """

    categories = CATEGORY_KEYWORDS.get(sentiment, {})

    extra_words = WORDCLOUD_EXTRA_KEYWORDS.get(sentiment, [])

    keywords: set[str] = set()

    for word_list in categories.values():

        for phrase in word_list:

            for word in phrase.split():

                keywords.add(word.lower())

    for phrase in extra_words:

        for word in phrase.split():

            keywords.add(word.lower())

    return keywords


def filter_category_words(text: str, sentiment: str) -> str:
    """
    Menyaring sebuah teks agar hanya menyisakan kata-kata
    yang termasuk dalam daftar keyword kategori insight
    (Positive/Negative), sehingga WordCloud hanya
    menampilkan kata yang relevan dengan kategori insight,
    bukan seluruh isi ulasan.
    """

    keywords = get_category_keyword_set(sentiment)

    words = text.split()

    filtered = [
        word
        for word in words
        if word.lower() in keywords
    ]

    return " ".join(filtered)