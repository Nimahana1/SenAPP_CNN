"""
utils/preprocess.py

Seluruh proses preprocessing teks sesuai notebook penelitian.
"""

from __future__ import annotations

import re
import string
from typing import Dict, List

import nltk
import pandas as pd
import streamlit as st

from nltk.tokenize import word_tokenize

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import (
    StopWordRemoverFactory,
)

import config


# ======================================================
# PASTIKAN DATA NLTK TERSEDIA
# ======================================================
# Penting untuk deployment (mis. Streamlit Community Cloud):
# environment baru tidak punya nltk_data bawaan seperti di
# laptop lokal, jadi word_tokenize() akan error kalau resource
# "punkt" belum di-download. Kode di bawah ini otomatis
# men-download-nya sekali saja kalau belum ada.

def _ensure_nltk_data() -> None:
    """Download resource NLTK yang dibutuhkan jika belum ada."""

    resources = [
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
    ]

    for path, package in resources:

        try:
            nltk.data.find(path)

        except LookupError:
            nltk.download(package, quiet=True)


_ensure_nltk_data()


# ======================================================
# LOAD NORMALIZATION DICTIONARY
# ======================================================

@st.cache_resource(show_spinner=False)
def load_normalization_dictionary() -> Dict[str, str]:
    """
    Memuat kamus kata baku.
    """

    dataframe = pd.read_excel(config.NORMALIZATION_PATH)

    return dict(
        zip(
            dataframe["tidak_baku"],
            dataframe["kata_baku"],
        )
    )


# ======================================================
# LOAD STOPWORDS
# ======================================================

@st.cache_resource(show_spinner=False)
def load_stopwords() -> set:
    """
    Memuat stopword Sastrawi + custom stopword.
    """

    factory = StopWordRemoverFactory()

    stopwords = set(factory.get_stop_words())

    stopwords.update(
        [
            "game",
            "gamenya",
            "main",
            "banget",
            "aja",
            "sih",
            "gue",
            "kayak",
            "nih",
            "dong",
            "nya",
            "yg",
            "udah",
            "sudah",
            "jadi",
            "lebih",
            "buat",
        ]
    )

    return stopwords


# ======================================================
# LOAD STEMMER
# ======================================================

@st.cache_resource(show_spinner=False)
def load_stemmer():
    """
    Membuat stemmer Sastrawi.
    """

    factory = StemmerFactory()

    return factory.create_stemmer()


# ======================================================
# CLEANING
# ======================================================

def cleaning_text(text: str) -> str:
    """
    Cleaning sesuai notebook.
    """

    text = str(text)

    text = re.sub(r"http\S+|www\S+", "", text)

    text = re.sub(r"@\w+|#\w+", "", text)

    text = re.sub(r"\d+", "", text)

    text = re.sub(r"[^\x00-\x7F]+", "", text)

    text = text.translate(
        str.maketrans(
            "",
            "",
            string.punctuation,
        )
    )

    text = re.sub(
        r"(.)\1{2,}",
        r"\1",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    ).strip()

    return text


# ======================================================
# CASE FOLDING
# ======================================================

def case_folding(text: str) -> str:
    """
    Mengubah menjadi huruf kecil.
    """

    return str(text).lower()


# ======================================================
# NORMALIZATION
# ======================================================

def normalize_text(text: str) -> str:
    """
    Normalisasi kata tidak baku.
    """

    dictionary = load_normalization_dictionary()

    words = text.split()

    normalized = [
        dictionary.get(word, word)
        for word in words
    ]

    return " ".join(normalized)


# ======================================================
# TOKENIZATION
# ======================================================

def tokenize_text(text: str) -> List[str]:
    """
    Tokenisasi menggunakan NLTK.
    """

    return word_tokenize(text)


# ======================================================
# STOPWORD REMOVAL
# ======================================================

def remove_stopwords(tokens: List[str]) -> List[str]:
    """
    Menghapus stopword.
    """

    stopwords = load_stopwords()

    return [
        word
        for word in tokens
        if word not in stopwords
    ]


# ======================================================
# STEMMING
# ======================================================

def stem_tokens(tokens: List[str]) -> List[str]:
    """
    Stemming setiap token.
    """

    stemmer = load_stemmer()

    return [
        stemmer.stem(word)
        for word in tokens
    ]


def stem_text(tokens: List[str]) -> str:
    """
    Mengubah hasil stemming menjadi string.
    """

    return " ".join(
        stem_tokens(tokens)
    )


# ======================================================
# MAIN PREPROCESS
# ======================================================

def preprocess_text(text: str) -> str:
    """
    Pipeline preprocessing lengkap.

    Return:
        String hasil stemming.
    """

    text = cleaning_text(text)

    text = case_folding(text)

    text = normalize_text(text)

    tokens = tokenize_text(text)

    tokens = remove_stopwords(tokens)

    text = stem_text(tokens)

    return text