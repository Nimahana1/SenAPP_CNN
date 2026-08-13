"""
app.py

Entry point aplikasi SenAPP.

Mengatur:
- Konfigurasi Streamlit
- Memuat CSS
- Inisialisasi Session State
- Sidebar Navigation
- Routing Halaman
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st
from streamlit_option_menu import option_menu

import config

from utils.helper import (
    load_css,
    initialize_session_state,
)

# ======================================================
# Konfigurasi Halaman
# ======================================================

st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout=config.LAYOUT,
    initial_sidebar_state=config.SIDEBAR_STATE,
)

# ======================================================
# Load CSS
# ======================================================

load_css(config.CSS_PATH)

# ======================================================
# Session State
# ======================================================

initialize_session_state()

# ======================================================
# NOTE: Import halaman TIDAK dilakukan di sini (top-level),
# melainkan dipindah ke masing-masing cabang routing di bawah
# (lazy import). Ini penting karena views.prediction meng-
# import TensorFlow (utils/predict.py), yang proses importnya
# sendiri bisa memakan waktu beberapa detik. Kalau diimpor di
# sini, TensorFlow akan selalu di-load di awal walau pengguna
# cuma mau membuka halaman Dashboard/Insight yang sama sekali
# tidak membutuhkannya.
# ======================================================

# ======================================================
# Sidebar
# ======================================================

with st.sidebar:

    if Path(config.LOGO_PATH).exists():
        st.image(str(config.LOGO_PATH), width=90)

    st.markdown(
        """
        <div class="sidebar-title">
            SenAPP
        </div>

        <div class="sidebar-subtitle">
            Sentiment Analysis
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    selected = option_menu(
        menu_title=None,
        options=[
            "Dashboard",
            "Insight Pemain",
            "Prediksi Sentimen",
        ],
        icons=[
            "house",
            "people",
            "graph-up",
        ],
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "transparent",
            },
            "icon": {
                "color": "#06B6D4",
                "font-size": "18px",
            },
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "6px 0",
                "padding": "12px",
                "border-radius": "12px",
            },
            "nav-link-selected": {
                "background-color": "#06B6D4",
                "color": "#FFFFFF",
            },
        },
    )

    st.divider()

    st.markdown(
        """
        <div class="sidebar-footer">
            <b>Skripsi BiLSTM 2026</b><br>
            © 2026 SenAPP
        </div>
        """,
        unsafe_allow_html=True,
    )

# ======================================================
# Simpan Halaman Aktif
# ======================================================

st.session_state.selected_page = selected

# ======================================================
# Routing Halaman
# ======================================================

if selected == "Dashboard":
    from views.dashboard import show_dashboard
    show_dashboard()

elif selected == "Insight Pemain":
    from views.insight import show_insight
    show_insight()

elif selected == "Prediksi Sentimen":
    from views.prediction import show_prediction
    show_prediction()