import streamlit as st
import os
import subprocess
from PIL import Image

# Title of the app
st.title("Image Processing App")

# Upload file section
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Save the uploaded file locally
    input_image_path = "input_image.png"
    with open(input_image_path, "wb") as f:
        f.write(uploaded_file.read())

    # Call the driver.py script
    st.write("Processing the image...")
    subprocess.run(["python", "driver.py", input_image_path])

    # Display the output image
    output_image_path = "output-flowchart.png"
    if os.path.exists(output_image_path):
        st.image(output_image_path, caption="Processed Output", use_column_width=True)
        
        # Allow user to download the processed image
        with open(output_image_path, "rb") as file:
            st.download_button(
                label="Download Processed Image",
                data=file,
                file_name="output-flowchart.png",
                mime="image/png"
            )
    else:
        st.error("The processed image was not found. Please try again.")
