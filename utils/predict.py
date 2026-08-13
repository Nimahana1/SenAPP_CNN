"""
utils/predict.py

Loader model Bi-LSTM.
"""

from __future__ import annotations

import pickle

import streamlit as st
from tensorflow.keras.models import load_model
from utils.interpret import interpret_prediction
import config


# ======================================================
# LOAD MODEL
# ======================================================

@st.cache_resource(show_spinner=False)
def load_bilstm_model():
    """
    Memuat model Bi-LSTM.
    """

    return load_model(config.MODEL_PATH)


# ======================================================
# LOAD TOKENIZER
# ======================================================

@st.cache_resource(show_spinner=False)
def load_tokenizer():
    """
    Memuat tokenizer.
    """

    with open(config.TOKENIZER_PATH, "rb") as file:
        tokenizer = pickle.load(file)

    return tokenizer


# ======================================================
# LOAD LABEL ENCODER
# ======================================================

@st.cache_resource(show_spinner=False)
def load_label_encoder():
    """
    Memuat Label Encoder.
    """

    with open(config.LABEL_ENCODER_PATH, "rb") as file:
        encoder = pickle.load(file)

    return encoder

from tensorflow.keras.preprocessing.sequence import pad_sequences

from utils.preprocess import preprocess_text


# ======================================================
# PREDICTION
# ======================================================

def predict_sentiment(text: str) -> dict:
    """
    Melakukan prediksi sentimen menggunakan model Bi-LSTM.
    """

    # ==================================================
    # Load Resource
    # ==================================================

    model = load_bilstm_model()
    tokenizer = load_tokenizer()
    encoder = load_label_encoder()

    # ==================================================
    # Preprocessing
    # ==================================================

    processed_text = preprocess_text(text)

    # ==================================================
    # Text to Sequence
    # ==================================================

    sequence = tokenizer.texts_to_sequences(
        [processed_text]
    )

    sequence = pad_sequences(
        sequence,
        maxlen=config.MAX_SEQUENCE_LENGTH,
        padding=config.PADDING,
        truncating=config.TRUNCATING,
    )

    # ==================================================
    # Predict
    # ==================================================

    probability = float(
        model.predict(
            sequence,
            verbose=0,
        )[0][0]
    )

    # ==================================================
    # Decode Label
    # ==================================================

    prediction = 1 if probability >= 0.5 else 0

    sentiment = encoder.inverse_transform(
        [prediction]
    )[0]

    confidence = (
        probability
        if probability >= 0.5
        else 1 - probability
    )

    # ==================================================
    # Interpretation
    # ==================================================

    interpretation = interpret_prediction(
        sentiment=sentiment,
        processed_text=processed_text,
    )

    # ==================================================
    # Return Result
    # ==================================================

    return {

        # Original Input
        "original_text": text,

        # NLP
        "processed_text": processed_text,

        # Prediction
        "sentiment": sentiment,
        "confidence": confidence,
        "probability": probability,

        # Interpretation
        "analysis": interpretation["analysis"],
        "category": interpretation["category"],
        "summary": interpretation["summary"],

    }