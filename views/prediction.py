"""
views/prediction.py
Halaman Prediksi Sentimen.
"""

from __future__ import annotations

import streamlit as st

from utils.predict import predict_sentiment

# ======================================================
# SHOW PAGE
# ======================================================

def show_prediction() -> None:
    """
    Menampilkan halaman prediksi sentimen.
    """

    header_section()

    input_section()

    # Tampilkan hasil jika sudah ada
    if st.session_state.prediction_result is not None:

        result_section(
            st.session_state.prediction_result
        )

    else:

        empty_state()


# ======================================================
# HEADER
# ======================================================

def header_section() -> None:
    """
    Header halaman prediksi.
    """

    st.markdown(
        '<div class="hero-title">Prediksi Sentimen</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="hero-subtitle">Analisis Sentimen Menggunakan Model CNN-BiLSTM</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="hero-description">'
        'Masukkan ulasan mengenai game <b>Zenless Zone Zero</b>. '
        'Sistem akan melakukan preprocessing sesuai tahapan penelitian '
        'kemudian memprediksi sentimen menggunakan model '
        '<b>hybrid Convolutional Neural Network dan Bidirectional Long Short-Term Memory (CNN-BiLSTM)</b>.'
        '</div>',
        unsafe_allow_html=True,
    )


# ======================================================
# PLAY STORE LINK CARD
# ======================================================

def playstore_link_card() -> None:
    """
    Menampilkan satu kartu link menuju halaman Google Play
    Store Zenless Zone Zero (ikon + judul + subjudul + panah),
    berbentuk satu baris horizontal utuh.
    """

    st.markdown(
        '<style>'
        '.playstore-link-card {'
        'display: flex;'
        'align-items: center;'
        'gap: 14px;'
        # --- LEBAR KOTAK ---
        # "100%" = selebar kolom kontennya. Ganti mis. "320px"
        # kalau mau ukuran tetap (tidak melebar penuh).
        'width: 100%;'
        'background: #1E293B;'
        'border: 1px solid #334155;'
        'border-radius: 14px;'
        # --- TINGGI/PADDING KOTAK ---
        # Perbesar/perkecil angka ini untuk mengatur tinggi
        # kotak (padding atas-bawah, kiri-kanan).
        'padding: 14px 18px;'
        'text-decoration: none;'
        'margin-bottom: 22px;'
        'box-sizing: border-box;'
        'transition: border-color 0.15s ease, transform 0.15s ease;'
        '}'
        '.playstore-link-card:hover {'
        'border-color: #06B6D4;'
        'transform: translateY(-2px);'
        '}'
        '.playstore-link-icon {'
        'flex-shrink: 0;'
        # --- UKURAN KOTAK IKON LOGO ---
        # Ubah width/height di sini kalau mau logo lebih
        # besar/kecil.
        'width: 44px;'
        'height: 44px;'
        'border-radius: 10px;'
        'background: rgba(255,255,255,0.06);'
        'display: flex;'
        'align-items: center;'
        'justify-content: center;'
        'font-size: 22px;'
        'color: #06B6D4;'
        '}'
        '.playstore-link-text {'
        'flex: 1;'
        'min-width: 0;'
        '}'
        '.playstore-link-title {'
        'font-size: 15px;'
        'font-weight: 700;'
        'color: #F8FAFC;'
        'line-height: 1.3;'
        '}'
        '.playstore-link-subtitle {'
        'font-size: 12px;'
        'color: #CBD5E1;'
        'margin-top: 2px;'
        '}'
        '.playstore-link-chevron {'
        'flex-shrink: 0;'
        'color: #94A3B8;'
        'font-size: 20px;'
        'line-height: 1;'
        '}'
        '</style>',
        unsafe_allow_html=True,
    )

    # Logo segitiga "play" berwarna-warni (biru-hijau-kuning-merah),
    # sesuai referensi wireframe. Ini ilustrasi generik ala tombol
    # play, BUKAN reproduksi presisi logo resmi Google Play (yang
    # merupakan trademark) - jadi aman dipakai tanpa perlu file
    # gambar/asset tambahan.
    playstore_icon_html = (
        '<svg width="24" height="24" viewBox="0 0 24 24" '
        'xmlns="http://www.w3.org/2000/svg">'
        '<defs>'
        '<linearGradient id="playGrad" x1="0%" y1="0%" x2="100%" y2="100%">'
        '<stop offset="0%" stop-color="#00D2FF"/>'
        '<stop offset="35%" stop-color="#22C55E"/>'
        '<stop offset="65%" stop-color="#FACC15"/>'
        '<stop offset="100%" stop-color="#EF4444"/>'
        '</linearGradient>'
        '</defs>'
        '<path d="M4 3 L20 12 L4 21 Z" fill="url(#playGrad)"/>'
        '</svg>'
    )

    # NOTE: tag PALING LUAR harus <div>, bukan <a>. Parser markdown
    # Streamlit mengenali <div> sebagai tag pembuka blok HTML mentah,
    # sedangkan <a> tidak - sehingga kalau <a> ditaruh sebagai tag
    # terluar, isinya malah dianggap teks biasa dan dibungkus <p> oleh
    # markdown. Begitu browser menemukan <div> di dalam <p> itu,
    # strukturnya otomatis "pecah" (div lepas jadi elemen sendiri-
    # sendiri, tidak lagi nested di dalam <a>) - itu penyebab
    # tampilannya berantakan seperti di screenshot.

    card_html = (
        '<div>'
        '<a href="https://play.google.com/store/apps/details?'
        'id=com.HoYoverse.Nap&hl=&hl=id&gl=ID" '
        'target="_blank" rel="noopener noreferrer" '
        'class="playstore-link-card">'
        f'<div class="playstore-link-icon">{playstore_icon_html}</div>'
        '<div class="playstore-link-text">'
        '<div class="playstore-link-title">Ulasan Zenless Zone Zero</div>'
        '<div class="playstore-link-subtitle">Sumber: Google Play Store</div>'
        '</div>'
        '<div class="playstore-link-chevron">&#8250;</div>'
        '</a>'
        '</div>'
    )

    st.markdown(card_html, unsafe_allow_html=True)


# ======================================================
# INPUT SECTION
# ======================================================

def input_section() -> None:
    """
    Input ulasan pengguna.
    """

    playstore_link_card()

    st.markdown(
        '<div class="section-title"><i class="bi bi-pencil-square"></i> Masukkan Ulasan</div>',
        unsafe_allow_html=True,
    )

    st.session_state.user_input = st.text_area(

        label="",

        value=st.session_state.user_input,

        placeholder=(
            "Contoh:\n"
            "Gameplay sangat seru tetapi masih sering lag "
            "ketika bermain."
        ),

        height=180,

    )

    analyze = st.button(

        "🔍 Analisis Sentimen",

        use_container_width=True,

        type="primary",

    )

    if analyze:

        # ----------------------------------------------

        text = st.session_state.user_input.strip()

        if not text:

            st.warning(
                "Silakan masukkan ulasan terlebih dahulu."
            )

            return

        # ----------------------------------------------

        with st.spinner(
            "Sedang menganalisis sentimen..."
        ):

            result = predict_sentiment(text)

        # Simpan hasil
        st.session_state.prediction_result = result

        st.toast(
            "Analisis selesai.",
            icon="✅",
        )

        st.rerun()

# ======================================================
# RESULT SECTION
# ======================================================

def result_section(result: dict) -> None:
    """
    Menampilkan hasil analisis sentimen.
    """

    sentiment = result["sentiment"]
    confidence = result["confidence"] * 100
    analysis = result["analysis"]
    category = result["category"]
    summary = result["summary"]

    # ==================================================
    # Theme
    # ==================================================

    if sentiment.lower() == "positive":

        emoji = "😊"
        color = "#22C55E"
        badge = "POSITIVE"

    else:

        emoji = "😞"
        color = "#EF4444"
        badge = "NEGATIVE"

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # HEADER CARD
    # ==================================================
    # NOTE: HTML ditulis tanpa indentasi (rata kiri) agar
    # tidak dianggap code block oleh parser Markdown Streamlit.

    header_html = (
        '<div class="prediction-card" style="text-align:center; padding:16px 0;">'
        f'<div style="font-size:40px; line-height:1.2;">{emoji}</div>'
        f'<div style="color:{color}; font-size:24px; font-weight:700; margin-top:4px;">{badge}</div>'
        '<div style="font-size:14px; opacity:0.75; margin-top:6px;">Tingkat Keyakinan Model</div>'
        f'<div style="font-size:20px; font-weight:600; margin-top:2px;">{confidence:.2f}%</div>'
        '</div>'
    )

    st.markdown(header_html, unsafe_allow_html=True)

    st.progress(confidence / 100)

    st.markdown("---")

    # ==================================================
    # JENIS ANALISIS
    # ==================================================

    jenis_html = (
        '<div class="info-card" style="padding:12px 0;">'
        '<div style="font-size:14px; opacity:0.75;">💬 Jenis Analisis</div>'
        f'<div style="font-size:20px; font-weight:700; margin-top:4px;">{analysis}</div>'
        '</div>'
    )

    st.markdown(jenis_html, unsafe_allow_html=True)

    st.markdown("---")

    # ==================================================
    # KATEGORI
    # ==================================================

    kategori_html = (
        '<div class="info-card" style="padding:12px 0;">'
        '<div style="font-size:14px; opacity:0.75;">🏷️ Kategori</div>'
        f'<div style="font-size:20px; font-weight:700; margin-top:4px;">{category}</div>'
        '</div>'
    )

    st.markdown(kategori_html, unsafe_allow_html=True)

    st.markdown("---")

    # ==================================================
    # SUMMARY
    # ==================================================

    st.markdown(
        '<div class="section-title" style="font-weight:700; margin-bottom:8px;">' \
        '📝 Kesimpulan Analisis</div>',
        unsafe_allow_html=True,
    )

    summary_html = (
        '<div style="font-size:17px; line-height:1.6; '
        'background-color:rgba(59,130,246,0.12); '
        'border-left:4px solid #3B82F6; '
        'padding:14px 18px; border-radius:6px;">'
        f'{summary}'
        '</div>'
    )

    st.markdown(summary_html, unsafe_allow_html=True)


# ======================================================
# EMPTY STATE
# ======================================================

def empty_state() -> None:
    """
    Ditampilkan sebelum pengguna melakukan prediksi.
    """

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="prediction-empty">'
        '<i class="bi bi-chat-square-text"></i>'
        '<h3>Belum Ada Hasil Analisis</h3>'
        '<p>Masukkan ulasan mengenai game <b>Zenless Zone Zero</b>, '
        'kemudian tekan tombol <b>Analisis Sentimen</b>.</p>'
        '</div>',
        unsafe_allow_html=True,
    )