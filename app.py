from dotenv import load_dotenv
load_dotenv() # Load all environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Configure Google GenAI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro Vision
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Multi Language Image to Text Chatbot", page_icon=":page_with_curl:")

# Apply custom CSS
st.markdown(
    """
    <style>
    /* Background and main styling */
    body {
        background-color: #f0f2f6;
        color: #333333;
    }
    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        margin: 20px auto;
        width: 80%;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        font-size: 16px;
    }
    /* Header styling */
    #header {
        text-align: center;
        padding: 10px;
        background-color: #4CAF50;
        color: white;
        border-radius: 10px 10px 0 0;
    }
    #header h1 {
        font-size: 2.5em;
        margin-bottom: 0;
    }
    #header h2 {
        font-size: 1.2em;
        margin-top: 0;
        font-weight: normal;
    }
    /* Footer styling */
    #footer {
        text-align: center;
        padding: 10px;
        font-size: 0.9em;
        color: #777;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True
)

# Sidebar with information and developer photo
st.sidebar.title("About the App")
st.sidebar.info("""
This app allows you to upload an invoice image written in any language and ask questions about it. 
Powered by Google GenAI, it provides accurate and multi-language responses.
""")

# Developer's Photo
developer_photo = Image.open("ashique_mahmud.jpg")  # Replace with the actual file name
st.sidebar.image(developer_photo, caption="Ashique Mahmud", use_column_width=True)

# Header section
st.markdown(
    """
    <div id="header">
        <h1>Multi Language Image to Text Chatbot</h1>
        <h2>Analyze Image and ask questions in multiple languages</h2>
    </div>
    """, unsafe_allow_html=True
)

# Upload section
uploaded_file = st.file_uploader("Choose an Image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Input prompt section
input = st.text_input("Your Question", key="input")

# Button to submit
submit = st.button("Tell me about the Image")

input_prompt = """
You are an expert in understanding invoices. We will upload an image as an invoice, 
and you will answer any questions based on the uploaded invoice image.
"""

# If the submit button is clicked
if submit:
    try:
        image_data = input_image_details(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, input)
        st.subheader("Response:")
        st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Footer section
st.markdown(
    """
    <div id="footer">
        &copy; 2024 Multi-Language Invoice Extractor | Powered by Google GenAI
    </div>
    """, unsafe_allow_html=True
)
