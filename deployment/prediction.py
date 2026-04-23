import numpy as np
import streamlit as st
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Load model sekali saja
model = load_model("model_inference.keras")

IMG_SIZE = (128, 128)
CLASS_NAMES = ["Garbage Bag Images", "Paper Bag Images", "Plastic Bag Images"]


def preprocess_image(img_file):
    img = image.load_img(img_file, target_size=IMG_SIZE)
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def predict_image(img_file):
    img_array = preprocess_image(img_file)
    pred = model.predict(img_array, verbose=0)

    pred_index = np.argmax(pred, axis=1)[0]
    confidence = float(np.max(pred))
    predicted_label = CLASS_NAMES[pred_index]

    return predicted_label, round(confidence * 100, 2)


def render_prediction():
    st.title("Garbage Bag Image Classification")
    st.write("Upload gambar untuk melakukan prediksi.")

    uploaded_file = st.file_uploader("Pilih gambar", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="Gambar yang diupload", use_container_width=True)

        if st.button("Predict"):
            label, confidence = predict_image(uploaded_file)
            st.success(f"Prediction: {label}")
            st.info(f"Confidence: {confidence}%")
    else:
        st.warning("Silakan upload gambar terlebih dahulu.")