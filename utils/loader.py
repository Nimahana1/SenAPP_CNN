"""
loader.py
Utility untuk memuat dataset, model, tokenizer,
label encoder, metrics, dan history.
"""

from __future__ import annotations

import pickle

import pandas as pd
import streamlit as st
from tensorflow.keras.models import load_model

import config


@st.cache_data(show_spinner=False)
def load_reviews() -> pd.DataFrame:
    """Memuat dataset hasil scraping."""
    return pd.read_csv(config.REVIEWS_DATASET)


@st.cache_data(show_spinner=False)
def load_preprocessing() -> pd.DataFrame:
    """Memuat dataset preprocessing."""
    return pd.read_csv(config.PREPROCESSING_DATASET)


@st.cache_data(show_spinner=False)
def load_labeling() -> pd.DataFrame:
    """Memuat dataset labeling."""
    return pd.read_csv(config.LABELING_DATASET)


@st.cache_data(show_spinner=False)
def load_prediction_dataset() -> pd.DataFrame:
    """Memuat dataset prediksi."""
    return pd.read_csv(config.PREDICTION_DATASET)


@st.cache_data(show_spinner=False)
def load_category_dataset() -> pd.DataFrame:
    """Memuat dataset kategori keyword."""
    return pd.read_csv(config.CATEGORY_DATASET)


@st.cache_resource(show_spinner=False)
def load_sentiment_model():
    """Memuat model Bi-LSTM."""
    return load_model(config.MODEL_PATH)


@st.cache_resource(show_spinner=False)
def load_tokenizer():
    """Memuat tokenizer."""
    with open(config.TOKENIZER_PATH, "rb") as file:
        return pickle.load(file)


@st.cache_resource(show_spinner=False)
def load_label_encoder():
    """Memuat label encoder."""
    with open(config.LABEL_ENCODER_PATH, "rb") as file:
        return pickle.load(file)


@st.cache_resource(show_spinner=False)
def load_metrics():
    """Memuat metrics model."""
    with open(config.METRICS_PATH, "rb") as file:
        return pickle.load(file)


@st.cache_resource(show_spinner=False)
def load_history():
    """Memuat history training."""
    with open(config.HISTORY_PATH, "rb") as file:
        return pickle.load(file)
    
# ======================================================
# Insight Dataset
# ======================================================

@st.cache_data(show_spinner=False)
def load_keluhan() -> pd.DataFrame:
    """
    Memuat dataset kategori keluhan.
    """
    return pd.read_csv(config.KELUHAN_DATASET)


@st.cache_data(show_spinner=False)
def load_kepuasan() -> pd.DataFrame:
    """
    Memuat dataset kategori kepuasan.
    """
    return pd.read_csv(config.KEPUASAN_DATASET)


@st.cache_data(show_spinner=False)
def load_review_positif() -> pd.DataFrame:
    """
    Memuat contoh review positif.
    """
    return pd.read_csv(config.REVIEW_POSITIF_DATASET)


@st.cache_data(show_spinner=False)
def load_review_negatif() -> pd.DataFrame:
    """
    Memuat dataset review negatif.
    """
    return pd.read_csv(config.REVIEW_NEGATIF_DATASET)