"""
utils/interpret.py

Interpretasi hasil prediksi sentimen.
"""

from __future__ import annotations


# ======================================================
# CATEGORY KEYWORDS
# ======================================================

# ======================================================
# WORDCLOUD EXTRA KEYWORDS
# ======================================================
#
# Daftar kata tambahan KHUSUS untuk memperkaya tampilan
# WordCloud di halaman Dashboard. Sengaja dipisah dari
# CATEGORY_KEYWORDS agar TIDAK mempengaruhi akurasi
# detect_category() yang dipakai pada halaman Prediksi
# Sentimen. Kata-kata umum/generik (mis. "good", "nice")
# di sini aman karena tidak dipakai untuk klasifikasi
# kategori, hanya untuk menambah variasi kata di WordCloud.

WORDCLOUD_EXTRA_KEYWORDS = {

    "Positive": [

        "suka",
        "nice",
        "good",
        "best",
        "love",
        "worth",
        "recommended",
        "top",
        "juara",
        "solid",
        "favorit",
        "favorite",
        "hebat",
        "sip",
        "oke",
        "top up",
        "puas",
        "worth it",
        "recommend",
        "gemas",

    ],

    "Negative": [

        "jelek",
        "buruk",
        "kecewa",
        "mengecewakan",
        "parah",
        "payah",
        "males",
        "malas",
        "error",
        "ganggu",
        "mengganggu",
        "annoying",
        "worst",
        "sampah",
        "kesal",
        "kesel",
        "menyebalkan",
        "nyesel",
        "menyesal",
        "buang",

    ],

}


CATEGORY_KEYWORDS = {

    # ==================================================
    # POSITIVE CATEGORY
    # ==================================================

    "Positive": {

        "Grafis": [

            "grafis",
            "grafik",
            "graphic",
            "graphics",
            "visual",
            "animasi",
            "efek",
            "detail",
            "hd",
            "kualitas",
            "cantik",
            "indah",
            "bagus",
            "keren",
            "mantap",
            "memukau",

        ],

        "Gameplay": [

            "gameplay",
            "combat",
            "mekanik",
            "seru",
            "asik",
            "menyenangkan",
            "lancar",
            "smooth",
            "responsif",
            "nyaman",
            "adiktif",
            "puas",

        ],

        "Musik": [

            "musik",
            "lagu",
            "soundtrack",
            "bgm",
            "audio",
            "suara",
            "voice",
            "dubbing",
            "ost",
            "merdu",
            "epic",

        ],

        "Gacha": [

            "gacha",
            "hoki",
            "lucky",
            "beruntung",
            "ramah",
            "baik",
            "murah",
            "gampang",
            "mudah",
            "wangi",
            "f2p",
            "menang",

        ],

        "Story & Karakter": [

            "story",
            "cerita",
            "alur",
            "plot",
            "lore",
            "karakter",
            "design",
            "desain",
            "hero",
            "unik",
            "waifu",
            "husbu",
            "personality",
            "emosional",

        ],

    },

    # ==================================================
    # NEGATIVE CATEGORY
    # ==================================================

    "Negative": {

        "Gameplay": [

            "gameplay",
            "combat",
            "kontrol",
            "control",
            "kamera",
            "mekanik",
            "delay",
            "kaku",
            "susah",
            "sulit",
            "lambat",
            "aiming",
            "dodge",
            "bug",
            "tidak nyaman",

        ],

        "Performa": [

            "lag",
            "ngelag",
            "frame",
            "fps",
            "stutter",
            "freeze",
            "crash",
            "force",
            "close",
            "fc",
            "panas",
            "overheat",
            "berat",
            "lemot",
            "loading",
            "macet",
            "stabil",

        ],

        "Storage": [

            "storage",
            "size",
            "gb",
            "memori",
            "penyimpanan",
            "ruang",
            "kapasitas",
            "download",
            "update",
            "install",
            "instalasi",
            "besar",

        ],

        "Grinding": [

            "grinding",
            "grind",
            "farm",
            "farming",
            "daily",
            "misi",
            "bosan",
            "boring",
            "monoton",
            "capek",
            "lama",
            "ribet",
            "melelahkan",
            "repetitif",

        ],

        "Gacha": [

            "gacha",
            "rate",
            "ampas",
            "pelit",
            "pity",
            "zonk",
            "rng",
            "banner",
            "kalah",
            "unlucky",
            "dapat",
            "tidak dapat",
            "gak dapet",
            "ga dapet",

        ],

    }

}


# ======================================================
# DETECT CATEGORY
# ======================================================

def detect_category(
    sentiment: str,
    processed_text: str,
) -> str:
    """
    Menentukan kategori berdasarkan
    hasil sentimen dan keyword.
    """

    sentiment = sentiment.capitalize()

    categories = CATEGORY_KEYWORDS.get(
        sentiment,
        {},
    )

    score = {}

    processed_text = processed_text.lower()

    for category, keywords in categories.items():

        score[category] = sum(

            keyword in processed_text

            for keyword in keywords

        )

    if not score:

        return "Umum"

    highest = max(score.values())

    if highest == 0:

        return "Umum"

    return max(
        score,
        key=score.get,
    )


# ======================================================
# INTERPRET RESULT
# ======================================================

def interpret_prediction(
    sentiment: str,
    processed_text: str,
) -> dict:
    """
    Menghasilkan interpretasi hasil prediksi.
    """

    category = detect_category(

        sentiment,

        processed_text,

    )

    # Frasa aspek, ditangani khusus untuk kategori "Umum"
    # agar kalimatnya tetap enak dibaca.

    if category == "Umum":

        aspek_phrase = "terhadap game secara umum"

    else:

        aspek_phrase = f"terhadap aspek {category.lower()}"

    if sentiment == "Positive":

        analysis = "Pujian"

        summary = (
            "Berdasarkan klasifikasi yang dilakukan oleh "
            "model Bi-LSTM, ulasan ini dikategorikan "
            "sebagai sentimen positif karena pengguna "
            "memberikan penilaian baik serta apresiasi "
            f"yang kuat {aspek_phrase}."
        )

    else:

        analysis = "Keluhan"

        summary = (
            "Berdasarkan klasifikasi yang dilakukan oleh "
            "model Bi-LSTM, ulasan ini dikategorikan "
            "sebagai sentimen negatif karena pengguna "
            "menyampaikan keluhan serta penilaian yang "
            f"kurang baik {aspek_phrase}."
        )

    return {

        "analysis": analysis,

        "category": category,

        "summary": summary,

    }