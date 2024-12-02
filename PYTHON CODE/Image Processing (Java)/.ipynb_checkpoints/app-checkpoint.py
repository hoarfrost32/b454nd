import streamlit as st
import subprocess
import os

# Create an image uploader widget
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save the uploaded image to a temporary file
    temp_image_path = "uploaded_image.jpg"
    with open(temp_image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Run driver.py with the image path
    subprocess.run(["python", "driver.py", temp_image_path])

    # Display the processed results
    # ...code to display output from output.ipynb...

    # Optionally, remove the temporary image file
    os.remove(temp_image_path)