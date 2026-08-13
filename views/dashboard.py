"""
views/dashboard.py
Halaman Dashboard SenAPP.
"""

from __future__ import annotations

import random

import streamlit as st

import config
from utils.helper import (
    filter_category_words,
    format_number,
    get_sample_reviews,
    get_sentiment_statistics,
)
from utils.loader import (
    load_labeling,
    load_metrics,
)
from utils.visualization import (
    cloud_mask,
    create_wordcloud,
    sentiment_pie_chart,
)


# ======================================================
# Entry Point
# ======================================================

def show_dashboard() -> None:
    """Menampilkan seluruh konten halaman Dashboard."""

    hero_section()
    metric_section()
    pie_chart_section()
    wordcloud_section()
    sample_review_section()


# ======================================================
# Hero Section
# ======================================================

def hero_section() -> None:
    """Menampilkan banner dan deskripsi aplikasi."""

    col_banner, col_text = st.columns([2, 3], gap="large")

    with col_banner:
        st.image(
            str(config.BANNER_PATH),
            use_container_width=True,
        )

    with col_text:
        st.markdown(
            """
            <div class="hero-title">SenAPP</div>

            <div class="hero-subtitle">
                Analisis Sentimen Ulasan Pengguna<br>
                Zenless Zone Zero
            </div>

            <div class="hero-description">
                Website ini menyajikan hasil analisis sentimen ulasan
                pengguna Zenless Zone Zero berdasarkan ulasan Google Play
                Store menggunakan model hybrid Convolutional Neural Network dan Bidirectional Long Short-Term Memory
                (CNN-BiLSTM). Website ini bertujuan membantu masyarakat umum
                memahami persepsi pemain melalui visualisasi data yang
                sederhana, informatif, dan mudah dipahami.
            </div>
            """,
            unsafe_allow_html=True,
        )


# ======================================================
# Metric Section
# ======================================================

def metric_section() -> None:
    """Menampilkan 4 kartu statistik utama penelitian."""

    dataframe = load_labeling()
    metrics   = load_metrics()

    statistic = get_sentiment_statistics(dataframe)
    accuracy  = metrics.get("accuracy", 0)

    # Section header
    st.markdown(
        """
        <div class="section-title">
            <i class="bi bi-bar-chart-fill"></i>
            Statistik Penelitian
        </div>
        <div class="section-description">
            Ringkasan jumlah ulasan serta distribusi sentimen
            yang diperoleh dari hasil penelitian.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Card data
    cards = [
        {
            "icon":  "💬",
            "title": "Total Ulasan",
            "value": format_number(statistic["total"]),
        },
        {
            "icon":  "😊",
            "title": "Sentimen Positif",
            "value": format_number(statistic["positive"]),
        },
        {
            "icon":  "😕",
            "title": "Sentimen Negatif",
            "value": format_number(statistic["negative"]),
        },
        {
            "icon":  "🎯",
            "title": "Akurasi Model",
            "value": f"{accuracy:.2%}",
        },
    ]

    cols = st.columns(4)

    for col, card in zip(cols, cards):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-emoji">{card["icon"]}</div>
                    <div class="metric-number">{card["value"]}</div>
                    <div class="metric-label">{card["title"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ======================================================
# Pie Chart Section
# ======================================================

def pie_chart_section() -> None:
    """Menampilkan donut chart distribusi sentimen."""

    dataframe = load_labeling()

    sentiment = dataframe["Sentimen"].value_counts()
    total     = len(dataframe)

    positive = sentiment.get("Positive", 0)
    negative = sentiment.get("Negative", 0)

    positive_percent = (positive / total * 100) if total else 0
    negative_percent = (negative / total * 100) if total else 0

    fig = sentiment_pie_chart(dataframe)

    # Section header
    st.markdown(
        """
        <div class="section-title">
            <i class="bi bi-pie-chart-fill"></i>
            Distribusi Sentimen
        </div>
        <div class="section-description">
            Persentase sentimen positif dan negatif berdasarkan
            seluruh ulasan pengguna Google Play Store.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False, "responsive": True},
    )

    # Summary cards
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="summary-card positive-card">
                <h2>{positive_percent:.2f}%</h2>
                <p>Sentimen Positif</p>
                <small>👍 {format_number(positive)} Ulasan</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="summary-card negative-card">
                <h2>{negative_percent:.2f}%</h2>
                <p>Sentimen Negatif</p>
                <small>👎 {format_number(negative)} Ulasan</small>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ======================================================
# WordCloud Section
# ======================================================

def wordcloud_section() -> None:
    """Menampilkan WordCloud untuk sentimen positif & negatif."""

    # NOTE: Sebelumnya di sini dilakukan
    # `preprocessing.merge(labeling, on="stemming")`, tapi
    # kolom "stemming" TIDAK unik (banyak ulasan berbeda
    # menghasilkan stemming yang sama, mis. "bagus" muncul
    # ratusan kali). Merge pada kolom yang penuh duplikat
    # menyebabkan row explosion (many-to-many join) sehingga
    # jumlah baris meledak dan rasio Positif/Negatif jadi
    # sangat jomplang dan tidak akurat.
    #
    # labeling.csv sudah memiliki kolom "stemming" dan
    # "Sentimen" sekaligus, jadi tidak perlu merge sama
    # sekali - langsung pakai labeling.csv saja.

    labeling = load_labeling()

    positive = labeling[labeling["Sentimen"] == "Positive"]
    negative = labeling[labeling["Sentimen"] == "Negative"]

    positive_text_raw = " ".join(positive["stemming"].astype(str))
    negative_text_raw = " ".join(negative["stemming"].astype(str))

    # Hanya sisakan kata yang termasuk dalam keyword kategori
    # insight (Grafis, Gameplay, Musik, Gacha, dst), bukan
    # seluruh isi ulasan.

    positive_text = filter_category_words(
        positive_text_raw,
        sentiment="Positive",
    )

    negative_text = filter_category_words(
        negative_text_raw,
        sentiment="Negative",
    )

    # Section header
    st.markdown(
        """
        <div class="section-title">
            <i class="bi bi-cloud-fill"></i>
            WordCloud
        </div>
        <div class="section-description">
            Visualisasi kata dari kategori insight (Grafis, Gameplay,
            Musik, Gacha, Story &amp; Karakter, Performa, Storage,
            Grinding) dalam bentuk awan, hijau untuk sentimen
            positif dan merah untuk sentimen negatif.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="wordcloud-card-title">
                <i class="bi bi-hand-thumbs-up-fill"></i>
                WordCloud Positif
            </div>
            """,
            unsafe_allow_html=True,
        )

        if positive_text.strip():

            positive_wc = create_wordcloud(
                positive_text,
                mask=cloud_mask(),
                colormap="Greens",
            )

            st.pyplot(positive_wc, use_container_width=True)

        else:

            st.info(
                "Belum ada kata kategori insight yang ditemukan "
                "pada ulasan positif."
            )

        st.caption(
            f"Jumlah Review : {len(positive):,}".replace(",", ".")
        )

    with col2:
        st.markdown(
            """
            <div class="wordcloud-card-title">
                <i class="bi bi-hand-thumbs-down-fill"></i>
                WordCloud Negatif
            </div>
            """,
            unsafe_allow_html=True,
        )

        if negative_text.strip():

            negative_wc = create_wordcloud(
                negative_text,
                mask=cloud_mask(),
                colormap="Reds",
            )

            st.pyplot(negative_wc, use_container_width=True)

        else:

            st.info(
                "Belum ada kata kategori insight yang ditemukan "
                "pada ulasan negatif."
            )

        st.caption(
            f"Jumlah Review : {len(negative):,}".replace(",", ".")
        )


# ======================================================
# Sample Review Section
# ======================================================

def sample_review_section() -> None:
    """Menampilkan contoh ulasan acak pengguna."""

    labeling = load_labeling()

    # Section header
    st.markdown(
        """
        <div class="section-title">
            <i class="bi bi-chat-left-text-fill"></i>
            Contoh Ulasan Pengguna
        </div>
        <div class="section-description">
            Berikut beberapa contoh ulasan asli pengguna yang dipilih
            secara acak dari Google Play Store.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Tombol acak ulang
    col_button, _ = st.columns([1, 4])

    with col_button:
        if st.button("🔄 Tampilkan Contoh Lain", use_container_width=True):
            st.session_state.review_seed = random.randint(0, 999_999)
            st.toast("Contoh ulasan berhasil diperbarui.", icon="✅")
            st.rerun()

    positive, negative = get_sample_reviews(
        labeling_df=labeling,
        seed=st.session_state.review_seed,
        n=5,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="review-header positive-review">
                <i class="bi bi-hand-thumbs-up-fill"></i>
                Ulasan Positif
            </div>
            """,
            unsafe_allow_html=True,
        )
        for review in positive["Review Text"]:
            st.markdown(
                f'<div class="review-card">{review}</div>',
                unsafe_allow_html=True,
            )

    with col2:
        st.markdown(
            """
            <div class="review-header negative-review">
                <i class="bi bi-hand-thumbs-down-fill"></i>
                Ulasan Negatif
            </div>
            """,
            unsafe_allow_html=True,
        )
        for review in negative["Review Text"]:
            st.markdown(
                f'<div class="review-card">{review}</div>',
                unsafe_allow_html=True,
            )