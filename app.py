import streamlit as st
from PIL import Image
import os
import uuid
import cv2
import numpy as np
UPLOAD_DIR = "uploads"
STYLED_DIR = "styled"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(STYLED_DIR, exist_ok=True)

st.title("Creator Upload Portal")

uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded:
    image_id = str(uuid.uuid4())
    upload_path = os.path.join(UPLOAD_DIR, f"{image_id}.png")
    with open(upload_path, "wb") as f:
        f.write(uploaded.read())

    st.image(upload_path, caption="Original Image", use_container_width=True)
    st.session_state['uploaded_path'] = upload_path
    st.session_state['image_id'] = image_id

def fake_stylize(input_path, output_path):
    try:
        img = cv2.imread(input_path)

        # 1. Apply bilateral filter for cartoon effect
        for _ in range(2):
            img = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)

        # 2. Convert to grayscale and find edges
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, blockSize=9, C=2
        )

        # 3. Combine edges with color
        color = cv2.bilateralFilter(img, 9, 300, 300)
        cartoon = cv2.bitwise_and(color, color, mask=edges)

        # 4. Add pastel tone using LAB color manipulation
        pastel = cv2.cvtColor(cartoon, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(pastel)
        l = cv2.equalizeHist(l)
        pastel = cv2.merge((l, a, b))
        pastel = cv2.cvtColor(pastel, cv2.COLOR_LAB2BGR)

        # 5. Slight blur for dreamy look
        pastel = cv2.GaussianBlur(pastel, (3, 3), 0)

        # Save final output
        cv2.imwrite(output_path, pastel)
    except Exception as e:
        st.error(f"Stylization failed: {e}")


if st.session_state.get('uploaded_path'):
    styled_path = os.path.join(STYLED_DIR, f"{st.session_state['image_id']}_styled.png")
    fake_stylize(st.session_state['uploaded_path'], styled_path)
    st.image(styled_path, caption="Stylized Image (Ghibli style)", use_container_width=True)
    st.session_state['styled_path'] = styled_path

    
    if st.button("Unlock Original (Demo Checkout)"):
        st.success("Payment successful (simulated)")
        st.image(st.session_state['uploaded_path'], caption="Original Image", use_container_width=True)
