from dotenv import load_dotenv


load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

# Ensure the API key is loaded correctly
api_key = os.getenv("GOOGLE_API_KEY")
if api_key is None:
    st.error("Google API key not set! Please check the .env file.")
else:
    genai.configure(api_key=api_key)

def get_gemini_response(input_text, pdf_parts, prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_parts[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to images (first page)
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        if len(images) == 0:
            raise ValueError("No pages in the PDF.")
        
        # Process the first page (as an image)
        first_page = images[0]

        # Convert image to byte format
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Encode image to base64
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App
st.set_page_config(page_title="InfiNity LooP")
st.header("InfiNity LooP ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")

submit3 = st.button("Percentage match")

##submit2 = st.button("Tell me about how to excel")

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches 
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

# Handle form submission for evaluation
if submit1:
    if uploaded_file is not None:
        try:
            # Process the PDF file into image
            pdf_parts = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_parts, input_prompt1)
            st.subheader("The Response is")
            st.write(response)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.write("Please upload the resume.")

# Handle form submission for percentage match
elif submit3:
    if uploaded_file is not None:
        try:
            # Process the PDF file into image
            pdf_parts = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_parts, input_prompt3)
            st.subheader("The Response is")
            st.write(response)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.write("Please upload the resume.")
