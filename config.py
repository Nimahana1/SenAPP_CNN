"""
config.py
Konfigurasi utama aplikasi SenApp.
Seluruh konstanta aplikasi didefinisikan di sini agar mudah dikelola.
"""

from pathlib import Path

# =============================================================================
# APP INFORMATION
# =============================================================================

APP_NAME = "SenApp"
APP_TITLE = "Analisis Sentimen Ulasan Zenless Zone Zero"
APP_ICON = "💬"
APP_VERSION = "1.0.0"

# =============================================================================
# BASE DIRECTORY
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent

# =============================================================================
# FOLDER
# =============================================================================

ASSETS_DIR = BASE_DIR / "assets"
DATASET_DIR = BASE_DIR / "dataset"
MODEL_DIR = BASE_DIR / "model"

# =============================================================================
# ASSETS
# =============================================================================

LOGO_PATH = ASSETS_DIR / "logo.png"
BANNER_PATH = ASSETS_DIR / "banner.png"
CSS_PATH = ASSETS_DIR / "css.css"

# =============================================================================
# DATASET
# =============================================================================

REVIEWS_DATASET = DATASET_DIR / "reviews.csv"
PREPROCESSING_DATASET = DATASET_DIR / "hasil_preprocessing_ulasan_app_Zenles_Zone_Zero_rev.csv"
LABELING_DATASET = DATASET_DIR / "labeling_rev.csv"
PREDICTION_DATASET = DATASET_DIR / "hasil_prediksi_full_rev.csv"
CATEGORY_DATASET = DATASET_DIR / "kategori_keyword.csv"

# ======================================================
# DATASET INSIGHT
# ======================================================

KELUHAN_DATASET = DATASET_DIR / "keluhan_dominan_full.csv"
KEPUASAN_DATASET = DATASET_DIR / "kepuasan_pengguna_full.csv"
REVIEW_POSITIF_DATASET = DATASET_DIR / "review_positif_full.csv"
REVIEW_NEGATIF_DATASET = DATASET_DIR / "review_negatif_full.csv"

# =============================================================================
# MODEL
# =============================================================================

MODEL_PATH = MODEL_DIR / "model_bilstm.keras"
TOKENIZER_PATH = MODEL_DIR / "tokenizer.pkl"
LABEL_ENCODER_PATH = MODEL_DIR / "label_encoder.pkl"

METRICS_PATH = MODEL_DIR / "metrics.pkl"
HISTORY_PATH = MODEL_DIR / "history.pkl"

# =============================================================================
# STREAMLIT
# =============================================================================

PAGE_TITLE = APP_NAME
PAGE_ICON = "💬"
LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# =============================================================================
# THEME
# =============================================================================

BACKGROUND_COLOR = "#0F172A"
CARD_COLOR = "#1E293B"
PRIMARY_COLOR = "#06B6D4"

TEXT_COLOR = "#F8FAFC"
TEXT_SECONDARY = "#CBD5E1"

BORDER_COLOR = "#334155"
HOVER_COLOR = "#38BDF8"

SUCCESS_COLOR = "#22C55E"
ERROR_COLOR = "#EF4444"

# =============================================================================
# MODEL CONFIG
# =============================================================================

RANDOM_STATE = 42

# Nilai ini akan disesuaikan dengan notebook modeling
MAX_SEQUENCE_LENGTH = 100

# =============================================================================
# WORDCLOUD
# =============================================================================

WORDCLOUD_WIDTH = 1000
WORDCLOUD_HEIGHT = 600

# =============================================================================
# SAMPLE REVIEW
# =============================================================================

NUMBER_OF_SAMPLE_REVIEW = 10

# ======================================================
# MODEL
# ======================================================

MODEL_PATH = MODEL_DIR / "bilstm_model.keras"

TOKENIZER_PATH = MODEL_DIR / "tokenizer.pkl"

LABEL_ENCODER_PATH = MODEL_DIR / "label_encoder.pkl"

MAX_SEQUENCE_LENGTH = 100

# ======================================================
# PREPROCESSING
# ======================================================

NORMALIZATION_PATH = DATASET_DIR / "kamuskatabaku.xlsx"

MAX_WORDS = 5000

MAX_SEQUENCE_LENGTH = 100

PADDING = "post"

TRUNCATING = "post"

OOV_TOKEN = "<OOV>"