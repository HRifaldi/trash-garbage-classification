import streamlit as st
import os
import random
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

DATASET_PATH = r"C:\Users\guard\HACKTIV8\phase_2\gc_7\p2-ftds-g7-s1-HRifaldi\dataset"

# -----------------------------------
# Fungsi bantu
# -----------------------------------
def count_images_in_folder(folder_path):
    valid_ext = (".jpg", ".jpeg", ".png", ".webp")
    return len([
        f for f in os.listdir(folder_path)
        if f.lower().endswith(valid_ext)
    ])

def build_distribution_df(dataset_path):
    rows = []
    splits = ["train", "val", "test"]

    for split in splits:
        split_path = os.path.join(dataset_path, split)
        if os.path.exists(split_path):
            classes = sorted([
                c for c in os.listdir(split_path)
                if os.path.isdir(os.path.join(split_path, c))
            ])

            for cls in classes:
                class_path = os.path.join(split_path, cls)
                count = count_images_in_folder(class_path)
                rows.append({
                    "dataset": split,
                    "class": cls,
                    "count": count
                })

    return pd.DataFrame(rows)

def get_random_images(dataset_path, split="train", n_samples=9):
    image_data = []
    split_path = os.path.join(dataset_path, split)

    if not os.path.exists(split_path):
        return image_data

    classes = sorted([
        c for c in os.listdir(split_path)
        if os.path.isdir(os.path.join(split_path, c))
    ])

    for cls in classes:
        class_path = os.path.join(split_path, cls)
        files = [
            f for f in os.listdir(class_path)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ]

        for f in files:
            image_data.append({
                "class": cls,
                "path": os.path.join(class_path, f)
            })

    random.shuffle(image_data)
    return image_data[:n_samples]

# -----------------------------------
# Render EDA
# -----------------------------------
def render_eda():
    st.subheader("Exploratory Data Analysis (EDA) Dataset")
    st.write("Halaman ini menampilkan distribusi data dan sampel gambar pada setiap kelas.")

    df_dist = build_distribution_df(DATASET_PATH)

    if df_dist.empty:
        st.error("Dataset tidak ditemukan atau folder kosong.")
    else:
        st.subheader("Ringkasan Dataset")

        total_images = df_dist["count"].sum()
        total_classes = df_dist["class"].nunique()

        col1, col2 = st.columns(2)
        col1.metric("Total Gambar", total_images)
        col2.metric("Jumlah Kelas", total_classes)

        st.dataframe(df_dist, use_container_width=True)

        st.subheader("Distribusi Dataset per Kelas")

        pivot_df = df_dist.pivot(index="dataset", columns="class", values="count").fillna(0)

        fig, ax = plt.subplots(figsize=(10, 5))
        pivot_df.plot(kind="bar", ax=ax)

        ax.set_title("Distribusi Dataset per Kelas")
        ax.set_xlabel("Dataset")
        ax.set_ylabel("Count")
        ax.tick_params(axis="x", rotation=0)
        plt.legend(title="Class")
        st.pyplot(fig)

        st.subheader("Insight")
        st.write(
            """
            Berdasarkan distribusi data, jumlah gambar pada setiap kelas di masing-masing subset
            train, validation, dan test terlihat seimbang. Kondisi ini baik karena dapat membantu
            model belajar secara lebih adil pada setiap kelas dan mengurangi bias prediksi.
            """
        )

        st.subheader("Contoh Gambar Acak")

        selected_split = st.selectbox("Pilih subset gambar", ["train", "val", "test"])
        n_show = st.slider("Jumlah sampel gambar", min_value=3, max_value=12, value=9)

        sample_images = get_random_images(DATASET_PATH, split=selected_split, n_samples=n_show)

        if not sample_images:
            st.warning("Tidak ada gambar yang ditemukan pada subset ini.")
        else:
            cols = st.columns(3)
            for i, item in enumerate(sample_images):
                with cols[i % 3]:
                    img = Image.open(item["path"])
                    st.image(img, caption=f"Class: {item['class']}", use_container_width=True)