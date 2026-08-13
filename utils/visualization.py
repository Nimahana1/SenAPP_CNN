"""
visualization.py
Fungsi visualisasi aplikasi.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image, ImageDraw
from wordcloud import WordCloud
import matplotlib.pyplot as plt


@st.cache_data(show_spinner=False)
def sentiment_pie_chart(
    dataframe: pd.DataFrame,
    label_column: str = "Sentimen",
):
    """
    Membuat Pie Chart distribusi sentimen.

    Di-cache agar tidak dibangun ulang dari nol setiap kali
    halaman Dashboard di-rerun (mis. saat pindah halaman lalu
    kembali lagi), selama datanya belum berubah.
    """

    sentiment = (
        dataframe[label_column]
        .value_counts()
        .reset_index()
    )

    sentiment.columns = ["Sentimen", "Jumlah"]

    fig = px.pie(
        sentiment,
        names="Sentimen",
        values="Jumlah",
        hole=0.45,

        color="Sentimen",
color_discrete_map={
    "Positive": "#22C55E",
    "Negative": "#EF4444",
}
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Jumlah : %{value}<extra></extra>",
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#F8FAFC",
            family="Poppins"
        ),
        showlegend=True,
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10,
        ),
        legend=dict(
            orientation="h",
            y=-0.1,
            x=0.3,
        ),
    )

    return fig

@st.cache_resource(show_spinner=False)
def create_wordcloud(
    text: str,
    mask: np.ndarray | None = None,
    colormap: str | None = None,
):
    """
    Membuat WordCloud.

    Di-cache (cache_resource, karena hasilnya berupa objek
    matplotlib Figure) supaya proses word-placement yang
    cukup berat tidak diulang dari nol setiap kali halaman
    Dashboard di-rerun, selama teks/mask/colormap-nya sama.

    Parameters
    ----------
    text : str
        Teks sumber kata untuk WordCloud.

    mask : np.ndarray | None
        Mask bentuk WordCloud (mis. hasil dari `cloud_mask()`).
        Jika None, WordCloud akan berbentuk kotak seperti biasa.

    colormap : str | None
        Nama colormap matplotlib (mis. "Greens", "Reds") untuk
        membedakan tone warna antar WordCloud meski bentuknya sama.
    """

    kwargs = dict(
        background_color=None,
        mode="RGBA",
        max_words=250,
        collocations=False,
        # Kata yang sudah ada akan diulang (dengan ukuran makin
        # kecil) sampai bentuk mask terisi penuh. Ini penting
        # karena setelah difilter dengan keyword kategori insight,
        # jumlah kata unik pada sisi Positif dan Negatif bisa
        # berbeda jauh, sehingga tanpa repeat=True salah satu
        # sisi bisa terlihat kosong/jomplang.
        repeat=True,
        min_font_size=4,
        relative_scaling=0.5,
    )

    if mask is not None:

        # Ukuran wordcloud mengikuti ukuran mask, bukan
        # width/height manual.
        #
        # NOTE: contour_width/contour_color SENGAJA tidak
        # dipakai di sini. Kombinasi mode="RGBA" (background
        # transparan) dengan contour_width menyebabkan crash
        # pada library wordcloud (_draw_contour mengalikan
        # array RGBA 4-channel dengan mask 2D yang shape-nya
        # tidak cocok). Bentuk mask sendiri sudah cukup
        # terlihat tanpa garis kontur.

        kwargs["mask"] = mask

    else:

        kwargs["width"] = 1200
        kwargs["height"] = 700

    if colormap:

        kwargs["colormap"] = colormap

    wordcloud = WordCloud(**kwargs).generate(text)

    figsize = (7, 7) if mask is not None else (10, 5)

    fig, ax = plt.subplots(figsize=figsize)

    ax.imshow(wordcloud, interpolation="bilinear")

    ax.axis("off")

    fig.patch.set_alpha(0)

    return fig


# ======================================================
# WORDCLOUD MASK - AWAN (CLOUD)
# ======================================================

def cloud_mask(size: int = 900) -> np.ndarray:
    """
    Membuat mask bentuk awan (cloud) secara terprogram
    menggunakan PIL, tanpa memerlukan file gambar eksternal.

    Area putih (255) = tidak diisi kata.
    Area hitam (0)    = diisi kata.
    """

    image = Image.new("L", (size, size), color=255)

    draw = ImageDraw.Draw(image)

    # Badan bawah awan (lebar, agak pipih)
    draw.rounded_rectangle(
        [size * 0.12, size * 0.55, size * 0.88, size * 0.80],
        radius=int(size * 0.12),
        fill=0,
    )

    # Gelembung-gelembung di atas membentuk siluet awan
    bumps = [
        (0.26, 0.55, 0.17),
        (0.42, 0.38, 0.22),
        (0.60, 0.33, 0.24),
        (0.77, 0.42, 0.19),
        (0.87, 0.56, 0.14),
    ]

    for cx, cy, r in bumps:

        x0 = (cx - r) * size
        y0 = (cy - r) * size
        x1 = (cx + r) * size
        y1 = (cy + r) * size

        draw.ellipse([x0, y0, x1, y1], fill=0)

    return np.array(image)