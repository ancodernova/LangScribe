import streamlit as st
from summarizer import summarize_text
from pdf_extractor import extract_text_from_pdf
from text_cleaner import clean_text
from QA_chatbot import ask_question
import base64

# Set page title and icon
st.set_page_config(
    page_title="PDF Summarizer & Q&A Chatbot",
    page_icon=":book:",
    layout="centered"
)

# Function to load and encode the logo
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.error("Logo file not found.")
        return None

# Path to the logo
logo_path = "8943377.png"
logo_base64 = get_base64_of_bin_file(logo_path)

if logo_base64:
    st.markdown(f"""
        <style>
            .main {{
                background-color: #e6f0ff;
            }}
            .stTextInput > div > div > input {{
                border: 2px solid #004080;
            }}
            .stButton>button {{
                background-color: #004080;
                color: white;
                border-radius: 5px;
                border: 2px solid #004080;
            }}
            .stButton>button:hover {{
                background-color: #003366;
                border: 2px solid #003366;
            }}
            .header {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                background-color: #b3d9ff;
                padding: 10px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }}
            .logo {{
                width: 100px;
            }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="header">
            <h2>PDF Text Summarization and Q&A Chatbot</h2>
            <img src="data:image/png;base64,{logo_base64}" class="logo">
        </div>
        <hr>
    """, unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Step 1: Extract raw text from PDF
    raw_text = extract_text_from_pdf(uploaded_file)
    if not raw_text:
        st.warning("No text could be extracted from the PDF. Please check the file format or content.")
    else:
        # Display raw text for debugging
        st.subheader("Raw Extracted Text")
        st.text_area("Raw Text", raw_text, height=200)
        
        # Step 2: Clean extracted text
        try:
            cleaned_text = clean_text(raw_text)
            if not cleaned_text:
                st.warning("The extracted text could not be processed further after cleaning.")
            else:
                st.subheader("Cleaned Text")
                st.text_area("Cleaned Text", cleaned_text, height=200)

                # Summarization section
                if st.button("Summarize"):
                    summary = summarize_text(cleaned_text)
                    if summary:
                        st.subheader("Summary")
                        st.success(summary)
                    else:
                        st.warning("Summarization resulted in an empty output.")

                # Q&A section
                st.subheader("Ask Questions About the PDF")
                question = st.text_input("Enter your question:")
                if question:
                    answer = ask_question(question, cleaned_text)
                    if answer:
                        st.subheader("Answer")
                        st.info(answer)
                    else:
                        st.warning("No answer could be generated.")
        except Exception as e:
            st.error(f"Error during cleaning: {e}")
else:
    st.info("Please upload a PDF file to start.")
