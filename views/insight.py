"""
views/insight.py
Halaman Insight Pemain.
"""

from __future__ import annotations

import streamlit as st
import plotly.express as px

from utils.loader import (
    load_keluhan,
    load_kepuasan,
    load_review_positif,
    load_review_negatif,
)

# ======================================================
# Entry Point
# ======================================================

def show_insight() -> None:
    """
    Menampilkan halaman Insight Pemain.
    """

    header_section()

    complaint_section()

    praise_section()

    conclusion_section()


# ======================================================
# Header
# ======================================================

def header_section() -> None:
    """
    Header halaman Insight.
    """

    st.markdown(
        """
        <div class="hero-title">
            Insight Pemain
        </div>

        <div class="hero-subtitle">
            Hasil Analisis Keluhan dan Hal yang Disukai Pemain
        </div>

        <div class="hero-description">
            Halaman ini menyajikan ringkasan hasil penelitian mengenai
            berbagai keluhan serta aspek yang paling disukai oleh pemain
            Zenless Zone Zero berdasarkan ulasan Google Play Store.
            Informasi disajikan dalam bentuk visual agar mudah dipahami
            oleh seluruh pengguna.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ======================================================
# Keluhan Dominan
# ======================================================

def complaint_section() -> None:
    """
    Menampilkan kategori keluhan dominan pemain.
    """

    # ======================================================
    # Load Dataset
    # ======================================================

    dataframe = load_keluhan()

    review_df = load_review_negatif()
    

    # ======================================================
    # Section Title
    # ======================================================

    st.markdown(
        """
        <div class="section-title">
            <i class="bi bi-exclamation-triangle-fill"></i>
            Keluhan Dominan Pemain
        </div>

        <div class="section-description">
            Grafik berikut menunjukkan kategori keluhan yang paling sering
            ditemukan berdasarkan hasil analisis ulasan pengguna Zenless Zone Zero.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ======================================================
    # Layout
    # ======================================================

    chart_col, table_col = st.columns([2, 1])

    # ======================================================
    # Horizontal Bar Chart
    # ======================================================

    with chart_col:

        fig = px.bar(
            dataframe.sort_values("Frekuensi"),
            x="Frekuensi",
            y="Kategori",
            orientation="h",
            text="Frekuensi",
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=430,
            margin=dict(
                l=20,
                r=20,
                t=10,
                b=10,
            ),
            font=dict(
                family="Poppins",
                color="#F8FAFC",
            ),
            xaxis_title="Frekuensi",
            yaxis_title="Kategori",
        )

        fig.update_traces(
            textposition="outside",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
            },
        )

    # ======================================================
    # Ringkasan
    # ======================================================

    with table_col:

        st.markdown(
            "#### 📋 Ringkasan Frekuensi"
        )

        st.dataframe(
            dataframe,
            hide_index=True,
            use_container_width=True,
        )

    # ======================================================
    # Sample Review
    # ======================================================

    st.markdown(
        """
        <div class="section-title">
            <i class="bi bi-chat-left-text-fill"></i>
            Contoh Ulasan Negatif
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "Beberapa contoh ulasan negatif yang digunakan pada proses penelitian."
    )

    sample = review_df.sample(
    min(5, len(review_df)),
    random_state=42,
)

    for review in sample["Review_Text"]:

        st.markdown(
            f"""
            <div class="review-card">
            {review}
        </div>
        """,
        unsafe_allow_html=True,
    )

# ======================================================
# Hal yang Disukai
# ======================================================

def praise_section() -> None:
    """
    Menampilkan kategori yang paling disukai oleh pemain.
    """

    # ======================================================
    # Load Dataset
    # ======================================================

    dataframe = load_kepuasan()

    review_df = load_review_positif()

    # ======================================================
    # Section Title
    # ======================================================

    st.markdown(
        """
        <div class="section-title">
            <i class="bi bi-heart-fill"></i>
            Hal yang Disukai Pemain
        </div>

        <div class="section-description">
            Grafik berikut menunjukkan aspek permainan yang paling banyak
            mendapatkan apresiasi dari pemain berdasarkan hasil penelitian.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ======================================================
    # Layout
    # ======================================================

    chart_col, table_col = st.columns([2, 1])

    # ======================================================
    # Chart
    # ======================================================

    with chart_col:

        fig = px.bar(
            dataframe,
            x="Frekuensi",
            y="Kategori",
            orientation="h",
            text="Frekuensi",
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#F8FAFC",
                family="Poppins",
            ),
            margin=dict(
                l=20,
                r=20,
                t=10,
                b=10,
            ),
            height=430,
        )

        fig.update_traces(
            textposition="outside",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
            },
        )

    # ======================================================
    # Table
    # ======================================================

    with table_col:

        st.markdown(
            "#### 📋 Ringkasan Frekuensi"
        )

        st.dataframe(
            dataframe,
            hide_index=True,
            use_container_width=True,
        )

    # ======================================================
    # Sample Review
    # ======================================================

    st.markdown(
        """
        <div class="section-title">
            <i class="bi bi-chat-heart-fill"></i>
            Contoh Ulasan Positif
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "Beberapa contoh ulasan positif dari pengguna Google Play Store."
    )

    sample = review_df.sample(
        min(5, len(review_df)),
        random_state=42,
    )

    for review in sample["Review_Text"]:

        st.markdown(
            f"""
            <div class="review-card">
                {review}
            </div>
            """,
            unsafe_allow_html=True,
        )

# ======================================================
# Kesimpulan
# ======================================================

def conclusion_section() -> None:
    """
    Menampilkan kesimpulan penelitian secara otomatis.
    """

    keluhan = load_keluhan()
    kepuasan = load_kepuasan()

    if keluhan.empty or kepuasan.empty:
        st.warning("Dataset insight belum tersedia.")
        return

    # ======================================================
    # Data Dominan
    # ======================================================

    top_keluhan = (
        keluhan.sort_values(
            by="Frekuensi",
            ascending=False,
        )
        .iloc[0]
    )

    top_pujian = (
        kepuasan.sort_values(
            by="Frekuensi",
            ascending=False,
        )
        .iloc[0]
    )

    total_keluhan = int(keluhan["Frekuensi"].sum())
    total_pujian = int(kepuasan["Frekuensi"].sum())

    # ======================================================
    # Header
    # ======================================================

    st.markdown(
        """
        <div class="section-title">
            <i class="bi bi-lightbulb-fill"></i>
            Kesimpulan Penelitian
        </div>

        <div class="section-description">
            Ringkasan hasil penelitian berdasarkan analisis kategori
            keluhan dan aspek yang paling disukai pemain.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ======================================================
    # Card 1
    # ======================================================

    st.markdown(
        f"""
<div class="conclusion-card">

<h4>📌 Keluhan Dominan</h4>

Kategori <b>{top_keluhan['Kategori']}</b> merupakan
keluhan yang paling banyak ditemukan dengan total
<b>{top_keluhan['Frekuensi']}</b> ulasan.

</div>
""",
        unsafe_allow_html=True,
    )

    # ======================================================
    # Card 2
    # ======================================================

    st.markdown(
        f"""
<div class="conclusion-card">

<h4>❤️ Hal yang Paling Disukai</h4>

Kategori <b>{top_pujian['Kategori']}</b> menjadi
aspek yang paling banyak memperoleh apresiasi,
dengan total <b>{top_pujian['Frekuensi']}</b> ulasan.

</div>
""",
        unsafe_allow_html=True,
    )

    # ======================================================
    # Card 3
    # ======================================================

    st.markdown(
        f"""
<div class="conclusion-card">

<h4>📊 Ringkasan Penelitian</h4>

Penelitian ini mengidentifikasi
<b>{total_keluhan}</b> temuan keluhan
dan <b>{total_pujian}</b> temuan mengenai
hal-hal yang disukai oleh pemain.

</div>
""",
        unsafe_allow_html=True,
    )

    # ======================================================
    # Card 4
    # ======================================================

    st.markdown(
        f"""
<div class="conclusion-card">

<h4>🎯 Implikasi Penelitian</h4>

Hasil penelitian menunjukkan bahwa pengembang
perlu memberikan perhatian lebih terhadap
kategori <b>{top_keluhan['Kategori']}</b>,
serta mempertahankan kualitas pada kategori
<b>{top_pujian['Kategori']}</b> yang telah
mendapatkan banyak respon positif dari pemain.

</div>
""",
        unsafe_allow_html=True,
    )